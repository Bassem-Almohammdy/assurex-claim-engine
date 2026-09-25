import pandas as pd
from sklearn.model_selection import train_test_split
from config import RANDOM_SEED

df = pd.read_csv("data/raw/claims_master.csv")

train, temp = train_test_split(
    df, test_size=0.30, random_state=RANDOM_SEED,
    stratify=df["claim_status"]
)

validation, test = train_test_split(
    temp, test_size=0.50, random_state=RANDOM_SEED,
    stratify=temp["claim_status"]
)

train.to_csv("splits/train.csv", index=False)
validation.to_csv("splits/validation.csv", index=False)
test.to_csv("splits/test.csv", index=False)

print("Training:", len(train))
print("Validation:", len(validation))
print("Testing:", len(test))

if len(set(train.claim_id) & set(validation.claim_id)) > 0:
    raise ValueError("Data leakage detected between train and validation.")

if len(set(train.claim_id) & set(test.claim_id)) > 0:
    raise ValueError("Data leakage detected between train and test.")

if len(set(validation.claim_id) & set(test.claim_id)) > 0:
    raise ValueError("Data leakage detected between validation and test.")

print("No claim ID overlap. Data leakage check passed.")
