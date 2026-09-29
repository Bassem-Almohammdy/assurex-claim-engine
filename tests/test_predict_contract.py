# tests/test_predict_contract.py — Member 3
# يتحقق من عقد TMPrediction (الدستور القسم 6) دون الحاجة لـ TensorFlow.
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import predict_tm as p  # noqa: E402

RAW = ["Manual_Review", "Invalid_Claim", "Valid_Claim"]  # نفس ترتيب labels.txt الحالي


def test_canonical_names_and_contract_fields():
    r = p.build_result(np.array([0.06, 0.03, 0.91]), RAW, "tm-test", claim_id=1250)
    assert r["tm_prediction"] == "Valid"
    assert set(r["tm_probabilities"]) == {"Valid", "Invalid", "Manual Review"}
    assert r["tm_confidence"] == pytest_approx(0.91)
    assert r["claim_id"] == 1250 and r["model_version"] == "tm-test"
    assert abs(sum(r["tm_probabilities"].values()) - 1.0) < 1e-6


def test_manual_review_and_invalid_map_correctly():
    assert p.build_result(np.array([0.7, 0.2, 0.1]), RAW, "v")["tm_prediction"] == "Manual Review"
    assert p.build_result(np.array([0.1, 0.8, 0.1]), RAW, "v")["tm_prediction"] == "Invalid"


def test_unknown_label_fails_loudly():
    try:
        p.canonical("Approved")
    except ValueError:
        return
    raise AssertionError("كان يجب رفض فئة غير معروفة")


def test_real_labels_file_is_supported():
    labels = p.load_labels(Path(__file__).resolve().parent.parent / "model" / "tm_model" / "labels.txt")
    assert sorted(p.canonical(l) for l in labels) == ["Invalid", "Manual Review", "Valid"]


def pytest_approx(x):
    class A:
        def __eq__(self, other):
            return abs(other - x) < 1e-6
    return A()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("[OK]", name)
