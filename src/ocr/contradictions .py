from .cleaning import normalize_model, normalize_serial
from datetime import datetime


def parse_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(
            str(value),
            "%Y-%m-%d"
        )
    except ValueError:
        return None


def detect_date_contradictions(claim_data):
    contradictions = []

    purchase_date = parse_date(
        claim_data.get("purchase_date")
    )

    fault_date = parse_date(
        claim_data.get("fault_date")
    )

    repair_date = parse_date(
        claim_data.get("repair_date")
    )

    submission_date = parse_date(
        claim_data.get("claim_submission_date")
    )

    if purchase_date and fault_date and fault_date < purchase_date:
        contradictions.append({
            "type": "FAULT_BEFORE_PURCHASE",
            "message": "Fault date is before purchase date."
        })

    if purchase_date and repair_date and repair_date < purchase_date:
        contradictions.append({
            "type": "REPAIR_BEFORE_PURCHASE",
            "message": "Repair date is before purchase date."
        })

    if fault_date and submission_date and fault_date > submission_date:
        contradictions.append({
            "type": "FAULT_AFTER_SUBMISSION",
            "message": "Fault date is after claim submission date."
        })

    if repair_date and submission_date and repair_date > submission_date:
        contradictions.append({
            "type": "REPAIR_AFTER_SUBMISSION",
            "message": "Repair date is after claim submission date."
        })

    return contradictions


def detect_serial_contradictions(
    extracted_serials,
    user_serial=None
):
    contradictions = []

    serials = [
        normalize_serial(s)
        for s in extracted_serials
        if s
    ]

    serials = [
        s for s in serials
        if s
    ]

    unique_serials = set(serials)

    normalized_user = (
        normalize_serial(user_serial)
        if user_serial
        else None
    )

    if len(unique_serials) > 1:
        contradictions.append({
            "type": "CONFLICTING_SERIALS",
            "message": "Different serial numbers were found."
        })

    if (
        normalized_user
        and serials
        and normalized_user not in unique_serials
    ):
        contradictions.append({
            "type": "SERIAL_MISMATCH",
            "message": (
                "User serial number does not match "
                "extracted serial numbers."
            )
        })

    return contradictions


def detect_model_contradictions(
    extracted_models,
    user_model=None
):
    contradictions = []

    models = [
        normalize_model(m)
        for m in extracted_models
        if m
    ]

    models = [
        m for m in models
        if m
    ]

    unique_models = set(models)

    normalized_user = (
        normalize_model(user_model)
        if user_model
        else None
    )

    if len(unique_models) > 1:
        contradictions.append({
            "type": "CONFLICTING_MODELS",
            "message": "Different model numbers were found."
        })

    if (
        normalized_user
        and models
        and normalized_user not in unique_models
    ):
        contradictions.append({
            "type": "MODEL_MISMATCH",
            "message": (
                "User model number does not match "
                "extracted model numbers."
            )
        })

    return contradictions


def detect_all_contradictions(
    claim_data,
    extracted_serials=None,
    extracted_models=None
):
    contradictions = []

    contradictions.extend(
        detect_date_contradictions(claim_data)
    )

    contradictions.extend(
        detect_serial_contradictions(
            extracted_serials or [],
            claim_data.get("serial_number")
        )
    )

    contradictions.extend(
        detect_model_contradictions(
            extracted_models or [],
            claim_data.get("model_number")
        )
    )

    return contradictions
