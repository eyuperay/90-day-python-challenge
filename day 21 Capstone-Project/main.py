import pandas as pd
import os
from datetime import datetime

from cleaner_utils import (
    clean_transactions,
    merge_with_departments,
    add_budget_status,
    add_rolling_average
)

# -----------------------------
# BASE DIRECTORY (CRITICAL FIX)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

TRANSACTIONS_PATH = os.path.join(DATA_DIR, "transactions.csv")
DEPARTMENTS_PATH = os.path.join(DATA_DIR, "department_meta.json")

REPORT_PATH = os.path.join(OUTPUT_DIR, "final_health_report.csv")
LOG_PATH = os.path.join(OUTPUT_DIR, "process.log")


# -----------------------------
# DECORATOR
# -----------------------------
def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print("Processing started...")

        result = func(*args, **kwargs)

        end = datetime.now()
        duration = (end - start).total_seconds()

        print(f"Processing finished in {duration:.4f} seconds")

        # LOGGING
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"Started: {start} | Duration: {duration}\n")

        return result

    return wrapper


# -----------------------------
# MAIN PIPELINE
# -----------------------------
@timer
def run_pipeline():

    print("Loading data...")

    # FIX: absolute safe paths
    transactions = pd.read_csv(TRANSACTIONS_PATH)
    departments = pd.read_json(DEPARTMENTS_PATH)

    print("Cleaning data...")
    transactions = clean_transactions(transactions)

    print("Merging data...")
    df = merge_with_departments(transactions, departments)

    print("Adding budget status...")
    df = add_budget_status(df)

    print("Adding rolling average...")
    df = add_rolling_average(df)

    print("Generating report...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(REPORT_PATH, index=False)

    print("Report generated successfully.")

    return df


if __name__ == "__main__":
    run_pipeline()