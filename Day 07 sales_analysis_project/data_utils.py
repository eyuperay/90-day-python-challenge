import csv
from typing import List, Dict, Tuple


def load_data(file_path: str) -> List[Dict]:
    """Loads CSV file and returns list of records."""
    data = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

        return data

    except FileNotFoundError:
        print("Error: File not found.")
        return []


def clean_data(data: List[Dict]) -> Tuple[List[Dict], List[str]]:
    """
    Cleans dataset:
    - Removes invalid prices (<= 0 or non-numeric)
    - Logs errors
    - Formats customer names
    """

    cleaned = []
    errors = []

    for row in data:
        try:
            price = float(row["Price"])

            # ❌ invalid price check
            if price <= 0:
                errors.append(f"Invalid price removed: {row}")
                continue

            row["Price"] = price
            row["Customer"] = row["Customer"].title()

            cleaned.append(row)

        except Exception:
            errors.append(f"Corrupted row: {row}")

    return cleaned, errors


def total_sales(data: List[Dict]) -> float:
    """Returns total sales amount."""
    return sum(item["Price"] for item in data)


def best_category(data: List[Dict]) -> str:
    """Returns category with highest total sales."""
    category_totals = {}

    for item in data:
        category = item["Category"]
        category_totals[category] = category_totals.get(category, 0) + item["Price"]

    if not category_totals:
        return "No Data"

    return max(category_totals, key=category_totals.get)


def premium_sales(data: List[Dict]) -> List[Dict]:
    """Returns sales above average price."""
    if not data:
        return []

    avg = total_sales(data) / len(data)

    return [item for item in data if item["Price"] > avg]