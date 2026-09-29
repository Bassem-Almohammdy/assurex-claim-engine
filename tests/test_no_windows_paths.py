# tests/test_no_windows_paths.py
# يمنع رجوع مسارات ويندوز (\) داخل ملفات النتائج، لأنها تكسر القراءة على لينكس/ماك.
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "reports/validation_evaluation.json",
    "reports/test_evaluation.json",
    "reports/comparison_30_results.json",
    "reports/comparison_30_manifest.json",
    "reports/manifest.csv",
]


def test_no_backslash_paths_in_output_files():
    for rel in FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "\\" not in text, f"{rel} يحتوي على '\\' (مسار ويندوز). استخدم '/'."


if __name__ == "__main__":
    test_no_backslash_paths_in_output_files()
    print("[OK] لا توجد مسارات ويندوز في ملفات output/")
