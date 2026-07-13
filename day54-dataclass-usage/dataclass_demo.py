"""
Dataclass Demo
Demonstrates Python dataclasses for clean data structures
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import json


# ==================== BASIC DATACLASS ====================

@dataclass
class Person:
    """Basic person dataclass"""
    name: str
    age: int
    email: str
    city: str = "Unknown"  # Default value
    
    def greet(self) -> str:
        """Method inside dataclass"""
        return f"Hello, my name is {self.name} and I'm {self.age} years old."


# ==================== DATACLASS WITH DEFAULT FACTORY ====================

@dataclass
class Product:
    """Product dataclass with default factory"""
    name: str
    price: float
    category: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    in_stock: bool = True
    
    def total_with_tax(self, tax_rate: float = 0.18) -> float:
        """Calculate price with tax"""
        return self.price * (1 + tax_rate)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'in_stock': self.in_stock
        }


# ==================== DATACLASS WITH INHERITANCE ====================

@dataclass
class User:
    """Base user dataclass"""
    username: str
    email: str
    is_active: bool = True
    
    def display(self) -> str:
        return f"User: {self.username} ({self.email})"


@dataclass
class Admin(User):
    """Admin user inherits from User"""
    permissions: List[str] = field(default_factory=list)
    admin_level: int = 1
    
    def display(self) -> str:
        return f"Admin: {self.username} (Level {self.admin_level})"


@dataclass
class Customer(User):
    """Customer user inherits from User"""
    loyalty_points: int = 0
    orders: List[int] = field(default_factory=list)
    
    def display(self) -> str:
        return f"Customer: {self.username} ({self.loyalty_points} points)"


# ==================== DATACLASS WITH VALIDATION ====================

@dataclass
class Transaction:
    """Transaction with validation"""
    amount: float
    currency: str = "TRY"
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validation after initialization"""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if self.currency not in ["TRY", "USD", "EUR", "GBP"]:
            raise ValueError(f"Unsupported currency: {self.currency}")


# ==================== DATACLASS WITH FROZEN ====================

@dataclass(frozen=True)
class Point:
    """Immutable point dataclass"""
    x: int
    y: int
    
    def distance_from_origin(self) -> float:
        """Calculate distance from origin"""
        return (self.x ** 2 + self.y ** 2) ** 0.5


# ==================== DATACLASS FOR DATA STORAGE ====================

@dataclass
class Student:
    """Student dataclass for data storage"""
    id: int
    name: str
    courses: List[str] = field(default_factory=list)
    grades: Dict[str, float] = field(default_factory=dict)
    
    def average_grade(self) -> float:
        """Calculate average grade"""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)
    
    def add_course(self, course: str, grade: float = None) -> None:
        """Add a course"""
        if course not in self.courses:
            self.courses.append(course)
            if grade is not None:
                self.grades[course] = grade
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'courses': self.courses,
            'grades': self.grades,
            'average': self.average_grade()
        }, indent=2)


# ==================== REAL-WORLD EXAMPLES ====================

@dataclass
class OrderItem:
    """Item in an order"""
    product_id: int
    name: str
    quantity: int
    unit_price: float
    
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    """Order dataclass"""
    order_id: str
    customer_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    
    def total_amount(self) -> float:
        """Calculate total order amount"""
        return sum(item.subtotal() for item in self.items)
    
    def add_item(self, product_id: int, name: str, quantity: int, unit_price: float) -> None:
        """Add item to order"""
        item = OrderItem(product_id, name, quantity, unit_price)
        self.items.append(item)
    
    def summary(self) -> str:
        """Get order summary"""
        return f"Order {self.order_id}: {len(self.items)} items, Total: {self.total_amount():.2f} TRY"


@dataclass
class Employee:
    """Employee dataclass"""
    employee_id: int
    first_name: str
    last_name: str
    department: str
    salary: float
    hire_date: datetime = field(default_factory=datetime.now)
    is_manager: bool = False
    
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def annual_salary(self) -> float:
        return self.salary * 12
    
    def promotion(self, new_salary: float, is_manager: bool = None) -> None:
        """Promote employee"""
        self.salary = new_salary
        if is_manager is not None:
            self.is_manager = is_manager


# ==================== UTILITY FUNCTIONS ====================

def compare_dataclass_vs_class():
    """Compare dataclass with traditional class"""
    print("\n" + "-"*50)
    print("DATACLASS VS TRADITIONAL CLASS")
    print("-"*50)
    
    # Traditional class
    class PersonClass:
        def __init__(self, name, age, email, city="Unknown"):
            self.name = name
            self.age = age
            self.email = email
            self.city = city
        
        def __repr__(self):
            return f"PersonClass(name={self.name!r}, age={self.age!r}, email={self.email!r}, city={self.city!r})"
        
        def __eq__(self, other):
            if not isinstance(other, PersonClass):
                return False
            return (self.name == other.name and self.age == other.age and 
                    self.email == other.email and self.city == other.city)
    
    # Dataclass version
    @dataclass
    class PersonDataclass:
        name: str
        age: int
        email: str
        city: str = "Unknown"
    
    print("Traditional Class: Need to write __init__, __repr__, __eq__ manually")
    print("Dataclass: Automatically generated")
    print("\nCode comparison:")
    print("  Traditional class: ~15 lines")
    print("  Dataclass: ~4 lines")
    
    print("\nBoth classes work the same way:")
    p1_class = PersonClass("Ali", 30, "ali@email.com")
    p1_dataclass = PersonDataclass("Ali", 30, "ali@email.com")
    
    print(f"  Traditional: {p1_class}")
    print(f"  Dataclass:   {p1_dataclass}")
