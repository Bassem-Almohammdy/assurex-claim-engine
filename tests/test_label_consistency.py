# tests/test_label_consistency.py
#
# AssureX Claim Engine — Member 3
#
# يمنع تكرار عطل سابق موثّق في README_Member3.md القسم 4: تعارض صامت بين
# label_mapping.json (يُستهلك من Member 5) و labels.txt (المصدر الحقيقي
# القادم من تصدير Teachable Machine). شغّله قبل أي commit يمس
# model/tm_model/ أو output/label_mapping.json.
#
#   python3 -m pytest tests/test_label_consistency.py -v

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from predict_tm import load_labels

MODEL_DIR = Path(__file__).resolve().parent.parent / "model" / "tm_model"
MAPPING_PATH = Path(__file__).resolve().parent.parent / "reports" / "label_mapping.json"


def test_label_mapping_matches_real_model():
    real_labels = load_labels(MODEL_DIR / "labels.txt")
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    mapped_labels = [mapping["index_to_label"][str(i)] for i in range(len(real_labels))]

    # لا نطلب تطابق الأسماء حرفيًا (Valid مقابل Valid_Claim) بل تطابق الترتيب المنطقي
    assert len(mapped_labels) == len(real_labels), "عدد الفئات غير متطابق!"

    def normalize(label):
        return label.replace("_", " ").replace("Claim", "").strip().lower()

    for i, (mapped, real) in enumerate(zip(mapped_labels, real_labels)):
        assert normalize(mapped) == normalize(real), (
            f"عدم تطابق ترتيب الفئات عند الفهرس {i}: "
            f"label_mapping.json يقول '{mapped}' بينما labels.txt الحقيقي يقول '{real}'. "
            f"شغّل build_label_mapping.py لإعادة التوليد."
        )


def test_model_version_file_exists_and_filled():
    version_path = MODEL_DIR / "model_version.json"
    assert version_path.exists(), "model_version.json غير موجود — شغّل set_model_version.py"
    info = json.loads(version_path.read_text(encoding="utf-8"))
    for key in ["version", "epochs", "learning_rate", "batch_size"]:
        assert info.get(key) is not None, f"model_version.json: الحقل '{key}' فارغ (null)"


if __name__ == "__main__":
    test_label_mapping_matches_real_model()
    test_model_version_file_exists_and_filled()
    print("[OK] كل اختبارات اتساق الفئات نجحت.")
