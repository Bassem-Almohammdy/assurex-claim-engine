from src.ocr.comparison import compare_extracted_with_claim
from src.ocr.missing_documents import detect_missing_documents
from src.ocr.duplicates import (
    detect_document_duplicate,
    detect_claim_duplicate,
)


def test_claim_document_mismatch():
    extracted_data = {
        "serial_number": "SN12345",
        "model_number": "MD100",
        "invoice_number": "INV001",
        "purchase_date": "2026-01-10",
    }

    claim_data = {
        "serial_number": "SN99999",
        "model_number": "MD100",
        "invoice_number": "INV001",
        "purchase_date": "2026-01-10",
    }

    result = compare_extracted_with_claim(
        extracted_data,
        claim_data
    )

    assert len(result["mismatches"]) > 0

    assert any(
        item["type"] == "CLAIM_DOCUMENT_MISMATCH"
        for item in result["mismatches"]
    )


def test_missing_document_detection():
    uploaded_documents = [
        {
            "document_type": "warranty_card"
        }
    ]

    missing = detect_missing_documents(
        uploaded_documents,
        required_documents=["receipt", "warranty_card"]
    )

    assert "receipt" in missing
    assert "warranty_card" not in missing


def test_duplicate_detection():
    claim_data = {
        "claim_id": "CLM001",
        "invoice_number": "INV001",
        "serial_number": "SN12345",
        "fault_description": "Screen not working",
        "claimant_name": "Test User",
        "claimant_email": "test@example.com",
    }

    previous_claims = [
        {
            "claim_id": "CLM001",
            "invoice_number": "INV001",
            "serial_number": "SN12345",
            "fault_description": "Screen not working",
            "claimant_name": "Test User",
            "claimant_email": "test@example.com",
        }
    ]

    indicators = detect_claim_duplicate(
        claim_data,
        previous_claims
    )

    types = {
        item["type"]
        for item in indicators
    }

    assert "DUPLICATE_CLAIM_ID" in types
    assert "DUPLICATE_INVOICE" in types
    assert "DUPLICATE_SERIAL" in types
