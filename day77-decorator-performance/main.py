#!/usr/bin/env python3
"""
Day 77 - Decorator Performance
Demonstrates performance monitoring with decorators
"""

import time
import random
import math
from decorators import (
    time_it, log_arguments, retry_on_error, cache_result,
    profile, limit_calls, tracker, PerformanceTracker
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


# ==================== SAMPLE FUNCTIONS WITH DECORATORS ====================

@time_it
def slow_function():
    """Slow function to demonstrate timing"""
    time.sleep(random.uniform(0.5, 1.0))
    return "Done"


@time_it
@log_arguments
def calculate_power(base: float, exponent: float) -> float:
    """Calculate power with logging"""
    return base ** exponent


@retry_on_error(max_attempts=3, delay=0.5)
def unreliable_function():
    """Function that sometimes fails"""
    if random.random() < 0.6:  # 60% chance of failure
        raise ValueError("Random error occurred!")
    return "Success!"


@cache_result(maxsize=10)
def expensive_computation(n: int) -> int:
    """Expensive computation with caching"""
    time.sleep(0.5)  # Simulate expensive operation
    return n * n * n


@profile
def complex_operation(n: int) -> float:
    """Complex operation with full profiling"""
    result = 0
    for i in range(n):
        result += math.sin(i) * math.cos(i)
    return result


@limit_calls(3)
def limited_function():
    """Function with call limit"""
    return "Called!"


# ==================== DEMO FUNCTIONS ====================

def demo_time_it():
    """Demonstrate time_it decorator"""
    print_section("1. TIME_IT DECORATOR")
    
    print("\nRunning slow_function()...")
    result = slow_function()
    print(f"  Result: {result}")
    
    print("\nRunning calculate_power(2, 10)...")
    result = calculate_power(2, 10)
    print(f"  Result: {result}")
    
    print("\nRunning calculate_power(3, 4)...")
    result = calculate_power(3, 4)
    print(f"  Result: {result}")


def demo_retry():
    """Demonstrate retry_on_error decorator"""
    print_section("2. RETRY_ON_ERROR DECORATOR")
    
    print("\nRunning unreliable_function() (will retry on error)...")
    try:
        result = unreliable_function()
        print(f"  Success! Result: {result}")
    except Exception as e:
        print(f"  Failed after retries: {e}")


def demo_cache():
    """Demonstrate cache_result decorator"""
    print_section("3. CACHE_RESULT DECORATOR")
    
    print("\nFirst call - expensive_computation(5)...")
    result1 = expensive_computation(5)
    print(f"  Result: {result1}")
    
    print("\nSecond call - expensive_computation(5) (should be cached)...")
    result2 = expensive_computation(5)
    print(f"  Result: {result2}")
    
    print("\nThird call - expensive_computation(7)...")
    result3 = expensive_computation(7)
    print(f"  Result: {result3}")


def demo_profile():
    """Demonstrate profile decorator"""
    print_section("4. PROFILE DECORATOR")
    
    print("\nRunning complex_operation(100000)...")
    result = complex_operation(100000)
    print(f"  Result: {result:.4f}")


def demo_limit_calls():
    """Demonstrate limit_calls decorator"""
    print_section("5. LIMIT_CALLS DECORATOR")
    
    print("\nCalling limited_function() 4 times (limit=3)...")
    for i in range(3):
        try:
            result = limited_function()
            print(f"  Call {i+1}: {result}")
        except RuntimeError as e:
            print(f"  Call {i+1}: {e}")


def demo_report():
    """Generate performance report"""
    print_section("6. PERFORMANCE REPORT")
    
    report = tracker.generate_report()
    print("\n" + report)
    
    # Save report
    tracker.save_report()
    
    # Reset tracker for next run
    tracker.reset()


def main():
    print("=" * 60)
    print("DAY 77 - DECORATOR PERFORMANCE")
    print("=" * 60 + "\n")
    
    print("Demonstrating various performance decorators...")
    
    demo_time_it()
    demo_retry()
    demo_cache()
    demo_profile()
    demo_limit_calls()
    demo_report()
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for performance report")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
