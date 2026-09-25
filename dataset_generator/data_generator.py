import random
import pandas as pd
from config import TARGET_PER_CLASS, RANDOM_SEED, PRODUCT_CATEGORIES, DAMAGE_TYPES, WARRANTY_OPTIONS, CLASS_NAMES

random.seed(RANDOM_SEED)

PRICE_RANGES = {
    "Smartphone": (150, 1500), "Laptop": (400, 2500),
    "Tablet": (150, 1200), "TV": (250, 2000),
    "Refrigerator": (400, 2500), "Washing Machine": (300, 1800),
    "Camera": (250, 2200), "Headphones": (30, 500)
}

def make_record(status):
    category = random.choice(PRODUCT_CATEGORIES)
    warranty = random.choice(WARRANTY_OPTIONS)

    if status == "Valid":
        age = random.randint(1, warranty)
        receipt, serial = 1, 1
        damage = random.choice(["Manufacturing Defect", "Battery Failure", "Software Failure", "Electrical Failure"])
        repairs = random.randint(0, 2)
        ratio = random.uniform(0.10, 0.85)

    elif status == "Invalid":
        age = random.randint(warranty + 1, 60)
        receipt = random.choices([0, 1], weights=[75, 25])[0]
        serial = random.choices([0, 1], weights=[70, 30])[0]
        damage = random.choice(["Water Damage", "Physical Damage", "Unknown"])
        repairs = random.randint(1, 4)
        ratio = random.uniform(0.10, 0.80)

    else:
        age = random.randint(1, 60)
        receipt, serial = random.randint(0, 1), random.randint(0, 1)
        damage = random.choice(DAMAGE_TYPES)
        repairs = random.randint(0, 4)
        ratio = random.uniform(0.50, 1.10)

    low, high = PRICE_RANGES[category]
    purchase_price = round(random.uniform(low, high), 2)
    claim_amount = round(purchase_price * ratio, 2)
    days_since_purchase = max(1, age * 30 + random.randint(-15, 15))

    return {
        "product_category": category,
        "product_age_months": age,
        "warranty_period_months": warranty,
        "receipt_available": receipt,
        "serial_number_valid": serial,
        "damage_type": damage,
        "repair_history": repairs,
        "purchase_price": purchase_price,
        "claim_amount": claim_amount,
        "days_since_purchase": days_since_purchase,
        "claim_status": status
    }

rows = []
for status in CLASS_NAMES:
    for _ in range(TARGET_PER_CLASS):
        rows.append(make_record(status))

random.shuffle(rows)

for i, row in enumerate(rows, 1):
    row["claim_id"] = i

columns = [
    "claim_id", "product_category", "product_age_months",
    "warranty_period_months", "receipt_available", "serial_number_valid",
    "damage_type", "repair_history", "purchase_price", "claim_amount",
    "days_since_purchase", "claim_status"
]

df = pd.DataFrame(rows)[columns]
df.to_csv("data/raw/claims_master.csv", index=False)

print("Master dataset created: data/raw/claims_master.csv")
print("Rows:", len(df))
print(df["claim_status"].value_counts())
