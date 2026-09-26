import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, StratifiedKFold

from xgboost import XGBClassifier


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
# 4. Encode Target Labels
# ==========================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)


# ==========================================
# 5. Define Feature Types
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
# 6. Split Dataset
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
# 7. Create Preprocessor
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
# 8. Create XGBoost Model
# ==========================================

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softprob",
    num_class=3,
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 9. Create Complete Pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 10. Train Model
# ==========================================

print("=" * 50)
print("TRAINING XGBOOST")
print("=" * 50)

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed.")

# ==========================================
# 10.5. 5-Fold Cross-Validation
# ==========================================

print("\n5-Fold Cross-Validation:")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    pipeline,
    X_train,
    y_train,
    cv=cv,
    scoring="accuracy"
)

print("Fold Accuracies:")
print(cv_scores)

print("Mean Accuracy:")
print(cv_scores.mean())

print("Standard Deviation:")
print(cv_scores.std())


# ==========================================
# 11. Validation Prediction
# ==========================================

y_val_pred = pipeline.predict(X_val)


# ==========================================
# 12. Convert Predictions Back to Labels
# ==========================================

y_val_pred_labels = label_encoder.inverse_transform(
    y_val_pred.astype(int)
)

y_val_labels = label_encoder.inverse_transform(
    y_val.astype(int)
)


# ==========================================
# 13. Validation Evaluation
# ==========================================

validation_accuracy = accuracy_score(
    y_val_labels,
    y_val_pred_labels
)

print("\nValidation Accuracy:")
print(validation_accuracy)


print("\nValidation Classification Report:")
print(
    classification_report(
        y_val_labels,
        y_val_pred_labels
    )
)


# ==========================================
# 14. Test Prediction
# ==========================================

y_test_pred = pipeline.predict(X_test)

y_test_pred_labels = label_encoder.inverse_transform(
    y_test_pred.astype(int)
)

y_test_labels = label_encoder.inverse_transform(
    y_test.astype(int)
)


# ==========================================
# 15. Test Evaluation
# ==========================================

test_accuracy = accuracy_score(
    y_test_labels,
    y_test_pred_labels
)

print("\nTest Accuracy:")
print(test_accuracy)


print("\nTest Classification Report:")
print(
    classification_report(
        y_test_labels,
        y_test_pred_labels
    )
)
print("\nTest Confusion Matrix:")
cm = confusion_matrix(y_test, y_test_pred)

print(cm)


# ==========================================
# 16. Test Probabilities
# ==========================================

test_probabilities = pipeline.predict_proba(X_test)

print("\nFirst 5 Test Predictions:")
print(y_test_pred_labels[:5])


print("\nFirst 5 Prediction Probabilities:")
print(test_probabilities[:5])


# ==========================================
# 17. Display Classes
# ==========================================

print("\nClasses:")

print(label_encoder.classes_)


print("\n" + "=" * 50)
print("XGBOOST TRAINING COMPLETED")
print("=" * 50)