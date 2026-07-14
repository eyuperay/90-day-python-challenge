"""
Core module - Basic utility functions
"""

import time
import functools


def greet(name: str = "World") -> str:
    """
    Return a greeting message
    
    Args:
        name: Name to greet (default: "World")
    
    Returns:
        Greeting message
    """
    return f"Hello, {name}!"


def reverse_string(text: str) -> str:
    """
    Reverse a string
    
    Args:
        text: String to reverse
    
    Returns:
        Reversed string
    """
    return text[::-1]


def count_vowels(text: str) -> int:
    """
    Count vowels in a string
    
    Args:
        text: String to analyze
    
    Returns:
        Number of vowels (a, e, i, o, u)
    """
    vowels = set('aeiouAEIOU')
    return sum(1 for char in text if char in vowels)


def is_palindrome(text: str) -> bool:
    """
    Check if a string is a palindrome
    
    Args:
        text: String to check
    
    Returns:
        True if palindrome, False otherwise
    """
    text = text.lower().replace(" ", "").replace(",", "").replace(".", "")
    return text == text[::-1]


def factorial(n: int) -> int:
    """
    Calculate factorial of a number
    
    Args:
        n: Non-negative integer
    
    Returns:
        Factorial of n
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> list:
    """
    Generate Fibonacci sequence up to n terms
    
    Args:
        n: Number of terms
    
    Returns:
        List of Fibonacci numbers
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence


def timer(func):
    """
    Decorator to measure function execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[Timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def main():
    """Command line entry point"""
    print("MyPackage - Sample Python Package")
    print("="*40)
    print("Available functions:")
    print("  - greet('name')")
    print("  - reverse_string('text')")
    print("  - count_vowels('text')")
    print("  - is_palindrome('text')")
    print("  - factorial(n)")
    print("  - fibonacci(n)")
    print("  - math functions (add, subtract, multiply, divide)")
    print("  - utils (read_file, write_file, json_to_dict, dict_to_json)")
