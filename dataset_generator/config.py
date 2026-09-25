DATASET_SIZE = 1500
TARGET_PER_CLASS = 500
RANDOM_SEED = 42

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

PRODUCT_CATEGORIES = [
    "Smartphone", "Laptop", "Tablet", "TV",
    "Refrigerator", "Washing Machine", "Camera", "Headphones"
]

DAMAGE_TYPES = [
    "Manufacturing Defect", "Screen Damage", "Battery Failure",
    "Water Damage", "Physical Damage", "Software Failure",
    "Electrical Failure", "Unknown"
]

WARRANTY_OPTIONS = [12, 24, 36]
CLASS_NAMES = ["Valid", "Invalid", "Manual Review"]
