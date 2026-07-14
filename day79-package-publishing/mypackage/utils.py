"""
Utilities module
"""

import json
import os
import time
import functools
from typing import Any, Dict, List, Optional


def read_file(filename: str) -> Optional[str]:
    """
    Read file content
    
    Args:
        filename: File path
    
    Returns:
        File content or None if error
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_file(filename: str, content: str) -> bool:
    """
    Write content to file
    
    Args:
        filename: File path
        content: Content to write
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def json_to_dict(json_str: str) -> Optional[Dict]:
    """
    Convert JSON string to dictionary
    
    Args:
        json_str: JSON string
    
    Returns:
        Dictionary or None if error
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def dict_to_json(data: Dict, indent: int = 2) -> Optional[str]:
    """
    Convert dictionary to JSON string
    
    Args:
        data: Dictionary
        indent: Indentation level
    
    Returns:
        JSON string or None if error
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as e:
        print(f"Error converting to JSON: {e}")
        return None


def timer(func):
    """
    Decorator to measure function execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[Timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def log_function(func):
    """
    Decorator to log function calls
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Log] Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[Log] {func.__name__} returned: {result}")
        return result
    return wrapper
