"""
MyPackage - A sample Python package

This package provides various utility functions for:
- Mathematical operations
- String manipulations
- Data processing
"""

from mypackage.core import (
    greet,
    reverse_string,
    count_vowels,
    is_palindrome,
    factorial,
    fibonacci
)

from mypackage.math_utils import (
    add,
    subtract,
    multiply,
    divide,
    power,
    sqrt,
    average,
    median,
    mode,
    is_prime,
    gcd,
    lcm
)

from mypackage.utils import (
    read_file,
    write_file,
    json_to_dict,
    dict_to_json,
    timer,
    log_function
)

__version__ = "1.0.0"
__all__ = [
    # core
    "greet",
    "reverse_string",
    "count_vowels",
    "is_palindrome",
    "factorial",
    "fibonacci",
    # math_utils
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "sqrt",
    "average",
    "median",
    "mode",
    "is_prime",
    "gcd",
    "lcm",
    # utils
    "read_file",
    "write_file",
    "json_to_dict",
    "dict_to_json",
    "timer",
    "log_function"
]
