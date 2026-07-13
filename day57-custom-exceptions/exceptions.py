"""
Custom Exceptions Module
Defines custom exception classes for various scenarios
"""


# ==================== BASE EXCEPTION ====================

class AppException(Exception):
    """Base exception for application"""
    def __init__(self, message: str, code: int = None):
        self.message = message
        self.code = code
        super().__init__(message)
    
    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


# ==================== USER-RELATED EXCEPTIONS ====================

class UserError(AppException):
    """Base exception for user-related errors"""
    pass


class UserNotFoundError(UserError):
    """Raised when a user is not found"""
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found", code=1001)


class UserAlreadyExistsError(UserError):
    """Raised when trying to create a user that already exists"""
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists", code=1002)


class InvalidEmailError(UserError):
    """Raised when email format is invalid"""
    def __init__(self, email: str):
        super().__init__(f"Invalid email format: '{email}'", code=1003)


class InvalidPasswordError(UserError):
    """Raised when password is invalid"""
    def __init__(self, message: str = "Invalid password"):
        super().__init__(message, code=1004)


class UserNotAuthorizedError(UserError):
    """Raised when user is not authorized"""
    def __init__(self, username: str, required_permission: str):
        super().__init__(
            f"User '{username}' does not have permission: {required_permission}",
            code=1005
        )


# ==================== AUTHENTICATION EXCEPTIONS ====================

class AuthError(AppException):
    """Base exception for authentication errors"""
    pass


class LoginFailedError(AuthError):
    """Raised when login fails"""
    def __init__(self, username: str):
        super().__init__(f"Login failed for user '{username}'", code=2001)


class TokenExpiredError(AuthError):
    """Raised when authentication token has expired"""
    def __init__(self, token: str = None):
        message = "Authentication token has expired"
        if token:
            message = f"Token '{token[:10]}...' has expired"
        super().__init__(message, code=2002)


class TokenInvalidError(AuthError):
    """Raised when authentication token is invalid"""
    def __init__(self):
        super().__init__("Invalid authentication token", code=2003)


# ==================== DATABASE EXCEPTIONS ====================

class DatabaseError(AppException):
    """Base exception for database errors"""
    pass


class ConnectionError(DatabaseError):
    """Raised when database connection fails"""
    def __init__(self, db_name: str, details: str = None):
        message = f"Failed to connect to database '{db_name}'"
        if details:
            message += f": {details}"
        super().__init__(message, code=3001)


class QueryError(DatabaseError):
    """Raised when a database query fails"""
    def __init__(self, query: str, error: str):
        super().__init__(f"Query failed: {query[:50]}... - Error: {error}", code=3002)


class RecordNotFoundError(DatabaseError):
    """Raised when a record is not found"""
    def __init__(self, table: str, record_id: int):
        super().__init__(f"Record not found in '{table}' with ID {record_id}", code=3003)


class DuplicateRecordError(DatabaseError):
    """Raised when trying to insert a duplicate record"""
    def __init__(self, table: str, field: str, value: str):
        super().__init__(f"Duplicate record in '{table}': {field}='{value}'", code=3004)


# ==================== VALIDATION EXCEPTIONS ====================

class ValidationError(AppException):
    """Base exception for validation errors"""
    pass


class FieldRequiredError(ValidationError):
    """Raised when a required field is missing"""
    def __init__(self, field_name: str):
        super().__init__(f"Field '{field_name}' is required", code=4001)


class InvalidFieldValueError(ValidationError):
    """Raised when a field value is invalid"""
    def __init__(self, field_name: str, value: str, expected: str = None):
        message = f"Invalid value for '{field_name}': '{value}'"
        if expected:
            message += f" (expected: {expected})"
        super().__init__(message, code=4002)


class OutOfRangeError(ValidationError):
    """Raised when a value is out of range"""
    def __init__(self, field_name: str, value, min_val, max_val):
        super().__init__(
            f"'{field_name}' value {value} must be between {min_val} and {max_val}",
            code=4003
        )


class LengthExceededError(ValidationError):
    """Raised when a value exceeds maximum length"""
    def __init__(self, field_name: str, value: str, max_length: int):
        super().__init__(
            f"'{field_name}' length {len(value)} exceeds maximum {max_length}",
            code=4004
        )


# ==================== BUSINESS LOGIC EXCEPTIONS ====================

class BusinessError(AppException):
    """Base exception for business logic errors"""
    pass


class InsufficientBalanceError(BusinessError):
    """Raised when balance is insufficient"""
    def __init__(self, required: float, available: float, currency: str = "TRY"):
        super().__init__(
            f"Insufficient balance: required {required:.2f} {currency}, "
            f"available {available:.2f} {currency}",
            code=5001
        )


class ProductOutOfStockError(BusinessError):
    """Raised when product is out of stock"""
    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(
            f"Product '{product_name}' out of stock: requested {requested}, "
            f"available {available}",
            code=5002
        )


class OrderAlreadyCancelledError(BusinessError):
    """Raised when trying to cancel an already cancelled order"""
    def __init__(self, order_id: str):
        super().__init__(f"Order '{order_id}' is already cancelled", code=5003)


class OrderNotDeliverableError(BusinessError):
    """Raised when order cannot be delivered"""
    def __init__(self, order_id: str, reason: str):
        super().__init__(f"Order '{order_id}' cannot be delivered: {reason}", code=5004)


class PaymentFailedError(BusinessError):
    """Raised when payment fails"""
    def __init__(self, amount: float, reason: str):
        super().__init__(f"Payment failed: {amount:.2f} TRY - {reason}", code=5005)


# ==================== FILE OPERATION EXCEPTIONS ====================

class FileOperationError(AppException):
    """Base exception for file operation errors"""
    pass


class FileNotFoundError(FileOperationError):
    """Raised when file is not found"""
    def __init__(self, filename: str):
        super().__init__(f"File not found: '{filename}'", code=6001)


class FileReadError(FileOperationError):
    """Raised when file read fails"""
    def __init__(self, filename: str, error: str):
        super().__init__(f"Failed to read file '{filename}': {error}", code=6002)


class FileWriteError(FileOperationError):
    """Raised when file write fails"""
    def __init__(self, filename: str, error: str):
        super().__init__(f"Failed to write file '{filename}': {error}", code=6003)


class FileFormatError(FileOperationError):
    """Raised when file format is invalid"""
    def __init__(self, filename: str, expected_format: str):
        super().__init__(
            f"Invalid file format for '{filename}': expected {expected_format}",
            code=6004
        )


# ==================== NETWORK EXCEPTIONS ====================

class NetworkError(AppException):
    """Base exception for network errors"""
    pass


class RequestTimeoutError(NetworkError):
    """Raised when request times out"""
    def __init__(self, url: str, timeout: int):
        super().__init__(f"Request to '{url}' timed out after {timeout}s", code=7001)


class APIError(NetworkError):
    """Raised when API returns an error"""
    def __init__(self, url: str, status_code: int, message: str):
        super().__init__(
            f"API error: {url} returned {status_code} - {message}",
            code=7002
        )


class ServiceUnavailableError(NetworkError):
    """Raised when service is unavailable"""
    def __init__(self, service_name: str):
        super().__init__(f"Service '{service_name}' is unavailable", code=7003)


# ==================== UTILITY FUNCTIONS ====================

def handle_exception(e: Exception) -> dict:
    """
    Convert exception to dictionary for logging/API responses
    
    Args:
        e: Exception instance
    
    Returns:
        Dictionary with error details
    """
    if isinstance(e, AppException):
        return {
            'success': False,
            'error': {
                'type': e.__class__.__name__,
                'message': str(e),
                'code': e.code if hasattr(e, 'code') else None
            }
        }
    else:
        return {
            'success': False,
            'error': {
                'type': e.__class__.__name__,
                'message': str(e),
                'code': None
            }
        }


def exception_to_json(e: Exception) -> str:
    """Convert exception to JSON string"""
    import json
    return json.dumps(handle_exception(e), indent=2)
