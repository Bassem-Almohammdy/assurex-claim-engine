from .cleaning import (
    clean_text,
    normalize_date,
    normalize_model,
    normalize_money,
    normalize_serial,
    normalize_duration,
)


FIELD_NORMALIZERS = {
    "purchase_date": normalize_date,
    "serial_number": normalize_serial,
    "model_number": normalize_model,
    "purchase_amount": normalize_money,
    "warranty_duration": normalize_duration,
}


def normalize_for_compare(field, value):
    if value is None or value == "":
        return None

    normalizer = FIELD_NORMALIZERS.get(field, clean_text)
    result = normalizer(value)

    if isinstance(result, str):
        return result.upper()

    return result


def compare_extracted_with_claim(extracted_data, claim_data):
    """Compare fields extracted from documents with user-entered claim data."""

    comparisons = []
    mismatches = []

    fields = [
        "purchase_date",
        "invoice_number",
        "product_name",
        "model_number",
        "serial_number",
        "retailer",
        "purchase_amount",
        "warranty_duration",
    ]

    for field in fields:
        extracted = normalize_for_compare(
            field,
            extracted_data.get(field)
        )

        claim = normalize_for_compare(
            field,
            claim_data.get(field)
        )

        if extracted is None or claim is None:
            continue

        match = extracted == claim

        item = {
            "field": field,
            "extracted_value": extracted,
            "claim_value": claim,
            "match": match,
        }

        comparisons.append(item)

        if not match:
            mismatches.append({
                "type": "CLAIM_DOCUMENT_MISMATCH",
                "field": field,
                "extracted_value": extracted,
                "claim_value": claim,
                "message": (
                    f"Claim value does not match "
                    f"document value for {field}."
                ),
            })

    return {
        "comparisons": comparisons,
        "mismatches": mismatches,
    }
