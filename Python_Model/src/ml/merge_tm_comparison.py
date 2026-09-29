import pandas as pd

COMPARISON_FILE = "models/model_comparison_30.csv"
TM_FILE = "models/mock_tm_predictions_30.csv"

comparison = pd.read_csv(COMPARISON_FILE)
tm = pd.read_csv(TM_FILE)

tm_columns = [
    "claim_id",
    "tm_prediction",
    "tm_invalid_probability",
    "tm_manual_review_probability",
    "tm_valid_probability"
]

tm = tm[tm_columns]

# Remove old TM columns if they already exist
columns_to_remove = [
    "tm_prediction",
    "tm_invalid_probability",
    "tm_manual_review_probability",
    "tm_valid_probability"
]

comparison = comparison.drop(
    columns=columns_to_remove,
    errors="ignore"
)

# Merge using claim_id
comparison = comparison.merge(
    tm,
    on="claim_id",
    how="left"
)

comparison.to_csv(
    COMPARISON_FILE,
    index=False
)

print("TM predictions merged successfully.")
print(f"Total claims: {len(comparison)}")
print(f"Updated: {COMPARISON_FILE}")

print("\nTM prediction distribution:")
print(comparison["tm_prediction"].value_counts())