DEFAULT_REQUIRED_DOCUMENTS = ["receipt"]


def detect_missing_documents(
    uploaded_documents,
    required_documents=None
):
    """Return required document types that were not uploaded.

    Passing [] explicitly means that no document types are required.
    """

    if required_documents is None:
        required_documents = DEFAULT_REQUIRED_DOCUMENTS

    uploaded_types = {
        doc.get("document_type")
        for doc in uploaded_documents
        if doc.get("document_type")
    }

    return [
        doc_type
        for doc_type in required_documents
        if doc_type not in uploaded_types
    ]
