"""
Performance Test Functions
Various algorithms to test and profile
"""

import math
import random
import time
from typing import List, Union


def slow_fibonacci(n: int) -> int:
    """
    Recursive Fibonacci (slow implementation)
    Time complexity: O(2^n)
    """
    if n <= 1:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


def fast_fibonacci(n: int) -> int:
    """
    Iterative Fibonacci (fast implementation)
    Time complexity: O(n)
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Bubble sort algorithm
    Time complexity: O(n^2)
    """
    n = len(arr)
    arr_copy = arr.copy()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
    
    return arr_copy


def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick sort algorithm
    Time complexity: O(n log n) average
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def find_primes_naive(n: int) -> List[int]:
    """
    Find primes using naive method
    Time complexity: O(n * sqrt(n))
    """
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes


def find_primes_sieve(n: int) -> List[int]:
    """
    Find primes using Sieve of Eratosthenes
    Time complexity: O(n log log n)
    """
    if n < 2:
        return []
    
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    
    return [i for i in range(2, n + 1) if sieve[i]]


def string_concat_test(n: int) -> str:
    """
    String concatenation using + operator (slow)
    """
    result = ""
    for i in range(n):
        result += str(i)
    return result


def string_join_test(n: int) -> str:
    """
    String concatenation using join (fast)
    """
    return ''.join(str(i) for i in range(n))


def list_append_test(n: int) -> List[int]:
    """
    List append test
    """
    result = []
    for i in range(n):
        result.append(i)
    return result


def list_comprehension_test(n: int) -> List[int]:
    """
    List comprehension test
    """
    return [i for i in range(n)]


def generate_test_data(size: int) -> List[int]:
    """Generate random test data"""
    random.seed(42)
    return [random.randint(1, 1000) for _ in range(size)]
