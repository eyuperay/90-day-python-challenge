"""
Iterable and Iterator Examples
Custom iterable and iterator classes
"""

import math
import random
from typing import Any, List, Iterator, Optional


# ==================== BASIC ITERABLE ====================

class CountDown:
    """
    CountDown iterable - counts down from a number to 0
    
    Usage:
        for i in CountDown(5):
            print(i)  # 5, 4, 3, 2, 1, 0
    """
    
    def __init__(self, start: int):
        self.start = start
    
    def __iter__(self):
        return CountDownIterator(self.start)


class CountDownIterator:
    """Iterator for CountDown"""
    
    def __init__(self, start: int):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# ==================== SIMPLE ITERABLE ====================

class Range:
    """
    Custom range iterable
    
    Usage:
        for i in Range(0, 10, 2):
            print(i)  # 0, 2, 4, 6, 8
    """
    
    def __init__(self, start: int, stop: int, step: int = 1):
        self.start = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += self.step


# ==================== FIBONACCI ITERABLE ====================

class Fibonacci:
    """
    Fibonacci sequence iterable
    
    Usage:
        for num in Fibonacci(10):
            print(num)  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    """
    
    def __init__(self, limit: int):
        self.limit = limit
    
    def __iter__(self):
        a, b = 0, 1
        count = 0
        while count < self.limit:
            yield a
            a, b = b, a + b
            count += 1


# ==================== PRIME NUMBER ITERABLE ====================

class PrimeNumbers:
    """
    Prime number generator iterable
    
    Usage:
        for prime in PrimeNumbers(10):
            print(prime)  # 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
    """
    
    def __init__(self, count: int):
        self.count = count
    
    def __iter__(self):
        return PrimeIterator(self.count)


class PrimeIterator:
    """Iterator for PrimeNumbers"""
    
    def __init__(self, count: int):
        self.count = count
        self.generated = 0
        self.current = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        
        while True:
            self.current += 1
            if self._is_prime(self.current):
                self.generated += 1
                return self.current
    
    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True


# ==================== PAGINATED DATA ITERABLE ====================

class PaginatedData:
    """
    Simulates paginated API data
    
    Usage:
        for page in PaginatedData(3, 5):
            print(page)  # Page 1, Page 2, Page 3
    """
    
    def __init__(self, total_pages: int, items_per_page: int):
        self.total_pages = total_pages
        self.items_per_page = items_per_page
        self.data = self._generate_data()
    
    def _generate_data(self):
        """Generate sample data"""
        return [f"Item_{i+1}" for i in range(self.total_pages * self.items_per_page)]
    
    def __iter__(self):
        return PaginatedIterator(self.data, self.items_per_page)


class PaginatedIterator:
    """Iterator for PaginatedData"""
    
    def __init__(self, data: List[str], items_per_page: int):
        self.data = data
        self.items_per_page = items_per_page
        self.current_page = 0
        self.total_pages = (len(data) + items_per_page - 1) // items_per_page
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_page >= self.total_pages:
            raise StopIteration
        
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data[start:end]
        self.current_page += 1
        
        return {
            'page': self.current_page,
            'total_pages': self.total_pages,
            'items': page_data,
            'total_items': len(self.data)
        }


# ==================== INFINITE ITERABLE ====================

class InfiniteCounter:
    """
    Infinite counter iterable
    
    Usage:
        counter = InfiniteCounter()
        for i in counter:
            if i > 10:
                break
            print(i)  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    """
    
    def __init__(self, start: int = 0, step: int = 1):
        self.start = start
        self.step = step
    
    def __iter__(self):
        current = self.start
        while True:
            yield current
            current += self.step


# ==================== RANDOM STREAM ITERABLE ====================

class RandomStream:
    """
    Infinite random data stream iterable
    
    Usage:
        stream = RandomStream()
        for i, data in enumerate(stream):
            if i >= 5:
                break
            print(data)
    """
    
    def __init__(self, min_val: float = 0, max_val: float = 100):
        self.min_val = min_val
        self.max_val = max_val
    
    def __iter__(self):
        while True:
            yield random.uniform(self.min_val, self.max_val)


# ==================== FILE LINE ITERABLE ====================

class FileLines:
    """
    Lazy file line reader iterable
    
    Usage:
        for line in FileLines('data.txt'):
            print(line)
    """
    
    def __init__(self, filename: str):
        self.filename = filename
    
    def __iter__(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()


# ==================== CHUNK ITERABLE ====================

class ChunkIterator:
    """
    Iterates over data in chunks
    
    Usage:
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for chunk in ChunkIterator(data, 3):
            print(chunk)  # [1,2,3], [4,5,6], [7,8,9], [10]
    """
    
    def __init__(self, data: List[Any], chunk_size: int):
        self.data = data
        self.chunk_size = chunk_size
        self.position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.position >= len(self.data):
            raise StopIteration
        
        chunk = self.data[self.position:self.position + self.chunk_size]
        self.position += self.chunk_size
        return chunk


# ==================== TREE ITERABLE ====================

class TreeNode:
    """Simple tree node for tree traversal"""
    
    def __init__(self, value: Any, children: List['TreeNode'] = None):
        self.value = value
        self.children = children or []
    
    def add_child(self, child: 'TreeNode'):
        self.children.append(child)


class TreeIterator:
    """
    Depth-first tree traversal iterable
    
    Usage:
        tree = TreeIterator(root)
        for node in tree:
            print(node.value)
    """
    
    def __init__(self, root: TreeNode):
        self.root = root
    
    def __iter__(self):
        return self._traverse(self.root)
    
    def _traverse(self, node: TreeNode):
        yield node.value
        for child in node.children:
            yield from self._traverse(child)


# ==================== ZIP ITERATOR ====================

class ZipIterator:
    """
    Custom zip iterator
    
    Usage:
        for a, b in ZipIterator([1,2,3], ['a','b','c']):
            print(a, b)  # (1,'a'), (2,'b'), (3,'c')
    """
    
    def __init__(self, *iterables):
        self.iterables = [iter(it) for it in iterables]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        values = []
        for it in self.iterables:
            try:
                values.append(next(it))
            except StopIteration:
                raise StopIteration
        return tuple(values)


# ==================== UTILITY FUNCTIONS ====================

def is_iterable(obj) -> bool:
    """Check if an object is iterable"""
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def get_iterator(obj) -> Optional[Iterator]:
    """Get iterator from an object"""
    try:
        return iter(obj)
    except TypeError:
        return None


def consume_iterator(iterator: Iterator, count: int = None) -> List[Any]:
    """Consume iterator and return items"""
    result = []
    try:
        if count is None:
            result = list(iterator)
        else:
            for _ in range(count):
                result.append(next(iterator))
    except StopIteration:
        pass
    return result
