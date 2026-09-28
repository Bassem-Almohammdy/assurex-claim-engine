from flask import Blueprint, request, jsonify
import os
import tempfile

from src.ocr.processor import DocumentProcessor


documents_api = Blueprint(
    "documents_api",
    __name__,
    url_prefix="/api/documents"
)

processor = DocumentProcessor(
    ocr_language="ara+eng"
)


@documents_api.route("/process", methods=["POST"])
def process_document():
    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded."
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "error": "No filename provided."
        }), 400

    document_type = request.form.get(
        "document_type",
        "unknown"
    )

    temp_path = None

    try:
        suffix = os.path.splitext(
            file.filename
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            file.save(temp_file.name)
            temp_path = temp_file.name

        result = processor.process_document(
            temp_path,
            document_type
        )

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
