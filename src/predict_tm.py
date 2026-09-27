#!/usr/bin/env python3
"""
predict_tm.py
--------------
AssureX Claim Engine — Member 3

يحمّل نموذج Teachable Machine بعد تصديره بصيغة Tensorflow/Keras (.h5)
ويعطي نتيجة تنبؤ بنفس أسماء الحقول المتفق عليها مع باقي الفريق
(انظر جدول العقد المشترك في دستور المشروع):

    tm_prediction      -> اسم الفئة المتوقعة (Valid / Invalid / Manual Review)
    tm_probabilities   -> احتمالات الفئات الثلاث
    tm_confidence      -> ثقة الفئة الأعلى
    model_version       -> رقم/تاريخ إصدار الموديل المحمّل

لا يعمل هذا الملف إلا بعد أن يقوم باسم بتصدير النموذج فعلياً من موقع
teachablemachine.withgoogle.com ووضع الملفين التاليين داخل model/tm_model/:

    model/tm_model/keras_model.h5
    model/tm_model/labels.txt

ملاحظة توافق مهمة:
    نماذج Teachable Machine تُصدَّر بصيغة Keras قديمة جداً (2.4.0)، ونسخ
    TensorFlow/Keras الحديثة (Keras 3، الافتراضية منذ TF 2.16) لا تستطيع
    تحميلها مباشرة وتعطي أخطاء مثل "Unrecognized keyword arguments...
    groups" أو أخطاء Sequential/Functional متداخلة. لهذا السبب هذا الملف
    يفرض استخدام محرك Keras 2 القديم (عبر متغير البيئة TF_USE_LEGACY_KERAS)
    *قبل* استيراد tensorflow. هذا يتطلب تثبيت حزمة tf-keras بجانب
    tensorflow (موجودة في requirements.txt).

الاستخدام:
    python3 predict_tm.py --image path/to/card.jpg --model-dir model/tm_model
"""

import os
# يجب ضبط هذا المتغير قبل أي استيراد لـ tensorflow حتى يُطبَّق فعلياً.
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")  # تقليل رسائل TensorFlow غير الضرورية

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

MODEL_VERSION_FILE = "model_version.json"


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


def preprocess(image_path: Path, size=(224, 224)):
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    array = np.asarray(image).astype(np.float32)
    normalized = (array / 127.5) - 1.0
    data = np.ndarray(shape=(1, size[0], size[1], 3), dtype=np.float32)
    data[0] = normalized
    return data


def get_model_version(model_dir: Path):
    version_file = model_dir / MODEL_VERSION_FILE
    if version_file.exists():
        return json.loads(version_file.read_text(encoding="utf-8")).get("version", "unknown")
    # افتراضي: وقت تعديل ملف الموديل نفسه كمعرّف نسخة تلقائي
    model_file = model_dir / "keras_model.h5"
    if model_file.exists():
        import datetime
        ts = model_file.stat().st_mtime
        return datetime.datetime.fromtimestamp(ts).strftime("tm-%Y%m%d-%H%M%S")
    return "unknown"


def predict(image_path: str, model_dir: str = "model/tm_model"):
    try:
        from tensorflow.keras.models import load_model
    except ImportError as e:
        raise SystemExit(
            "يلزم تثبيت tensorflow و tf-keras لتشغيل هذا السكربت:\n"
            "pip install tensorflow tf-keras"
        ) from e

    model_dir = Path(model_dir)
    model_path = model_dir / "keras_model.h5"
    labels_path = model_dir / "labels.txt"

    if not model_path.exists() or not labels_path.exists():
        raise SystemExit(
            f"لم يتم العثور على النموذج المُصدَّر في {model_dir}.\n"
            "درّب النموذج على teachablemachine.withgoogle.com ثم صدّره بصيغة "
            "Tensorflow > Keras وضع الملفين keras_model.h5 و labels.txt هنا."
        )

    model = load_model(model_path, compile=False)
    labels = load_labels(labels_path)

    data = preprocess(Path(image_path))
    probabilities = model.predict(data, verbose=0)[0]

    top_index = int(np.argmax(probabilities))
    result = {
        "tm_prediction": labels[top_index],
        "tm_probabilities": {labels[i]: float(probabilities[i]) for i in range(len(labels))},
        "tm_confidence": float(probabilities[top_index]),
        "model_version": get_model_version(model_dir),
    }
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="مسار صورة Claim Summary Card")
    ap.add_argument("--model-dir", default="model/tm_model")
    args = ap.parse_args()

    output = predict(args.image, args.model_dir)
    print(json.dumps(output, ensure_ascii=False, indent=2))
