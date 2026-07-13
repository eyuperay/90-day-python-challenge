#!/usr/bin/env python3
"""
Day 51 - Performance Profiling
Profile and compare performance of different algorithms
"""

import sys
from performance_test import *
from profiler import PerformanceProfiler


def run_profiling():
    """Run performance profiling"""
    print("=" * 60)
    print("DAY 51 - PERFORMANCE PROFILING")
    print("=" * 60 + "\n")
    
    profiler = PerformanceProfiler()
    
    print("Generating test data...")
    test_data = generate_test_data(1000)
    test_data_small = generate_test_data(100)
    print(f"  Generated {len(test_data)} test items\n")
    
    print("="*60)
    print("PROFILING FUNCTIONS")
    print("="*60 + "\n")
    
    functions_to_profile = [
        (slow_fibonacci, (25,), {}, "slow_fibonacci(25)"),
        (fast_fibonacci, (35,), {}, "fast_fibonacci(35)"),
        (bubble_sort, (test_data_small,), {}, "bubble_sort(100)"),
        (quick_sort, (test_data_small,), {}, "quick_sort(100)"),
        (find_primes_naive, (500,), {}, "find_primes_naive(500)"),
        (find_primes_sieve, (500,), {}, "find_primes_sieve(500)"),
        (string_concat_test, (1000,), {}, "string_concat_test(1000)"),
        (string_join_test, (1000,), {}, "string_join_test(1000)"),
        (list_append_test, (10000,), {}, "list_append_test(10000)"),
        (list_comprehension_test, (10000,), {}, "list_comprehension_test(10000)"),
    ]
    
    profiler.profile_multiple(functions_to_profile)
    
    print("\n" + "="*60)
    print("GENERATING REPORT")
    print("="*60 + "\n")
    profiler.generate_report()
    
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISONS")
    print("="*60 + "\n")
    
    comparison1 = profiler.compare_performance(
        slow_fibonacci, fast_fibonacci,
        (25,), (35,),
        "slow_fibonacci(25)", "fast_fibonacci(35)",
        iterations=5
    )
    profiler.print_comparison(comparison1)
    
    test_data_comp = generate_test_data(200)
    comparison2 = profiler.compare_performance(
        bubble_sort, quick_sort,
        (test_data_comp,), (test_data_comp,),
        "bubble_sort(200)", "quick_sort(200)",
        iterations=3
    )
    profiler.print_comparison(comparison2)
    
    comparison3 = profiler.compare_performance(
        find_primes_naive, find_primes_sieve,
        (1000,), (1000,),
        "find_primes_naive(1000)", "find_primes_sieve(1000)",
        iterations=3
    )
    profiler.print_comparison(comparison3)
    
    comparison4 = profiler.compare_performance(
        string_concat_test, string_join_test,
        (2000,), (2000,),
        "string_concat_test(2000)", "string_join_test(2000)",
        iterations=3
    )
    profiler.print_comparison(comparison4)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("Performance profiling completed!")
    print("  - All functions profiled successfully")
    print("  - Report saved to: output/profile_report.txt")
    print("  - Performance comparisons completed")
    print("="*60 + "\n")


def main():
    try:
        run_profiling()
    except KeyboardInterrupt:
        print("\n\n[INFO] Profiling interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Profiling failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
