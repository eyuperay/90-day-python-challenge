"""
Context Manager Demo
Demonstrates custom context managers using __enter__/__exit__ and contextlib
"""

import time
import sqlite3
from datetime import datetime
from contextlib import contextmanager
from typing import Any, Optional


# ==================== CLASS-BASED CONTEXT MANAGER ====================

class Timer:
    """
    Context manager for timing code execution
    Usage: with Timer("Operation name"): ...
    """
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Start timing"""
        self.start_time = time.time()
        print(f"[Timer] Starting: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and print duration"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"[Timer] {self.name} completed in {duration:.4f} seconds")
        
        # Return False to propagate exceptions
        return False
    
    def elapsed(self) -> float:
        """Get elapsed time if still running"""
        if self.start_time and not self.end_time:
            return time.time() - self.start_time
        elif self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


class DatabaseConnection:
    """
    Context manager for database connections
    Automatically handles connection and commit/rollback
    """
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        print(f"[DB] Connected to {self.db_path}")
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection with commit/rollback"""
        if exc_type:
            # Error occurred - rollback
            self.connection.rollback()
            print(f"[DB] Rollback due to error: {exc_type.__name__}")
        else:
            # No error - commit
            self.connection.commit()
            print("[DB] Committed successfully")
        
        self.connection.close()
        print("[DB] Connection closed")
        
        # Return False to propagate exceptions
        return False


class FileHandler:
    """
    Context manager for file operations
    Automatically handles open/close with error checking
    """
    
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Open file"""
        try:
            self.file = open(self.filename, self.mode, encoding='utf-8')
            print(f"[File] Opened: {self.filename} (mode: {self.mode})")
            return self.file
        except Exception as e:
            print(f"[File] Error opening {self.filename}: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close file"""
        if self.file:
            self.file.close()
            print(f"[File] Closed: {self.filename}")
        
        # Return False to propagate exceptions
        return False


class LoggingContext:
    """
    Context manager that logs entry and exit
    Useful for debugging and monitoring
    """
    
    def __init__(self, name: str = "Context"):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        """Log entry"""
        self.start_time = datetime.now()
        print(f"[LOG] Entering: {self.name} at {self.start_time.strftime('%H:%M:%S')}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log exit with status"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        if exc_type:
            print(f"[LOG] Exiting: {self.name} with ERROR ({exc_type.__name__}) - Duration: {duration:.2f}s")
        else:
            print(f"[LOG] Exiting: {self.name} successfully - Duration: {duration:.2f}s")
        
        # Return False to propagate exceptions
        return False


class SuppressErrors:
    """
    Context manager that suppresses specific exceptions
    Similar to contextlib.suppress
    """
    
    def __init__(self, *exceptions):
        self.exceptions = exceptions or (Exception,)
        self.exception = None
    
    def __enter__(self):
        """Return self for accessing exception info"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suppress specified exceptions"""
        if exc_type and issubclass(exc_type, self.exceptions):
            self.exception = exc_val
            print(f"[Suppress] Suppressed: {exc_type.__name__}: {exc_val}")
            return True  # Suppress the exception
        return False  # Propagate other exceptions


class Transaction:
    """
    Context manager for transaction operations
    Commits on success, rolls back on error
    """
    
    def __init__(self, connection):
        self.connection = connection
        self.success = False
    
    def __enter__(self):
        """Start transaction"""
        print("[Transaction] Starting transaction")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback"""
        if exc_type:
            self.connection.rollback()
            print(f"[Transaction] Rollback due to: {exc_type.__name__}")
        else:
            self.connection.commit()
            self.success = True
            print("[Transaction] Committed successfully")
        
        return False


# ==================== DECORATOR-BASED CONTEXT MANAGER ====================

@contextmanager
def timed_operation(name: str = "Operation"):
    """
    Generator-based context manager for timing
    Usage: with timed_operation("Name"): ...
    """
    start = time.time()
    print(f"[Timed] Starting: {name}")
    try:
        yield
    finally:
        duration = time.time() - start
        print(f"[Timed] {name} completed in {duration:.4f} seconds")


@contextmanager
def open_file_safe(filename: str, mode: str = 'r'):
    """
    Generator-based context manager for file operations
    With error handling
    """
    file = None
    try:
        file = open(filename, mode, encoding='utf-8')
        print(f"[FileSafe] Opened: {filename}")
        yield file
    except Exception as e:
        print(f"[FileSafe] Error: {e}")
        raise
    finally:
        if file:
            file.close()
            print(f"[FileSafe] Closed: {filename}")


@contextmanager
def change_directory(path: str):
    """
    Generator-based context manager for changing directory
    Restores original directory on exit
    """
    import os
    original_dir = os.getcwd()
    print(f"[Dir] Changing from {original_dir} to {path}")
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_dir)
        print(f"[Dir] Restored to {original_dir}")


@contextmanager
def suppress_exceptions(*exceptions):
    """
    Generator-based context manager for suppressing exceptions
    """
    try:
        yield
    except exceptions as e:
        print(f"[Suppress] Suppressed: {type(e).__name__}: {e}")


@contextmanager
def measure_memory():
    """
    Generator-based context manager for memory usage
    (Simplified version - requires psutil for real memory tracking)
    """
    import os
    import psutil
    
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024
    
    print(f"[Memory] Before: {memory_before:.2f} MB")
    yield
    memory_after = process.memory_info().rss / 1024 / 1024
    diff = memory_after - memory_before
    
    print(f"[Memory] After: {memory_after:.2f} MB")
    print(f"[Memory] Difference: {diff:+.2f} MB")
