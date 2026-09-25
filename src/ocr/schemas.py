from typing import Any, Dict, List

SCHEMA_VERSION = "1.0"


def create_document_result(
    extracted_data: Dict[str, Any] | None = None,
    missing_documents: List[str] | None = None,
    contradictions: List[Dict[str, Any]] | None = None,
    duplicate_indicators: List[Dict[str, Any]] | None = None,
    validation_status: str = "VALID",
    claim_document_comparisons: List[Dict[str, Any]] | None = None,
    validation_errors: List[str] | None = None,
    validation_warnings: List[str] | None = None,
    documents: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "extracted_data": extracted_data or {},
        "missing_documents": missing_documents or [],
        "contradictions": contradictions or [],
        "duplicate_indicators": duplicate_indicators or [],
        "claim_document_comparisons": claim_document_comparisons or [],
        "validation_status": validation_status,
        "validation_errors": validation_errors or [],
        "validation_warnings": validation_warnings or [],
        "documents": documents or [],
    }
