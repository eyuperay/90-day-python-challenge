"""
Calculator module with various mathematical functions
To be tested with unit tests
"""

import math
import re
from typing import Union, List


class Calculator:
    """A simple calculator class with basic operations"""
    
    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers"""
        return a + b
    
    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Subtract b from a"""
        return a - b
    
    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiply two numbers"""
        return a * b
    
    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> float:
        """Divide a by b. Raises ValueError if b is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def power(base: Union[int, float], exponent: Union[int, float]) -> float:
        """Raise base to the power of exponent"""
        return base ** exponent
    
    @staticmethod
    def square_root(x: Union[int, float]) -> float:
        """Calculate square root. Raises ValueError if x is negative."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial. Raises ValueError if n is negative."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if not isinstance(n, int):
            raise TypeError("Factorial requires an integer")
        return math.factorial(n)
    
    @staticmethod
    def is_even(n: int) -> bool:
        """Check if a number is even"""
        return n % 2 == 0
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def average(numbers: List[Union[int, float]]) -> float:
        """Calculate average of a list of numbers. Raises ValueError if list is empty."""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """Generate Fibonacci sequence up to n terms"""
        if n <= 0:
            return []
        if n == 1:
            return [0]
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        return sequence
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm"""
        a = abs(a)
        b = abs(b)
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate Least Common Multiple"""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // Calculator.gcd(a, b)


def greet(name: str) -> str:
    """Return a greeting message"""
    if not name:
        return "Hello, Guest!"
    return f"Hello, {name}!"


def validate_email(email: str) -> bool:
    """Validate email format with proper regex"""
    if not email or not isinstance(email, str):
        return False
    
    # More strict email validation
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    # Additional checks for invalid patterns
    if re.match(pattern, email):
        # Check for consecutive dots, dots before @, etc.
        if '..' in email:
            return False
        if email.startswith('.') or email.startswith('@'):
            return False
        if email.endswith('.') or email.endswith('@'):
            return False
        local_part, domain = email.split('@')
        if len(local_part) == 0 or len(domain) == 0:
            return False
        if domain.startswith('.') or domain.endswith('.'):
            return False
        return True
    
    return False


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9
