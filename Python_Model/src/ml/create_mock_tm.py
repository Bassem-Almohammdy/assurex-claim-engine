import pandas as pd
import os

INPUT_FILE = "models/model_comparison_30.csv"
OUTPUT_FILE = "models/mock_tm_predictions_30.csv"

df = pd.read_csv(INPUT_FILE)

mock_predictions = []

for i, claim_id in enumerate(df["claim_id"], start=1):

    pattern = i % 3

    if pattern == 1:
        prediction = "Valid"
        invalid = 0.05
        manual = 0.10
        valid = 0.85

    elif pattern == 2:
        prediction = "Invalid"
        invalid = 0.82
        manual = 0.13
        valid = 0.05

    else:
        prediction = "Manual Review"
        invalid = 0.15
        manual = 0.72
        valid = 0.13

    mock_predictions.append({
        "claim_id": claim_id,
        "tm_prediction": prediction,
        "tm_invalid_probability": invalid,
        "tm_manual_review_probability": manual,
        "tm_valid_probability": valid
    })

mock_df = pd.DataFrame(mock_predictions)

os.makedirs("models", exist_ok=True)

mock_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Mock TM predictions created successfully.")
print(f"Total claims: {len(mock_df)}")
print(f"Saved to: {OUTPUT_FILE}")