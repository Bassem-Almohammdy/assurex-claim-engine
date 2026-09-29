import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("data/claims.csv")


# ==========================================
# 2. Feature Engineering
# ==========================================

df["remaining_warranty_months"] = (
    df["warranty_period_months"] - df["product_age_months"]
)


# ==========================================
# 3. Separate Features and Target
# ==========================================

X = df.drop(["claim_status", "claim_id"], axis=1)

y = df["claim_status"]


# ==========================================
# 4. Define Feature Types
# ==========================================

numeric_features = [
    "product_age_months",
    "warranty_period_months",
    "receipt_available",
    "serial_number_valid",
    "repair_history",
    "purchase_price",
    "claim_amount",
    "days_since_purchase",
    "remaining_warranty_months"
]

categorical_features = [
    "product_category",
    "damage_type"
]


# ==========================================
# 5. Split Dataset
# ==========================================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)


# ==========================================
# 6. Create Preprocessor
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# ==========================================
# 7. Create Logistic Regression Model
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# ==========================================
# 8. Create Complete Pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 9. Train Model
# ==========================================

print("=" * 50)
print("TRAINING LOGISTIC REGRESSION")
print("=" * 50)

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# ==========================================
# 10. Validation Prediction
# ==========================================

y_val_pred = pipeline.predict(X_val)


# ==========================================
# 11. Validation Evaluation
# ==========================================

validation_accuracy = accuracy_score(
    y_val,
    y_val_pred
)

print("\nValidation Accuracy:")
print(validation_accuracy)


print("\nValidation Classification Report:")
print(
    classification_report(
        y_val,
        y_val_pred
    )
)


# ==========================================
# 12. Test Prediction
# ==========================================

y_test_pred = pipeline.predict(X_test)


# ==========================================
# 13. Test Evaluation
# ==========================================

test_accuracy = accuracy_score(
    y_test,
    y_test_pred
)

print("\nTest Accuracy:")
print(test_accuracy)


print("\nTest Classification Report:")
print(
    classification_report(
        y_test,
        y_test_pred
    )
)


# ==========================================
# 14. Test Probabilities
# ==========================================

test_probabilities = pipeline.predict_proba(X_test)

print("\nFirst 5 Test Predictions:")
print(pipeline.predict(X_test[:5]))

print("\nFirst 5 Prediction Probabilities:")
print(test_probabilities[:5])


print("\nClasses:")
print(pipeline.classes_)

print("\n" + "=" * 50)
print("MODEL TRAINING COMPLETED")
print("=" * 50)