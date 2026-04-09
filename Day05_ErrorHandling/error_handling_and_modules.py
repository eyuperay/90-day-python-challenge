"""
Main script for Day 05: Error Handling and Modules.

This script demonstrates user input handling, exception management,
and modular programming using utility functions.

For full task description and details, please refer to the README.md file.
"""

from utils import safe_divide, validate_age


def main():
    """Run the main program flow."""

    # Division example
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        result = safe_divide(num1, num2)
        print("Division result:", result)

    except ValueError:
        print("Invalid input. Please enter numeric values.")

    # Age validation example
    try:
        age = int(input("Enter your age: "))
        validate_age(age)
        print("Age is valid.")

    except ValueError as e:
        print("Warning:", e)


if __name__ == "__main__":
    main()