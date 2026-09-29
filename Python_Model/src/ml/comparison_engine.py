import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

# These thresholds are TEAM-CONFIGURED.
# The SRS requires configurable thresholds but does not
# specify exact numeric values.

MIN_CONFIDENCE_THRESHOLD = 0.60

STRONG_MATCH_MAX_DIFF = 0.10
ACCEPTABLE_MATCH_MAX_DIFF = 0.20


# =========================================================
# CONSISTENCY LOGIC
# =========================================================

def calculate_consistency(row):

    python_prediction = row["python_prediction"]
    tm_prediction = row["tm_prediction"]

    python_confidences = {
        "Invalid": float(row["Invalid_probability"]),
        "Manual Review": float(row["Manual_Review_probability"]),
        "Valid": float(row["Valid_probability"])
    }

    tm_confidences = {
        "Invalid": float(row["tm_invalid_probability"]),
        "Manual Review": float(row["tm_manual_review_probability"]),
        "Valid": float(row["tm_valid_probability"])
    }

    python_top_confidence = max(python_confidences.values())
    tm_top_confidence = max(tm_confidences.values())

    # -----------------------------------------------------
    # Predicted-class match
    # -----------------------------------------------------

    predicted_class_match = (
        python_prediction == tm_prediction
    )

    # -----------------------------------------------------
    # Confidence difference
    # -----------------------------------------------------

    confidence_difference = abs(
        python_top_confidence - tm_top_confidence
    )

    # -----------------------------------------------------
    # Consistency status
    # -----------------------------------------------------

    if not predicted_class_match:
        status = "Model Disagreement"

    elif (
        python_top_confidence < MIN_CONFIDENCE_THRESHOLD
        or tm_top_confidence < MIN_CONFIDENCE_THRESHOLD
    ):
        status = "Uncertain Result"

    elif confidence_difference <= STRONG_MATCH_MAX_DIFF:
        status = "Strong Match"

    elif confidence_difference <= ACCEPTABLE_MATCH_MAX_DIFF:
        status = "Acceptable Match"

    else:
        status = "Weak Match"

    return pd.Series({
        "predicted_class_match": predicted_class_match,
        "top_class_confidence_difference": round(
            confidence_difference, 6
        ),
        "model_consistency_status": status
    })


# =========================================================
# MAIN
# =========================================================

input_file = "models/model_comparison_30.csv"
output_file = "models/final_model_comparison.csv"

df = pd.read_csv(input_file)

required_columns = [
    "python_prediction",
    "Invalid_probability",
    "Manual_Review_probability",
    "Valid_probability",
    "tm_prediction",
    "tm_invalid_probability",
    "tm_manual_review_probability",
    "tm_valid_probability"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("Missing required columns:")
    for column in missing_columns:
        print("-", column)

    print("\nTM results must be added before running this script.")
    exit()


results = df.apply(
    calculate_consistency,
    axis=1
)

df[
    [
        "predicted_class_match",
        "top_class_confidence_difference",
        "model_consistency_status"
    ]
] = results


df.to_csv(output_file, index=False)


print("=" * 50)
print("MODEL COMPARISON UPDATED")
print("=" * 50)

print(f"Total Claims: {len(df)}")

print("\nConsistency Status:")
print(
    df["model_consistency_status"]
    .value_counts()
)

print("\nSaved:")
print(output_file)