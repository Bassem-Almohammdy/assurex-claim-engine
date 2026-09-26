#!/usr/bin/env python3
"""
evaluate_model.py
------------------
AssureX Claim Engine — Member 3

يختبر نموذج Teachable Machine على كامل مجلدات Validation و/أو Test
(وليس فقط عينة الـ30 صورة)، ويحسب:
  - الدقة الإجمالية
  - الدقة لكل فئة (Valid / Invalid / Manual Review)
  - قائمة كل الأخطاء (Confusion) مع الثقة، لتوثيقها في evaluation_notes.md

بخلاف predict_tm.py، هذا السكربت يحمّل النموذج مرة واحدة فقط، فيكون
سريعاً حتى مع مئات الصور.

الاستخدام:
    python3 evaluate_model.py --dataset-dir output/tm_dataset/validation
    python3 evaluate_model.py --dataset-dir output/tm_dataset/test
    (كرر الأمر مرتين لتقييم كل مجموعة على حدة)

يتوقع أن يكون هيكل المجلد:
    <dataset-dir>/<Class_Name>/<claim_id>.jpg
مثل:
    output/tm_dataset/validation/Valid_Claim/123.jpg
    output/tm_dataset/validation/Invalid_Claim/456.jpg
"""

import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import argparse
import json
from pathlib import Path

import numpy as np
from tensorflow.keras.models import load_model

from predict_tm import load_labels, preprocess, get_model_version


def evaluate(dataset_dir: Path, model_dir: Path):
    model = load_model(model_dir / "keras_model.h5", compile=False)
    labels = load_labels(model_dir / "labels.txt")
    version = get_model_version(model_dir)

    total = 0
    correct = 0
    per_class = {}
    errors = []

    class_folders = sorted([d for d in dataset_dir.iterdir() if d.is_dir()])
    if not class_folders:
        raise SystemExit(f"لا توجد مجلدات فئات داخل {dataset_dir}")

    for class_dir in class_folders:
        true_label = class_dir.name
        images = sorted(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
        per_class.setdefault(true_label, {"total": 0, "correct": 0})

        for img_path in images:
            data = preprocess(img_path)
            probs = model.predict(data, verbose=0)[0]
            top = int(np.argmax(probs))
            pred_label = labels[top]
            confidence = float(probs[top])

            ok = (pred_label == true_label)
            total += 1
            correct += int(ok)
            per_class[true_label]["total"] += 1
            per_class[true_label]["correct"] += int(ok)

            if not ok:
                errors.append({
                    "file": str(img_path),
                    "true": true_label,
                    "predicted": pred_label,
                    "confidence": round(confidence, 4),
                })

    return {
        "model_version": version,
        "dataset_dir": str(dataset_dir),
        "total_images": total,
        "correct": correct,
        "accuracy": round(correct / total, 4) if total else 0.0,
        "per_class": {
            cls: {
                "total": v["total"],
                "correct": v["correct"],
                "accuracy": round(v["correct"] / v["total"], 4) if v["total"] else 0.0,
            }
            for cls, v in per_class.items()
        },
        "errors": errors,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-dir", required=True,
                     help="مثال: output/tm_dataset/validation أو output/tm_dataset/test")
    ap.add_argument("--model-dir", default="model/tm_model")
    ap.add_argument("--save-json", default=None,
                     help="مسار لحفظ النتيجة كاملة كـ JSON (اختياري)")
    args = ap.parse_args()

    result = evaluate(Path(args.dataset_dir), Path(args.model_dir))

    print(f"\n=== النتائج: {args.dataset_dir} ===")
    print(f"عدد الصور: {result['total_images']}")
    print(f"الدقة الإجمالية: {result['correct']}/{result['total_images']} = {result['accuracy']:.2%}")
    print("\nحسب الفئة:")
    for cls, v in result["per_class"].items():
        print(f"  {cls}: {v['correct']}/{v['total']} = {v['accuracy']:.2%}")

    print(f"\nعدد الأخطاء: {len(result['errors'])}")
    if result["errors"]:
        print("أول 10 أخطاء (الحقيقي -> توقّع النموذج، الثقة):")
        for e in result["errors"][:10]:
            print(f"  {Path(e['file']).name}: {e['true']} -> {e['predicted']} (ثقة {e['confidence']})")

    if args.save_json:
        with open(args.save_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nتم حفظ التفاصيل الكاملة في: {args.save_json}")
