import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Load dataset
df = pd.read_csv("data/claims.csv")

# First split: 70% train, 30% temporary
train, temp = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["claim_status"]
)

# Second split: 15% validation, 15% test
validation, test = train_test_split(
    temp,
    test_size=0.50,
    random_state=42,
    stratify=temp["claim_status"]
)

# Save files
os.makedirs("data", exist_ok=True)

train.to_csv("data/train.csv", index=False)
validation.to_csv("data/validation.csv", index=False)
test.to_csv("data/test.csv", index=False)

# Display results
print("=" * 50)
print("DATASET SPLIT COMPLETED")
print("=" * 50)

print("\nTrain:")
print(len(train))
print(train["claim_status"].value_counts())

print("\nValidation:")
print(len(validation))
print(validation["claim_status"].value_counts())

print("\nTest:")
print(len(test))
print(test["claim_status"].value_counts())

print("\nFiles created:")
print("data/train.csv")
print("data/validation.csv")
print("data/test.csv")

print("=" * 50)