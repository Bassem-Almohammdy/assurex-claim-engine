# tests/test_dataset_integrity.py — Member 3
# يتحقق من قواعد الدستور (القسم 14): لا تسريب بين الأقسام، 70/15/15، توازن الفئات،
# 2100 صورة تدريب كحد أدنى، تطابق manifest مع CSV، وأن عينة الـ30 من Test فقط.
#   python3 -m pytest tests/test_dataset_integrity.py -v     (أو python3 tests/test_dataset_integrity.py)
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLASSES = {"Valid", "Invalid", "Manual Review"}


def read(name):
    with open(ROOT / "data" / "splits" / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_split_sizes_and_balance():
    tr, va, te = read("train"), read("validation"), read("test")
    assert (len(tr), len(va), len(te)) == (1050, 225, 225)
    for rows, per in ((tr, 350), (va, 75), (te, 75)):
        assert Counter(r["claim_status"] for r in rows) == {c: per for c in CLASSES}


def test_no_leakage_between_splits():
    ids = [set(r["claim_id"] for r in read(n)) for n in ("train", "validation", "test")]
    assert not (ids[0] & ids[1]) and not (ids[0] & ids[2]) and not (ids[1] & ids[2])
    assert len(ids[0] | ids[1] | ids[2]) == 1500


def test_manifest_matches_csv_and_minimum_training_images():
    with open(ROOT / "reports" / "manifest.csv", newline="", encoding="utf-8") as f:
        m = list(csv.DictReader(f))
    split_of = {}
    for n in ("train", "validation", "test"):
        for r in read(n):
            split_of[r["claim_id"]] = (n, r["claim_status"])
    for row in m:
        assert split_of[row["claim_id"]] == (row["split"], row["claim_status"]), row
        assert "\\" not in row["file_path"], "مسار بصيغة ويندوز"
    train_imgs = [r for r in m if r["split"] == "train"]
    assert len(train_imgs) >= 2100
    per_claim = Counter(r["claim_id"] for r in train_imgs)
    assert min(per_claim.values()) >= 2, "كل Claim تدريب يحتاج نسختين على الأقل"


def test_comparison_sample_is_30_unseen_test_claims():
    man = json.loads((ROOT / "reports" / "comparison_30_manifest.json").read_text(encoding="utf-8"))
    test_ids = {r["claim_id"] for r in read("test")}
    assert len(man) == 30 and len({x["claim_id"] for x in man}) == 30
    assert all(x["claim_id"] in test_ids for x in man)
    assert Counter(x["true_class"] for x in man) == {c: 10 for c in CLASSES}


def test_generator_never_writes_model_outputs_on_cards():
    src = (ROOT / "src" / "generate_claim_cards.py").read_text(encoding="utf-8")
    body = src.split("def render_card", 1)[1].split("def read_split", 1)[0]
    for forbidden in ("python_prediction", "python_confidence", "final_decision", "claim_status"):
        assert forbidden not in body, f"'{forbidden}' ظهر داخل render_card"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("[OK]", name)
