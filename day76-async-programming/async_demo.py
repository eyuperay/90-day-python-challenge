"""
Async Programming Demo
Demonstrates asyncio and aiohttp usage
"""

import asyncio
import aiohttp
import time
import random
import json
from datetime import datetime
from typing import List, Dict, Any


class AsyncDemo:
    """Async programming demonstrations"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    # ==================== SYNC VS ASYNC ====================
    
    def sync_task(self, task_id: int, duration: float = 1.0) -> str:
        """Synchronous task"""
        time.sleep(duration)
        return f"Task {task_id} completed in {duration}s"
    
    async def async_task(self, task_id: int, duration: float = 1.0) -> str:
        """Asynchronous task"""
        await asyncio.sleep(duration)
        return f"Task {task_id} completed in {duration}s"
    
    def run_sync_tasks(self, count: int = 5) -> List[str]:
        """Run tasks synchronously"""
        self.start_time = time.time()
        results = []
        for i in range(count):
            duration = random.uniform(0.5, 2.0)
            result = self.sync_task(i, duration)
            results.append(result)
        self.end_time = time.time()
        return results
    
    async def run_async_tasks(self, count: int = 5) -> List[str]:
        """Run tasks asynchronously"""
        self.start_time = time.time()
        tasks = []
        for i in range(count):
            duration = random.uniform(0.5, 2.0)
            tasks.append(self.async_task(i, duration))
        results = await asyncio.gather(*tasks)
        self.end_time = time.time()
        return results
    
    def compare_sync_async(self, count: int = 5) -> Dict[str, Any]:
        """Compare sync vs async performance"""
        print(f"\nComparing {count} tasks (sync vs async):")
        print("-" * 50)
        
        # Sync
        sync_results = self.run_sync_tasks(count)
        sync_time = self.end_time - self.start_time
        print(f"Sync: {sync_time:.2f}s")
        
        # Async
        async_results = asyncio.run(self.run_async_tasks(count))
        async_time = self.end_time - self.start_time
        print(f"Async: {async_time:.2f}s")
        
        return {
            "sync_time": sync_time,
            "async_time": async_time,
            "speedup": sync_time / async_time if async_time > 0 else 0,
            "sync_results": sync_results,
            "async_results": async_results
        }
    
    # ==================== HTTP REQUESTS ====================
    
    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch a URL asynchronously"""
        try:
            start = time.time()
            async with session.get(url, timeout=10) as response:
                status = response.status
                content_length = len(await response.text())
                elapsed = time.time() - start
                return {
                    "url": url,
                    "status": status,
                    "content_length": content_length,
                    "time": elapsed,
                    "success": status == 200
                }
        except Exception as e:
            return {
                "url": url,
                "status": 0,
                "content_length": 0,
                "time": 0,
                "success": False,
                "error": str(e)
            }
    
    async def fetch_multiple_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch multiple URLs asynchronously"""
        self.start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
        self.end_time = time.time()
        return results
    
    def fetch_urls_sync(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch URLs synchronously using requests (simulated)"""
        # This is a simulation - in reality we would use requests library
        print("Simulating sync requests...")
        results = []
        self.start_time = time.time()
        for url in urls:
            # Simulate network delay
            time.sleep(random.uniform(0.5, 1.5))
            results.append({
                "url": url,
                "status": 200,
                "content_length": random.randint(1000, 5000),
                "time": random.uniform(0.5, 1.5),
                "success": True
            })
        self.end_time = time.time()
        return results
    
    def demo_http_requests(self) -> Dict[str, Any]:
        """Demonstrate async HTTP requests"""
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent",
            "https://httpbin.org/headers",
            "https://httpbin.org/status/200",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/3"
        ]
        
        print(f"\nFetching {len(urls)} URLs:")
        print("-" * 50)
        
        # Async
        print("\nAsync fetching...")
        async_results = asyncio.run(self.fetch_multiple_urls(urls))
        async_time = self.end_time - self.start_time
        
        # Results
        successful = sum(1 for r in async_results if r.get('success', False))
        print(f"Async: {async_time:.2f}s, {successful}/{len(urls)} successful")
        
        # Show results
        for result in async_results[:3]:
            print(f"  {result['url']} - {result['status']} - {result['time']:.2f}s")
        if len(async_results) > 3:
            print(f"  ... and {len(async_results)-3} more")
        
        return {
            "async_time": async_time,
            "results": async_results,
            "successful": successful,
            "total": len(urls)
        }
    
    # ==================== PARALLEL PROCESSING ====================
    
    async def process_item(self, item_id: int, data: int) -> Dict[str, Any]:
        """Simulate processing an item"""
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return {
            "id": item_id,
            "input": data,
            "output": data * data,
            "processed_at": datetime.now().isoformat()
        }
    
    async def process_items_parallel(self, items: List[int]) -> List[Dict[str, Any]]:
        """Process items in parallel"""
        self.start_time = time.time()
        tasks = [self.process_item(i, item) for i, item in enumerate(items)]
        results = await asyncio.gather(*tasks)
        self.end_time = time.time()
        return results
    
    def process_items_sync(self, items: List[int]) -> List[Dict[str, Any]]:
        """Process items synchronously"""
        self.start_time = time.time()
        results = []
        for i, item in enumerate(items):
            time.sleep(random.uniform(0.1, 0.5))
            results.append({
                "id": i,
                "input": item,
                "output": item * item,
                "processed_at": datetime.now().isoformat()
            })
        self.end_time = time.time()
        return results
    
    def demo_parallel_processing(self, count: int = 10) -> Dict[str, Any]:
        """Demonstrate parallel processing"""
        items = list(range(count))
        print(f"\nProcessing {count} items:")
        print("-" * 50)
        
        # Sync
        sync_results = self.process_items_sync(items)
        sync_time = self.end_time - self.start_time
        print(f"Sync: {sync_time:.2f}s")
        
        # Async
        async_results = asyncio.run(self.process_items_parallel(items))
        async_time = self.end_time - self.start_time
        print(f"Async: {async_time:.2f}s")
        
        return {
            "sync_time": sync_time,
            "async_time": async_time,
            "speedup": sync_time / async_time if async_time > 0 else 0,
            "sync_results": sync_results,
            "async_results": async_results
        }
    
    # ==================== STREAMLINING ====================
    
    async def stream_data(self, count: int = 10) -> List[int]:
        """Stream data asynchronously"""
        results = []
        for i in range(count):
            await asyncio.sleep(random.uniform(0.1, 0.3))
            value = i * 2
            results.append(value)
            print(f"  Streamed: {value}")
        return results
    
    async def process_stream(self, data: List[int]) -> List[int]:
        """Process streamed data"""
        results = []
        for item in data:
            await asyncio.sleep(0.1)
            results.append(item * 3)
        return results
    
    async def run_stream_pipeline(self) -> Dict[str, Any]:
        """Run a streaming pipeline"""
        print("\nStreaming pipeline:")
        print("-" * 50)
        
        self.start_time = time.time()
        
        # Create task for streaming and processing
        stream_task = self.stream_data(10)
        process_task = self.process_stream(await stream_task)
        
        results = await process_task
        self.end_time = time.time()
        
        print(f"Pipeline completed in {self.end_time - self.start_time:.2f}s")
        print(f"Results: {results[:5]}...")
        
        return {
            "time": self.end_time - self.start_time,
            "results": results
        }
    
    # ==================== BATCH PROCESSING ====================
    
    async def process_batch(self, batch_id: int, items: List[int]) -> List[Dict[str, Any]]:
        """Process a batch of items"""
        await asyncio.sleep(random.uniform(0.2, 0.8))
        results = []
        for item in items:
            results.append({
                "batch": batch_id,
                "input": item,
                "output": item * 2,
                "processed_at": datetime.now().isoformat()
            })
        return results
    
    async def run_batch_processing(self, batches: List[List[int]]) -> List[List[Dict[str, Any]]]:
        """Process multiple batches in parallel"""
        self.start_time = time.time()
        tasks = [self.process_batch(i, batch) for i, batch in enumerate(batches)]
        results = await asyncio.gather(*tasks)
        self.end_time = time.time()
        return results
    
    def demo_batch_processing(self) -> Dict[str, Any]:
        """Demonstrate batch processing"""
        batches = [
            list(range(10)),
            list(range(10, 20)),
            list(range(20, 30)),
            list(range(30, 40)),
            list(range(40, 50))
        ]
        
        print(f"\nProcessing {len(batches)} batches:")
        print("-" * 50)
        
        results = asyncio.run(self.run_batch_processing(batches))
        total_items = sum(len(b) for b in results)
        
        print(f"Async: {self.end_time - self.start_time:.2f}s")
        print(f"Processed {total_items} items in {len(batches)} batches")
        
        return {
            "time": self.end_time - self.start_time,
            "batch_count": len(batches),
            "total_items": total_items,
            "results": results
        }
