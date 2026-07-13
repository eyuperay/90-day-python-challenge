"""
Performance Profiler using cProfile and pstats
"""

import cProfile
import pstats
import io
import os
from datetime import datetime
from typing import Callable, Any, List, Tuple


class PerformanceProfiler:
    """
    Performance profiler for Python functions
    """
    
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.results = {}
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Tuple[Any, pstats.Stats]:
        """
        Profile a single function
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Tuple of (result, stats)
        """
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler)
        return result, stats
    
    def profile_multiple(self, functions: List[Tuple[Callable, tuple, dict, str]]) -> None:
        """
        Profile multiple functions
        
        Args:
            functions: List of tuples (func, args, kwargs, name)
        """
        for func, args, kwargs, name in functions:
            print(f"Profiling: {name}...")
            result, stats = self.profile_function(func, *args, **kwargs)
            self.results[name] = {
                'result': result,
                'stats': stats,
                'func': func,
                'args': args,
                'kwargs': kwargs
            }
            print(f"  OK {name} completed")
    
    def generate_report(self, filename: str = "profile_report.txt") -> str:
        """
        Generate a performance report
        
        Args:
            filename: Output filename
        
        Returns:
            Report as string
        """
        lines = []
        lines.append("="*60)
        lines.append("PERFORMANCE PROFILE REPORT")
        lines.append("="*60)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*60)
        lines.append("")
        
        for name, data in self.results.items():
            stats = data['stats']
            lines.append("-"*60)
            lines.append(f"Function: {name}")
            lines.append("-"*60)
            
            stats_stream = io.StringIO()
            stats.sort_stats('cumtime').print_stats(10)
            lines.append(stats_stream.getvalue())
            lines.append("")
        
        lines.append("="*60)
        lines.append("[OK] Report generated successfully")
        lines.append("="*60)
        
        report = "\n".join(lines)
        
        os.makedirs("output", exist_ok=True)
        filepath = f"output/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[OK] Report saved to: {filepath}")
        return report
    
    def compare_performance(self, func1: Callable, func2: Callable, 
                           args1: tuple, args2: tuple, 
                           name1: str, name2: str,
                           iterations: int = 5) -> dict:
        """
        Compare performance of two functions
        """
        import time
        
        print(f"\nComparing {name1} vs {name2}...")
        
        times1 = []
        for _ in range(iterations):
            start = time.time()
            func1(*args1)
            times1.append(time.time() - start)
        
        times2 = []
        for _ in range(iterations):
            start = time.time()
            func2(*args2)
            times2.append(time.time() - start)
        
        avg1 = sum(times1) / len(times1)
        avg2 = sum(times2) / len(times2)
        
        comparison = {
            'name1': name1,
            'name2': name2,
            'avg_time1': avg1,
            'avg_time2': avg2,
            'times1': times1,
            'times2': times2,
            'speedup': avg1 / avg2 if avg2 > 0 else 0,
            'iterations': iterations
        }
        
        print(f"  {name1}: {avg1:.6f} seconds (avg)")
        print(f"  {name2}: {avg2:.6f} seconds (avg)")
        print(f"  Speedup: {comparison['speedup']:.2f}x")
        
        return comparison
    
    def print_comparison(self, comparison: dict):
        """
        Print comparison results
        """
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON")
        print("="*60)
        print(f"{'Function':<30} {'Avg Time (s)':>15} {'Min (s)':>15} {'Max (s)':>15}")
        print("-"*60)
        
        print(f"{comparison['name1'][:30]:<30} {comparison['avg_time1']:>15.6f} "
              f"{min(comparison['times1']):>15.6f} {max(comparison['times1']):>15.6f}")
        print(f"{comparison['name2'][:30]:<30} {comparison['avg_time2']:>15.6f} "
              f"{min(comparison['times2']):>15.6f} {max(comparison['times2']):>15.6f}")
        print("-"*60)
        print(f"Speedup: {comparison['speedup']:.2f}x faster")
        print("="*60)
