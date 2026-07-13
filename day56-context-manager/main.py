#!/usr/bin/env python3
"""
Day 56 - Context Manager
Demonstrates custom context managers
"""

import time
import sqlite3
from context_managers import *


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 56 - CONTEXT MANAGER")
    print("=" * 60 + "\n")
    
    # ==================== 1. TIMER ====================
    print_section("1. TIMER CONTEXT MANAGER")
    
    with Timer("Sleep Operation"):
        time.sleep(0.5)
    
    print()
    with Timer("Nested Operations"):
        for i in range(3):
            time.sleep(0.1)
            print(f"  Step {i+1} completed")
    
    # ==================== 2. DATABASE CONNECTION ====================
    print_section("2. DATABASE CONNECTION")
    
    with DatabaseConnection(":memory:") as cursor:
        cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'Ahmet')")
        cursor.execute("INSERT INTO users VALUES (2, 'Mehmet')")
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print(f"[DB] Data: {rows}")
    
    print()
    
    # Bu hata beklenen bir hatadır - try-except ile yakalanır
    try:
        with DatabaseConnection(":memory:") as cursor:
            cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO users VALUES (1, 'Ahmet')")
            cursor.execute("INSERT INTO users VALUES (2, 'Mehmet')")
            cursor.execute("SELECT * FROM wrong_table")  # Bu hata fırlatır
    except sqlite3.OperationalError as e:
        print(f"[Error] Caught expected error: {e}")
    
    # ==================== 3. FILE HANDLER ====================
    print_section("3. FILE HANDLER")
    
    with FileHandler("output/test.txt", 'w') as f:
        f.write("Hello from context manager!\n")
        f.write("This is line 2\n")
        f.write("This is line 3\n")
    
    print()
    
    with FileHandler("output/test.txt", 'r') as f:
        content = f.read()
        print(f"[File] Content:\n{content}")
    
    # ==================== 4. LOGGING CONTEXT ====================
    print_section("4. LOGGING CONTEXT")
    
    with LoggingContext("Processing Data"):
        print("  Processing step 1...")
        time.sleep(0.2)
        print("  Processing step 2...")
        time.sleep(0.2)
    
    print()
    
    try:
        with LoggingContext("Error Operation"):
            print("  Doing something risky...")
            raise ValueError("Something went wrong!")
    except ValueError:
        print("[Error] Caught ValueError as expected")
    
    # ==================== 5. SUPPRESS ERRORS ====================
    print_section("5. SUPPRESS ERRORS")
    
    with SuppressErrors(ValueError, ZeroDivisionError):
        print("  Trying to divide by zero...")
        result = 10 / 0
        print(f"  Result: {result}")
    
    print()
    
    with SuppressErrors(ValueError):
        print("  Trying to convert string to int...")
        int("abc")
    
    # ==================== 6. DECORATOR-BASED CONTEXT MANAGERS ====================
    print_section("6. DECORATOR-BASED CONTEXT MANAGERS")
    
    with timed_operation("Sleep Operation"):
        time.sleep(0.3)
    
    print()
    
    with open_file_safe("output/safe_test.txt", 'w') as f:
        f.write("This is written with open_file_safe\n")
        f.write("Line 2\n")
    
    print()
    
    with open_file_safe("output/safe_test.txt", 'r') as f:
        content = f.read()
        print(f"Read content: {content[:50]}...")
    
    print()
    
    with suppress_exceptions(ValueError, ZeroDivisionError):
        print("  Trying operation that might fail...")
        int("invalid")
        print("  This won't be printed")
    
    print()
    
    with suppress_exceptions(ValueError, ZeroDivisionError):
        print("  Trying to divide by zero...")
        result = 10 / 0
        print(f"  Result: {result}")
    
    # ==================== 7. TRANSACTION ====================
    print_section("7. TRANSACTION CONTEXT MANAGER")
    
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INTEGER, balance REAL)")
    
    with Transaction(conn):
        cursor.execute("INSERT INTO accounts VALUES (1, 1000)")
        cursor.execute("INSERT INTO accounts VALUES (2, 500)")
        print("[Transaction] Records inserted successfully")
    
    print()
    
    try:
        with Transaction(conn):
            cursor.execute("INSERT INTO accounts VALUES (3, 2000)")
            cursor.execute("INSERT INTO accounts VALUES (4, 3000)")
            print("[Transaction] Before error...")
            raise ValueError("Something went wrong in transaction!")
    except ValueError:
        print("[Error] Transaction rolled back")
    
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    print(f"[DB] Final data: {rows}")
    conn.close()
    
    # ==================== 8. DIRECTORY CHANGER ====================
    print_section("8. DIRECTORY CHANGER")
    
    import os
    print(f"Current directory: {os.getcwd()}")
    
    with change_directory("output"):
        print(f"Inside context: {os.getcwd()}")
        with open("inside_output.txt", 'w') as f:
            f.write("Created inside output directory")
        print("  Created file: inside_output.txt")
    
    print(f"Back to: {os.getcwd()}")
    
    # ==================== 9. SUMMARY ====================
    print_section("SUMMARY")
    print("""
Context Manager - Key Concepts:

1. What is Context Manager?
   - Manages resources with with statement
   - Automatically handles setup/cleanup
   - Ensures resources are released

2. Two Ways to Create:
   a) Class-based: __enter__ and __exit__
   b) Decorator-based: @contextmanager with yield

3. Class-based:
   - __enter__: Setup resources
   - __exit__: Cleanup resources
   - Return False to propagate exceptions
   - Return True to suppress exceptions

4. Decorator-based:
   - @contextmanager from contextlib
   - yield: Where code executes
   - try/finally for cleanup

5. Common Uses:
   - File operations
   - Database connections
   - Timing/performance
   - Transaction management
   - Error handling
   - Directory changes

6. Built-in Context Managers:
   - open()
   - threading.Lock
   - sqlite3 connections
   - contextlib.suppress
   - contextlib.redirect_stdout
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
