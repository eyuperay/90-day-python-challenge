"""
Purpose of this script:
The goal of this script is to collect the user's first name, last name,
birth year, and height, calculate the age based on the birth year, and
display this information in a professional sentence.
All variables include type hints.
"""

from datetime import datetime

# Type hints for all variables
first_name: str = input("Please enter your first name: ")
last_name: str = input("Please enter your last name: ")
birth_year: int = int(input("Please enter your birth year: "))
height: float = float(input("Please enter your height in meters (e.g., 1.75): "))

# Calculate age dynamically
current_year: int = datetime.now().year
age: int = current_year - birth_year

# Output professional message
print(f"{first_name} {last_name} is {age} years old and {height} meters tall.")