"""
Utility functions for Day 05: Error Handling and Modular Design.

This module contains helper functions used in the main program:
- safe_divide: Performs division safely with zero-check.
- validate_age: Validates that an age is non-negative.

For detailed explanations and usage examples, please refer to the README.md file.
"""

def safe_divide(a: float, b: float) -> float:
    """
    Safely divides two numbers. Returns 0.0 if dividing by zero,
    and prints an informative message.
    """
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return 0.0

def validate_age(age: int) -> bool:
    """
    Validates age. Raises ValueError if the input is negative.
    """
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return True
