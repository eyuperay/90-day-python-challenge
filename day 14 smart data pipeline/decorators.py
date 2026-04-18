"""
Decorators module for performance tracking.
"""

from functools import wraps
from time import time


def time_logger(func):
    """
    Measures execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        print(f"[START] {func.__name__}")

        result = func(*args, **kwargs)

        end = time()
        print(f"[END] {func.__name__} | Duration: {end - start:.6f} seconds")

        return result

    return wrapper