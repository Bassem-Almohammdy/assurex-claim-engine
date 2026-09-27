import re

from .cleaning import (
    clean_text,
    normalize_serial,
    normalize_model,
    normalize_money,
    normalize_date,
    normalize_duration,
)

LABELS = {
    "invoice": r"(?:invoice|inv|فاتورة|رقم\s*الفاتورة)",
    "purchase_date": r"(?:purchase\s*date|date\s*of\s*purchase|تاريخ\s*الشراء|تاريخ\s*شراء)",
    "serial": r"(?:serial\s*(?:number|no|#)?|s\s*/\s*n|الرقم\s*التسلسلي|رقم\s*التسلسل|السيريال)",
    "model": r"(?:model\s*(?:number|no|#)?|موديل|رقم\s*الموديل)",
    "retailer": r"(?:retailer|store|seller|المتجر|البائع|المورد)",
    "product": r"(?:product\s*(?:name)?|item|المنتج|اسم\s*المنتج|الصنف)",
    "total": r"(?:total|amount|price|المبلغ|الإجمالي|السعر|قيمة\s*الشراء)",
    "warranty": r"(?:warranty|الضمان|مدة\s*الضمان|فترة\s*الضمان)",
    "fault_date": r"(?:fault\s*date|failure\s*date|incident\s*date|تاريخ\s*العطل|تاريخ\s*الخلل|تاريخ\s*العطل\s*والخلل)",
    "repair_date": r"(?:repair\s*date|service\s*date|تاريخ\s*الإصلاح|تاريخ\s*الصيانة)",
    "fault_description": r"(?:fault\s*(?:description|details)?|failure\s*(?:description|details)?|وصف\s*العطل|تفاصيل\s*العطل|وصف\s*الخلل)",
    "repair_center": r"(?:repair\s*center|service\s*center|repair\s*shop|مركز\s*الصيانة|مركز\s*الإصلاح)",
    "repair_cost": r"(?:repair\s*cost|service\s*cost|تكلفة\s*الإصلاح|تكلفة\s*الصيانة)",
}


def find_value(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            value = clean_text(match.group(1))
            if value:
                return value
    return None


def _label_value(label_pattern, text, value_pattern=r"([^\r\n]+)"):
    return find_value(
        text,
        [rf"{label_pattern}\s*[:#\-]?\s*{value_pattern}"]
    )


def extract_invoice_number(text):
    return find_value(text, [
        r"(?:invoice\s*(?:number|no|#)|رقم\s*الفاتورة)\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        r"(?:inv\s*(?:no|#))\s*[:\-]?\s*([A-Z0-9\-\/]+)"
    ])


def extract_purchase_date(text):
    value = _label_value(
        LABELS["purchase_date"],
        text,
        r"([0-9]{1,4}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{1,4})"
    )

    if value is None:
        value = find_value(
            text,
            [
                r"date\s*[:\-]?\s*([0-9]{1,4}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{1,4})"
            ]
        )

    return normalize_date(value)


def extract_serial_number(text):
    value = _label_value(
        LABELS["serial"],
        text,
        r"([A-Z0-9\-\/]+)"
    )
    return normalize_serial(value)


def extract_model_number(text):
    value = _label_value(
        LABELS["model"],
        text,
        r"([A-Z0-9\-\/]+)"
    )
    return normalize_model(value)


def extract_purchase_amount(text):
    value = _label_value(
        LABELS["total"],
        text,
        r"(?:[$€£]|ريال|ر\.ي)?\s*([0-9,]+(?:\.[0-9]{1,2})?)"
    )

    if value is None:
        value = find_value(
            text,
            [
                r"[$€£]\s*([0-9,]+(?:\.[0-9]{1,2})?)"
            ]
        )

    return normalize_money(value)


def extract_warranty_duration(text):
    value = _label_value(
        LABELS["warranty"],
        text,
        r"(\d+\s*(?:months?|years?|شهر|أشهر|سنة|سنوات))"
    )

    if value is None:
        value = find_value(
            text,
            [
                r"(\d+\s*(?:months?|years?|شهر|أشهر|سنة|سنوات))\s*(?:warranty|الضمان)"
            ]
        )

    return normalize_duration(value)


def extract_retailer(text):
    return _label_value(LABELS["retailer"], text)


def extract_product_name(text):
    return _label_value(LABELS["product"], text)


def extract_date_field(text, label_key):
    value = _label_value(
        LABELS[label_key],
        text,
        r"([0-9]{1,4}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{1,4})"
    )
    return normalize_date(value)


def extract_fault_description(text):
    return find_value(
        text,
        [
            r"(?:fault\s*(?:description|details)|failure\s*(?:description|details)|وصف\s*العطل|تفاصيل\s*العطل|وصف\s*الخلل)\s*[:\-]?\s*([^\r\n]+)"
        ]
    )


def extract_repair_center(text):
    return _label_value(LABELS["repair_center"], text)


def extract_repair_cost(text):
    value = _label_value(
        LABELS["repair_cost"],
        text,
        r"(?:[$€£]|ريال|ر\.ي)?\s*([0-9,]+(?:\.[0-9]{1,2})?)"
    )
    return normalize_money(value)


def extract_data(text):
    """Return canonical extracted fields; optional fault/repair fields are included when present."""
    data = {
        "purchase_date": extract_purchase_date(text),
        "invoice_number": extract_invoice_number(text),
        "product_name": extract_product_name(text),
        "model_number": extract_model_number(text),
        "serial_number": extract_serial_number(text),
        "retailer": extract_retailer(text),
        "purchase_amount": extract_purchase_amount(text),
        "warranty_duration": extract_warranty_duration(text),
        "fault_date": extract_date_field(text, "fault_date"),
        "repair_date": extract_date_field(text, "repair_date"),
        "fault_description": extract_fault_description(text),
        "repair_center": extract_repair_center(text),
        "repair_cost": extract_repair_cost(text),
    }

    return {
        key: value
        for key, value in data.items()
        if value not in (None, "")
    }
