#!/usr/bin/env python3
"""
Day 50 - Unit Test Writing
Run unit tests for calculator module
"""

import sys
import os
from datetime import datetime


def main():
    print("=" * 60)
    print("DAY 50 - UNIT TEST WRITING")
    print("=" * 60 + "\n")
    
    print("Running unit tests...")
    print("=" * 60 + "\n")
    
    # Import and run tests
    try:
        import test_calculator
        test_calculator.run_tests()
    except ImportError as e:
        print(f"[ERROR] Failed to import test module: {e}")
        print("Please ensure test_calculator.py exists")
        return
    except Exception as e:
        print(f"[ERROR] Test execution failed: {e}")
        return
    
    print("\n" + "=" * 60)
    print("[OK] ALL TESTS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for test report")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
