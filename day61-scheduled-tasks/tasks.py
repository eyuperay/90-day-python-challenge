"""
Sample tasks for the scheduler
"""

import time
import random
import datetime


def hello_task():
    """Print hello message"""
    print("  Hello from scheduled task!")


def time_task():
    """Print current time"""
    now = datetime.datetime.now()
    print(f"  Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


def counter_task():
    """Increment and print counter"""
    global counter
    counter += 1
    print(f"  Counter: {counter}")


def random_number_task():
    """Generate and print random number"""
    number = random.randint(1, 100)
    print(f"  Random number: {number}")


def file_write_task():
    """Write to log file"""
    import os
    os.makedirs("logs", exist_ok=True)
    with open("logs/task_log.txt", 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - Task executed\n")
    print("  Log entry written")


def expensive_task():
    """Simulate expensive operation"""
    time.sleep(2)
    return "Expensive task completed"


def error_task():
    """Task that randomly fails"""
    if random.random() < 0.3:
        raise ValueError("Random error occurred!")
    print("  Error task succeeded")


def data_processing_task():
    """Simulate data processing"""
    data = [random.randint(1, 100) for _ in range(10)]
    processed = [x * 2 for x in data]
    print(f"  Data processed: {sum(processed)}")


def api_check_task():
    """Simulate API health check"""
    status = random.choice(['OK', 'WARNING', 'ERROR'])
    print(f"  API Health: {status}")
    if status == 'ERROR':
        raise Exception("API is down!")


def backup_task():
    """Simulate backup operation"""
    time.sleep(1)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"  Backup completed: backup_{timestamp}.zip")


def notification_task():
    """Simulate sending notification"""
    messages = [
        "System update available",
        "New user registered",
        "Payment processed",
        "Security alert",
        "Maintenance scheduled"
    ]
    message = random.choice(messages)
    print(f"  Notification sent: {message}")


counter = 0
