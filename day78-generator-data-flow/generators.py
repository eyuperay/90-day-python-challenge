"""
Generator Functions Module
Various generator examples for data streaming
"""

import time
import random
import csv
import json
import os
from typing import Generator, List, Dict, Any
from datetime import datetime, timedelta


# ==================== BASIC GENERATORS ====================

def number_generator(start: int = 0, end: int = 10, step: int = 1) -> Generator[int, None, None]:
    """
    Generate numbers from start to end with step
    
    Yields:
        Numbers one by one
    """
    current = start
    while current < end:
        yield current
        current += step


def fibonacci_generator(limit: int = 10) -> Generator[int, None, None]:
    """
    Generate Fibonacci sequence
    
    Yields:
        Fibonacci numbers one by one
    """
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1


def even_numbers_generator(numbers: List[int]) -> Generator[int, None, None]:
    """
    Filter even numbers from a list
    
    Yields:
        Even numbers only
    """
    for num in numbers:
        if num % 2 == 0:
            yield num


# ==================== DATA STREAM GENERATORS ====================

def generate_sales_data(count: int = 100) -> Generator[Dict[str, Any], None, None]:
    """
    Generate sample sales data
    
    Yields:
        Sales records one by one
    """
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Printer', 'Scanner', 'Tablet', 'Phone']
    categories = ['Electronics', 'Accessories', 'Computers', 'Office']
    regions = ['North', 'South', 'East', 'West', 'Central']
    statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
    
    for i in range(count):
        product = random.choice(products)
        price = round(random.uniform(50, 2000), 2)
        quantity = random.randint(1, 20)
        
        yield {
            'id': i + 1,
            'product': product,
            'category': random.choice(categories),
            'region': random.choice(regions),
            'price': price,
            'quantity': quantity,
            'total': round(price * quantity, 2),
            'date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'status': random.choice(statuses)
        }


def generate_large_data_chunks(chunk_size: int = 1000, total_items: int = 10000) -> Generator[List[Dict], None, None]:
    """
    Generate data in chunks for memory efficiency
    
    Yields:
        Chunks of data
    """
    chunk = []
    for i in range(total_items):
        chunk.append({
            'id': i + 1,
            'value': random.randint(1, 1000),
            'category': random.choice(['A', 'B', 'C']),
            'timestamp': datetime.now().isoformat()
        })
        
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    
    if chunk:
        yield chunk


# ==================== FILE STREAM GENERATORS ====================

def stream_csv_file(filename: str, delimiter: str = ',') -> Generator[Dict[str, Any], None, None]:
    """
    Stream CSV file line by line
    
    Yields:
        CSV rows as dictionaries
    """
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            yield row


def stream_json_file(filename: str) -> Generator[Dict[str, Any], None, None]:
    """
    Stream JSON file (assuming array of objects)
    
    Yields:
        JSON objects one by one
    """
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            for item in data:
                yield item


# ==================== PROCESSING PIPELINE GENERATORS ====================

def filter_by_status(data_generator: Generator, status: str) -> Generator[Dict, None, None]:
    """
    Filter data by status
    
    Yields:
        Items with matching status
    """
    for item in data_generator:
        if item.get('status') == status:
            yield item


def filter_by_region(data_generator: Generator, region: str) -> Generator[Dict, None, None]:
    """
    Filter data by region
    
    Yields:
        Items from matching region
    """
    for item in data_generator:
        if item.get('region') == region:
            yield item


def transform_total(data_generator: Generator, tax_rate: float = 0.18) -> Generator[Dict, None, None]:
    """
    Add tax to total field
    
    Yields:
        Items with tax added
    """
    for item in data_generator:
        if 'total' in item:
            item['total_with_tax'] = round(item['total'] * (1 + tax_rate), 2)
        yield item


def aggregate_by_category(data_generator: Generator) -> Generator[Dict, None, None]:
    """
    Aggregate data by category
    
    Yields:
        Category totals
    """
    totals = {}
    counts = {}
    
    for item in data_generator:
        category = item.get('category', 'Unknown')
        if category not in totals:
            totals[category] = 0
            counts[category] = 0
        totals[category] += item.get('total', 0)
        counts[category] += 1
    
    for category in totals:
        yield {
            'category': category,
            'total_sales': round(totals[category], 2),
            'count': counts[category],
            'average': round(totals[category] / counts[category], 2)
        }


def batch_process(data_generator: Generator, batch_size: int = 10) -> Generator[List[Dict], None, None]:
    """
    Process data in batches
    
    Yields:
        Batches of items
    """
    batch = []
    for item in data_generator:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    if batch:
        yield batch


# ==================== INFINITE GENERATORS ====================

def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """
    Infinite counter generator
    
    Yields:
        Numbers forever
    """
    current = start
    while True:
        yield current
        current += step


def random_data_stream(interval: float = 1.0) -> Generator[Dict, None, None]:
    """
    Continuous random data stream
    
    Yields:
        Random data points
    """
    while True:
        yield {
            'timestamp': datetime.now().isoformat(),
            'value': random.random() * 100,
            'category': random.choice(['A', 'B', 'C']),
            'status': random.choice(['OK', 'WARNING', 'ERROR'])
        }
        time.sleep(interval)


def web_log_stream() -> Generator[Dict, None, None]:
    """
    Simulate web log stream
    
    Yields:
        Web log entries
    """
    ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '192.168.1.103']
    urls = ['/home', '/about', '/products', '/contact', '/api/data']
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    statuses = [200, 200, 200, 301, 404, 500]
    
    counter = 0
    while True:
        yield {
            'id': counter + 1,
            'ip': random.choice(ips),
            'method': random.choice(methods),
            'url': random.choice(urls),
            'status': random.choice(statuses),
            'size': random.randint(100, 5000),
            'timestamp': datetime.now().isoformat()
        }
        counter += 1
        time.sleep(0.1)


# ==================== UTILITY GENERATORS ====================

def progress_generator(total: int, label: str = "Progress") -> Generator[int, None, None]:
    """
    Generator with progress tracking
    
    Yields:
        Progress percentage
    """
    for i in range(total + 1):
        progress = int((i / total) * 100)
        if i == 0 or progress % 10 == 0 or i == total:
            print(f"\r{label}: {progress}%", end="")
        yield i
    print()


def pipeline_processor(generators: List[Generator]) -> Generator[Any, None, None]:
    """
    Chain multiple generators together
    
    Yields:
        Processed data through pipeline
    """
    current_generator = generators[0] if generators else None
    if not current_generator:
        return
    
    # Chain generators
    for gen in generators[1:]:
        current_generator = gen(current_generator)
    
    yield from current_generator
