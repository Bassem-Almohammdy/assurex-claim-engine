#!/usr/bin/env python3
"""
set_model_version.py
----------------------
AssureX Claim Engine — Member 3

ينشئ model/tm_model/model_version.json صراحةً بدل الاعتماد على طابع تعديل
ملف keras_model.h5 (غير موثوق عبر git clone — انظر get_model_version() في
predict_tm.py).

يُشغَّل يدويًا بعد كل جولة تدريب/تصدير جديدة، مع تعبئة أرقام الدقة بعد
تشغيل evaluate_model.py على Validation وTest.

الاستخدام:
    python3 set_model_version.py --model-dir model/tm_model \
        --trained-on "2100 images (700/700/700), variations=2" \
        --epochs 50 --lr 0.001 --batch-size 16 \
        --val-accuracy 0.7333 --test-accuracy 0.7467 \
        --tag v1
"""

import argparse
import datetime
import json
from pathlib import Path


def set_model_version(model_dir, trained_on, epochs, lr, batch_size,
                       val_accuracy=None, test_accuracy=None, tag="v1"):
    model_dir = Path(model_dir)
    version_info = {
        "version": f"tm-{datetime.date.today().isoformat()}-{tag}",
        "trained_on": trained_on,
        "epochs": epochs,
        "learning_rate": lr,
        "batch_size": batch_size,
        "validation_accuracy": val_accuracy,
        "test_accuracy": test_accuracy,
    }
    out_path = model_dir / "model_version.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(version_info, f, ensure_ascii=False, indent=2)
    print(f"[OK] {out_path}:")
    print(json.dumps(version_info, ensure_ascii=False, indent=2))
    return version_info


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="model/tm_model")
    ap.add_argument("--trained-on", required=True)
    ap.add_argument("--epochs", type=int, required=True)
    ap.add_argument("--lr", type=float, required=True)
    ap.add_argument("--batch-size", type=int, required=True)
    ap.add_argument("--val-accuracy", type=float, default=None)
    ap.add_argument("--test-accuracy", type=float, default=None)
    ap.add_argument("--tag", default="v1")
    args = ap.parse_args()
    set_model_version(args.model_dir, args.trained_on, args.epochs, args.lr,
                       args.batch_size, args.val_accuracy, args.test_accuracy, args.tag)
