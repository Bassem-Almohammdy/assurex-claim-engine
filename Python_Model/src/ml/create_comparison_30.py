import pandas as pd

# Load Python test predictions
df = pd.read_csv("models/python_test_predictions.csv")

# Select 10 claims from each actual class
comparison = (
    df.groupby("actual_class", group_keys=False)
      .head(10)
      .copy()
)

# Add Teachable Machine / Rule Engine fields
comparison["claim_summary_card_filename"] = ""

comparison["tm_prediction"] = ""

comparison["tm_invalid_probability"] = ""
comparison["tm_manual_review_probability"] = ""
comparison["tm_valid_probability"] = ""

comparison["predicted_class_match"] = ""

comparison["top_class_confidence_difference"] = ""

comparison["model_consistency_status"] = ""

comparison["warranty_rule_result"] = ""

comparison["missing_documents"] = ""

comparison["contradictions_detected"] = ""

comparison["duplicate_claim_indicators"] = ""

comparison["final_application_decision"] = ""

comparison["major_disagreement_explanation"] = ""

# Save
comparison.to_csv(
    "models/model_comparison_30.csv",
    index=False
)

print("=" * 60)
print("30-CLAIM COMPARISON DATASET")
print("=" * 60)

print("\nTotal Claims:")
print(len(comparison))

print("\nActual Class Distribution:")
print(comparison["actual_class"].value_counts())

print("\nSaved:")
print("models/model_comparison_30.csv")

print("=" * 60)