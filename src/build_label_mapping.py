#!/usr/bin/env python3
"""
build_label_mapping.py
-----------------------
AssureX Claim Engine — Member 3

يُشغَّل مرة واحدة بعد كل تصدير جديد من Teachable Machine (الخطوة 6 في
README_Member3.md)، ليضمن أن output/label_mapping.json يعكس دائمًا الترتيب
الحقيقي الذي صدّره TM في model/tm_model/labels.txt، بدل الاعتماد على ترتيب
CLASSES المكتوب يدويًا في generate_claim_cards.py (وهو مصدر عطل سابق موثّق في
README_Member3.md القسم 4: label_mapping.json كان يقول
{0: Valid, 1: Invalid, 2: Manual Review} بينما labels.txt الحقيقي يقول
{0: Valid_Claim, 1: Manual_Review, 2: Invalid_Claim} — ترتيب مختلف تمامًا).

الاستخدام:
    python3 build_label_mapping.py --model-dir model/tm_model --out output/label_mapping.json
"""

import argparse
import json
from pathlib import Path

from predict_tm import load_labels

# نفس أسماء المجلدات الآمنة المستخدمة في generate_claim_cards.py، بترتيب
# لا علاقة له بترتيب التصدير — تُستخدم فقط لمطابقة اسم المجلد الآمن باسم
# الفئة الحقيقي القادم من labels.txt.
FOLDER_TO_DISPLAY = {
    "Valid_Claim": "Valid",
    "Invalid_Claim": "Invalid",
    "Manual_Review": "Manual Review",
}


def build_label_mapping_from_export(model_dir="model/tm_model", out_path="output/label_mapping.json"):
    model_dir = Path(model_dir)
    labels = load_labels(model_dir / "labels.txt")  # نفس دالة predict_tm.py — نفس المصدر الحقيقي

    mapping = {
        "classes": labels,
        "index_to_label": {i: l for i, l in enumerate(labels)},
        "folder_names": {FOLDER_TO_DISPLAY.get(l, l): l for l in labels},
        "source": "auto-generated from labels.txt — do not edit manually",
    }

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"[OK] {out_path} مُحدَّث من {model_dir / 'labels.txt'} (الترتيب الحقيقي):")
    print(json.dumps(mapping, ensure_ascii=False, indent=2))
    return mapping


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="model/tm_model")
    ap.add_argument("--out", default="output/label_mapping.json")
    args = ap.parse_args()
    build_label_mapping_from_export(args.model_dir, args.out)
