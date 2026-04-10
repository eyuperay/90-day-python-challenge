import json
import os

from data_utils import (
    load_data,
    clean_data,
    total_sales,
    best_category,
    premium_sales
)


def main():

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "sales_data.csv")

    #  Load data
    data = load_data(file_path)

    if not data:
        print("No data found or file missing.")
        return

    # Clean data
    cleaned_data, errors = clean_data(data)

    if not cleaned_data:
        print("No valid data after cleaning.")
        return

    #  Analysis report
    report = {
        "total_sales": total_sales(cleaned_data),
        "best_category": best_category(cleaned_data),
        "premium_sales": premium_sales(cleaned_data)
    }

    # Save report.json
    with open(os.path.join(base_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # Save errors.log
    with open(os.path.join(base_dir, "errors.log"), "w", encoding="utf-8") as f:
        for error in errors:
            f.write(error + "\n")

    print("Project executed successfully!")


if __name__ == "__main__":
    main()