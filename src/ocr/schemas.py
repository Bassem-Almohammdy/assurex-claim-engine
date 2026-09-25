from typing import Any, Dict, List


def create_document_result(
    extracted_data: Dict[str, Any] | None = None,
    missing_documents: List[str] | None = None,
    contradictions: List[Dict[str, Any]] | None = None,
    duplicate_indicators: List[Dict[str, Any]] | None = None,
    validation_status: str = "VALID"
) -> Dict[str, Any]:
    return {
        "extracted_data": extracted_data or {},
        "missing_documents": missing_documents or [],
        "contradictions": contradictions or [],
        "duplicate_indicators": duplicate_indicators or [],
        "validation_status": validation_status
    }
