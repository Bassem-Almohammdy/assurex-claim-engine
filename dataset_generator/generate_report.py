"""
Generates statistical charts and a short summary report describing the
AssureX common claims dataset. Run this after run_pipeline.py so that
data/claims.csv, data/train.csv, data/validation.csv and data/test.csv
already exist.

Output:
    reports/class_distribution.png
    reports/product_category_distribution.png
    reports/product_age_distribution.png
    reports/claim_amount_distribution.png
    reports/split_distribution.png
    reports/dataset_report.md
"""

import os
import sys

try:
    import pandas as pd
except ModuleNotFoundError:
    sys.exit(
        "Missing dependency: pandas.\n"
        "Run: pip install -r requirements.txt"
    )

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    sys.exit(
        "Missing dependency: matplotlib.\n"
        "Run: pip install -r requirements.txt"
    )

try:
    import tabulate  # noqa: F401  (required by DataFrame.to_markdown)
except ModuleNotFoundError:
    sys.exit(
        "Missing dependency: tabulate.\n"
        "Run: pip install -r requirements.txt"
    )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

DATA_DIR = "data"
REPORTS_DIR = "reports"

required_files = ["claims.csv", "train.csv", "validation.csv", "test.csv"]
missing = [f for f in required_files if not os.path.exists(os.path.join(DATA_DIR, f))]
if missing:
    sys.exit(
        "Missing input file(s) in data/: " + ", ".join(missing) + "\n"
        "Run data_generator.py and create_splits.py first (or run_pipeline.py)."
    )

os.makedirs(REPORTS_DIR, exist_ok=True)

master = pd.read_csv(os.path.join(DATA_DIR, "claims.csv"))
train = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
validation = pd.read_csv(os.path.join(DATA_DIR, "validation.csv"))
test = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))


def save_bar(series, title, xlabel, filename, rotate=0):
    counts = series.value_counts().sort_index()
    plt.figure(figsize=(7, 4.5))
    counts.plot(kind="bar", color="#4C72B0")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.xticks(rotation=rotate, ha="right" if rotate else "center")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, filename), dpi=150)
    plt.close()


def save_hist(series, title, xlabel, filename, bins=20):
    plt.figure(figsize=(7, 4.5))
    plt.hist(series, bins=bins, color="#55A868", edgecolor="white")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, filename), dpi=150)
    plt.close()


# 1. Class distribution (Valid / Invalid / Manual Review)
save_bar(master["claim_status"], "Claim Status Distribution",
         "Claim Status", "class_distribution.png")

# 2. Product category distribution
save_bar(master["product_category"], "Product Category Distribution",
         "Product Category", "product_category_distribution.png", rotate=30)

# 3. Product age distribution
save_hist(master["product_age_months"], "Product Age Distribution",
          "Product Age (months)", "product_age_distribution.png")

# 4. Claim amount distribution
save_hist(master["claim_amount"], "Claim Amount Distribution",
          "Claim Amount", "claim_amount_distribution.png")

# 5. Train / validation / test split sizes
split_counts = pd.Series({
    "Train": len(train),
    "Validation": len(validation),
    "Test": len(test),
})
plt.figure(figsize=(6, 4.5))
split_counts.plot(kind="bar", color="#C44E52")
plt.title("Dataset Split Sizes")
plt.ylabel("Number of Claims")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "split_distribution.png"), dpi=150)
plt.close()

# Written summary report
report_lines = [
    "# Dataset Statistical Report",
    "",
    f"Total records: {len(master)}",
    "",
    "## Claim Status Distribution",
    master["claim_status"].value_counts().to_markdown(),
    "",
    "## Split Sizes",
    split_counts.to_frame("count").to_markdown(),
    "",
    "## Product Category Distribution",
    master["product_category"].value_counts().to_markdown(),
    "",
    "## Numeric Feature Summary",
    master[["product_age_months", "warranty_period_months",
             "purchase_price", "claim_amount",
             "days_since_purchase"]].describe().round(2).to_markdown(),
    "",
    "## Charts",
    "- class_distribution.png",
    "- product_category_distribution.png",
    "- product_age_distribution.png",
    "- claim_amount_distribution.png",
    "- split_distribution.png",
]

with open(os.path.join(REPORTS_DIR, "dataset_report.md"), "w") as f:
    f.write("\n\n".join(report_lines))

print("Report generated in:", REPORTS_DIR)
