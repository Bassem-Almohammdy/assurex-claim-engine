import pandas as pd
import joblib

pipeline = joblib.load("models/xgboost_pipeline.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

MODEL_VERSION = "1.0"


def predict_claim(claim_data, claim_id):

    df = pd.DataFrame([claim_data])

    # Derived feature
    if "remaining_warranty_months" not in df.columns:
        df["remaining_warranty_months"] = (
            df["warranty_period_months"]
            - df["product_age_months"]
        )

    prediction = pipeline.predict(df)[0]
    probabilities = pipeline.predict_proba(df)[0]

    predicted_label = label_encoder.inverse_transform(
        [prediction]
    )[0]

    class_probabilities = {}

    for class_label, probability in zip(
        label_encoder.classes_,
        probabilities
    ):
        class_probabilities[class_label] = float(probability)

    result = {
        "claim_id": claim_id,

        "python_prediction": predicted_label,

        "python_probabilities": class_probabilities,

        "python_confidence": float(probabilities.max()),

        "model_name": "XGBoost",
        "model_version": MODEL_VERSION
    }

    return result