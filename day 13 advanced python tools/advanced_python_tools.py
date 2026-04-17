"""
Purpose of this script:
This script demonstrates advanced Python concepts including decorators,
generators, and typing to simulate a simple data processing pipeline.
"""

from typing import Callable, Iterator
from datetime import datetime


def log_execution(func: Callable) -> Callable:
    """
    Decorator that logs the execution start and end of a function.
    """

    def wrapper(*args, **kwargs):
        print(f"[START] {func.__name__} at {datetime.now()}")
        result = func(*args, **kwargs)
        print(f"[END] {func.__name__} at {datetime.now()}")
        return result

    return wrapper


def data_streamer(data: list) -> Iterator[int]:
    """
    Generator that yields data one by one with a processing message.
    """
    for item in data:
        print("Processing data...")
        yield item


@log_execution
def process_data(value: int) -> None:
    """
    Simulates processing of a single data item.
    """
    print(f"Processed value: {value}")


if __name__ == "__main__":
    large_data = list(range(10))  # You can increase to 100

    for item in data_streamer(large_data):
        process_data(item)