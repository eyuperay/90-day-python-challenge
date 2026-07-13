#!/usr/bin/env python3
"""
Day 59 - JSON Transformation
Demonstrates JSON operations: read, write, transform, validate
"""

import json
import os
from json_handler import JSONHandler


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def create_sample_data():
    """Create sample JSON data"""
    
    # Sample user data
    users = {
        "users": [
            {
                "id": 1,
                "name": "Ahmet Yilmaz",
                "email": "ahmet@email.com",
                "age": 30,
                "address": {
                    "city": "Istanbul",
                    "district": "Kadikoy",
                    "zip": "34700"
                },
                "orders": [
                    {"id": 101, "amount": 150.50, "date": "2026-01-15"},
                    {"id": 102, "amount": 75.00, "date": "2026-01-20"}
                ],
                "active": True
            },
            {
                "id": 2,
                "name": "Mehmet Demir",
                "email": "mehmet@email.com",
                "age": 25,
                "address": {
                    "city": "Ankara",
                    "district": "Cankaya",
                    "zip": "06500"
                },
                "orders": [
                    {"id": 103, "amount": 200.00, "date": "2026-01-18"}
                ],
                "active": True
            },
            {
                "id": 3,
                "name": "Ayse Kaya",
                "email": "ayse@email.com",
                "age": 28,
                "address": {
                    "city": "Izmir",
                    "district": "Bornova",
                    "zip": "35000"
                },
                "orders": [],
                "active": False
            }
        ]
    }
    
    # Sample product data
    products = {
        "products": [
            {"id": 1, "name": "Laptop", "price": 15000, "category": "Electronics"},
            {"id": 2, "name": "Mouse", "price": 200, "category": "Accessories"},
            {"id": 3, "name": "Keyboard", "price": 500, "category": "Accessories"},
            {"id": 4, "name": "Monitor", "price": 3500, "category": "Electronics"}
        ]
    }
    
    return users, products


def demo_basic_operations(handler: JSONHandler):
    """Demonstrate basic JSON operations"""
    print_section("1. BASIC JSON OPERATIONS")
    
    # Create sample data
    users, products = create_sample_data()
    
    # Write to file
    handler.write_json(users, "data/users.json")
    handler.write_json(products, "data/products.json")
    
    # Read from file
    read_users = handler.read_json("data/users.json")
    
    print(f"\n  Read {len(read_users.get('users', []))} users")
    for user in read_users.get('users', []):
        print(f"    - {user['name']} ({user['email']})")
    
    # Convert to JSON string
    json_string = handler.to_json_string(read_users)
    print(f"\n  JSON string length: {len(json_string)} characters")
    
    # Read from string
    parsed = handler.read_json_string(json_string)
    print(f"  Parsed from string: {len(parsed.get('users', []))} users")


def demo_flatten_json(handler: JSONHandler):
    """Demonstrate flattening JSON"""
    print_section("2. FLATTEN JSON")
    
    # Load data
    data = handler.read_json("data/users.json")
    
    if data:
        user = data['users'][0]
        print(f"\n  Original user data:")
        print(f"    {json.dumps(user, indent=2)[:200]}...")
        
        # Flatten
        flattened = handler.flatten_json(user)
        print(f"\n  Flattened data:")
        for key, value in flattened.items():
            print(f"    {key}: {value}")


def demo_extract_fields(handler: JSONHandler):
    """Demonstrate extracting fields"""
    print_section("3. EXTRACT FIELDS")
    
    data = handler.read_json("data/users.json")
    
    if data:
        users = data.get('users', [])
        
        # Extract only name and email
        extracted = handler.extract_fields(users, ['name', 'email'])
        
        print(f"\n  Extracted fields (name, email):")
        for item in extracted:
            print(f"    {item['name']} - {item['email']}")


def demo_filter_data(handler: JSONHandler):
    """Demonstrate filtering data"""
    print_section("4. FILTER DATA")
    
    data = handler.read_json("data/users.json")
    
    if data:
        users = data.get('users', [])
        
        # Filter active users
        active_users = handler.filter_data(users, 'active', True)
        
        print(f"\n  Active users:")
        for user in active_users:
            print(f"    - {user['name']} (Active: {user['active']})")
        
        # Filter by city
        istanbul_users = [user for user in users if user.get('address', {}).get('city') == 'Istanbul']
        print(f"\n  Users in Istanbul:")
        for user in istanbul_users:
            print(f"    - {user['name']} - {user['address']['city']}")


def demo_transform_keys(handler: JSONHandler):
    """Demonstrate transforming keys"""
    print_section("5. TRANSFORM KEYS")
    
    data = handler.read_json("data/users.json")
    
    if data:
        user = data['users'][0]
        
        key_map = {
            'name': 'full_name',
            'email': 'email_address',
            'active': 'is_active',
            'address': 'location'
        }
        
        transformed = handler.transform_keys(user, key_map)
        
        print(f"\n  Original keys: {list(user.keys())}")
        print(f"  Transformed keys: {list(transformed.keys())}")
        print(f"\n  Transformed data:")
        for key, value in transformed.items():
            if not isinstance(value, (dict, list)):
                print(f"    {key}: {value}")


def demo_add_timestamp(handler: JSONHandler):
    """Demonstrate adding timestamp"""
    print_section("6. ADD TIMESTAMP")
    
    data = handler.read_json("data/users.json")
    
    if data:
        data_with_time = handler.add_timestamp(data)
        
        print(f"\n  Timestamp added: {data_with_time.get('timestamp')}")
        print(f"  Processed at: {data_with_time.get('processed_at')}")
        
        # Save with timestamp
        handler.write_json(data_with_time, "output/users_with_timestamp.json")


def demo_merge_json(handler: JSONHandler):
    """Demonstrate merging JSON"""
    print_section("7. MERGE JSON")
    
    data1 = {"user": {"name": "Ali", "age": 30}}
    data2 = {"user": {"city": "Istanbul", "active": True}}
    
    merged = handler.merge_json(data1, data2)
    
    print(f"\n  Data1: {data1}")
    print(f"  Data2: {data2}")
    print(f"  Merged: {merged}")


def demo_validation(handler: JSONHandler):
    """Demonstrate validation"""
    print_section("8. VALIDATION")
    
    data = handler.read_json("data/users.json")
    
    if data:
        user = data['users'][0]
        
        # Schema validation
        schema = {
            'id': int,
            'name': str,
            'email': str,
            'age': int
        }
        
        errors = handler.validate_schema(user, schema)
        
        print(f"\n  Schema validation errors: {len(errors)}")
        for error in errors:
            print(f"    - {error}")
        
        # Required fields validation
        required = ['id', 'name', 'email', 'age', 'orders']
        missing = handler.validate_required_fields(user, required)
        
        print(f"\n  Required fields missing: {missing if missing else 'None'}")


def demo_nested_operations(handler: JSONHandler):
    """Demonstrate nested operations"""
    print_section("9. NESTED OPERATIONS")
    
    data = handler.read_json("data/users.json")
    
    if data:
        user = data['users'][0]
        
        # Get nested value
        city = handler.get_nested_value(user, 'address.city')
        print(f"\n  City (nested): {city}")
        
        # Set nested value
        updated = handler.set_nested_value(user, 'address.country', 'Turkey')
        print(f"  Updated with country: {updated['address']['country']}")
        
        # Remove empty values
        user_with_empty = {
            'name': 'Test',
            'email': '',
            'age': None,
            'orders': [],
            'address': {'city': 'Istanbul'}
        }
        
        cleaned = handler.remove_empty_values(user_with_empty)
        print(f"\n  Before cleaning: {user_with_empty}")
        print(f"  After cleaning: {cleaned}")


def demo_transform_products(handler: JSONHandler):
    """Demonstrate product transformation"""
    print_section("10. PRODUCT DATA TRANSFORMATION")
    
    data = handler.read_json("data/products.json")
    
    if data:
        products = data.get('products', [])
        
        # Transform products
        transformed_products = []
        for product in products:
            # Add tax
            price_with_tax = product['price'] * 1.18
            
            transformed = {
                'product_id': product['id'],
                'name': product['name'].upper(),
                'price': product['price'],
                'price_with_tax': round(price_with_tax, 2),
                'category': product['category'],
                'in_stock': True
            }
            transformed_products.append(transformed)
        
        result = {'transformed_products': transformed_products}
        
        print(f"\n  Transformed {len(transformed_products)} products")
        for p in transformed_products:
            print(f"    {p['name']}: {p['price']} TRY -> {p['price_with_tax']} TRY (with tax)")
        
        # Save transformed data
        handler.write_json(result, "output/transformed_products.json")


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
JSON Transformation - Key Concepts:

1. JSON Operations:
   - Read from file/string
   - Write to file
   - Convert to/from string

2. Transformations:
   - Flatten nested JSON
   - Extract specific fields
   - Filter data
   - Transform keys
   - Add timestamps
   - Merge JSON objects

3. Validation:
   - Schema validation
   - Required fields check
   - Type checking

4. Nested Operations:
   - Get nested values (dot notation)
   - Set nested values
   - Remove empty values

5. Use Cases:
   - API data processing
   - Data cleaning
   - ETL pipelines
   - Configuration management
   - Data export

6. Best Practices:
   - Validate before processing
   - Handle missing keys gracefully
   - Use meaningful key names
   - Add timestamps for tracking
   - Keep backups of original data
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check 'data' and 'output' folders for results")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 59 - JSON TRANSFORMATION")
    print("=" * 60 + "\n")
    
    handler = JSONHandler()
    
    # Run all demos
    demo_basic_operations(handler)
    demo_flatten_json(handler)
    demo_extract_fields(handler)
    demo_filter_data(handler)
    demo_transform_keys(handler)
    demo_add_timestamp(handler)
    demo_merge_json(handler)
    demo_validation(handler)
    demo_nested_operations(handler)
    demo_transform_products(handler)
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
