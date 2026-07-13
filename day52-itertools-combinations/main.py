#!/usr/bin/env python3
"""
Day 52 - Itertools Combinations
Demonstrates itertools functions for data combinations
"""

import time
from itertools_demo import ItertoolsDemo


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 52 - ITERTOOLS COMBINATIONS")
    print("=" * 60 + "\n")
    
    demo = ItertoolsDemo()
    
    # ==================== COMBINATIONS ====================
    print_section("1. COMBINATIONS")
    
    items = ['A', 'B', 'C', 'D']
    print(f"Items: {items}")
    
    # Basic combinations
    print(f"\nCombinations of length 2:")
    combos = demo.combinations_basic(items, 2)
    for c in combos:
        print(f"  {c}")
    print(f"Total: {len(combos)}")
    
    # Combinations with replacement
    print(f"\nCombinations with replacement (length 2):")
    combos_wr = demo.combinations_with_replacement(items, 2)
    for c in combos_wr:
        print(f"  {c}")
    print(f"Total: {len(combos_wr)}")
    
    # ==================== PERMUTATIONS ====================
    print_section("2. PERMUTATIONS")
    
    print(f"Items: {items}")
    
    print(f"\nPermutations of length 2:")
    perms = demo.permutations_basic(items, 2)
    for p in perms[:10]:
        print(f"  {p}")
    if len(perms) > 10:
        print(f"  ... and {len(perms) - 10} more")
    print(f"Total: {len(perms)}")
    
    print(f"\nAll permutations (length {len(items)}):")
    perms_all = demo.permutations_basic(items)
    print(f"Total: {len(perms_all)}")
    
    # ==================== CARTESIAN PRODUCT ====================
    print_section("3. CARTESIAN PRODUCT")
    
    list1 = ['A', 'B']
    list2 = [1, 2]
    list3 = ['X', 'Y']
    
    print(f"List 1: {list1}")
    print(f"List 2: {list2}")
    print(f"List 3: {list3}")
    
    product = demo.cartesian_product(list1, list2, list3)
    print(f"\nCartesian product:")
    for p in product:
        print(f"  {p}")
    print(f"Total: {len(product)}")
    
    # ==================== INFINITE ITERATORS ====================
    print_section("4. INFINITE ITERATORS")
    
    print("count(start=5, step=2) - first 10:")
    print(f"  {demo.count_demo(5, 2, 10)}")
    
    print("cycle(['A', 'B', 'C']) - first 10:")
    print(f"  {demo.cycle_demo(['A', 'B', 'C'], 10)}")
    
    print("repeat('Hello', 5):")
    print(f"  {demo.repeat_demo('Hello', 5)}")
    
    # ==================== CHAINING ====================
    print_section("5. CHAINING")
    
    list_a = [1, 2, 3]
    list_b = ['a', 'b', 'c']
    list_c = ['X', 'Y', 'Z']
    
    print(f"List A: {list_a}")
    print(f"List B: {list_b}")
    print(f"List C: {list_c}")
    
    chained = demo.chain_demo(list_a, list_b, list_c)
    print(f"Chained: {chained}")
    
    list_of_lists = [[1, 2], [3, 4], [5, 6]]
    print(f"List of lists: {list_of_lists}")
    chained_from_iter = demo.chain_from_iterable_demo(list_of_lists)
    print(f"Chained from iterable: {chained_from_iter}")
    
    # ==================== FILTERING ====================
    print_section("6. FILTERING")
    
    data = ['A', 'B', 'C', 'D', 'E']
    selectors = [True, False, True, False, True]
    
    print(f"Data: {data}")
    print(f"Selectors: {selectors}")
    compressed = demo.compress_demo(data, selectors)
    print(f"Compressed: {compressed}")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"\nNumbers: {numbers}")
    print(f"Drop while < 5: {demo.dropwhile_demo(lambda x: x < 5, numbers)}")
    print(f"Take while < 5: {demo.takewhile_demo(lambda x: x < 5, numbers)}")
    
    # ==================== GROUPING ====================
    print_section("7. GROUPING")
    
    data = ['apple', 'banana', 'apricot', 'blueberry', 'avocado']
    print(f"Data: {data}")
    print(f"Grouped by first letter:")
    grouped = demo.groupby_demo(data, key_func=lambda x: x[0])
    for key, group in grouped.items():
        print(f"  {key}: {group}")
    
    # ==================== REAL-WORLD SCENARIOS ====================
    print_section("8. REAL-WORLD SCENARIOS")
    
    # Product catalog
    demo.product_catalog_scenario()
    
    # Menu combinations
    demo.menu_combo_scenario()
    
    # Lottery combinations
    demo.lottery_combinations_scenario()
    
    # Team formation
    demo.team_formation_scenario()
    
    # ==================== SUMMARY ====================
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("All itertools functions demonstrated successfully!")
    print("\nFunctions used:")
    print("  - combinations() - Order doesn't matter, no repetition")
    print("  - combinations_with_replacement() - Order doesn't matter, repetition allowed")
    print("  - permutations() - Order matters, no repetition")
    print("  - product() - Cartesian product of multiple lists")
    print("  - count() - Infinite counter")
    print("  - cycle() - Infinite cycle through items")
    print("  - repeat() - Repeat items")
    print("  - chain() - Chain multiple iterables")
    print("  - compress() - Filter with selectors")
    print("  - dropwhile() - Drop while condition is true")
    print("  - takewhile() - Take while condition is true")
    print("  - groupby() - Group items by key")
    print("="*60 + "\n")
    
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
