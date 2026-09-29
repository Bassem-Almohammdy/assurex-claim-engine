import pandas as pd
import joblib
import os

# Load trained model
pipeline = joblib.load("models/xgboost_pipeline.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# Load test dataset
test_df = pd.read_csv("data/test.csv")

# Save actual labels
actual_labels = test_df["claim_status"]

# Keep claim IDs
claim_ids = test_df["claim_id"]

# Prepare input data
X_test = test_df.drop(
    ["claim_status", "claim_id"],
    axis=1
)

# Add derived feature
X_test["remaining_warranty_months"] = (
    X_test["warranty_period_months"]
    - X_test["product_age_months"]
)

# Predict
predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)

# Convert predictions to labels
predicted_labels = label_encoder.inverse_transform(
    predictions.astype(int)
)

# Create results
results = pd.DataFrame({
    "claim_id": claim_ids,
    "actual_class": actual_labels,
    "python_prediction": predicted_labels,
    "Invalid_probability": probabilities[:, 0],
    "Manual_Review_probability": probabilities[:, 1],
    "Valid_probability": probabilities[:, 2],
    "top_confidence": probabilities.max(axis=1)
})

# Create output folder
os.makedirs("models", exist_ok=True)

# Save results
results.to_csv(
    "models/python_test_predictions.csv",
    index=False
)

print("=" * 60)
print("ASSUREX BATCH PREDICTION")
print("=" * 60)

print("\nTotal Claims:")
print(len(results))

print("\nFirst 10 Predictions:")
print(results.head(10).to_string(index=False))

print("\nPrediction Distribution:")
print(results["python_prediction"].value_counts())

print("\nResults saved to:")
print("models/python_test_predictions.csv")

print("=" * 60)