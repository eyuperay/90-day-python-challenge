"""
Pandas GroupBy & Aggregation - Sales Performance Analysis
"""

import pandas as pd


def main() -> None:
    # Create dataset
    data = {
        "Sales_Rep": ["John", "Michael", "John", "Emily", "Michael", "Emily", "John"],
        "Region": ["North", "West", "North", "Central", "West", "Central", "North"],
        "Sales_Amount": [5000, 3000, 4500, 7000, 3200, 6500, 5200],
        "Units_Sold": [10, 5, 8, 15, 6, 12, 11]
    }

    df = pd.DataFrame(data)

    print("Original DataFrame:")
    print(df)

    # Question 1: Total sales by region
    total_sales_by_region = df.groupby("Region")["Sales_Amount"].sum()

    print("\nTotal Sales by Region:")
    print(total_sales_by_region)

    # Question 2: Average units sold by sales rep (sorted descending)
    avg_units_by_rep = df.groupby("Sales_Rep")["Units_Sold"].mean().sort_values(ascending=False)

    print("\nAverage Units Sold by Sales Rep (Descending):")
    print(avg_units_by_rep)

    # Question 3: Multiple aggregations using .agg()
    region_summary = df.groupby("Region").agg({
        "Sales_Amount": "sum",
        "Units_Sold": "max"
    })

    print("\nRegion Summary (Total Sales & Max Units Sold):")
    print(region_summary)

    # Question 4: Count records where Sales_Amount > 5000 grouped by region
    high_sales = df[df["Sales_Amount"] > 5000]
    high_sales_count = high_sales.groupby("Region").size()

    print("\nCount of High Sales (>5000) by Region:")
    print(high_sales_count)


if __name__ == "__main__":
    main()