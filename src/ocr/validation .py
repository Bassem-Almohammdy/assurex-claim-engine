import os
from datetime import datetime


REQUIRED_FIELDS = [
    "purchase_date",
    "invoice_number",
    "product_name",
    "model_number",
    "serial_number",
    "retailer",
    "purchase_amount",
    "warranty_duration",
]

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
}

MAX_FILE_SIZE_MB = 10


def validate_extracted_data(data):
    errors = []
    warnings = []

    # Check required extracted fields
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            errors.append(
                f"Missing extracted field: {field}"
            )

    # Validate purchase amount
    amount = data.get("purchase_amount")

    if amount is not None:
        try:
            if float(amount) < 0:
                errors.append(
                    "Purchase amount cannot be negative."
                )
        except (ValueError, TypeError):
            errors.append(
                "Purchase amount must be numeric."
            )

    # Validate purchase date
    date_value = data.get("purchase_date")

    if date_value:
        try:
            datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )
        except ValueError:
            errors.append(
                "Invalid purchase date format."
            )

    if errors:
        status = "INVALID"
    elif warnings:
        status = "NEEDS_REVIEW"
    else:
        status = "VALID"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
    }


def validate_file(file_path):
    errors = []

    # Check whether file exists
    if not os.path.exists(file_path):
        return {
            "status": "INVALID",
            "errors": ["File does not exist."],
        }

    # Check file extension
    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        errors.append(
            f"Unsupported file type: {extension}"
        )

    # Check file size
    size_mb = os.path.getsize(
        file_path
    ) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        errors.append(
            f"File exceeds {MAX_FILE_SIZE_MB} MB."
        )

    return {
        "status": "INVALID" if errors else "VALID",
        "errors": errors,
    }
