#!/usr/bin/env python3
"""
Day 46 - SQLite Database
Product management system with SQLite database
"""

import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import Database
from models import Product, Customer, Order


def create_sample_data(db: Database):
    """Insert sample data into database"""
    print("\n" + "="*50)
    print("INSERTING SAMPLE DATA")
    print("="*50)

    product_model = Product(db)
    customer_model = Customer(db)
    order_model = Order(db)

    # Sample products
    products = [
        ("Laptop Pro", "Electronics", 1200.00, 50, "TechSupplier Inc"),
        ("Smartphone X", "Electronics", 800.00, 100, "MobileWorld Ltd"),
        ("Tablet Air", "Computers", 500.00, 75, "TechSupplier Inc"),
        ("Smart Watch", "Accessories", 300.00, 200, "WearableTech Co"),
        ("Wireless Earbuds", "Audio", 150.00, 300, "AudioPro LLC"),
        ("Gaming Console", "Gaming", 450.00, 40, "GameMaster Corp"),
        ("Monitor Ultra", "Computers", 350.00, 60, "DisplayTech Inc"),
        ("Keyboard Mech", "Accessories", 120.00, 150, "InputDevices Ltd"),
        ("Mouse Pro", "Accessories", 80.00, 200, "InputDevices Ltd"),
        ("External SSD", "Computers", 200.00, 90, "StoragePro Inc"),
    ]

    print("Adding products...")
    for product in products:
        product_model.create(*product)
    print(f"[OK] {len(products)} products added")

    # Sample customers
    customers = [
        ("Ahmet", "Yilmaz", "ahmet@email.com", "555-0101", "Istanbul"),
        ("Mehmet", "Demir", "mehmet@email.com", "555-0102", "Ankara"),
        ("Ayse", "Kaya", "ayse@email.com", "555-0103", "Izmir"),
        ("Fatma", "Celik", "fatma@email.com", "555-0104", "Bursa"),
        ("Ali", "Ozturk", "ali@email.com", "555-0105", "Antalya"),
        ("Zeynep", "Aydin", "zeynep@email.com", "555-0106", "Konya"),
        ("Emre", "Sahin", "emre@email.com", "555-0107", "Adana"),
        ("Elif", "Karaca", "elif@email.com", "555-0108", "Gaziantep"),
    ]

    print("Adding customers...")
    for customer in customers:
        customer_model.create(*customer)
    print(f"[OK] {len(customers)} customers added")

    # Sample orders
    print("Adding orders...")
    for customer_id in range(1, 5):
        # Create order
        total_amount = round(random.uniform(100, 1500), 2)
        order_id = order_model.create(customer_id, total_amount)

        # Add items to order
        for _ in range(random.randint(1, 4)):
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 3)
            unit_price = round(random.uniform(50, 800), 2)
            order_model.add_item(order_id, product_id, quantity, unit_price)

        # Update order status
        statuses = ['pending', 'processing', 'shipped', 'delivered']
        order_model.update_status(order_id, random.choice(statuses))

    print("[OK] Sample orders added")
    print("[OK] Sample data insertion complete!\n")


def generate_reports(db: Database):
    """Generate reports from database"""
    print("\n" + "="*50)
    print("GENERATING REPORTS")
    print("="*50)

    # Get data
    products = db.get_table_data('products')
    customers = db.get_table_data('customers')
    orders = db.get_table_data('orders')

    # Convert to DataFrames
    df_products = pd.DataFrame(products)
    df_customers = pd.DataFrame(customers)
    df_orders = pd.DataFrame(orders)

    # Save as CSV
    os.makedirs("output", exist_ok=True)
    df_products.to_csv("output/products_export.csv", index=False)
    df_customers.to_csv("output/customers_export.csv", index=False)
    df_orders.to_csv("output/orders_export.csv", index=False)
    print("[OK] Data exported to CSV files")

    # Generate visualizations
    print("\nGenerating visualizations...")

    # Set style
    sns.set_style("whitegrid")

    # 1. Products by category (Bar chart)
    plt.figure(figsize=(10, 6))
    category_counts = df_products['category'].value_counts()
    category_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Products by Category', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Number of Products', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/products_by_category.png', dpi=300)
    plt.close()
    print("[OK] Products by category chart saved")

    # 2. Price distribution (Histogram)
    plt.figure(figsize=(10, 6))
    df_products['price'].hist(bins=20, color='lightcoral', edgecolor='black')
    plt.title('Price Distribution of Products', fontsize=14)
    plt.xlabel('Price (TRY)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig('output/price_distribution.png', dpi=300)
    plt.close()
    print("[OK] Price distribution chart saved")

    # 3. Orders by status (Pie chart)
    if not df_orders.empty:
        plt.figure(figsize=(8, 6))
        status_counts = df_orders['status'].value_counts()
        status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Orders by Status', fontsize=14)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('output/orders_by_status.png', dpi=300)
        plt.close()
        print("[OK] Orders by status chart saved")

    # 4. Price by category (Box plot)
    plt.figure(figsize=(10, 6))
    df_products.boxplot(column='price', by='category')
    plt.title('Price Distribution by Category', fontsize=14)
    plt.suptitle('')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Price (TRY)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/price_by_category.png', dpi=300)
    plt.close()
    print("[OK] Price by category box plot saved")

    # Report summary
    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)
    print(f"Total Products: {len(df_products)}")
    print(f"Total Categories: {df_products['category'].nunique() if not df_products.empty else 0}")
    print(f"Total Customers: {len(df_customers)}")
    print(f"Total Orders: {len(df_orders)}")
    if not df_orders.empty:
        print(f"Total Revenue: {df_orders['total_amount'].sum():,.2f} TRY")
        print(f"Average Order Value: {df_orders['total_amount'].mean():,.2f} TRY")
    print("="*50)


def main():
    print("=" * 60)
    print("DAY 46 - SQLITE DATABASE")
    print("=" * 60 + "\n")

    # Initialize database
    db = Database("data/products.db")
    db.connect()

    # Create tables
    db.create_tables()

    # Check if data exists
    product_count = db.get_table_count('products')

    if product_count == 0:
        print("No data found. Creating sample data...")
        create_sample_data(db)
    else:
        print(f"Data already exists. {product_count} products found.")

    # Generate reports
    generate_reports(db)

    # Close connection
    db.close()

    print("\n" + "="*50)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for reports")
    print("[OK] Check 'data/products.db' for the database file")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()