#!/usr/bin/env python3
"""
Day 53 - Functools Caching
Demonstrates lru_cache for function result caching
"""

import time
import functools
from caching_demo import CachingDemo


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 53 - FUNCTOOLS CACHING")
    print("=" * 60 + "\n")
    
    demo = CachingDemo()
    
    # ==================== BASIC DEMO ====================
    print_section("1. BASIC CACHING DEMO")
    
    print("\nComputing fibonacci(5) multiple times...")
    
    # First call - computes
    print("\nFirst call - fibonacci_cached(5):")
    start = time.time()
    result = demo.fibonacci_cached(5)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.6f}s")
    print(f"  Calls: {demo.get_call_count('fibonacci_cached')}")
    
    # Second call - returns cached result
    print("\nSecond call - fibonacci_cached(5):")
    start = time.time()
    result = demo.fibonacci_cached(5)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.6f}s")
    print(f"  Calls: {demo.get_call_count('fibonacci_cached')}")
    
    # Third call - different value
    print("\nThird call - fibonacci_cached(6):")
    start = time.time()
    result = demo.fibonacci_cached(6)
    elapsed = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.6f}s")
    print(f"  Calls: {demo.get_call_count('fibonacci_cached')}")
    
    # Cache info
    info = demo.get_cache_info(demo.fibonacci_cached)
    print(f"\nCache Info:")
    print(f"  Hits: {info.get('hits', 0)}")
    print(f"  Misses: {info.get('misses', 0)}")
    print(f"  Current Size: {info.get('currsize', 0)}")
    print(f"  Max Size: {info.get('maxsize', 'None')}")
    
    # ==================== PERFORMANCE TEST ====================
    print_section("2. PERFORMANCE TEST")
    demo.run_performance_test()
    
    # ==================== CACHE CLEAR ====================
    print_section("3. CACHE CLEAR DEMONSTRATION")
    demo.demonstrate_cache_clear()
    
    # ==================== MAXSIZE EFFECT ====================
    print_section("4. MAXSIZE EFFECT DEMONSTRATION")
    demo.demonstrate_maxsize_effect()
    
    # ==================== PRACTICAL EXAMPLE ====================
    print_section("5. PRACTICAL EXAMPLE - DATA PROCESSING")
    
    # Simulate data processing with caching
    @functools.lru_cache(maxsize=100)
    def process_data(data_id: int) -> dict:
        """Simulate expensive data processing"""
        print(f"  Processing data_id={data_id} (expensive operation)")
        time.sleep(0.05)  # Simulate processing
        return {
            'id': data_id,
            'result': data_id * data_id,
            'timestamp': time.time()
        }
    
    # Process some data
    print("\nProcessing data (first time - all expensive):")
    for i in range(5):
        result = process_data(i)
        print(f"  ID: {i}, Result: {result['result']}")
    
    print("\nProcessing data (second time - cached):")
    for i in range(5):
        result = process_data(i)
        print(f"  ID: {i}, Result: {result['result']}")
    
    info = process_data.cache_info()
    print(f"\nProcess data cache info:")
    print(f"  Hits: {info.hits}")
    print(f"  Misses: {info.misses}")
    print(f"  Current Size: {info.currsize}")
    print(f"  Max Size: {info.maxsize}")
    
    # Process new data
    print("\nProcessing new data (some cached, some new):")
    for i in range(3, 8):
        result = process_data(i)
        print(f"  ID: {i}, Result: {result['result']}")
    
    info = process_data.cache_info()
    print(f"\nFinal cache info:")
    print(f"  Hits: {info.hits}")
    print(f"  Misses: {info.misses}")
    print(f"  Current Size: {info.currsize}")
    print(f"  Max Size: {info.maxsize}")
    
    # ==================== SUMMARY ====================
    print_section("SUMMARY")
    print("""
Functools Caching - Key Concepts:

1. @lru_cache(maxsize=128)
   - Caches function results
   - LRU (Least Recently Used) eviction policy
   - maxsize: maximum number of items to cache

2. Benefits:
   - Dramatically improves performance
   - Reduces redundant computations
   - Useful for expensive/recursive functions

3. Methods:
   - cache_info() - Get cache statistics
   - cache_clear() - Clear the cache

4. Use Cases:
   - Recursive functions (Fibonacci)
   - Database queries
   - API calls
   - Expensive computations
   - Data processing

5. Considerations:
   - Memory usage
   - Cache size limits
   - Function arguments must be hashable
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
