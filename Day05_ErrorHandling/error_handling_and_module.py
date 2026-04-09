"""
Day 05: Error Handling and Modular Design

This script demonstrates the use of helper functions imported
from the 'utils.py' module. It includes:
- Performing a safe division between two user-provided numbers.
- Validating user-provided age input using exception handling.

For detailed explanations of the functions and concepts, please refer to the README.md file in this folder.
"""

from utils import safe_divide, validate_age

def main():
    # Safe division example
    try:
        num1 = float(input("Enter numerator: "))
        num2 = float(input("Enter denominator: "))
        result = safe_divide(num1, num2)
        print(f"Result: {result}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")

    # Age validation example
    try:
        age = int(input("Enter your age: "))
        validate_age(age)
        print(f"Your age is valid: {age}")
    except ValueError as ve:
        print(f"Invalid age: {ve}")

if __name__ == "__main__":
    main()