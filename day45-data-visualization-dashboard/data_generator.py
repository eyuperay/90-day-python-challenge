"""
Data Generator for Sales Dashboard
Creates synthetic sales data for visualization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sales_data(days: int = 365, products: list = None) -> pd.DataFrame:
    """
    Generate synthetic sales data for dashboard visualization
    
    Args:
        days: Number of days to generate data for
        products: List of product names
    
    Returns:
        DataFrame with sales data
    """
    if products is None:
        products = [
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
        ]
    
    regions = ["North", "South", "East", "West", "Central"]
    categories = ["Electronics", "Accessories", "Gaming", "Audio", "Computers"]
    
    data = []
    start_date = datetime.now() - timedelta(days=days)
    
    for i in range(days * 20):  # 20 transactions per day on average
        current_date = start_date + timedelta(days=random.randint(0, days-1))
        
        product = random.choice(products)
        category = random.choice(categories)
        region = random.choice(regions)
        
        # Base price varies by product
        base_price = {
            "Laptop Pro": 1200,
            "Smartphone X": 800,
            "Tablet Air": 500,
            "Smart Watch": 300,
            "Wireless Earbuds": 150,
            "Gaming Console": 450,
            "Monitor Ultra": 350,
            "Keyboard Mech": 120,
            "Mouse Pro": 80,
            "External SSD": 200
        }.get(product, 500)
        
        # Add some variation to price
        price = base_price * random.uniform(0.8, 1.2)
        
        # Quantity sold (1-5 units)
        quantity = random.randint(1, 5)
        
        # Total amount
        total = price * quantity
        
        # Add some seasonality
        if current_date.month in [11, 12]:
            total *= random.uniform(1.1, 1.3)  # Holiday season boost
        
        data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "product": product,
            "category": category,
            "region": region,
            "price": round(price, 2),
            "quantity": quantity,
            "total": round(total, 2)
        })
    
    df = pd.DataFrame(data)
    return df


def generate_customer_data(n_customers: int = 500) -> pd.DataFrame:
    """
    Generate synthetic customer data
    
    Args:
        n_customers: Number of customers to generate
    
    Returns:
        DataFrame with customer data
    """
    cities = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", 
              "Konya", "Adana", "Gaziantep", "Mersin", "Kayseri"]
    
    customers = []
    for i in range(n_customers):
        age = random.randint(18, 70)
        customers.append({
            "customer_id": f"CUST{str(i+1).zfill(5)}",
            "age": age,
            "city": random.choice(cities),
            "total_spent": round(random.uniform(100, 10000), 2),
            "purchase_count": random.randint(1, 100),
            "last_purchase": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "segment": random.choices(["Premium", "Standard", "Basic"], weights=[20, 50, 30])[0]
        })
    
    return pd.DataFrame(customers)
