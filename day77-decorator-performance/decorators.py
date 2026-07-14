"""
Performance Decorators Module
Decorators for measuring and logging function performance
"""

import time
import functools
import json
import os
from datetime import datetime
from typing import Any, Callable, Dict, List


class PerformanceTracker:
    """Track performance metrics across functions"""
    
    def __init__(self):
        self.metrics: Dict[str, List[Dict]] = {}
        self.total_calls = 0
        self.total_time = 0
    
    def add_metric(self, func_name: str, duration: float, args: tuple, kwargs: dict, result: Any):
        """Add a performance metric"""
        if func_name not in self.metrics:
            self.metrics[func_name] = []
        
        self.metrics[func_name].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'args': str(args),
            'kwargs': str(kwargs),
            'result': str(result)[:100]  # Limit result length
        })
        
        self.total_calls += 1
        self.total_time += duration
    
    def get_stats(self, func_name: str = None) -> Dict:
        """Get statistics for a function or all functions"""
        if func_name:
            data = self.metrics.get(func_name, [])
            if not data:
                return {}
            
            durations = [m['duration'] for m in data]
            return {
                'function': func_name,
                'calls': len(data),
                'total_time': sum(durations),
                'avg_time': sum(durations) / len(durations),
                'min_time': min(durations),
                'max_time': max(durations),
                'last_call': data[-1]['timestamp']
            }
        
        # All functions
        stats = {}
        for name in self.metrics:
            stats[name] = self.get_stats(name)
        return stats
    
    def generate_report(self) -> str:
        """Generate a performance report"""
        lines = []
        lines.append("="*60)
        lines.append("PERFORMANCE REPORT")
        lines.append("="*60)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Calls: {self.total_calls}")
        lines.append(f"Total Time: {self.total_time:.4f}s")
        lines.append("="*60)
        lines.append("")
        
        stats = self.get_stats()
        
        for func_name, stat in stats.items():
            if not stat:
                continue
            
            lines.append(f"Function: {func_name}")
            lines.append("-"*40)
            lines.append(f"  Calls: {stat['calls']}")
            lines.append(f"  Total Time: {stat['total_time']:.4f}s")
            lines.append(f"  Average Time: {stat['avg_time']:.4f}s")
            lines.append(f"  Min Time: {stat['min_time']:.4f}s")
            lines.append(f"  Max Time: {stat['max_time']:.4f}s")
            lines.append(f"  Last Call: {stat['last_call']}")
            lines.append("")
        
        lines.append("="*60)
        
        return "\n".join(lines)
    
    def save_report(self, filename: str = "performance_report.txt"):
        """Save performance report to file"""
        os.makedirs("output", exist_ok=True)
        report = self.generate_report()
        filepath = f"output/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[OK] Report saved to: {filepath}")
        return filepath
    
    def reset(self):
        """Reset all metrics"""
        self.metrics = {}
        self.total_calls = 0
        self.total_time = 0


# Global tracker instance
tracker = PerformanceTracker()


# ==================== PERFORMANCE DECORATORS ====================

def time_it(func: Callable) -> Callable:
    """
    Decorator to measure function execution time
    
    Usage:
        @time_it
        def my_function():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        # Log to console
        print(f"[TIMER] {func.__name__}() took {duration:.4f}s")
        
        # Track metrics
        tracker.add_metric(func.__name__, duration, args, kwargs, result)
        
        return result
    return wrapper


def log_arguments(func: Callable) -> Callable:
    """
    Decorator to log function arguments and return value
    
    Usage:
        @log_arguments
        def my_function(x, y):
            return x + y
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ', '.join(str(a) for a in args)
        kwargs_str = ', '.join(f"{k}={v}" for k, v in kwargs.items())
        
        all_args = args_str
        if kwargs_str:
            all_args += (', ' if all_args else '') + kwargs_str
        
        print(f"[LOG] Calling: {func.__name__}({all_args})")
        
        result = func(*args, **kwargs)
        
        print(f"[LOG] {func.__name__}() returned: {result}")
        
        return result
    return wrapper


def retry_on_error(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on error
    
    Usage:
        @retry_on_error(max_attempts=3, delay=1.0)
        def my_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def cache_result(maxsize: int = 128):
    """
    Decorator to cache function results
    
    Usage:
        @cache_result(maxsize=100)
        def expensive_function(n):
            return n * n
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            
            if key in cache:
                print(f"[CACHE] {func.__name__}() returning cached result")
                return cache[key]
            
            result = func(*args, **kwargs)
            
            if len(cache) >= maxsize:
                # Remove oldest item (simple FIFO)
                cache.pop(next(iter(cache)))
            
            cache[key] = result
            print(f"[CACHE] {func.__name__}() cached result")
            
            return result
        return wrapper
    return decorator


def profile(func: Callable) -> Callable:
    """
    Comprehensive profiling decorator
    
    Combines time_it, log_arguments, and adds more details
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        # Start profiling
        start = time.time()
        start_memory = None
        
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            start_memory = process.memory_info().rss / 1024 / 1024
        except:
            pass
        
        result = func(*args, **kwargs)
        
        duration = time.time() - start
        end_memory = None
        
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            end_memory = process.memory_info().rss / 1024 / 1024
        except:
            pass
        
        # Log results
        print(f"\n[PROFILE] {func_name}()")
        print(f"  Duration: {duration:.4f}s")
        if start_memory is not None and end_memory is not None:
            print(f"  Memory: {start_memory:.2f}MB -> {end_memory:.2f}MB ({end_memory - start_memory:+.2f}MB)")
        
        # Track metrics
        tracker.add_metric(func_name, duration, args, kwargs, result)
        
        return result
    return wrapper


def limit_calls(max_calls: int):
    """
    Decorator to limit number of function calls
    
    Usage:
        @limit_calls(5)
        def my_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        calls = 0
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= max_calls:
                raise RuntimeError(f"{func.__name__}() called more than {max_calls} times")
            calls += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
