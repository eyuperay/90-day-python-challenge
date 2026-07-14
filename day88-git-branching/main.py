#!/usr/bin/env python3
"""
Day 88 - Git Branching Demo
Main application entry point
"""

import sys
from features.auth import AuthManager
from features.data import DataManager


def main():
    """Main entry point"""
    print("="*60)
    print("DAY 88 - GIT BRANCHING DEMO")
    print("="*60 + "\n")
    
    auth = AuthManager()
    data = DataManager()
    
    print("1. Authentication Module:")
    print(f"   Version: {auth.get_version()}")
    print(f"   Features: {auth.get_features()}")
    
    print("\n2. Data Module:")
    print(f"   Version: {data.get_version()}")
    print(f"   Features: {data.get_features()}")
    
    print("\n" + "="*60)
    print("Application running successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
