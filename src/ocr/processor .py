from .ocr import OCRProcessor
from .extraction import extract_data
from .validation import validate_file, validate_extracted_data
from .missing_documents import detect_missing_documents
from .contradictions import detect_all_contradictions
from .duplicates import (
    detect_document_duplicate,
    detect_claim_duplicate,
)
from .comparison import compare_extracted_with_claim
from .schemas import create_document_result


class DocumentProcessor:

    def __init__(self, ocr_language="eng"):
        self.ocr = OCRProcessor(
            language=ocr_language
        )

    def process_document(
        self,
        file_path,
        document_type
    ):
        file_validation = validate_file(
            file_path
        )

        if file_validation["status"] == "INVALID":
            return {
                "document_type": document_type,
                "validation": file_validation,
                "extracted_data": {},
                "ocr_text": "",
            }

        ocr_result = self.ocr.process(
            file_path
        )

        extracted_data = extract_data(
            ocr_result["text"]
        )

        data_validation = validate_extracted_data(
            extracted_data
        )

        return {
            "document_type": document_type,
            "file_name": ocr_result["file_name"],
            "file_type": ocr_result["file_type"],
            "ocr_text": ocr_result["text"],
            "extracted_data": extracted_data,
            "validation": data_validation,
        }

    def process_claim(
        self,
        documents,
        claim_data,
        previous_document_hashes=None,
        previous_claims=None,
        required_documents=None,
    ):
        previous_document_hashes = (
            previous_document_hashes or []
        )

        previous_claims = (
            previous_claims or []
        )

        processed_documents = []
        all_extracted = {}

        serials = []
        models = []

        duplicate_indicators = []
        validation_errors = []
        validation_warnings = []
        comparisons = []

        for document in documents:

            result = self.process_document(
                document["file_path"],
                document["document_type"],
            )

            processed_documents.append(
                result
            )

            extracted = result.get(
                "extracted_data",
                {}
            )

            for key, value in extracted.items():
                if value is not None and value != "":
                    all_extracted[key] = value

            if extracted.get("serial_number"):
                serials.append(
                    extracted["serial_number"]
                )

            if extracted.get("model_number"):
                models.append(
                    extracted["model_number"]
                )

            validation = result.get(
                "validation",
                {}
            )

            validation_errors.extend(
                validation.get("errors", [])
            )

            validation_warnings.extend(
                validation.get("warnings", [])
            )

            comparison = (
                compare_extracted_with_claim(
                    extracted,
                    claim_data,
                )
            )

            comparisons.extend(
                comparison["comparisons"]
            )

            duplicate = (
                detect_document_duplicate(
                    document["file_path"],
                    previous_document_hashes,
                )
            )

            if duplicate["is_duplicate"]:
                duplicate_indicators.append({
                    "type": "DUPLICATE_DOCUMENT",
                    "file_name": document["file_path"],
                    "hash": duplicate["hash"],
                })

        missing_documents = (
            detect_missing_documents(
                documents,
                required_documents,
            )
        )

        contradictions = (
            detect_all_contradictions(
                claim_data,
                extracted_serials=serials,
                extracted_models=models,
            )
        )

        for item in comparisons:

            if not item["match"]:

                contradictions.append({
                    "type": "CLAIM_DOCUMENT_MISMATCH",
                    "field": item["field"],
                    "claim_value": item["claim_value"],
                    "extracted_value": item[
                        "extracted_value"
                    ],
                    "message": (
                        "Claim value does not match "
                        "document value for "
                        f"{item['field']}."
                    ),
                })

        duplicate_indicators.extend(
            detect_claim_duplicate(
                claim_data,
                previous_claims,
            )
        )

        if validation_errors:
            validation_status = "INVALID"

        elif (
            missing_documents
            or contradictions
            or duplicate_indicators
            or validation_warnings
        ):
            validation_status = "NEEDS_REVIEW"

        else:
            validation_status = "VALID"

        return create_document_result(
            extracted_data=all_extracted,
            missing_documents=missing_documents,
            contradictions=contradictions,
            duplicate_indicators=duplicate_indicators,
            claim_document_comparisons=comparisons,
            validation_status=validation_status,
            validation_errors=validation_errors,
            validation_warnings=validation_warnings,
            documents=processed_documents,
        )
