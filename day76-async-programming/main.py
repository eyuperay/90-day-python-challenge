#!/usr/bin/env python3
"""
Day 76 - Async Programming
Demonstrates asyncio and aiohttp usage
"""

import os
import json
import asyncio
from datetime import datetime
from async_demo import AsyncDemo


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def save_results(data: dict, filename: str):
    """Save results to JSON file"""
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"[OK] Results saved to: {filepath}")


def main():
    print("=" * 60)
    print("DAY 76 - ASYNC PROGRAMMING")
    print("=" * 60 + "\n")
    
    demo = AsyncDemo()
    
    # ==================== 1. SYNC VS ASYNC ====================
    print_section("1. SYNC VS ASYNC COMPARISON")
    
    sync_async_results = demo.compare_sync_async(8)
    print(f"\nSpeedup: {sync_async_results['speedup']:.2f}x faster")
    save_results(sync_async_results, "sync_async_comparison.json")
    
    # ==================== 2. HTTP REQUESTS ====================
    print_section("2. HTTP REQUESTS")
    
    http_results = demo.demo_http_requests()
    save_results(http_results, "http_requests.json")
    
    # ==================== 3. PARALLEL PROCESSING ====================
    print_section("3. PARALLEL PROCESSING")
    
    parallel_results = demo.demo_parallel_processing(15)
    print(f"\nSpeedup: {parallel_results['speedup']:.2f}x faster")
    save_results(parallel_results, "parallel_processing.json")
    
    # ==================== 4. STREAM PIPELINE ====================
    print_section("4. STREAM PIPELINE")
    
    stream_results = asyncio.run(demo.run_stream_pipeline())
    save_results(stream_results, "stream_pipeline.json")
    
    # ==================== 5. BATCH PROCESSING ====================
    print_section("5. BATCH PROCESSING")
    
    batch_results = demo.demo_batch_processing()
    save_results(batch_results, "batch_processing.json")
    
    # ==================== SUMMARY ====================
    print_section("SUMMARY")
    print("""
Async Programming - Key Concepts:

1. Sync vs Async:
   - Sync: Blocking, sequential execution
   - Async: Non-blocking, concurrent execution

2. Key Components:
   - async def: Define async function
   - await: Wait for async result
   - asyncio.run(): Run async code
   - asyncio.gather(): Run multiple tasks
   - aiohttp: Async HTTP client

3. Benefits:
   - Better performance for I/O operations
   - Concurrent execution
   - Resource efficient
   - Scalable applications

4. Use Cases:
   - HTTP requests
   - Database queries
   - File operations
   - Web scraping
   - API calls
   - Real-time applications

5. Performance Comparison:
   - Sync: Tasks run sequentially
   - Async: Tasks run concurrently
   - Speedup: 2-10x for I/O operations
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for results")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
