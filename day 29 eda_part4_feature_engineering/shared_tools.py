import time
from functools import wraps


def timer(func):
    """Decorator to measure execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"[TIMER] Execution Time: {end - start:.4f} seconds")

        return result

    return wrapper


def log_step(message: str) -> None:
    """Simple logging helper."""
    print(f"[LOG] {message}")