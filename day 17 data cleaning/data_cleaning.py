"""
Data Cleaning - E-commerce Sales Dataset
"""

import pandas as pd


def main() -> None:
    # Raw (dirty) data
    raw_data = {
        "Order_ID": [101, 102, 102, 104, 105, 106],
        "Customer": ["John", "Michael", "Michael", "Sarah", None, "David"],
        "Amount": [250, 450, 450, None, 300, -100],
        "City": ["NY", "LA", "LA", "Chicago", "NY", "Houston"]
    }

    df = pd.DataFrame(raw_data)

    print("Original DataFrame:")
    print(df)

    # Detect duplicate rows
    print("\nDuplicate rows:")
    print(df[df.duplicated()])

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing Customer values
    df["Customer"] = df["Customer"].fillna("Unknown Customer")

    # Fix negative values in Amount
    df["Amount"] = df["Amount"].apply(lambda x: abs(x) if pd.notnull(x) else x)

    # Fill missing Amount with mean
    mean_amount = df["Amount"].mean()
    df["Amount"] = df["Amount"].fillna(mean_amount)

    # Standardize City names
    city_mapping = {
        "NY": "New York",
        "LA": "Los Angeles",
        "Chicago": "Chicago",
        "Houston": "Houston"
    }

    df["City"] = df["City"].replace(city_mapping)

    print("\nCleaned DataFrame:")
    print(df)


if __name__ == "__main__":
    main()