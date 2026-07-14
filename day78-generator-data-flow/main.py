#!/usr/bin/env python3
"""
Day 78 - Generator Data Flow
Demonstrates generators for data streaming and processing
"""

import os
import time
import csv
import json
from generators import *
from datetime import datetime


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def save_generator_data(generator, filename: str, max_items: int = 100):
    """Save generator data to JSON file"""
    os.makedirs("output", exist_ok=True)
    data = []
    count = 0
    
    for item in generator:
        data.append(item)
        count += 1
        if count >= max_items:
            break
    
    filepath = f"output/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"[OK] Saved {len(data)} items to: {filepath}")
    return data


def demo_basic_generators():
    """Demonstrate basic generators"""
    print_section("1. BASIC GENERATORS")
    
    print("\nNumber Generator (0-10, step 2):")
    for num in number_generator(0, 10, 2):
        print(f"  {num}", end=" ")
    print()
    
    print("\nFibonacci Generator (first 10):")
    for num in fibonacci_generator(10):
        print(f"  {num}", end=" ")
    print()
    
    print("\nEven Numbers Filter (from 1-10):")
    for num in even_numbers_generator(list(range(1, 11))):
        print(f"  {num}", end=" ")
    print()


def demo_sales_data_generator():
    """Demonstrate sales data generator"""
    print_section("2. SALES DATA GENERATOR")
    
    sales_gen = generate_sales_data(10)
    
    print("\nGenerated 10 sales records:")
    for i, record in enumerate(sales_gen, 1):
        print(f"  {i}. {record['product']} - {record['total']:.2f} TRY ({record['region']})")


def demo_data_pipeline():
    """Demonstrate data processing pipeline"""
    print_section("3. DATA PROCESSING PIPELINE")
    
    # Create pipeline
    sales_gen = generate_sales_data(20)
    filtered_gen = filter_by_status(sales_gen, 'Delivered')
    transformed_gen = transform_total(filtered_gen, tax_rate=0.18)
    
    print("\nPipeline: Sales -> Filter(Delivered) -> Transform(with tax)")
    print("\nResults:")
    
    for i, record in enumerate(transformed_gen, 1):
        print(f"  {i}. {record['product']} - Total: {record['total']:.2f} - With Tax: {record['total_with_tax']:.2f}")
        if i >= 10:
            break


def demo_aggregation():
    """Demonstrate aggregation"""
    print_section("4. AGGREGATION")
    
    sales_gen = generate_sales_data(50)
    aggregated_gen = aggregate_by_category(sales_gen)
    
    print("\nSales by Category:")
    for category in aggregated_gen:
        print(f"  {category['category']}:")
        print(f"    Total Sales: {category['total_sales']:.2f} TRY")
        print(f"    Count: {category['count']}")
        print(f"    Average: {category['average']:.2f} TRY")


def demo_batch_processing():
    """Demonstrate batch processing"""
    print_section("5. BATCH PROCESSING")
    
    data_gen = generate_sales_data(25)
    batch_gen = batch_process(data_gen, batch_size=5)
    
    print("\nProcessing in batches (size 5):")
    for i, batch in enumerate(batch_gen, 1):
        print(f"  Batch {i}: {len(batch)} records")
        for record in batch[:3]:
            print(f"    - {record['product']} - {record['total']:.2f} TRY")
        if len(batch) > 3:
            print(f"    ... and {len(batch)-3} more")


def demo_infinite_counter():
    """Demonstrate infinite counter with limit"""
    print_section("6. INFINITE COUNTER (Limited)")
    
    counter = infinite_counter(0, 3)
    print("\nFirst 10 numbers from infinite counter:")
    for i in range(10):
        print(f"  {next(counter)}", end=" ")
    print()


def demo_progress_generator():
    """Demonstrate progress generator"""
    print_section("7. PROGRESS GENERATOR")
    
    print("\nProcessing with progress:")
    for i in progress_generator(50, "Processing"):
        time.sleep(0.01)  # Simulate work
    print(" Done!")


def demo_file_stream():
    """Demonstrate file streaming"""
    print_section("8. FILE STREAMING")
    
    # Create sample CSV
    os.makedirs("output", exist_ok=True)
    csv_file = "output/sample_data.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'value', 'category'])
        for i in range(20):
            writer.writerow([i+1, f"Item_{i+1}", random.randint(1, 100), random.choice(['A', 'B', 'C'])])
    
    print(f"\nStreaming CSV file: {csv_file}")
    for row in stream_csv_file(csv_file):
        print(f"  {row}")
        # Limit output
        if int(row['id']) >= 5:
            print("  ...")
            break


def demo_random_stream():
    """Demonstrate random stream with limit"""
    print_section("9. RANDOM DATA STREAM (Limited)")
    
    print("\nFirst 5 random data points:")
    stream = random_data_stream(0.1)
    for i in range(5):
        data = next(stream)
        print(f"  {i+1}. Value: {data['value']:.2f}, Category: {data['category']}, Status: {data['status']}")


def demo_web_log_stream():
    """Demonstrate web log stream with limit"""
    print_section("10. WEB LOG STREAM (Limited)")
    
    print("\nFirst 5 web log entries:")
    logs = web_log_stream()
    for i in range(5):
        log = next(logs)
        print(f"  {i+1}. {log['ip']} - {log['method']} {log['url']} - {log['status']}")


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
Generator Data Flow - Key Concepts:

1. What are Generators?
   - Functions that yield values one at a time
   - Memory efficient for large data
   - Lazy evaluation

2. Generator Benefits:
   - Memory efficient
   - Stream processing
   - Lazy evaluation
   - Pipeline building
   - Infinite sequences

3. Use Cases:
   - Large file processing
   - Data streaming
   - API pagination
   - Real-time data
   - Batch processing

4. Generator Types:
   - Basic generators (yield)
   - Infinite generators (while True)
   - Pipeline generators (chaining)
   - File stream generators

5. When to Use:
   - Large datasets
   - Streaming data
   - Memory constraints
   - Real-time processing
   - Data pipelines
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 78 - GENERATOR DATA FLOW")
    print("=" * 60 + "\n")
    
    demo_basic_generators()
    demo_sales_data_generator()
    demo_data_pipeline()
    demo_aggregation()
    demo_batch_processing()
    demo_infinite_counter()
    demo_progress_generator()
    demo_file_stream()
    demo_random_stream()
    demo_web_log_stream()
    
    print_summary()


if __name__ == "__main__":
    main()
