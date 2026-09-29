import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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
# 6. Create Preprocessing Pipeline
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
# 7. Display Dataset Information
# ==========================================

print("=" * 50)
print("ASSUREX CLAIM ENGINE - DATA PREPROCESSING")
print("=" * 50)

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nTraining Set:")
print(X_train.shape)

print("\nValidation Set:")
print(X_val.shape)

print("\nTest Set:")
print(X_test.shape)

print("\nTarget Distribution - Training:")
print(y_train.value_counts())

print("\nTarget Distribution - Validation:")
print(y_val.value_counts())

print("\nTarget Distribution - Test:")
print(y_test.value_counts())

print("\nFeatures:")
print(X.columns.tolist())

print("\nPreprocessing is ready.")
print("=" * 50)