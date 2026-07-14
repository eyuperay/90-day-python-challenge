#!/usr/bin/env python3
"""
Day 80 - Iterable and Iterator
Demonstrates custom iterable and iterator classes
"""

from iterables import *
import json
import os


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_countdown():
    """Demonstrate CountDown iterable"""
    print_section("1. COUNTDOWN ITERABLE")
    
    print("\nCountdown from 5:")
    for i in CountDown(5):
        print(f"  {i}", end=" ")
    print()


def demo_custom_range():
    """Demonstrate custom Range iterable"""
    print_section("2. CUSTOM RANGE ITERABLE")
    
    print("\nRange(0, 10, 2):")
    for i in Range(0, 10, 2):
        print(f"  {i}", end=" ")
    print()
    
    print("\nRange(5, 15, 3):")
    for i in Range(5, 15, 3):
        print(f"  {i}", end=" ")
    print()


def demo_fibonacci():
    """Demonstrate Fibonacci iterable"""
    print_section("3. FIBONACCI ITERABLE")
    
    print("\nFirst 10 Fibonacci numbers:")
    for num in Fibonacci(10):
        print(f"  {num}", end=" ")
    print()


def demo_primes():
    """Demonstrate PrimeNumbers iterable"""
    print_section("4. PRIME NUMBER ITERABLE")
    
    print("\nFirst 10 prime numbers:")
    for prime in PrimeNumbers(10):
        print(f"  {prime}", end=" ")
    print()


def demo_paginated():
    """Demonstrate PaginatedData iterable"""
    print_section("5. PAGINATED DATA ITERABLE")
    
    paginated = PaginatedData(3, 5)
    print("\nPaginated data:")
    for page in paginated:
        print(f"  Page {page['page']}/{page['total_pages']}:")
        for item in page['items']:
            print(f"    - {item}")


def demo_infinite_counter():
    """Demonstrate InfiniteCounter iterable"""
    print_section("6. INFINITE COUNTER")
    
    counter = InfiniteCounter(0, 2)
    print("\nFirst 10 numbers from infinite counter:")
    for i, num in enumerate(counter):
        if i >= 10:
            break
        print(f"  {num}", end=" ")
    print()


def demo_random_stream():
    """Demonstrate RandomStream iterable"""
    print_section("7. RANDOM DATA STREAM")
    
    stream = RandomStream(0, 100)
    print("\nFirst 5 random numbers:")
    for i, num in enumerate(stream):
        if i >= 5:
            break
        print(f"  {num:.2f}", end=" ")
    print()


def demo_chunk_iterator():
    """Demonstrate ChunkIterator"""
    print_section("8. CHUNK ITERATOR")
    
    data = list(range(1, 21))
    print(f"\nData: {data}")
    
    print("\nChunks of 4:")
    for chunk in ChunkIterator(data, 4):
        print(f"  {chunk}")


def demo_tree_iterator():
    """Demonstrate TreeIterator"""
    print_section("9. TREE ITERATOR")
    
    # Build a tree
    root = TreeNode("Root")
    child1 = TreeNode("Child 1")
    child2 = TreeNode("Child 2")
    child3 = TreeNode("Child 3")
    
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(TreeNode("Grandchild 1.1"))
    child1.add_child(TreeNode("Grandchild 1.2"))
    child2.add_child(TreeNode("Grandchild 2.1"))
    
    print("\nTree traversal (depth-first):")
    for node in TreeIterator(root):
        print(f"  {node}")


def demo_zip_iterator():
    """Demonstrate ZipIterator"""
    print_section("10. ZIP ITERATOR")
    
    names = ["Alice", "Bob", "Charlie", "Diana"]
    ages = [25, 30, 35, 28]
    cities = ["Istanbul", "Ankara", "Izmir", "Bursa"]
    
    print(f"\nNames: {names}")
    print(f"Ages: {ages}")
    print(f"Cities: {cities}")
    
    print("\nZipped data:")
    for name, age, city in ZipIterator(names, ages, cities):
        print(f"  {name}, {age}, {city}")


def demo_iterable_check():
    """Demonstrate iterable utility functions"""
    print_section("11. ITERABLE UTILITIES")
    
    test_objects = [
        [1, 2, 3],
        "Hello",
        123,
        {"a": 1, "b": 2},
        (1, 2, 3),
        CountDown(3)
    ]
    
    print("\nChecking if objects are iterable:")
    for obj in test_objects:
        is_iter = is_iterable(obj)
        print(f"  {type(obj).__name__}: {is_iter}")


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
Iterable and Iterator - Key Concepts:

1. Iterable:
   - Object that can be iterated over
   - Implements __iter__() method
   - Returns an iterator

2. Iterator:
   - Object that produces values
   - Implements __iter__() and __next__()
   - Raises StopIteration when done

3. Creating Iterables:
   - Class with __iter__() method
   - Can use yield (generator)
   - Return self as iterator

4. Creating Iterators:
   - Class with __iter__() and __next__()
   - Track state with instance variables
   - Raise StopIteration at end

5. Common Patterns:
   - Data streaming
   - Infinite sequences
   - Pagination
   - Tree traversal
   - Lazy evaluation

6. Benefits:
   - Memory efficient
   - Clean code
   - Lazy evaluation
   - Reusable components
   - Custom iteration logic
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 80 - ITERABLE AND ITERATOR")
    print("=" * 60 + "\n")
    
    demo_countdown()
    demo_custom_range()
    demo_fibonacci()
    demo_primes()
    demo_paginated()
    demo_infinite_counter()
    demo_random_stream()
    demo_chunk_iterator()
    demo_tree_iterator()
    demo_zip_iterator()
    demo_iterable_check()
    
    print_summary()


if __name__ == "__main__":
    main()
