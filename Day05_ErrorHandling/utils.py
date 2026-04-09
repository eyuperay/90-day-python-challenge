"""
Utility functions for Day 05.

For full task description and usage details, please refer to the README.md file.
"""


def safe_divide(a: float, b: float) -> float:
    """
    Safely divide two numbers.

    Returns 0.0 if division by zero occurs.
    """
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return 0.0


def validate_age(age: int) -> bool:
    """
    Validate that age is not negative.

    Raises:
        ValueError: If age is less than 0.
    """
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return True