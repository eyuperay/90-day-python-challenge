"""
Task Scheduler Module
Manages scheduled tasks using threading and time
"""

import time
import threading
import datetime
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task status enum"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """Task dataclass"""
    name: str
    func: Callable
    interval: int
    status: str = "pending"
    last_run: datetime.datetime = None
    next_run: datetime.datetime = None
    run_count: int = 0
    error_count: int = 0
    args: tuple = ()
    kwargs: dict = None


class TaskScheduler:
    """
    Simple task scheduler using threading
    """
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.thread = None
        self.logger = None
        self._lock = threading.Lock()
    
    def add_task(self, name: str, func: Callable, interval: int, 
                 args: tuple = (), kwargs: dict = None) -> None:
        """
        Add a scheduled task
        
        Args:
            name: Task name
            func: Function to execute
            interval: Interval in seconds
            args: Arguments for the function
            kwargs: Keyword arguments for the function
        """
        if kwargs is None:
            kwargs = {}
        
        task = ScheduledTask(
            name=name,
            func=func,
            interval=interval,
            status=TaskStatus.PENDING.value,
            args=args,
            kwargs=kwargs
        )
        
        with self._lock:
            self.tasks[name] = task
        
        print(f"[Scheduler] Task added: {name} (interval: {interval}s)")
    
    def remove_task(self, name: str) -> bool:
        """
        Remove a task
        
        Args:
            name: Task name
        
        Returns:
            True if removed, False otherwise
        """
        with self._lock:
            if name in self.tasks:
                del self.tasks[name]
                print(f"[Scheduler] Task removed: {name}")
                return True
        print(f"[Scheduler] Task not found: {name}")
        return False
    
    def get_task(self, name: str) -> ScheduledTask:
        """Get task by name"""
        with self._lock:
            return self.tasks.get(name)
    
    def get_all_tasks(self) -> List[ScheduledTask]:
        """Get all tasks"""
        with self._lock:
            return list(self.tasks.values())
    
    def get_task_status(self, name: str) -> str:
        """Get task status"""
        task = self.get_task(name)
        return task.status if task else None
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            print("[Scheduler] Already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("[Scheduler] Started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Scheduler] Stopped")
    
    def _run(self):
        """Main scheduler loop"""
        print("[Scheduler] Scheduler loop started")
        
        while self.running:
            current_time = datetime.datetime.now()
            
            with self._lock:
                for task in self.tasks.values():
                    if task.status in [TaskStatus.RUNNING.value, TaskStatus.CANCELLED.value]:
                        continue
                    
                    if task.next_run is None:
                        task.next_run = current_time + datetime.timedelta(seconds=task.interval)
                    
                    if current_time >= task.next_run:
                        self._execute_task(task)
                        task.next_run = current_time + datetime.timedelta(seconds=task.interval)
            
            time.sleep(1)
    
    def _execute_task(self, task: ScheduledTask):
        """Execute a single task"""
        try:
            task.status = TaskStatus.RUNNING.value
            task.last_run = datetime.datetime.now()
            
            print(f"\n[Task] Running: {task.name} at {task.last_run.strftime('%H:%M:%S')}")
            
            result = task.func(*task.args, **task.kwargs)
            
            task.run_count += 1
            task.status = TaskStatus.COMPLETED.value
            
            print(f"[Task] Completed: {task.name} (run #{task.run_count})")
            if result:
                print(f"[Task] Result: {result}")
            
        except Exception as e:
            task.error_count += 1
            task.status = TaskStatus.FAILED.value
            print(f"[Task] Failed: {task.name} - {e}")
    
    def run_now(self, name: str) -> bool:
        """
        Run a task immediately
        
        Args:
            name: Task name
        
        Returns:
            True if executed, False otherwise
        """
        task = self.get_task(name)
        if task:
            self._execute_task(task)
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get scheduler statistics
        
        Returns:
            Dictionary with statistics
        """
        with self._lock:
            total_tasks = len(self.tasks)
            total_runs = sum(t.run_count for t in self.tasks.values())
            total_errors = sum(t.error_count for t in self.tasks.values())
            
            stats = {
                'total_tasks': total_tasks,
                'total_runs': total_runs,
                'total_errors': total_errors,
                'tasks': {}
            }
            
            for name, task in self.tasks.items():
                stats['tasks'][name] = {
                    'status': task.status,
                    'run_count': task.run_count,
                    'error_count': task.error_count,
                    'interval': task.interval,
                    'last_run': task.last_run.isoformat() if task.last_run else None,
                    'next_run': task.next_run.isoformat() if task.next_run else None
                }
            
            return stats
    
    def cancel_task(self, name: str) -> bool:
        """
        Cancel a task
        
        Args:
            name: Task name
        
        Returns:
            True if cancelled, False otherwise
        """
        task = self.get_task(name)
        if task:
            task.status = TaskStatus.CANCELLED.value
            print(f"[Scheduler] Task cancelled: {name}")
            return True
        return False
    
    def reset_task(self, name: str) -> bool:
        """
        Reset a task (clear statistics)
        
        Args:
            name: Task name
        
        Returns:
            True if reset, False otherwise
        """
        task = self.get_task(name)
        if task:
            task.run_count = 0
            task.error_count = 0
            task.last_run = None
            task.next_run = None
            task.status = TaskStatus.PENDING.value
            print(f"[Scheduler] Task reset: {name}")
            return True
        return False
