import hashlib
import json
import re


def sha256_file(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(
            lambda: file.read(8192),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def detect_document_duplicate(
    file_path,
    previous_hashes
):
    current_hash = sha256_file(file_path)

    return {
        "is_duplicate": current_hash in (previous_hashes or []),
        "hash": current_hash,
    }


def _norm(value):
    if value is None:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value).strip().upper()
    )


def _claimant_fingerprint(claim):
    # Supports either a structured claimant_details object
    # or the canonical claimant_* fields if the Backend provides them.

    details = claim.get("claimant_details")

    if isinstance(details, dict):
        parts = [
            details.get(k)
            for k in (
                "claimant_id",
                "name",
                "email",
                "phone"
            )
        ]
    else:
        parts = [
            claim.get(k)
            for k in (
                "claimant_id",
                "claimant_name",
                "claimant_email",
                "claimant_phone"
            )
        ]

    normalized = [
        _norm(v)
        for v in parts
        if _norm(v)
    ]

    return (
        json.dumps(
            normalized,
            ensure_ascii=False
        )
        if normalized
        else ""
    )


def detect_claim_duplicate(
    claim_data,
    previous_claims
):
    indicators = []

    current_claimant = _claimant_fingerprint(
        claim_data
    )

    for previous in previous_claims or []:

        if (
            claim_data.get("claim_id")
            and claim_data.get("claim_id")
            == previous.get("claim_id")
        ):
            indicators.append({
                "type": "DUPLICATE_CLAIM_ID",
                "value": claim_data.get("claim_id"),
            })

        if (
            claim_data.get("invoice_number")
            and claim_data.get("invoice_number")
            == previous.get("invoice_number")
        ):
            indicators.append({
                "type": "DUPLICATE_INVOICE",
                "value": claim_data.get("invoice_number"),
            })

        if (
            claim_data.get("serial_number")
            and claim_data.get("serial_number")
            == previous.get("serial_number")
        ):
            indicators.append({
                "type": "DUPLICATE_SERIAL",
                "value": claim_data.get("serial_number"),
            })

        if (
            claim_data.get("fault_description")
            and _norm(
                claim_data.get("fault_description")
            )
            == _norm(
                previous.get("fault_description")
            )
        ):
            indicators.append({
                "type": "DUPLICATE_FAULT_DESCRIPTION",
                "value": claim_data.get(
                    "fault_description"
                ),
            })

        previous_claimant = _claimant_fingerprint(
            previous
        )

        if (
            current_claimant
            and previous_claimant
            and current_claimant == previous_claimant
        ):
            indicators.append({
                "type": "DUPLICATE_CLAIMANT_DETAILS",
                "value": current_claimant,
            })

    return indicators
