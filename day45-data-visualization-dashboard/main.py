#!/usr/bin/env python3
"""
Day 45 - Data Visualization Dashboard
Creates comprehensive sales dashboard with static and interactive charts
"""

import os
import pandas as pd
from data_generator import generate_sales_data, generate_customer_data
from dashboard import SalesDashboard


def main():
    print("=" * 60)
    print("DAY 45 - DATA VISUALIZATION DASHBOARD")
    print("=" * 60 + "\n")
    
    # Generate data
    print("Generating sales data...")
    sales_df = generate_sales_data(days=180, products=[
        "Laptop Pro",
        "Smartphone X",
        "Tablet Air",
        "Smart Watch",
        "Wireless Earbuds",
        "Gaming Console",
        "Monitor Ultra",
        "Keyboard Mech",
        "Mouse Pro",
        "External SSD"
    ])
    
    print(f"Sales data generated: {len(sales_df)} records")
    
    print("\nGenerating customer data...")
    customer_df = generate_customer_data(n_customers=300)
    print(f"Customer data generated: {len(customer_df)} records")
    
    # Save raw data
    os.makedirs("data", exist_ok=True)
    sales_df.to_csv("data/sales_data.csv", index=False)
    customer_df.to_csv("data/customer_data.csv", index=False)
    print("\n✓ Raw data saved to 'data/' folder\n")
    
    # Create dashboard
    dashboard = SalesDashboard(sales_df, customer_df)
    dashboard.run_all()


if __name__ == "__main__":
    main()
