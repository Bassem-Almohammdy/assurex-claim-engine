import os
import subprocess
import sys

# Always work relative to this script's own folder, no matter where
# the terminal's current directory is when the script is launched.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

steps = [
    "data_generator.py",
    "data_validation.py",
    "create_splits.py",
    "generate_report.py",
]

for step in steps:
    print("\nRunning:", step)
    result = subprocess.run([sys.executable, step], cwd=BASE_DIR)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

print("\nAssureX Data Engineering pipeline completed successfully.")
