"""
Enum Demo
Demonstrates Python Enum for constants management
"""

from enum import Enum, auto, IntEnum, unique
from datetime import datetime
from typing import Optional, List, Dict, Any


# ==================== BASIC ENUM ====================

class Color(Enum):
    """Basic color enum"""
    RED = 1
    GREEN = 2
    BLUE = 3
    
    def describe(self) -> str:
        """Method inside enum"""
        return f"{self.name}: {self.value}"


class Status(Enum):
    """Order status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    def is_active(self) -> bool:
        """Check if status is active"""
        return self not in [Status.CANCELLED, Status.DELIVERED]
    
    def next_status(self):
        """Get next status in workflow"""
        workflow = [
            Status.PENDING,
            Status.PROCESSING,
            Status.SHIPPED,
            Status.DELIVERED
        ]
        try:
            idx = workflow.index(self)
            return workflow[idx + 1] if idx < len(workflow) - 1 else None
        except ValueError:
            return None


# ==================== AUTO-VALUE ENUM ====================

class Priority(Enum):
    """Auto-generated values"""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    URGENT = auto()


# ==================== INTEGER ENUM ====================

class HttpStatus(IntEnum):
    """HTTP status codes as IntEnum"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


# ==================== UNIQUE ENUM ====================

@unique
class UniqueColors(Enum):
    """Unique values only - will error if duplicates"""
    RED = 1
    GREEN = 2
    BLUE = 3
    # YELLOW = 1  # This would raise ValueError


# ==================== ENUM WITH MIXED TYPES ====================

class UserRole(Enum):
    """User roles with mixed types"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
    SUPER_ADMIN = 999


# ==================== ENUM WITH METHODS ====================

class Day(Enum):
    """Days of week with methods"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
    def is_weekend(self) -> bool:
        """Check if day is weekend"""
        return self in [Day.SATURDAY, Day.SUNDAY]
    
    def is_weekday(self) -> bool:
        """Check if day is weekday"""
        return not self.is_weekend()
    
    def next_day(self):
        """Get next day"""
        days = list(Day)
        idx = days.index(self)
        return days[(idx + 1) % len(days)]
    
    def previous_day(self):
        """Get previous day"""
        days = list(Day)
        idx = days.index(self)
        return days[(idx - 1) % len(days)]


# ==================== ENUM WITH CUSTOM PROPERTIES ====================

class Currency(Enum):
    """Currency enum with additional properties"""
    USD = ("USD", "$", 1.0)
    EUR = ("EUR", "€", 0.85)
    TRY = ("TRY", "₺", 7.5)
    GBP = ("GBP", "£", 0.73)
    JPY = ("JPY", "¥", 110.0)
    
    def __init__(self, code: str, symbol: str, rate_to_usd: float):
        self.code = code
        self.symbol = symbol
        self.rate_to_usd = rate_to_usd
    
    def convert_from_usd(self, amount: float) -> float:
        """Convert USD to this currency"""
        return amount * self.rate_to_usd
    
    def convert_to_usd(self, amount: float) -> float:
        """Convert from this currency to USD"""
        return amount / self.rate_to_usd
    
    def format(self, amount: float) -> str:
        """Format amount with currency symbol"""
        return f"{self.symbol}{amount:,.2f}"


# ==================== ENUM WITH FUNCTIONAL CREATION ====================

# Create enum dynamically
Animal = Enum('Animal', ['DOG', 'CAT', 'BIRD', 'FISH'])
# Animal.DOG, Animal.CAT, etc.


# ==================== REAL-WORLD EXAMPLES ====================

class OrderStatus(Enum):
    """Order status with workflow"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled"""
        return self in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def can_refund(self) -> bool:
        """Check if order can be refunded"""
        return self in [OrderStatus.DELIVERED]
    
    def is_completed(self) -> bool:
        """Check if order is completed"""
        return self in [OrderStatus.DELIVERED, OrderStatus.CANCELLED, OrderStatus.REFUNDED]


class PaymentMethod(Enum):
    """Payment methods"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    E_WALLET = "e_wallet"
    CASH = "cash"
    CRYPTO = "crypto"
    
    def is_online(self) -> bool:
        """Check if payment is online"""
        return self not in [PaymentMethod.CASH]
    
    def requires_approval(self) -> bool:
        """Check if payment requires approval"""
        return self in [PaymentMethod.BANK_TRANSFER, PaymentMethod.CRYPTO]


class LogLevel(Enum):
    """Log levels"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    
    def __str__(self):
        return f"[{self.name}]"
    
    def is_higher_than(self, other) -> bool:
        """Check if this level is higher than other"""
        return self.value > other.value


# ==================== UTILITY FUNCTIONS ====================

def enum_to_dict(enum_class) -> Dict[str, Any]:
    """Convert enum to dictionary"""
    return {member.name: member.value for member in enum_class}


def enum_to_list(enum_class) -> List[str]:
    """Get all enum member names"""
    return [member.name for member in enum_class]


def enum_values(enum_class) -> List[Any]:
    """Get all enum member values"""
    return [member.value for member in enum_class]


def find_enum_by_value(enum_class, value) -> Optional[Enum]:
    """Find enum member by value"""
    for member in enum_class:
        if member.value == value:
            return member
    return None
