#!/usr/bin/env python3
"""
predict_tm.py
--------------
AssureX Claim Engine — Member 3

يحمّل نموذج Teachable Machine (Keras .h5) ويُرجع التنبؤ بصيغة العقد المشترك
(TMPrediction في دستور المشروع، القسم 6):

    claim_id, tm_prediction, tm_probabilities, tm_confidence, model_version

أسماء الفئات في المخرجات قانونية دائمًا: "Valid" / "Invalid" / "Manual Review"
(نفس قيم claim_status في الـ Dataset). الاسم الخام القادم من labels.txt
(مثل Valid_Claim) يُرجَع في الحقل الإضافي tm_raw_label للتتبع فقط.

ملاحظات:
  * النموذج يُحمَّل مرة واحدة ويُخزَّن (cache) — مهم لشرط الـ 5 ثوانٍ في SRS.
  * نماذج TM بصيغة Keras 2 القديمة: نفرض TF_USE_LEGACY_KERAS=1 قبل استيراد
    tensorflow ونعتمد على tf-keras (موجودة في requirements.txt).

الاستخدام:
    python3 predict_tm.py --image path/to/card.jpg --claim-id 1250

من الـ Backend:
    from predict_tm import predict
    result = predict(pil_image_or_path, claim_id=1250)
"""

import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import argparse
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

MODEL_VERSION_FILE = "model_version.json"

# الاسم الخام في labels.txt  ->  القيمة القانونية في الدستور
CANONICAL_LABEL = {
    "Valid_Claim": "Valid",
    "Invalid_Claim": "Invalid",
    "Manual_Review": "Manual Review",
}


def canonical(label: str) -> str:
    """يحوّل اسم فئة TM إلى القيمة القانونية؛ يفشل صراحةً إن كانت الفئة غير معروفة."""
    if label in CANONICAL_LABEL:
        return CANONICAL_LABEL[label]
    if label in CANONICAL_LABEL.values():
        return label
    raise ValueError(f"فئة غير معروفة في labels.txt: {label!r}")


def load_labels(labels_path: Path):
    labels = []
    with open(labels_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # صيغة Teachable Machine المعتادة: "0 Valid_Claim"
            parts = line.split(" ", 1)
            labels.append(parts[1] if len(parts) == 2 else parts[0])
    return labels


def preprocess(image, size=(224, 224)):
    """يقبل مسار ملف أو كائن PIL.Image (لتصنيف بطاقة مولَّدة في الذاكرة)."""
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    array = np.asarray(image).astype(np.float32)
    data = np.ndarray(shape=(1, size[0], size[1], 3), dtype=np.float32)
    data[0] = (array / 127.5) - 1.0
    return data


def get_model_version(model_dir: Path):
    version_file = Path(model_dir) / MODEL_VERSION_FILE
    if version_file.exists():
        return json.loads(version_file.read_text(encoding="utf-8")).get("version", "unknown")
    return "unknown"


@lru_cache(maxsize=2)
def _load_model(model_path: str):
    try:
        from tensorflow.keras.models import load_model
    except ImportError as e:
        raise SystemExit(
            "يلزم تثبيت tensorflow و tf-keras لتشغيل هذا السكربت:\n"
            "pip install tensorflow tf-keras"
        ) from e
    return load_model(model_path, compile=False)


def build_result(probabilities, labels, version, claim_id=None):
    """يبني مخرجات العقد من متجه الاحتمالات. مفصولة عن TF لتسهيل الاختبار."""
    if len(probabilities) != len(labels):
        raise ValueError("عدد الاحتمالات لا يطابق عدد الفئات في labels.txt")
    top = int(np.argmax(probabilities))
    return {
        "claim_id": claim_id,
        "tm_prediction": canonical(labels[top]),
        "tm_probabilities": {canonical(labels[i]): float(probabilities[i]) for i in range(len(labels))},
        "tm_confidence": float(probabilities[top]),
        "tm_raw_label": labels[top],
        "model_version": version,
    }


def predict(image, model_dir: str = "model/tm_model", claim_id=None):
    model_dir = Path(model_dir)
    model_path = model_dir / "keras_model.h5"
    labels_path = model_dir / "labels.txt"

    if not model_path.exists() or not labels_path.exists():
        raise SystemExit(
            f"لم يتم العثور على النموذج المُصدَّر في {model_dir}.\n"
            "ضع keras_model.h5 و labels.txt المُصدَّرَين من Teachable Machine هنا."
        )

    model = _load_model(str(model_path))
    labels = load_labels(labels_path)
    probabilities = model.predict(preprocess(image), verbose=0)[0]
    return build_result(probabilities, labels, get_model_version(model_dir), claim_id)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="مسار صورة Claim Summary Card")
    ap.add_argument("--claim-id", default=None)
    ap.add_argument("--model-dir", default="model/tm_model")
    args = ap.parse_args()
    print(json.dumps(predict(args.image, args.model_dir, args.claim_id), ensure_ascii=False, indent=2))
