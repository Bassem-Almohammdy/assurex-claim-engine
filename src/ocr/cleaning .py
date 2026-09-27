import re
from datetime import datetime


def clean_text(value):
    if value is None:
        return ""

    value = str(value).replace("\n", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_serial(value):
    value = clean_text(value).upper()
    return re.sub(r"[^A-Z0-9\-]", "", value)


def normalize_model(value):
    value = clean_text(value).upper()
    return re.sub(r"[^A-Z0-9\-]", "", value)


def normalize_money(value):
    if value is None:
        return None

    value = str(value).replace(",", "")
    value = re.sub(r"[^\d.]", "", value)

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def normalize_date(value):
    if not value:
        return None

    value = clean_text(value)

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d.%m.%Y",
    ]

    for fmt in formats:
        try:
            date = datetime.strptime(value, fmt)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return value


def normalize_duration(value):
    if not value:
        return None

    value = clean_text(value).lower()

    match = re.search(
        r"(\d+)\s*(month|months|year|years|شهر|أشهر|سنة|سنوات)",
        value
    )

    if not match:
        return value

    number = int(match.group(1))
    unit = match.group(2)

    if unit in ("year", "years", "سنة", "سنوات"):
        number *= 12

    return f"{number} months"
