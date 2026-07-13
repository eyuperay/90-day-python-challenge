#!/usr/bin/env python3
"""
Day 57 - Custom Exceptions
Demonstrates custom exception classes
"""

from exceptions import *
import json


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_user_exceptions():
    """Demonstrate user-related exceptions"""
    print("\n--- User Exceptions ---")
    
    try:
        raise UserNotFoundError(123)
    except UserNotFoundError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise UserAlreadyExistsError("john_doe")
    except UserAlreadyExistsError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise InvalidEmailError("invalid-email")
    except InvalidEmailError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise InvalidPasswordError("Password must be at least 8 characters")
    except InvalidPasswordError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise UserNotAuthorizedError("alice", "admin")
    except UserNotAuthorizedError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_auth_exceptions():
    """Demonstrate authentication exceptions"""
    print("\n--- Authentication Exceptions ---")
    
    try:
        raise LoginFailedError("alice")
    except LoginFailedError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise TokenExpiredError()
    except TokenExpiredError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise TokenInvalidError()
    except TokenInvalidError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_database_exceptions():
    """Demonstrate database exceptions"""
    print("\n--- Database Exceptions ---")
    
    try:
        raise ConnectionError("prod_db", "Connection refused")
    except ConnectionError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise QueryError("SELECT * FROM users", "Table not found")
    except QueryError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise RecordNotFoundError("users", 999)
    except RecordNotFoundError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise DuplicateRecordError("users", "email", "alice@email.com")
    except DuplicateRecordError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_validation_exceptions():
    """Demonstrate validation exceptions"""
    print("\n--- Validation Exceptions ---")
    
    try:
        raise FieldRequiredError("username")
    except FieldRequiredError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise InvalidFieldValueError("age", "abc", "integer")
    except InvalidFieldValueError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise OutOfRangeError("age", 150, 0, 120)
    except OutOfRangeError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise LengthExceededError("username", "very_long_username", 10)
    except LengthExceededError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_business_exceptions():
    """Demonstrate business logic exceptions"""
    print("\n--- Business Exceptions ---")
    
    try:
        raise InsufficientBalanceError(1000, 500)
    except InsufficientBalanceError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise ProductOutOfStockError("Laptop", 5, 3)
    except ProductOutOfStockError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise OrderAlreadyCancelledError("ORD-123")
    except OrderAlreadyCancelledError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise PaymentFailedError(1500, "Insufficient funds")
    except PaymentFailedError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_file_exceptions():
    """Demonstrate file operation exceptions"""
    print("\n--- File Operation Exceptions ---")
    
    try:
        raise FileNotFoundError("data.txt")
    except FileNotFoundError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise FileReadError("data.txt", "Permission denied")
    except FileReadError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise FileFormatError("data.txt", "JSON")
    except FileFormatError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_network_exceptions():
    """Demonstrate network exceptions"""
    print("\n--- Network Exceptions ---")
    
    try:
        raise RequestTimeoutError("https://api.example.com", 30)
    except RequestTimeoutError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise APIError("https://api.example.com", 404, "Not Found")
    except APIError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")
    
    try:
        raise ServiceUnavailableError("Payment Service")
    except ServiceUnavailableError as e:
        print(f"  {e}")
        print(f"  Code: {e.code}")


def demo_catching_multiple():
    """Demonstrate catching multiple custom exceptions"""
    print("\n--- Catching Multiple Exceptions ---")
    
    def risky_operation(operation_type: str):
        if operation_type == "user":
            raise UserNotFoundError(123)
        elif operation_type == "db":
            raise ConnectionError("prod_db", "Connection refused")
        elif operation_type == "validation":
            raise FieldRequiredError("email")
        elif operation_type == "business":
            raise InsufficientBalanceError(1000, 500)
        else:
            return "Success!"
    
    try:
        risky_operation("user")
    except UserNotFoundError as e:
        print(f"  Caught UserError: {e}")
    except ConnectionError as e:
        print(f"  Caught DatabaseError: {e}")
    except FieldRequiredError as e:
        print(f"  Caught ValidationError: {e}")
    except InsufficientBalanceError as e:
        print(f"  Caught BusinessError: {e}")
    except Exception as e:
        print(f"  Caught Generic: {e}")
    
    try:
        risky_operation("db")
    except UserNotFoundError as e:
        print(f"  Caught UserError: {e}")
    except ConnectionError as e:
        print(f"  Caught DatabaseError: {e}")
    except FieldRequiredError as e:
        print(f"  Caught ValidationError: {e}")
    except InsufficientBalanceError as e:
        print(f"  Caught BusinessError: {e}")
    except Exception as e:
        print(f"  Caught Generic: {e}")


def demo_exception_handler():
    """Demonstrate exception handling utility"""
    print("\n--- Exception Handler Utility ---")
    
    try:
        raise UserNotFoundError(123)
    except Exception as e:
        result = handle_exception(e)
        print(f"  Error dict: {json.dumps(result, indent=2)}")


def main():
    print("=" * 60)
    print("DAY 57 - CUSTOM EXCEPTIONS")
    print("=" * 60 + "\n")
    
    # ==================== 1. USER EXCEPTIONS ====================
    print_section("1. USER-RELATED EXCEPTIONS")
    demo_user_exceptions()
    
    # ==================== 2. AUTHENTICATION EXCEPTIONS ====================
    print_section("2. AUTHENTICATION EXCEPTIONS")
    demo_auth_exceptions()
    
    # ==================== 3. DATABASE EXCEPTIONS ====================
    print_section("3. DATABASE EXCEPTIONS")
    demo_database_exceptions()
    
    # ==================== 4. VALIDATION EXCEPTIONS ====================
    print_section("4. VALIDATION EXCEPTIONS")
    demo_validation_exceptions()
    
    # ==================== 5. BUSINESS EXCEPTIONS ====================
    print_section("5. BUSINESS LOGIC EXCEPTIONS")
    demo_business_exceptions()
    
    # ==================== 6. FILE EXCEPTIONS ====================
    print_section("6. FILE OPERATION EXCEPTIONS")
    demo_file_exceptions()
    
    # ==================== 7. NETWORK EXCEPTIONS ====================
    print_section("7. NETWORK EXCEPTIONS")
    demo_network_exceptions()
    
    # ==================== 8. CATCHING MULTIPLE ====================
    print_section("8. CATCHING MULTIPLE EXCEPTIONS")
    demo_catching_multiple()
    
    # ==================== 9. EXCEPTION HANDLER ====================
    print_section("9. EXCEPTION HANDLER UTILITY")
    demo_exception_handler()
    
    # ==================== 10. SUMMARY ====================
    print_section("SUMMARY")
    print("""
Custom Exceptions - Key Concepts:

1. Why Custom Exceptions?
   - Better error handling
   - Specific error types
   - Meaningful error messages
   - Code organization

2. Exception Hierarchy:
   - Base Exception: AppException
   - Child exceptions: UserError, AuthError, DatabaseError, etc.
   - Specific exceptions: UserNotFoundError, LoginFailedError, etc.

3. Benefits:
   - Clear error handling
   - Easy debugging
   - Better API responses
   - Consistent error format

4. Best Practices:
   - Inherit from Exception or custom base
   - Use descriptive names
   - Include error codes
   - Provide helpful messages

5. Use Cases:
   - API development
   - Data validation
   - Business logic
   - File operations
   - Network operations

6. Exception Categories:
   - User Errors (1000-1999)
   - Auth Errors (2000-2999)
   - Database Errors (3000-3999)
   - Validation Errors (4000-4999)
   - Business Errors (5000-5999)
   - File Errors (6000-6999)
   - Network Errors (7000-7999)
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
