#!/usr/bin/env python3
"""
run_comparison_30.py — Member 3
يشغّل نموذج Teachable Machine على صور output/comparison_30/ ويحفظ نتائج TM
بالحقول المطلوبة في تقرير المقارنة (SRS البند 6): claim_id، الفئة الحقيقية،
اسم ملف البطاقة، الفئة المتوقعة، احتمالات الفئات الثلاث، الثقة.

الاستخدام:
    python3 run_comparison_30.py --model-dir model/tm_model --out output/comparison_30_results.json
"""
import argparse
import json
from pathlib import Path

import predict_tm  # يضبط بيئة Keras القديمة قبل استيراد tensorflow


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="model/tm_model")
    ap.add_argument("--manifest", default="output/comparison_30_manifest.json")
    ap.add_argument("--out", default="output/comparison_30_results.json")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    results, correct = [], 0
    for item in manifest:
        # المسارات في الـ manifest بصيغة POSIX؛ نحوّل أي "\" قديمة احتياطًا.
        img_path = Path(item["file"].replace("\\", "/"))
        r = predict_tm.predict(img_path, args.model_dir, claim_id=item["claim_id"])
        ok = r["tm_prediction"] == item["true_class"]
        correct += int(ok)
        results.append({
            "claim_id": item["claim_id"],
            "actual_class": item["true_class"],
            "card_filename": img_path.name,
            "tm_prediction": r["tm_prediction"],
            "tm_probabilities": r["tm_probabilities"],
            "tm_confidence": r["tm_confidence"],
            "correct": ok,
            "model_version": r["model_version"],
        })

    Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"الدقة على عينة المقارنة: {correct}/{len(results)} = {100*correct/len(results):.2f}%")
    print(f"تم الحفظ في: {args.out}")


if __name__ == "__main__":
    main()
