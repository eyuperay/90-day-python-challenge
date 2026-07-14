"""
Tests for core module
"""

import unittest
from mypackage.core import (
    greet,
    reverse_string,
    count_vowels,
    is_palindrome,
    factorial,
    fibonacci
)


class TestCore(unittest.TestCase):
    """Test cases for core module"""
    
    def test_greet(self):
        """Test greet function"""
        self.assertEqual(greet(), "Hello, World!")
        self.assertEqual(greet("Alice"), "Hello, Alice!")
    
    def test_reverse_string(self):
        """Test reverse_string function"""
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("python"), "nohtyp")
        self.assertEqual(reverse_string(""), "")
    
    def test_count_vowels(self):
        """Test count_vowels function"""
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("AEIOU"), 5)
        self.assertEqual(count_vowels("xyz"), 0)
        self.assertEqual(count_vowels("Hello World"), 3)
    
    def test_is_palindrome(self):
        """Test is_palindrome function"""
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("hello"))
    
    def test_factorial(self):
        """Test factorial function"""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(7), 5040)
        with self.assertRaises(ValueError):
            factorial(-1)
    
    def test_fibonacci(self):
        """Test fibonacci function"""
        self.assertEqual(fibonacci(0), [])
        self.assertEqual(fibonacci(1), [0])
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci(8), [0, 1, 1, 2, 3, 5, 8, 13])


if __name__ == "__main__":
    unittest.main()
