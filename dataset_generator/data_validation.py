import pandas as pd

REQUIRED_COLUMNS = [
    "claim_id", "product_category", "product_age_months",
    "warranty_period_months", "receipt_available", "serial_number_valid",
    "damage_type", "repair_history", "purchase_price",
    "claim_amount", "days_since_purchase", "claim_status"
]

df = pd.read_csv("data/raw/claims_master.csv")
errors = []

missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing:
    errors.append("Missing columns: " + ", ".join(missing))

if not df["claim_id"].is_unique:
    errors.append("Duplicate claim_id values found.")

if df.duplicated().any():
    errors.append("Duplicate claim records found.")

if df[REQUIRED_COLUMNS].isnull().any().any():
    errors.append("Missing values found.")

if (df["purchase_price"] <= 0).any():
    errors.append("purchase_price must be greater than 0.")

if (df["claim_amount"] < 0).any():
    errors.append("claim_amount cannot be negative.")

if (df["product_age_months"] < 0).any():
    errors.append("product_age_months cannot be negative.")

if (df["warranty_period_months"] <= 0).any():
    errors.append("warranty_period_months must be greater than 0.")

if (df["days_since_purchase"] < 0).any():
    errors.append("days_since_purchase cannot be negative.")

if (df["repair_history"] < 0).any():
    errors.append("repair_history cannot be negative.")

if not df["receipt_available"].isin([0, 1]).all():
    errors.append("receipt_available must contain only 0 or 1.")

if not df["serial_number_valid"].isin([0, 1]).all():
    errors.append("serial_number_valid must contain only 0 or 1.")

if not df["claim_status"].isin(["Valid", "Invalid", "Manual Review"]).all():
    errors.append("Invalid claim_status value found.")

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("VALIDATION PASSED")
print("Rows:", len(df))
print(df["claim_status"].value_counts())
