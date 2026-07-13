#!/usr/bin/env python3
"""
Day 61 - Scheduled Tasks
Demonstrates task scheduling using threading
"""

import time
import datetime
from task_scheduler import TaskScheduler
from tasks import *


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_basic_tasks():
    """Demonstrate basic scheduled tasks"""
    print_section("1. BASIC SCHEDULED TASKS")
    
    scheduler = TaskScheduler()
    
    scheduler.add_task("hello", hello_task, 5)
    scheduler.add_task("time", time_task, 10)
    scheduler.add_task("counter", counter_task, 3)
    scheduler.add_task("random", random_number_task, 7)
    scheduler.add_task("file_log", file_write_task, 6)  # Her 6 saniyede log yazar
    
    print("\n[INFO] Starting scheduler...")
    scheduler.start()
    
    print("\n[INFO] Running tasks for 30 seconds...")
    time.sleep(30)
    
    stats = scheduler.get_statistics()
    print("\n[STATS] Scheduler statistics:")
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Total runs: {stats['total_runs']}")
    
    scheduler.stop()


def demo_task_with_args():
    """Demonstrate tasks with arguments"""
    print_section("2. TASKS WITH ARGUMENTS")
    
    def greet(name, greeting="Hello"):
        print(f"  {greeting}, {name}!")
    
    scheduler = TaskScheduler()
    
    scheduler.add_task("greet_alice", greet, 5, args=("Alice",))
    scheduler.add_task("greet_bob", greet, 7, args=("Bob", "Hi"))
    
    scheduler.start()
    
    print("\n[INFO] Running tasks for 20 seconds...")
    time.sleep(20)
    
    scheduler.stop()


def demo_long_running_tasks():
    """Demonstrate long-running tasks"""
    print_section("3. LONG-RUNNING TASKS")
    
    def progress_task():
        for i in range(1, 4):
            print(f"  Progress: {i}/3")
            time.sleep(0.5)
        print("  Long task completed!")
    
    scheduler = TaskScheduler()
    scheduler.add_task("progress", progress_task, 15)
    scheduler.add_task("expensive", expensive_task, 20)
    
    scheduler.start()
    
    print("\n[INFO] Running tasks for 45 seconds...")
    time.sleep(45)
    
    stats = scheduler.get_statistics()
    print(f"\n[STATS] Total runs: {stats['total_runs']}")
    
    scheduler.stop()


def demo_error_handling():
    """Demonstrate error handling in tasks"""
    print_section("4. ERROR HANDLING")
    
    scheduler = TaskScheduler()
    scheduler.add_task("error", error_task, 5)
    
    scheduler.start()
    
    print("\n[INFO] Running tasks for 20 seconds (some may fail)...")
    time.sleep(20)
    
    stats = scheduler.get_statistics()
    print(f"\n[STATS] Total runs: {stats['total_runs']}")
    print(f"[STATS] Total errors: {stats['total_errors']}")
    
    scheduler.stop()


def demo_multiple_tasks():
    """Demonstrate multiple tasks running together"""
    print_section("5. MULTIPLE TASKS RUNNING TOGETHER")
    
    scheduler = TaskScheduler()
    
    scheduler.add_task("data", data_processing_task, 8)
    scheduler.add_task("api", api_check_task, 6)
    scheduler.add_task("backup", backup_task, 12)
    scheduler.add_task("notify", notification_task, 5)
    scheduler.add_task("time", time_task, 10)
    scheduler.add_task("file_log", file_write_task, 7)
    
    scheduler.start()
    
    print("\n[INFO] Running multiple tasks for 40 seconds...")
    time.sleep(40)
    
    stats = scheduler.get_statistics()
    print(f"\n[STATS] Total runs: {stats['total_runs']}")
    print(f"[STATS] Total errors: {stats['total_errors']}")
    
    for name, task_stats in stats['tasks'].items():
        print(f"  {name}: {task_stats['run_count']} runs, {task_stats['error_count']} errors")
    
    scheduler.stop()


def demo_manual_control():
    """Demonstrate manual control of tasks"""
    print_section("6. MANUAL CONTROL")
    
    scheduler = TaskScheduler()
    scheduler.add_task("hello", hello_task, 5)
    scheduler.add_task("time", time_task, 10)
    scheduler.add_task("file_log", file_write_task, 8)
    
    scheduler.start()
    
    print("\n[INFO] Running for 15 seconds...")
    time.sleep(15)
    
    print("\n[INFO] Manually running 'hello' task...")
    scheduler.run_now("hello")
    
    print("\n[INFO] Running for another 10 seconds...")
    time.sleep(10)
    
    print("\n[INFO] Cancelling 'time' task...")
    scheduler.cancel_task("time")
    
    print("\n[INFO] Running for another 10 seconds...")
    time.sleep(10)
    
    stats = scheduler.get_statistics()
    print(f"\n[STATS] Total runs: {stats['total_runs']}")
    for name, task_stats in stats['tasks'].items():
        print(f"  {name}: {task_stats['run_count']} runs, status: {task_stats['status']}")
    
    scheduler.stop()


def demo_real_world_scenario():
    """Demonstrate a real-world scheduling scenario"""
    print_section("7. REAL-WORLD SCENARIO")
    
    def daily_report():
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"  [{timestamp}] Daily report generated")
        print("  - Total users: 1,234")
        print("  - Active users: 567")
        print("  - Revenue: 45,678.90 TRY")
    
    def hourly_cleanup():
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"  [{timestamp}] Hourly cleanup completed")
        print("  - Cache cleared")
        print("  - Temp files removed")
    
    def health_check():
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = random.choice(['OK', 'OK', 'OK', 'WARNING'])
        print(f"  [{timestamp}] Health check: {status}")
        if status == 'WARNING':
            print("  - High memory usage: 85%")
    
    scheduler = TaskScheduler()
    scheduler.add_task("report", daily_report, 20)
    scheduler.add_task("cleanup", hourly_cleanup, 12)
    scheduler.add_task("health", health_check, 8)
    scheduler.add_task("file_log", file_write_task, 6)
    
    scheduler.start()
    
    print("\n[INFO] Running real-world scenario for 45 seconds...")
    time.sleep(45)
    
    stats = scheduler.get_statistics()
    print(f"\n[STATS] Total runs: {stats['total_runs']}")
    print(f"[STATS] Total errors: {stats['total_errors']}")
    
    scheduler.stop()


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
Scheduled Tasks - Key Concepts:

1. Task Scheduling:
   - Run tasks at regular intervals
   - Background execution
   - Automatic retry

2. Task Types:
   - Time-based (every N seconds)
   - Event-based (on trigger)
   - One-time (delayed execution)

3. Implementation:
   - threading for background execution
   - time.sleep() for intervals
   - Lock for thread safety

4. Task Management:
   - Add/remove tasks
   - Start/stop scheduler
   - Cancel individual tasks
   - Reset task statistics

5. Error Handling:
   - Try/except in tasks
   - Error tracking
   - Failed task recovery

6. Use Cases:
   - Database backups
   - Health checks
   - Report generation
   - Cache cleanup
   - Monitoring alerts
   - Data synchronization
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check 'logs' folder for task logs")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 61 - SCHEDULED TASKS")
    print("=" * 60 + "\n")
    
    demo_basic_tasks()
    demo_task_with_args()
    demo_long_running_tasks()
    demo_error_handling()
    demo_multiple_tasks()
    demo_manual_control()
    demo_real_world_scenario()
    
    print_summary()


if __name__ == "__main__":
    counter = 0
    main()
