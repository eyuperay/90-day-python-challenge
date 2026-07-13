"""
Helper functions for data cleaning and formatting
"""

import re


def clean_price(price_text: str) -> float:
    """
    Extracts numeric value from price strings like "1.250.000 TL"
    """
    if not price_text:
        return 0.0

    # Remove currency symbols and codes
    for currency in ["TL", "USD", "EUR", "$", "€", "₺", "TRY"]:
        price_text = price_text.replace(currency, "")

    # Clean up dots and commas
    price_text = price_text.replace(".", "").replace(",", ".").strip()

    # Extract only numbers
    number = re.search(r"[\d.]+", price_text)
    if number:
        return float(number.group())
    return 0.0


def clean_square_meters(text: str) -> float:
    """
    Extracts square meter value from strings like "120 m²"
    """
    if not text:
        return 0.0

    text = text.replace("m²", "").replace("m2", "").replace("sqm", "").strip()
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return 0.0


def clean_room_count(text: str) -> str:
    """
    Returns room count as-is from strings like "3+1"
    """
    if not text:
        return "Unknown"
    return text.strip()


def clean_text(text: str) -> str:
    """
    Removes extra spaces and converts to title case
    """
    if not text:
        return ""
    return " ".join(text.split()).title()