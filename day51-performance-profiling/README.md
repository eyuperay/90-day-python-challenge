# Day 51 - Performance Profiling

## About This Project
This project demonstrates performance profiling in Python using `cProfile` and `pstats`. It compares different algorithm implementations and identifies performance bottlenecks.

## Features
- Profile functions with cProfile
- Generate detailed performance reports
- Compare algorithm performance
- Identify slow functions
- Optimize code based on profiling results

## Functions Profiled
### Fibonacci
- `slow_fibonacci` - Recursive (O(2^n))
- `fast_fibonacci` - Iterative (O(n))

### Sorting
- `bubble_sort` - O(n^2)
- `quick_sort` - O(n log n)

### Prime Numbers
- `find_primes_naive` - O(n * sqrt(n))
- `find_primes_sieve` - O(n log log n)

### String Operations
- `string_concat_test` - Using + operator
- `string_join_test` - Using join()

### List Operations
- `list_append_test` - Using append
- `list_comprehension_test` - Using comprehension

## Usage

### 1. Run the program
python main.py

### 2. Check the report
cat output/profile_report.txt

## Performance Metrics
- **Total Time**: Time spent in function
- **Cumulative Time**: Time including sub-functions
- **Call Count**: Number of calls
- **Time per Call**: Average time per call

## Profiling Tools in Python
- **cProfile** - Built-in profiler
- **pstats** - Statistics analysis
- **line_profiler** - Line-by-line profiling
- **memory_profiler** - Memory usage profiling

## Learning Objectives
- Using cProfile for performance analysis
- Understanding performance bottlenecks
- Comparing algorithm efficiency
- Optimizing Python code
- Using pstats for report generation
