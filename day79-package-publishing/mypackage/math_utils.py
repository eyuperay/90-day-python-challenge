"""
Math utilities module
"""

import math
from collections import Counter
from typing import List, Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers"""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Subtract two numbers"""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers"""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: Number, exponent: Number) -> Number:
    """Calculate power"""
    return base ** exponent


def sqrt(x: Number) -> float:
    """Calculate square root"""
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(x)


def average(numbers: List[Number]) -> float:
    """Calculate average of numbers"""
    if not numbers:
        raise ValueError("List is empty")
    return sum(numbers) / len(numbers)


def median(numbers: List[Number]) -> float:
    """Calculate median of numbers"""
    if not numbers:
        raise ValueError("List is empty")
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid-1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]


def mode(numbers: List[Number]) -> Number:
    """Find mode of numbers"""
    if not numbers:
        raise ValueError("List is empty")
    counter = Counter(numbers)
    return max(counter.items(), key=lambda x: x[1])[0]


def is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor"""
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)
