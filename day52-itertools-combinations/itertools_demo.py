"""
Itertools Demo - Combinations, Permutations, and Products
Demonstrates various itertools functions for data combinations
"""

import itertools
import math
import time
from typing import List, Tuple, Any, Dict


class ItertoolsDemo:
    """Demonstrates itertools functions for combinations"""
    
    def __init__(self):
        self.results = {}
    
    # ==================== COMBINATIONS ====================
    
    def combinations_basic(self, items: List, r: int) -> List[Tuple]:
        """
        combinations: Returns all possible combinations of length r
        Order does NOT matter, no repetition
        Example: combinations('ABC', 2) -> AB, AC, BC
        """
        return list(itertools.combinations(items, r))
    
    def combinations_with_replacement(self, items: List, r: int) -> List[Tuple]:
        """
        combinations_with_replacement: Returns combinations with repetition
        Order does NOT matter, repetition allowed
        Example: combinations_with_replacement('ABC', 2) -> AA, AB, AC, BB, BC, CC
        """
        return list(itertools.combinations_with_replacement(items, r))
    
    # ==================== PERMUTATIONS ====================
    
    def permutations_basic(self, items: List, r: int = None) -> List[Tuple]:
        """
        permutations: Returns all possible permutations of length r
        Order matters, no repetition
        Example: permutations('ABC', 2) -> AB, AC, BA, BC, CA, CB
        """
        if r is None:
            r = len(items)
        return list(itertools.permutations(items, r))
    
    # ==================== CARTESIAN PRODUCT ====================
    
    def cartesian_product(self, *lists) -> List[Tuple]:
        """
        product: Returns Cartesian product of multiple lists
        Example: product('AB', '12') -> A1, A2, B1, B2
        """
        return list(itertools.product(*lists))
    
    # ==================== INFINITE ITERATORS ====================
    
    def count_demo(self, start: int = 0, step: int = 1, limit: int = 10) -> List[int]:
        """
        count: Infinite counter starting from start
        """
        return list(itertools.islice(itertools.count(start, step), limit))
    
    def cycle_demo(self, items: List, limit: int = 10) -> List:
        """
        cycle: Cycles through items infinitely
        """
        return list(itertools.islice(itertools.cycle(items), limit))
    
    def repeat_demo(self, item: Any, times: int = 5) -> List:
        """
        repeat: Repeats item n times
        """
        return list(itertools.repeat(item, times))
    
    # ==================== CHAINING ====================
    
    def chain_demo(self, *lists) -> List:
        """
        chain: Chains multiple iterables together
        """
        return list(itertools.chain(*lists))
    
    def chain_from_iterable_demo(self, list_of_lists: List) -> List:
        """
        chain.from_iterable: Chains from a list of iterables
        """
        return list(itertools.chain.from_iterable(list_of_lists))
    
    # ==================== FILTERING ====================
    
    def compress_demo(self, data: List, selectors: List) -> List:
        """
        compress: Filters data based on selectors (True/False)
        """
        return list(itertools.compress(data, selectors))
    
    def dropwhile_demo(self, predicate, iterable) -> List:
        """
        dropwhile: Drops elements while predicate is True
        """
        return list(itertools.dropwhile(predicate, iterable))
    
    def takewhile_demo(self, predicate, iterable) -> List:
        """
        takewhile: Takes elements while predicate is True
        """
        return list(itertools.takewhile(predicate, iterable))
    
    # ==================== GROUPING ====================
    
    def groupby_demo(self, data: List, key_func=None) -> Dict:
        """
        groupby: Groups elements by key function
        """
        if key_func is None:
            key_func = lambda x: x
        
        result = {}
        data_sorted = sorted(data, key=key_func)
        
        for key, group in itertools.groupby(data_sorted, key_func):
            result[key] = list(group)
        
        return result
    
    # ==================== ADVANCED ====================
    
    def product_with_conditions(self, *lists, condition=None) -> List[Tuple]:
        """
        product with a condition filter
        """
        result = list(itertools.product(*lists))
        if condition:
            return [item for item in result if condition(item)]
        return result
    
    def combinations_with_filter(self, items: List, r: int, filter_func=None) -> List[Tuple]:
        """
        combinations with a filter function
        """
        result = list(itertools.combinations(items, r))
        if filter_func:
            return [item for item in result if filter_func(item)]
        return result
    
    # ==================== SCENARIOS ====================
    
    def product_catalog_scenario(self):
        """
        Scenario: Product catalog combinations
        """
        sizes = ['S', 'M', 'L', 'XL']
        colors = ['Red', 'Blue', 'Green', 'Black']
        materials = ['Cotton', 'Polyester', 'Wool']
        
        print("\n" + "-"*40)
        print("PRODUCT CATALOG COMBINATIONS")
        print("-"*40)
        
        # All possible product variations
        products = list(itertools.product(sizes, colors, materials))
        print(f"Total product variations: {len(products)}")
        
        # Show first 10
        for i, (size, color, material) in enumerate(products[:10], 1):
            print(f"  {i}. {size} - {color} - {material}")
        
        if len(products) > 10:
            print(f"  ... and {len(products) - 10} more")
        
        return products
    
    def menu_combo_scenario(self):
        """
        Scenario: Menu combination calculator
        """
        appetizers = ['Salad', 'Soup', 'Bruschetta']
        mains = ['Pasta', 'Steak', 'Fish', 'Chicken']
        desserts = ['Cake', 'Ice Cream', 'Fruit']
        drinks = ['Water', 'Soda', 'Juice', 'Wine']
        
        print("\n" + "-"*40)
        print("MENU COMBINATION CALCULATOR")
        print("-"*40)
        
        # Total possible meal combinations
        total = len(appetizers) * len(mains) * len(desserts) * len(drinks)
        print(f"Total possible meal combinations: {total}")
        
        # Show sample combos
        combos = list(itertools.product(
            appetizers[:2], mains[:2], desserts[:2], drinks[:2]
        ))
        
        print("\nSample meal combinations:")
        for i, (app, main, dessert, drink) in enumerate(combos[:5], 1):
            print(f"  {i}. {app} + {main} + {dessert} + {drink}")
        
        return total
    
    def lottery_combinations_scenario(self):
        """
        Scenario: Lottery number combinations
        """
        numbers = list(range(1, 50))  # 1-49
        picks = 6
        
        print("\n" + "-"*40)
        print("LOTTERY COMBINATIONS CALCULATOR")
        print("-"*40)
        
        # Number of possible combinations
        total = math.comb(len(numbers), picks)
        print(f"Total possible 6-number combinations from 1-49: {total:,}")
        print(f"(This would take {total/1000000:.0f} million tickets!)")
        
        # Show some random combos using islice
        print("\nSample lottery combinations:")
        combos = itertools.combinations(numbers, picks)
        
        for i, combo in enumerate(itertools.islice(combos, 10), 1):
            print(f"  {i}. {combo}")
        
        return total
    
    def team_formation_scenario(self):
        """
        Scenario: Team formation combinations
        """
        players = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
        team_size = 3
        
        print("\n" + "-"*40)
        print("TEAM FORMATION CALCULATOR")
        print("-"*40)
        
        # All possible teams
        teams = list(itertools.combinations(players, team_size))
        print(f"Total possible teams of {team_size} from {len(players)} players: {len(teams)}")
        
        print("\nSample teams:")
        for i, team in enumerate(teams[:10], 1):
            print(f"  {i}. {', '.join(team)}")
        
        if len(teams) > 10:
            print(f"  ... and {len(teams) - 10} more teams")
        
        return teams
