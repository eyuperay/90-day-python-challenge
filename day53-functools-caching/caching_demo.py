"""
Functools Caching Demo
Demonstrates lru_cache for function result caching
"""

import functools
import time
import random
import math
from typing import List, Dict, Any


class CachingDemo:
    """Demonstrates caching with functools.lru_cache"""
    
    def __init__(self):
        self.call_counts = {}
        self.cache_info = {}
    
    # ==================== WITHOUT CACHING ====================
    
    def fibonacci_slow(self, n: int) -> int:
        """
        Recursive Fibonacci WITHOUT caching
        Very slow for large n
        """
        self._increment_call_count('fibonacci_slow')
        if n <= 1:
            return n
        return self.fibonacci_slow(n - 1) + self.fibonacci_slow(n - 2)
    
    # ==================== WITH CACHING ====================
    
    @functools.lru_cache(maxsize=128)
    def fibonacci_cached(self, n: int) -> int:
        """
        Recursive Fibonacci WITH lru_cache
        Much faster for repeated calls
        """
        self._increment_call_count('fibonacci_cached')
        if n <= 1:
            return n
        return self.fibonacci_cached(n - 1) + self.fibonacci_cached(n - 2)
    
    # ==================== EXPENSIVE COMPUTATIONS ====================
    
    def expensive_computation_slow(self, n: int) -> float:
        """
        Expensive computation WITHOUT caching
        """
        self._increment_call_count('expensive_slow')
        time.sleep(0.1)  # Simulate heavy computation
        return math.sqrt(n) * math.pi * math.e
    
    @functools.lru_cache(maxsize=50)
    def expensive_computation_cached(self, n: int) -> float:
        """
        Expensive computation WITH caching
        """
        self._increment_call_count('expensive_cached')
        time.sleep(0.1)  # Simulate heavy computation
        return math.sqrt(n) * math.pi * math.e
    
    # ==================== PRIME NUMBER CHECK ====================
    
    def is_prime_slow(self, n: int) -> bool:
        """
        Prime check WITHOUT caching
        """
        self._increment_call_count('is_prime_slow')
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    @functools.lru_cache(maxsize=1000)
    def is_prime_cached(self, n: int) -> bool:
        """
        Prime check WITH caching
        """
        self._increment_call_count('is_prime_cached')
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    # ==================== FACTORIAL ====================
    
    @functools.lru_cache(maxsize=100)
    def factorial_cached(self, n: int) -> int:
        """
        Factorial with caching
        """
        self._increment_call_count('factorial_cached')
        if n <= 1:
            return 1
        return n * self.factorial_cached(n - 1)
    
    # ==================== COMBINATION ====================
    
    @functools.lru_cache(maxsize=1000)
    def combination_cached(self, n: int, k: int) -> int:
        """
        Combination (n choose k) with caching
        """
        self._increment_call_count('combination_cached')
        if k == 0 or k == n:
            return 1
        if k > n:
            return 0
        return self.combination_cached(n - 1, k - 1) + self.combination_cached(n - 1, k)
    
    # ==================== HELPER METHODS ====================
    
    def _increment_call_count(self, func_name: str):
        """Increment call count for a function"""
        if func_name not in self.call_counts:
            self.call_counts[func_name] = 0
        self.call_counts[func_name] += 1
    
    def get_call_count(self, func_name: str) -> int:
        """Get call count for a function"""
        return self.call_counts.get(func_name, 0)
    
    def get_cache_info(self, func) -> Dict[str, Any]:
        """Get cache info for a cached function"""
        if hasattr(func, 'cache_info'):
            info = func.cache_info()
            return {
                'hits': info.hits,
                'misses': info.misses,
                'maxsize': info.maxsize,
                'currsize': info.currsize
            }
        return {}
    
    def clear_cache(self, func):
        """Clear cache for a function"""
        if hasattr(func, 'cache_clear'):
            func.cache_clear()
    
    def reset_stats(self):
        """Reset all statistics"""
        self.call_counts = {}
    
    # ==================== DEMO FUNCTIONS ====================
    
    def run_performance_test(self):
        """
        Run performance comparison between cached and non-cached functions
        """
        print("\n" + "-"*50)
        print("PERFORMANCE TEST")
        print("-"*50)
        
        # Test Fibonacci
        print("\n1. Fibonacci Comparison:")
        n = 30
        
        # Slow version
        start = time.time()
        result_slow = self.fibonacci_slow(n)
        time_slow = time.time() - start
        
        # Reset call count for cached version
        self.call_counts['fibonacci_cached'] = 0
        
        # Cached version
        start = time.time()
        result_cached = self.fibonacci_cached(n)
        time_cached = time.time() - start
        
        print(f"   n={n}")
        print(f"   Without cache: {time_slow:.6f}s, calls={self.get_call_count('fibonacci_slow')}")
        print(f"   With cache:    {time_cached:.6f}s, calls={self.get_call_count('fibonacci_cached')}")
        print(f"   Speedup:       {time_slow/time_cached:.2f}x")
        
        # Cache info
        info = self.get_cache_info(self.fibonacci_cached)
        print(f"   Cache hits: {info.get('hits', 0)}, misses: {info.get('misses', 0)}")
        
        # Test expensive computation
        print("\n2. Expensive Computation:")
        numbers = [random.randint(10, 50) for _ in range(20)]
        
        # Slow version
        self.call_counts['expensive_slow'] = 0
        start = time.time()
        for num in numbers:
            self.expensive_computation_slow(num)
        time_slow = time.time() - start
        
        # Cached version
        self.call_counts['expensive_cached'] = 0
        start = time.time()
        for num in numbers:
            self.expensive_computation_cached(num)
        time_cached = time.time() - start
        
        print(f"   Numbers: {len(numbers)} unique values")
        print(f"   Without cache: {time_slow:.4f}s, calls={self.get_call_count('expensive_slow')}")
        print(f"   With cache:    {time_cached:.4f}s, calls={self.get_call_count('expensive_cached')}")
        print(f"   Speedup:       {time_slow/time_cached:.2f}x")
        
        # Test prime numbers
        print("\n3. Prime Number Check:")
        primes_to_check = [random.randint(1000, 10000) for _ in range(50)]
        
        self.call_counts['is_prime_slow'] = 0
        start = time.time()
        for num in primes_to_check:
            self.is_prime_slow(num)
        time_slow = time.time() - start
        
        self.call_counts['is_prime_cached'] = 0
        start = time.time()
        for num in primes_to_check:
            self.is_prime_cached(num)
        time_cached = time.time() - start
        
        print(f"   Numbers: {len(primes_to_check)} unique values")
        print(f"   Without cache: {time_slow:.6f}s, calls={self.get_call_count('is_prime_slow')}")
        print(f"   With cache:    {time_cached:.6f}s, calls={self.get_call_count('is_prime_cached')}")
        print(f"   Speedup:       {time_slow/time_cached:.2f}x")
        
        # Test combination
        print("\n4. Combination (n choose k):")
        self.call_counts['combination_cached'] = 0
        start = time.time()
        
        results = []
        for i in range(10):
            results.append(self.combination_cached(20, i))
        
        time_cached = time.time() - start
        
        print(f"   Computing C(20, k) for k=0..9")
        print(f"   Results: {results}")
        print(f"   Time: {time_cached:.6f}s")
        print(f"   Calls: {self.get_call_count('combination_cached')}")
        
        info = self.get_cache_info(self.combination_cached)
        print(f"   Cache hits: {info.get('hits', 0)}, misses: {info.get('misses', 0)}")
    
    def demonstrate_cache_clear(self):
        """
        Demonstrate cache clearing
        """
        print("\n" + "-"*50)
        print("CACHE CLEAR DEMONSTRATION")
        print("-"*50)
        
        # Run some computations
        print("Computing fibonacci values...")
        for i in range(10, 20):
            self.fibonacci_cached(i)
        
        info_before = self.get_cache_info(self.fibonacci_cached)
        print(f"Before clear - Cache size: {info_before.get('currsize', 0)}")
        
        # Clear cache
        self.fibonacci_cached.cache_clear()
        
        info_after = self.get_cache_info(self.fibonacci_cached)
        print(f"After clear  - Cache size: {info_after.get('currsize', 0)}")
        
        # Run again
        print("Running fibonacci again after cache clear...")
        for i in range(10, 15):
            self.fibonacci_cached(i)
        
        info_final = self.get_cache_info(self.fibonacci_cached)
        print(f"After recompute - Cache size: {info_final.get('currsize', 0)}")
    
    def demonstrate_maxsize_effect(self):
        """
        Demonstrate maxsize effect on caching
        """
        print("\n" + "-"*50)
        print("MAXSIZE EFFECT DEMONSTRATION")
        print("-"*50)
        
        # Clear existing cache
        self.fibonacci_cached.cache_clear()
        
        print("Adding 200 numbers to cache (maxsize=128)...")
        for i in range(200):
            self.fibonacci_cached(i)
        
        info = self.get_cache_info(self.fibonacci_cached)
        print(f"Cache size: {info.get('currsize', 0)} (max: {info.get('maxsize', 'None')})")
        print(f"Cache hits: {info.get('hits', 0)}")
        print(f"Cache misses: {info.get('misses', 0)}")
