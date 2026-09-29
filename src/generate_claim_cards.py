#!/usr/bin/env python3
"""
generate_claim_cards.py
------------------------
AssureX Claim Engine — Member 3 (Teachable Machine / Computer Vision Lead)

يحوّل سجلات الـ Claims (train / validation / test) إلى صور "Claim Summary
Card" جاهزة للاستخدام في تدريب Google Teachable Machine.

قواعد صارمة تم الالتزام بها (بحسب الدستور التشغيلي للمشروع):
  * لا تُطبع أي نتيجة Python model / confidence / Final Decision على البطاقة.
  * يبقى نفس claim_id مستخدَمًا كمعرّف فريد للصورة.
  * فصل تام بين Train / Validation / Test (لا تسريب بيانات).
  * لكل Claim في Train يتم توليد >= 2 نسخة بصرية مختلفة (Variations)
    بحيث يتجاوز إجمالي صور التدريب 2100 صورة (1050 claim × 2).
  * التصنيف الفعلي للصورة (Valid / Invalid / Manual Review) يُستخدم فقط
    كاسم للمجلد الذي توضع فيه الصورة (Folder Label) — ولا يُكتب نص الحالة
    داخل البطاقة نفسها حتى لا يحفظ النموذج "قراءة النص" بدل "تعلّم النمط
    البصري".

الاستخدام:
    python3 generate_claim_cards.py --data-dir data/splits --out-dir output

المخرجات:
    output/tm_dataset/train/<Class>/<claim_id>_v<n>.jpg   (للتدريب على TM)
    output/tm_dataset/validation/<Class>/<claim_id>.jpg   (Holdout - لا تُستخدم في التدريب)
    output/tm_dataset/test/<Class>/<claim_id>.jpg         (Holdout - لا تُستخدم في التدريب)
    output/comparison_30/<claim_id>_<Class>.jpg           (عينة مقارنة نهائية، 30 Claim غير مستخدمة في التدريب)
    output/manifest.csv                                   (سجل كل صورة تم توليدها)
    output/training_log.json                              (إحصائيات التوليد لتوثيقها في التسليم)
"""

import argparse
import csv
import hashlib
import json
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------------
# إعدادات عامة
# ----------------------------------------------------------------------------

CARD_W, CARD_H = 720, 960          # لوحة الرسم الداخلية (لدقة أفضل أثناء الرسم)
SAVE_W, SAVE_H = 480, 640          # الحجم النهائي المحفوظ (يكفي ويزيد لتدريب TM ويقلّل حجم الملفات)
CLASSES = ["Valid", "Invalid", "Manual Review"]          # كما تظهر في claim_status
CLASS_FOLDER = {                                          # أسماء مجلدات آمنة (بدون مسافات)
    "Valid": "Valid_Claim",
    "Invalid": "Invalid_Claim",
    "Manual Review": "Manual_Review",
}
MIN_VARIATIONS_PER_TRAIN_CLAIM = 2
COMPARISON_SAMPLE_SIZE = 30

FONT_DIR = Path(__file__).resolve().parent / "fonts"
FONT_REGULAR = str(FONT_DIR / "DejaVuSans.ttf")
FONT_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")

if not Path(FONT_REGULAR).exists() or not Path(FONT_BOLD).exists():
    raise SystemExit(
        "لم يتم العثور على ملفات الخط داخل مجلد fonts/ بجانب هذا السكربت.\n"
        "تأكد أن مجلد fonts يحتوي على DejaVuSans.ttf و DejaVuSans-Bold.ttf "
        "في نفس مجلد generate_claim_cards.py."
    )

# 3 نُسَخ ألوان (Themes) يتم التدوير عليها بين الـ Variations حتى لا تحفظ
# الشبكة "لون الفئة" كحل مختصر، بل تتعرض لنفس الفئة بألوان مختلفة.
THEMES = [
    {"bg": (247, 249, 252), "panel": (255, 255, 255), "accent": (37, 99, 235), "text": (30, 41, 59), "muted": (100, 116, 139)},
    {"bg": (250, 247, 242), "panel": (255, 255, 255), "accent": (180, 83, 9),  "text": (41, 30, 20),  "muted": (120, 100, 90)},
    {"bg": (244, 248, 246), "panel": (255, 255, 255), "accent": (5, 122, 85),  "text": (20, 40, 35),  "muted": (90, 115, 105)},
]

GOOD = (22, 163, 74)
BAD = (220, 38, 38)
WARN = (217, 119, 6)   # برتقالي تحذيري — لون ثابت غير مرتبط بالثيم لضمان قابلية تعلّمه بمعزل عن الثيم

random.seed(42)  # ملاحظة: التشويش (Image.effect_noise) غير مُبذَّر، فالصور تتطابق في المحتوى لا في البايتات

# ----------------------------------------------------------------------------
# عتبات خطورة — مقاسة فعليًا على data/splits/train.csv (t-test + Cohen's d)
# (القياسات مأخوذة من تحليل train.csv أثناء تطوير التصميم.)
# ----------------------------------------------------------------------------
REPAIR_RISK_THRESHOLD = 2       # فوق متوسط Invalid (2.54~2.63) ويفصل بوضوح عن Valid (~1.0)
# ملاحظة تصحيح (تحقّق فعلي على الفئات الثلاث معًا، وليس فقط Invalid مقابل
# Manual Review كما في الوثيقة الأصلية): Valid وInvalid متقاربتان في هذه
# النسبة (~0.50 لكلتيهما)، فقط Manual Review أعلى بوضوح (~0.69-0.79) — لذا
# نستخدم عتبة تحذير واحدة (WARN) فقط، لا عتبتين GOOD/BAD.
CLAIM_RATIO_WARN = 0.65
DAYS_RECENT_THRESHOLD = 600     # القيمة الوسطى تقريبًا بين متوسطي Valid/Manual/Invalid (366 / 937 / 1325 يوم)
INVALID_ONLY_DAMAGE_TYPES = {"Physical Damage", "Unknown", "Water Damage"}


def risk_level(rec) -> str:
    """مؤشر خطورة مشتق (Derived Variable) من أربع حقول خام موجودة على البطاقة.
    لا يستخدم claim_status ولا أي مخرج نموذج؛ انظر README_Member3.md القسم 8."""
    score = 0
    if rec.purchase_price > 0 and rec.claim_amount / rec.purchase_price >= CLAIM_RATIO_WARN:
        score += 1
    if rec.repair_history > REPAIR_RISK_THRESHOLD:
        score += 1
    if rec.damage_type in INVALID_ONLY_DAMAGE_TYPES:
        score += 1
    if rec.warranty_period_months > 0 and rec.product_age_months / rec.warranty_period_months > 1.0:
        score += 1
    return "high" if score >= 2 else ("medium" if score == 1 else "low")
RISK_COLOR = {"high": BAD, "medium": WARN, "low": GOOD}


# ----------------------------------------------------------------------------
# أدوات رسم مساعدة
# ----------------------------------------------------------------------------

def font(path, size):
    return ImageFont.truetype(path, size)


def claim_seed(claim_id, variation):
    """seed ثابت لكل (claim_id, variation) حتى تتكرر نفس الصورة لو أعيد التشغيل."""
    h = hashlib.sha256(f"{claim_id}-{variation}".encode()).hexdigest()
    return int(h[:8], 16)


def draw_rounded_panel(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(text, fnt, max_width, draw):
    words = str(text).split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def badge(draw, xy, text, fg, bg, fnt, pad=10):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    box = (x, y, x + tw + pad * 2, y + th + pad * 1.4)
    draw_rounded_panel(draw, box, radius=th, fill=bg)
    draw.text((x + pad, y + pad * 0.2), text, font=fnt, fill=fg)
    return box


def status_dot(draw, xy, ok, r=9):
    x, y = xy
    color = GOOD if ok else BAD
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)


# ----------------------------------------------------------------------------
# توليد بطاقة واحدة
# ----------------------------------------------------------------------------

@dataclass
class ClaimRecord:
    claim_id: str
    product_category: str
    product_age_months: int
    warranty_period_months: int
    receipt_available: int
    serial_number_valid: int
    damage_type: str
    repair_history: int
    purchase_price: float
    claim_amount: float
    days_since_purchase: int
    claim_status: str


def render_card(rec: ClaimRecord, variation: int) -> Image.Image:
    rng = random.Random(claim_seed(rec.claim_id, variation))
    theme = THEMES[variation % len(THEMES)]

    # تنويعات بصرية بسيطة لا تغيّر المحتوى، فقط الشكل، حتى تتعلم الشبكة
    # النمط العام لا مواضع بكسل ثابتة.
    jitter_x = rng.randint(-6, 6)
    jitter_y = rng.randint(-6, 6)
    noise_level = rng.uniform(2, 6)
    layout_shift = rng.choice([0, 1])  # ترتيب بديل بسيط لبعض الصفوف

    img = Image.new("RGB", (CARD_W, CARD_H), theme["bg"])
    draw = ImageDraw.Draw(img)

    f_title = font(FONT_BOLD, 30)
    f_h2 = font(FONT_BOLD, 20)
    f_label = font(FONT_REGULAR, 17)
    f_value = font(FONT_BOLD, 19)
    f_small = font(FONT_REGULAR, 14)
    f_badge = font(FONT_BOLD, 15)

    margin = 36
    panel_box = (margin + jitter_x, margin + jitter_y, CARD_W - margin + jitter_x, CARD_H - margin + jitter_y)
    draw_rounded_panel(draw, panel_box, radius=22, fill=theme["panel"], outline=(226, 232, 240), width=2)

    # -- Risk Banner: شريط لوني كبير منفصل تمامًا عن الرأس، ليس فوقه ------
    level = risk_level(rec)
    banner_x0 = panel_box[0] + 24
    banner_x1 = panel_box[2] - 24
    banner_y0 = panel_box[1] + 22
    banner_y1 = banner_y0 + 46
    draw_rounded_panel(draw, (banner_x0, banner_y0, banner_x1, banner_y1), radius=12, fill=RISK_COLOR[level])
    draw.text((banner_x0 + 18, banner_y0 + 13), f"RISK LEVEL: {level.upper()}", font=f_h2, fill=(255, 255, 255))

    # -- Header --------------------------------------------------------
    hx, hy = panel_box[0] + 28, banner_y1 + 24
    draw_rounded_panel(draw, (hx, hy, hx + 54, hy + 54), radius=14, fill=theme["accent"])
    draw.text((hx + 15, hy + 10), "AX", font=f_h2, fill=(255, 255, 255))

    draw.text((hx + 68, hy - 2), "Claim Summary Card", font=f_title, fill=theme["text"])
    draw.text((hx + 68, hy + 32), f"Claim ID: {rec.claim_id}", font=f_label, fill=theme["muted"])

    line_y = hy + 68
    draw.line((panel_box[0] + 28, line_y, panel_box[2] - 28, line_y), fill=(226, 232, 240), width=2)

    # -- Product block ---------------------------------------------------
    y = line_y + 22
    x = panel_box[0] + 28
    draw.text((x, y), rec.product_category.upper(), font=f_h2, fill=theme["accent"])
    y += 34
    # Invalid تظهر حصريًا في 3 أنواع من أصل 8 — إشارة تصنيفية شبه حتمية
    damage_color = WARN if rec.damage_type in INVALID_ONLY_DAMAGE_TYPES else theme["text"]
    draw.text((x, y), f"Damage Type: {rec.damage_type}", font=f_label, fill=damage_color)
    y += 38

    # -- Warranty timeline bar -------------------------------------------
    bar_x0, bar_x1 = x, panel_box[2] - 28
    bar_y = y + 6
    bar_h = 16
    draw_rounded_panel(draw, (bar_x0, bar_y, bar_x1, bar_y + bar_h), radius=8, fill=(226, 232, 240))
    raw_ratio = 0.0
    if rec.warranty_period_months > 0:
        raw_ratio = rec.product_age_months / rec.warranty_period_months
    # التشبّع الثنائي عند 1.0 كان يرسم Invalid (~1.78x تجاوز) و
    # Manual Review (~1.34x تجاوز) بشريط "ممتلئ بالكامل + أحمر" متطابق بصريًا،
    # رغم أن شدة التجاوز نفسها هي الإشارة المميِّزة بين الفئتين.
    if raw_ratio <= 1.0:
        bar_color = GOOD
        ratio = raw_ratio
    elif raw_ratio <= 1.5:
        bar_color = WARN            # تجاوز متوسط (نطاق Manual Review الشائع: ~1.34)
        ratio = min(1.0, raw_ratio / 2.0)
    else:
        bar_color = BAD             # تجاوز حاد (نطاق Invalid الشائع: ~1.78)
        ratio = 1.0
    fill_x = bar_x0 + int((bar_x1 - bar_x0) * ratio)
    if fill_x > bar_x0:
        draw_rounded_panel(draw, (bar_x0, bar_y, fill_x, bar_y + bar_h), radius=8, fill=bar_color)
    draw.text((bar_x0, bar_y + bar_h + 6),
              f"Product Age: {rec.product_age_months} mo", font=f_small, fill=theme["muted"])
    warranty_label = f"Warranty: {rec.warranty_period_months} mo"
    draw.text((bar_x1 - draw.textlength(warranty_label, font=f_small), bar_y + bar_h + 6),
              warranty_label, font=f_small, fill=theme["muted"])

    y = bar_y + bar_h + 34

    # -- Status rows (receipt / serial number) ----------------------------
    rows = [
        ("Receipt Available", bool(rec.receipt_available)),
        ("Serial Number Valid", bool(rec.serial_number_valid)),
    ]
    if layout_shift:
        rows = rows[::-1]

    col_w = (panel_box[2] - panel_box[0] - 56) / 2
    for i, (label, ok) in enumerate(rows):
        cx = x + i * (col_w + 0)
        status_dot(draw, (cx + 9, y + 12), ok)
        draw.text((cx + 26, y), label, font=f_label, fill=theme["text"])
        state_txt = "Yes" if ok else "No"
        badge(draw, (cx + 26, y + 24), state_txt, (255, 255, 255), GOOD if ok else BAD, f_badge)
    y += 76

    draw.line((x, y, panel_box[2] - 28, y), fill=(226, 232, 240), width=1)
    y += 20

    # -- Repair history -----------------------------------------------------
    draw.text((x, y), "Repair History", font=f_label, fill=theme["text"])
    rh = max(0, int(rec.repair_history))
    risk = rh > REPAIR_RISK_THRESHOLD
    dot_color = BAD if risk else theme["accent"]
    dot_x = x
    dot_y = y + 30
    for i in range(min(rh, 8)):
        draw.ellipse((dot_x, dot_y, dot_x + 14, dot_y + 14), fill=dot_color)
        dot_x += 22
    if rh == 0:
        draw.text((x, dot_y - 2), "No previous repairs", font=f_small, fill=theme["muted"])
    else:
        suffix = " \u26a0" if risk else ""
        draw.text((dot_x + 6, dot_y - 2), f"({rh}){suffix}", font=f_small,
                   fill=(BAD if risk else theme["muted"]))
    y += 66

    # -- Days since purchase tag (مع تصحيح الاتجاه) --------------
    # تحقق فعلي على train.csv: Valid=366 يوم بالمتوسط، Manual Review=937،
    # Invalid=1325 (الأعلى) — الملكية القديمة هي المرتبطة بـ Invalid، وليس
    # الشراء الحديث كما افترضت المسودة الأصلية حتى بعد تصحيح رقم العتبة.
    is_established = rec.days_since_purchase > DAYS_RECENT_THRESHOLD
    tag_text = "Established Ownership" if is_established else "Recent Purchase"
    if is_established:
        badge(draw, (x, y), tag_text, (255, 255, 255), WARN, f_badge)
    else:
        badge(draw, (x, y), tag_text, theme["text"], (226, 232, 240), f_badge)
    y += 40

    draw.line((x, y, panel_box[2] - 28, y), fill=(226, 232, 240), width=1)
    y += 20

    # -- Financial block ------------------------------------------------
    money_rows = [
        ("Purchase Price", f"${rec.purchase_price:,.2f}"),
        ("Claim Amount", f"${rec.claim_amount:,.2f}"),
        ("Days Since Purchase", f"{rec.days_since_purchase} days"),
    ]
    if layout_shift:
        money_rows[0], money_rows[1] = money_rows[1], money_rows[0]

    for label, value in money_rows:
        draw.text((x, y), label, font=f_label, fill=theme["muted"])
        vw = draw.textlength(value, font=f_value)
        draw.text((panel_box[2] - 28 - vw, y), value, font=f_value, fill=theme["text"])
        y += 32

    # -- claim amount vs purchase price mini bar (مصحَّح) --------
    # تحقق فعلي على الفئات الثلاث معًا (الوثيقة الأصلية قارنت Invalid بـ Manual
    # Review فقط): Valid≈0.50 وInvalid≈0.50 متطابقتان تقريبًا، وManual Review
    # فقط هي الأعلى بوضوح (~0.69-0.79). إذن هذا المؤشر يفصل Manual Review عن
    # البقية، ولا يميّز Invalid عن Valid — لذا لا يُستخدم لونان (GOOD/BAD) بل
    # درجة تحذير واحدة فقط عند دخول نطاق Manual Review النمطي، وإلا محايد.
    y += 6
    ratio2 = 0.0
    if rec.purchase_price > 0:
        ratio2 = max(0.0, min(1.5, rec.claim_amount / rec.purchase_price))
    bar2_color = WARN if ratio2 >= CLAIM_RATIO_WARN else theme["accent"]
    draw_rounded_panel(draw, (x, y, panel_box[2] - 28, y + 12), radius=6, fill=(226, 232, 240))
    fill2 = x + int((panel_box[2] - 28 - x) * min(1.0, ratio2))
    if fill2 > x:
        draw_rounded_panel(draw, (x, y, fill2, y + 12), radius=6, fill=bar2_color)
    y += 30

    # -- Footer / watermark (no prediction, no decision) --------------------
    footer_txt = "AssureX Claim Engine — Source Claim Data"
    draw.text((x, panel_box[3] - 34), footer_txt, font=f_small, fill=theme["muted"])
    idw = draw.textlength(str(rec.claim_id), font=f_small)
    draw.text((panel_box[2] - 28 - idw, panel_box[3] - 34), str(rec.claim_id), font=f_small, fill=theme["muted"])

    # -- subtle per-variation texture (noise) so images aren't pixel-identical
    if noise_level > 0:
        noise = Image.effect_noise(img.size, int(noise_level * 10)).convert("L")
        noise = noise.point(lambda p: 128 + (p - 128) // 6)
        img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), alpha=0.02)

    img = img.filter(ImageFilter.SMOOTH_MORE if variation % 2 else ImageFilter.SHARPEN)
    img = img.resize((SAVE_W, SAVE_H), Image.LANCZOS)
    return img


# ----------------------------------------------------------------------------
# قراءة البيانات وتشغيل التوليد
# ----------------------------------------------------------------------------

def read_split(path):
    records = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append(ClaimRecord(
                claim_id=row["claim_id"],
                product_category=row["product_category"],
                product_age_months=int(row["product_age_months"]),
                warranty_period_months=int(row["warranty_period_months"]),
                receipt_available=int(row["receipt_available"]),
                serial_number_valid=int(row["serial_number_valid"]),
                damage_type=row["damage_type"],
                repair_history=int(row["repair_history"]),
                purchase_price=float(row["purchase_price"]),
                claim_amount=float(row["claim_amount"]),
                days_since_purchase=int(row["days_since_purchase"]),
                claim_status=row["claim_status"],
            ))
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/splits")
    ap.add_argument("--out-dir", default="output")
    ap.add_argument("--variations", type=int, default=MIN_VARIATIONS_PER_TRAIN_CLAIM)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    tm_dir = out_dir / "tm_dataset"
    comp_dir = out_dir / "comparison_30"

    for split in ["train", "validation", "test"]:
        for cls in CLASSES:
            (tm_dir / split / CLASS_FOLDER[cls]).mkdir(parents=True, exist_ok=True)
    comp_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    per_class_counts = {"train": {c: 0 for c in CLASSES},
                         "validation": {c: 0 for c in CLASSES},
                         "test": {c: 0 for c in CLASSES}}

    # ---- TRAIN: عدة نسخ (Variations) لكل Claim ----------------------------
    train_records = read_split(data_dir / "train.csv")
    for rec in train_records:
        n_var = max(args.variations, MIN_VARIATIONS_PER_TRAIN_CLAIM)
        for v in range(1, n_var + 1):
            img = render_card(rec, variation=v)
            fname = f"{rec.claim_id}_v{v}.jpg"
            fpath = tm_dir / "train" / CLASS_FOLDER[rec.claim_status] / fname
            img.save(fpath, "JPEG", quality=88, optimize=True)
            manifest_rows.append([rec.claim_id, "train", rec.claim_status, v, fpath.as_posix()])
            per_class_counts["train"][rec.claim_status] += 1

    # ---- VALIDATION: نسخة واحدة لكل Claim (Holdout - لا تُستخدم بالتدريب) --
    val_records = read_split(data_dir / "validation.csv")
    for rec in val_records:
        img = render_card(rec, variation=0)
        fname = f"{rec.claim_id}.jpg"
        fpath = tm_dir / "validation" / CLASS_FOLDER[rec.claim_status] / fname
        img.save(fpath, "JPEG", quality=88, optimize=True)
        manifest_rows.append([rec.claim_id, "validation", rec.claim_status, 0, fpath.as_posix()])
        per_class_counts["validation"][rec.claim_status] += 1

    # ---- TEST: نسخة واحدة لكل Claim (Holdout) ------------------------------
    test_records = read_split(data_dir / "test.csv")
    for rec in test_records:
        img = render_card(rec, variation=0)
        fname = f"{rec.claim_id}.jpg"
        fpath = tm_dir / "test" / CLASS_FOLDER[rec.claim_status] / fname
        img.save(fpath, "JPEG", quality=88, optimize=True)
        manifest_rows.append([rec.claim_id, "test", rec.claim_status, 0, fpath.as_posix()])
        per_class_counts["test"][rec.claim_status] += 1

    # ---- عينة المقارنة النهائية: 30 Claim (10 لكل فئة) من TEST فقط --------
    rng = random.Random(7)
    by_class = {c: [r for r in test_records if r.claim_status == c] for c in CLASSES}
    per_cls_n = COMPARISON_SAMPLE_SIZE // len(CLASSES)
    comparison_records = []
    for c in CLASSES:
        pool = by_class[c][:]
        rng.shuffle(pool)
        comparison_records.extend(pool[:per_cls_n])
    rng.shuffle(comparison_records)

    comp_manifest = []
    for rec in comparison_records:
        src = tm_dir / "test" / CLASS_FOLDER[rec.claim_status] / f"{rec.claim_id}.jpg"
        dst = comp_dir / f"{rec.claim_id}__{CLASS_FOLDER[rec.claim_status]}.jpg"
        Image.open(src).save(dst, "JPEG", quality=88, optimize=True)
        comp_manifest.append({"claim_id": rec.claim_id, "true_class": rec.claim_status, "file": dst.as_posix()})

    # ---- ملفات التوثيق -----------------------------------------------------
    with open(out_dir / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "split", "claim_status", "variation", "file_path"])
        w.writerows(manifest_rows)

    with open(out_dir / "comparison_30_manifest.json", "w", encoding="utf-8") as f:
        json.dump(comp_manifest, f, ensure_ascii=False, indent=2)

    # ملاحظة: label_mapping.json لا يُكتب هنا عمدًا. ترتيب الفئات الحقيقي يأتي من
    # labels.txt المُصدَّر من Teachable Machine ويُولَّد فقط عبر build_label_mapping.py.

    total_train_images = sum(per_class_counts["train"].values())
    log = {
        "variations_per_train_claim": max(args.variations, MIN_VARIATIONS_PER_TRAIN_CLAIM),
        "train_claims": len(train_records),
        "validation_claims": len(val_records),
        "test_claims": len(test_records),
        "total_train_images": total_train_images,
        "meets_2100_minimum": total_train_images >= 2100,
        "per_class_counts": per_class_counts,
        "comparison_sample_size": len(comparison_records),
    }
    with open(out_dir / "training_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
