#!/usr/bin/env python3
"""
Day 58 - Logging System
Demonstrates Python logging module
"""

import logging
import time
import random
from logger_config import (
    setup_logger,
    get_app_logger,
    get_debug_logger,
    get_error_logger,
    get_module_logger,
    LoggerFactory,
    log_timing,
    log_function
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


# ==================== 1. BASIC LOGGER ====================

def demo_basic_logger():
    """Demonstrate basic logger"""
    print_section("1. BASIC LOGGER")
    
    logger = setup_logger('basic', 'DEBUG', True, True, 'logs', 'basic')
    
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    
    print("  All log levels demonstrated")


# ==================== 2. PREDEFINED LOGGERS ====================

def demo_predefined_loggers():
    """Demonstrate predefined loggers"""
    print_section("2. PREDEFINED LOGGERS")
    
    app_logger = get_app_logger()
    debug_logger = get_debug_logger()
    error_logger = get_error_logger()
    
    app_logger.info("App logger: Application started")
    debug_logger.debug("Debug logger: This is a debug message")
    error_logger.error("Error logger: This is an error message")
    
    print("  All predefined loggers tested")


# ==================== 3. MODULE LOGGER ====================

def demo_module_logger():
    """Demonstrate module-specific logger"""
    print_section("3. MODULE LOGGER")
    
    db_logger = get_module_logger('database', 'DEBUG')
    api_logger = get_module_logger('api', 'INFO')
    auth_logger = get_module_logger('auth', 'WARNING')
    
    db_logger.debug("Database: Connecting to database...")
    db_logger.info("Database: Connected successfully")
    
    api_logger.info("API: Request received")
    api_logger.warning("API: Rate limit approaching")
    
    auth_logger.warning("Auth: User login failed")
    auth_logger.error("Auth: Multiple failed attempts")
    
    print("  Module loggers tested")


# ==================== 4. LOGGER FACTORY ====================

def demo_logger_factory():
    """Demonstrate logger factory"""
    print_section("4. LOGGER FACTORY")
    
    app_logger = LoggerFactory.get_app_logger()
    debug_logger = LoggerFactory.get_debug_logger()
    
    app_logger.info("Factory: Application ready")
    debug_logger.debug("Factory: Debug mode enabled")
    
    print("  Logger factory tested")


# ==================== 5. LOGGING LEVELS ====================

def demo_logging_levels():
    """Demonstrate different logging levels"""
    print_section("5. LOGGING LEVELS")
    
    logger = setup_logger('levels', 'DEBUG', True, True, 'logs', 'levels')
    
    print("  Log levels (from lowest to highest):")
    logger.debug("  DEBUG - Detailed information")
    logger.info("  INFO - General information")
    logger.warning("  WARNING - Warning messages")
    logger.error("  ERROR - Error messages")
    logger.critical("  CRITICAL - Critical errors")
    
    print("\n  Level filtering:")
    logger.setLevel(logging.WARNING)
    logger.debug("  This DEBUG message will NOT appear")
    logger.info("  This INFO message will NOT appear")
    logger.warning("  This WARNING message WILL appear")
    logger.error("  This ERROR message WILL appear")


# ==================== 6. CONTEXT MANAGER ====================

def demo_log_timing():
    """Demonstrate timing context manager"""
    print_section("6. TIMING CONTEXT MANAGER")
    
    logger = setup_logger('timing', 'INFO', True, True, 'logs', 'timing')
    
    with log_timing(logger, "Database query"):
        time.sleep(0.5)
    
    with log_timing(logger, "API call"):
        time.sleep(0.3)
    
    # With error
    try:
        with log_timing(logger, "Error operation"):
            time.sleep(0.1)
            raise ValueError("Something went wrong!")
    except ValueError:
        pass
    
    print("  Timing logs generated")


# ==================== 7. DECORATOR ====================

def demo_log_decorator():
    """Demonstrate log decorator"""
    print_section("7. LOG DECORATOR")
    
    logger = setup_logger('decorator', 'DEBUG', True, True, 'logs', 'decorator')
    
    @log_function(logger)
    def calculate_sum(a, b):
        return a + b
    
    @log_function(logger)
    def divide_numbers(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    result1 = calculate_sum(5, 3)
    print(f"  calculate_sum(5, 3) = {result1}")
    
    result2 = calculate_sum(10, 20)
    print(f"  calculate_sum(10, 20) = {result2}")
    
    try:
        divide_numbers(10, 0)
    except ValueError:
        print("  divide_numbers(10, 0) - Error caught as expected")
    
    print("  Decorator logs generated")


# ==================== 8. REAL-WORLD SCENARIO ====================

def demo_real_world_scenario():
    """Demonstrate real-world logging scenario"""
    print_section("8. REAL-WORLD SCENARIO")
    
    # Create loggers for different components
    app_logger = setup_logger('app', 'INFO', True, True, 'logs', 'app')
    db_logger = setup_logger('database', 'DEBUG', True, True, 'logs', 'database')
    api_logger = setup_logger('api', 'INFO', True, True, 'logs', 'api')
    auth_logger = setup_logger('auth', 'WARNING', True, True, 'logs', 'auth')
    
    app_logger.info("Application starting...")
    
    # Database operations
    db_logger.info("Connecting to database...")
    time.sleep(0.1)
    db_logger.debug("Connection established successfully")
    
    # API operations
    api_logger.info("Processing API request...")
    time.sleep(0.1)
    api_logger.debug("Request data validated")
    api_logger.info("Response sent successfully")
    
    # Authentication
    auth_logger.info("User login attempt: john_doe")
    time.sleep(0.1)
    auth_logger.warning("Invalid password attempt: john_doe")
    
    # Error scenario
    try:
        db_logger.warning("Database query slow: 2.5s")
        time.sleep(0.1)
        raise ConnectionError("Database connection lost")
    except ConnectionError as e:
        db_logger.error(f"Database error: {e}")
        app_logger.critical("Application cannot continue without database")
    
    app_logger.info("Application shutting down...")
    
    print("  Real-world scenario logs generated")


# ==================== 9. LOG ROTATION DEMO ====================

def demo_log_rotation():
    """Demonstrate log file rotation"""
    print_section("9. LOG FILE ROTATION")
    
    logger = setup_logger('rotation', 'INFO', True, True, 'logs', 'rotation')
    
    for i in range(10):
        logger.info(f"Log entry #{i+1}")
        time.sleep(0.05)
    
    print("  Log rotation demo completed")
    print("  Check logs/rotation_*.log files")


# ==================== 10. SUMMARY ====================

def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
Logging System - Key Concepts:

1. Log Levels:
   - DEBUG (10): Detailed information
   - INFO (20): General information
   - WARNING (30): Warning messages
   - ERROR (40): Error messages
   - CRITICAL (50): Critical errors

2. Components:
   - Logger: Main logging object
   - Handler: Where logs go (console, file, etc.)
   - Formatter: Log message format
   - Filter: Filter log messages

3. Best Practices:
   - Use different levels appropriately
   - Include timestamps
   - Add module/function names
   - Log exceptions with traceback
   - Use structured logging

4. Benefits:
   - Debugging
   - Monitoring
   - Auditing
   - Performance tracking
   - Error tracking

5. Log Types:
   - Application logs
   - Access logs
   - Error logs
   - Audit logs
   - Performance logs
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print(f"[OK] Log files saved in 'logs' directory")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 58 - LOGGING SYSTEM")
    print("=" * 60 + "\n")
    
    # Run all demos
    demo_basic_logger()
    demo_predefined_loggers()
    demo_module_logger()
    demo_logger_factory()
    demo_logging_levels()
    demo_log_timing()
    demo_log_decorator()
    demo_real_world_scenario()
    demo_log_rotation()
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
