"""
Logger Configuration Module
Configures logging for the application
"""

import logging
import os
from datetime import datetime


# ==================== LOG LEVELS ====================

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


# ==================== LOG FORMATS ====================

# Detailed format with timestamp, level, module, and message
DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Simple format with timestamp and message
SIMPLE_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Format for console output
CONSOLE_FORMAT = '%(asctime)s | %(levelname)-8s | %(message)s'

# Format for file output (includes module and line number)
FILE_FORMAT = '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'

# JSON-like format for structured logging
JSON_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'


# ==================== DATE FORMATS ====================

DATE_FORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_DETAILED = '%Y-%m-%d %H:%M:%S.%f'
DATE_FORMAT_FILE = '%Y%m%d_%H%M%S'


# ==================== LOGGER CONFIGURATION ====================

def setup_logger(
    name: str = 'app',
    log_level: str = 'INFO',
    log_to_file: bool = True,
    log_to_console: bool = True,
    log_dir: str = 'logs',
    file_prefix: str = 'app'
) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console
        log_dir: Directory for log files
        file_prefix: Prefix for log files
    
    Returns:
        Configured logger
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = logging.Formatter(CONSOLE_FORMAT, datefmt=DATE_FORMAT_DEFAULT)
    file_formatter = logging.Formatter(FILE_FORMAT, datefmt=DATE_FORMAT_DEFAULT)
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log filename with date
        timestamp = datetime.now().strftime(DATE_FORMAT_FILE)
        log_filename = f"{file_prefix}_{timestamp}.log"
        log_filepath = os.path.join(log_dir, log_filename)
        
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Also create a symlink to latest log
        latest_path = os.path.join(log_dir, f"{file_prefix}_latest.log")
        try:
            if os.path.exists(latest_path):
                os.remove(latest_path)
            # On Windows, use copy instead of symlink
            import shutil
            shutil.copy2(log_filepath, latest_path)
        except Exception:
            pass
    
    return logger


# ==================== PREDEFINED LOGGERS ====================

def get_app_logger() -> logging.Logger:
    """Get application logger"""
    return setup_logger('app', 'INFO', True, True, 'logs', 'app')


def get_debug_logger() -> logging.Logger:
    """Get debug logger"""
    return setup_logger('debug', 'DEBUG', True, True, 'logs', 'debug')


def get_error_logger() -> logging.Logger:
    """Get error logger"""
    return setup_logger('error', 'ERROR', True, True, 'logs', 'error')


def get_module_logger(module_name: str, level: str = 'INFO') -> logging.Logger:
    """Get logger for a specific module"""
    return setup_logger(module_name, level, True, True, 'logs', module_name)


# ==================== CONTEXT MANAGER FOR LOGGING ====================

import contextlib
from io import StringIO


@contextlib.contextmanager
def log_timing(logger: logging.Logger, operation: str):
    """
    Context manager for logging operation timing
    
    Usage:
        with log_timing(logger, "Database query"):
            # Do something
    """
    import time
    start = time.time()
    logger.info(f"Starting: {operation}")
    try:
        yield
    except Exception as e:
        logger.error(f"Failed: {operation} - {e}")
        raise
    finally:
        elapsed = time.time() - start
        logger.info(f"Completed: {operation} in {elapsed:.4f}s")


# ==================== DECORATORS ====================

def log_function(logger: logging.Logger):
    """
    Decorator to log function calls
    
    Usage:
        @log_function(logger)
        def my_function():
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Calling: {func.__name__}()")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Completed: {func.__name__}()")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}(): {e}")
                raise
        return wrapper
    return decorator


# ==================== LOGGER FACTORY ====================

class LoggerFactory:
    """Factory for creating loggers"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = 'app', level: str = 'INFO') -> logging.Logger:
        """Get or create a logger"""
        key = f"{name}_{level}"
        if key not in cls._loggers:
            cls._loggers[key] = setup_logger(name, level, True, True, 'logs', name)
        return cls._loggers[key]
    
    @classmethod
    def get_app_logger(cls) -> logging.Logger:
        return cls.get_logger('app', 'INFO')
    
    @classmethod
    def get_debug_logger(cls) -> logging.Logger:
        return cls.get_logger('app', 'DEBUG')
    
    @classmethod
    def get_error_logger(cls) -> logging.Logger:
        return cls.get_logger('error', 'ERROR')
    
    @classmethod
    def clear_loggers(cls):
        """Clear all loggers"""
        cls._loggers.clear()
