"""
Data processors for CSV and JSON files.
Handles type normalization for CSV data.
"""

import csv
import json
import os
from typing import Iterator, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseProcessor:
    def __init__(self, file_name: str) -> None:
        self._file_path = os.path.join(BASE_DIR, file_name)
        self._processed_count = 0

    def __len__(self) -> int:
        return self._processed_count

    def __str__(self) -> str:
        return f"{self.__class__.__name__} -> {self._file_path}"


class CSVProcessor(BaseProcessor):
    def read_data(self) -> Iterator[Dict]:
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # 🔥 TYPE NORMALIZATION (IMPORTANT FIX)
                    if "price" in row:
                        try:
                            row["price"] = float(row["price"])
                        except ValueError:
                            row["price"] = 0.0

                    self._processed_count += 1
                    yield row

        except FileNotFoundError:
            print("CSV file not found!")
        except Exception as e:
            print(f"CSV error: {e}")


class JSONProcessor(BaseProcessor):
    def read_data(self) -> Iterator[Dict]:
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                for item in data:
                    self._processed_count += 1
                    yield item

        except FileNotFoundError:
            print("JSON file not found!")
        except json.JSONDecodeError:
            print("Invalid JSON format!")
        except Exception as e:
            print(f"JSON error: {e}")