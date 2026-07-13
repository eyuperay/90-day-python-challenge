#!/usr/bin/env python3
"""
Day 54 - Dataclass Usage
Demonstrates Python dataclasses for clean data structures
"""

import time
import json
from datetime import datetime
from dataclass_demo import *


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 54 - DATACLASS USAGE")
    print("=" * 60 + "\n")
    
    # ==================== 1. BASIC DATACLASS ====================
    print_section("1. BASIC DATACLASS")
    
    person = Person("Ali", 30, "ali@email.com", "Istanbul")
    print(f"Person: {person}")
    print(f"Greeting: {person.greet()}")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Email: {person.email}")
    print(f"City: {person.city}")
    
    # Auto-generated methods
    person2 = Person("Ali", 30, "ali@email.com", "Istanbul")
    print(f"\nEquality check: {person == person2} (Same data)")
    
    person3 = Person("Ayse", 25, "ayse@email.com")
    print(f"Equality check: {person == person3} (Different data)")
    
    # ==================== 2. DATACLASS WITH DEFAULTS ====================
    print_section("2. DATACLASS WITH DEFAULT VALUES")
    
    product = Product(
        name="Laptop",
        price=15000.00,
        category="Electronics",
        tags=["new", "gaming", "premium"]
    )
    
    print(f"Product: {product}")
    print(f"Created at: {product.created_at}")
    print(f"Price with tax: {product.total_with_tax():.2f} TRY")
    print(f"To dict: {product.to_dict()}")
    
    # ==================== 3. INHERITANCE ====================
    print_section("3. INHERITANCE WITH DATACLASS")
    
    user = User("john_doe", "john@email.com")
    admin = Admin("admin_user", "admin@email.com", permissions=["read", "write", "delete"])
    customer = Customer("customer_user", "customer@email.com", loyalty_points=150)
    
    print(f"User: {user}")
    print(f"  {user.display()}")
    print(f"\nAdmin: {admin}")
    print(f"  {admin.display()}")
    print(f"  Permissions: {admin.permissions}")
    print(f"\nCustomer: {customer}")
    print(f"  {customer.display()}")
    print(f"  Loyalty Points: {customer.loyalty_points}")
    
    # ==================== 4. VALIDATION ====================
    print_section("4. VALIDATION WITH __post_init__")
    
    try:
        transaction1 = Transaction(amount=1000, currency="TRY", description="Payment")
        print(f"Valid transaction: {transaction1}")
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        transaction2 = Transaction(amount=-50, currency="USD")
        print(f"Invalid transaction: {transaction2}")
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        transaction3 = Transaction(amount=100, currency="JPY")
        print(f"Invalid transaction: {transaction3}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # ==================== 5. FROZEN DATACLASS ====================
    print_section("5. FROZEN (IMMUTABLE) DATACLASS")
    
    point = Point(3, 4)
    print(f"Point: {point}")
    print(f"Distance from origin: {point.distance_from_origin():.2f}")
    print("Point is immutable - cannot change values")
    
    # Trying to modify frozen dataclass will raise error
    try:
        point.x = 5
    except Exception as e:
        print(f"Cannot modify frozen dataclass: {e}")
    
    # ==================== 6. DATA STORAGE ====================
    print_section("6. DATA STORAGE WITH DATACLASS")
    
    student = Student(1, "Mehmet Demir")
    student.add_course("Math", 85.5)
    student.add_course("Physics", 92.0)
    student.add_course("Chemistry", 78.5)
    
    print(f"Student: {student}")
    print(f"Courses: {student.courses}")
    print(f"Grades: {student.grades}")
    print(f"Average: {student.average_grade():.2f}")
    print(f"\nJSON representation:")
    print(student.to_json())
    
    # ==================== 7. REAL-WORLD EXAMPLES ====================
    print_section("7. REAL-WORLD EXAMPLES")
    
    # Order Example
    print("\n--- Order Management ---")
    order = Order(order_id="ORD-001", customer_id=1001)
    order.add_item(1, "Laptop", 1, 15000.00)
    order.add_item(2, "Mouse", 2, 200.00)
    order.add_item(3, "Keyboard", 1, 500.00)
    
    print(f"Order: {order.summary()}")
    print(f"Status: {order.status}")
    print(f"Created: {order.created_at}")
    
    # Employee Example
    print("\n--- Employee Management ---")
    employee = Employee(
        employee_id=101,
        first_name="Ahmet",
        last_name="Yilmaz",
        department="Engineering",
        salary=50000
    )
    
    print(f"Employee: {employee.full_name()}")
    print(f"Department: {employee.department}")
    print(f"Salary: {employee.salary} TRY/month")
    print(f"Annual Salary: {employee.annual_salary():,.0f} TRY")
    print(f"Is Manager: {employee.is_manager}")
    
    employee.promotion(65000, True)
    print(f"\nAfter promotion:")
    print(f"New Salary: {employee.salary} TRY/month")
    print(f"Is Manager: {employee.is_manager}")
    
    # ==================== 8. COMPARISON ====================
    print_section("8. DATACLASS VS TRADITIONAL CLASS")
    compare_dataclass_vs_class()
    
    # ==================== 9. PERFORMANCE ====================
    print_section("9. PERFORMANCE COMPARISON")
    
    # Create many dataclass instances
    start = time.time()
    persons = []
    for i in range(10000):
        persons.append(Person(f"Person{i}", i % 50, f"person{i}@email.com"))
    dataclass_time = time.time() - start
    print(f"Dataclass: Created 10,000 instances in {dataclass_time:.4f}s")
    
    # Create many traditional class instances
    class PersonTraditional:
        def __init__(self, name, age, email):
            self.name = name
            self.age = age
            self.email = email
    
    start = time.time()
    persons = []
    for i in range(10000):
        persons.append(PersonTraditional(f"Person{i}", i % 50, f"person{i}@email.com"))
    traditional_time = time.time() - start
    print(f"Traditional: Created 10,000 instances in {traditional_time:.4f}s")
    
    print(f"\nDataclass is {traditional_time/dataclass_time:.2f}x faster!")
    
    # ==================== 10. SUMMARY ====================
    print_section("SUMMARY")
    print("""
Dataclass - Key Concepts:

1. What is Dataclass?
   - Automatically generates __init__, __repr__, __eq__
   - Reduces boilerplate code
   - Clean and readable

2. Features:
   - Default values
   - Default factory (field(default_factory=list))
   - Inheritance support
   - __post_init__ for validation
   - Frozen (immutable) dataclasses

3. Benefits:
   - Less code to write
   - Auto-generated methods
   - Better type hints
   - Cleaner code structure

4. When to Use:
   - Data containers
   - DTOs (Data Transfer Objects)
   - Models
   - Configuration objects
   - Value objects

5. Comparison with Traditional Class:
   - Dataclass: ~4 lines
   - Traditional: ~15 lines
   - Same functionality
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
