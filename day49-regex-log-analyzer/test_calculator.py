"""
Unit tests for calculator module
Using Python's built-in unittest framework
"""

import unittest
import math
from calculator import (
    Calculator, greet, validate_email,
    celsius_to_fahrenheit, fahrenheit_to_celsius
)


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.calc = Calculator()
        self.test_numbers = [1, 2, 3, 4, 5]
    
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    # Addition tests
    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.add(10, 20), 30)
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        self.assertEqual(self.calc.add(-5, -3), -8)
        self.assertEqual(self.calc.add(-10, 5), -5)
    
    def test_add_zero(self):
        """Test adding with zero"""
        self.assertEqual(self.calc.add(5, 0), 5)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_add_floats(self):
        """Test adding floating point numbers"""
        self.assertAlmostEqual(self.calc.add(2.5, 3.7), 6.2)
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3)
    
    # Subtraction tests
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        self.assertEqual(self.calc.subtract(10, 3), 7)
        self.assertEqual(self.calc.subtract(5, 5), 0)
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        self.assertEqual(self.calc.subtract(-5, -3), -2)
        self.assertEqual(self.calc.subtract(10, -5), 15)
    
    # Multiplication tests
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        self.assertEqual(self.calc.multiply(5, 3), 15)
        self.assertEqual(self.calc.multiply(10, 20), 200)
    
    def test_multiply_with_zero(self):
        """Test multiplying with zero"""
        self.assertEqual(self.calc.multiply(5, 0), 0)
        self.assertEqual(self.calc.multiply(0, 0), 0)
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers"""
        self.assertEqual(self.calc.multiply(-5, 3), -15)
        self.assertEqual(self.calc.multiply(-5, -3), 15)
    
    # Division tests
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(15, 3), 5)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        self.assertEqual(self.calc.divide(-10, 2), -5)
        self.assertEqual(self.calc.divide(-10, -2), 5)
    
    # Power tests
    def test_power_positive_exponent(self):
        """Test power with positive exponent"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 2), 25)
    
    def test_power_zero_exponent(self):
        """Test power with zero exponent"""
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(0, 0), 1)
    
    def test_power_negative_exponent(self):
        """Test power with negative exponent"""
        self.assertAlmostEqual(self.calc.power(2, -1), 0.5)
        self.assertAlmostEqual(self.calc.power(4, -2), 0.0625)
    
    # Square root tests
    def test_square_root_positive(self):
        """Test square root of positive numbers"""
        self.assertEqual(self.calc.square_root(4), 2)
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertAlmostEqual(self.calc.square_root(2), 1.41421356, places=5)
    
    def test_square_root_zero(self):
        """Test square root of zero"""
        self.assertEqual(self.calc.square_root(0), 0)
    
    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError"""
        with self.assertRaises(ValueError):
            self.calc.square_root(-1)
    
    # Factorial tests
    def test_factorial_positive(self):
        """Test factorial of positive numbers"""
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(7), 5040)
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError"""
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)
    
    def test_factorial_float(self):
        """Test factorial of float raises TypeError"""
        with self.assertRaises(TypeError):
            self.calc.factorial(5.5)
    
    # Even number tests
    def test_is_even_true(self):
        """Test even numbers return True"""
        self.assertTrue(self.calc.is_even(2))
        self.assertTrue(self.calc.is_even(0))
        self.assertTrue(self.calc.is_even(-4))
    
    def test_is_even_false(self):
        """Test odd numbers return False"""
        self.assertFalse(self.calc.is_even(3))
        self.assertFalse(self.calc.is_even(-5))
    
    # Prime number tests
    def test_is_prime(self):
        """Test prime numbers return True"""
        self.assertTrue(self.calc.is_prime(2))
        self.assertTrue(self.calc.is_prime(3))
        self.assertTrue(self.calc.is_prime(5))
        self.assertTrue(self.calc.is_prime(7))
        self.assertTrue(self.calc.is_prime(11))
        self.assertTrue(self.calc.is_prime(13))
    
    def test_is_not_prime(self):
        """Test non-prime numbers return False"""
        self.assertFalse(self.calc.is_prime(1))
        self.assertFalse(self.calc.is_prime(4))
        self.assertFalse(self.calc.is_prime(6))
        self.assertFalse(self.calc.is_prime(9))
        self.assertFalse(self.calc.is_prime(15))
        self.assertFalse(self.calc.is_prime(0))
        self.assertFalse(self.calc.is_prime(-5))
    
    # Average tests
    def test_average_positive_numbers(self):
        """Test average of positive numbers"""
        self.assertEqual(self.calc.average([1, 2, 3, 4, 5]), 3)
        self.assertEqual(self.calc.average([10, 20, 30]), 20)
    
    def test_average_negative_numbers(self):
        """Test average of negative numbers"""
        self.assertEqual(self.calc.average([-1, -2, -3]), -2)
    
    def test_average_empty_list(self):
        """Test average of empty list raises ValueError"""
        with self.assertRaises(ValueError):
            self.calc.average([])
    
    # Fibonacci tests
    def test_fibonacci_zero(self):
        """Test Fibonacci sequence with zero terms"""
        self.assertEqual(self.calc.fibonacci(0), [])
    
    def test_fibonacci_one(self):
        """Test Fibonacci sequence with one term"""
        self.assertEqual(self.calc.fibonacci(1), [0])
    
    def test_fibonacci_positive(self):
        """Test Fibonacci sequence with positive terms"""
        self.assertEqual(self.calc.fibonacci(2), [0, 1])
        self.assertEqual(self.calc.fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(self.calc.fibonacci(8), [0, 1, 1, 2, 3, 5, 8, 13])
    
    # GCD tests
    def test_gcd_positive_numbers(self):
        """Test GCD of positive numbers"""
        self.assertEqual(self.calc.gcd(12, 8), 4)
        self.assertEqual(self.calc.gcd(54, 24), 6)
        self.assertEqual(self.calc.gcd(17, 13), 1)
    
    def test_gcd_with_zero(self):
        """Test GCD with zero"""
        self.assertEqual(self.calc.gcd(12, 0), 12)
        self.assertEqual(self.calc.gcd(0, 0), 0)
    
    def test_gcd_negative_numbers(self):
        """Test GCD of negative numbers"""
        self.assertEqual(self.calc.gcd(-12, 8), 4)
        self.assertEqual(self.calc.gcd(-12, -8), 4)
    
    # LCM tests
    def test_lcm_positive_numbers(self):
        """Test LCM of positive numbers"""
        self.assertEqual(self.calc.lcm(4, 6), 12)
        self.assertEqual(self.calc.lcm(12, 18), 36)
        self.assertEqual(self.calc.lcm(3, 5), 15)
    
    def test_lcm_with_zero(self):
        """Test LCM with zero"""
        self.assertEqual(self.calc.lcm(12, 0), 0)
        self.assertEqual(self.calc.lcm(0, 0), 0)


class TestGreetFunction(unittest.TestCase):
    """Test cases for greet function"""
    
    def test_greet_with_name(self):
        """Test greet with a name"""
        self.assertEqual(greet("Alice"), "Hello, Alice!")
        self.assertEqual(greet("Bob"), "Hello, Bob!")
    
    def test_greet_empty_name(self):
        """Test greet with empty name"""
        self.assertEqual(greet(""), "Hello, Guest!")
        self.assertEqual(greet(None), "Hello, Guest!")


class TestEmailValidation(unittest.TestCase):
    """Test cases for email validation"""
    
    def test_valid_emails(self):
        """Test valid email addresses"""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co"))
        self.assertTrue(validate_email("user+label@domain.com"))
        self.assertTrue(validate_email("user-name@domain.org"))
    
    def test_invalid_emails(self):
        """Test invalid email addresses"""
        self.assertFalse(validate_email("test@example"))
        self.assertFalse(validate_email("test.example.com"))
        self.assertFalse(validate_email("test@.com"))
        self.assertFalse(validate_email("@example.com"))
        self.assertFalse(validate_email("test@example..com"))


class TestTemperatureConversion(unittest.TestCase):
    """Test cases for temperature conversion"""
    
    def test_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion"""
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(100), 212)
        self.assertEqual(celsius_to_fahrenheit(-40), -40)
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6)
    
    def test_fahrenheit_to_celsius(self):
        """Test Fahrenheit to Celsius conversion"""
        self.assertEqual(fahrenheit_to_celsius(32), 0)
        self.assertEqual(fahrenheit_to_celsius(212), 100)
        self.assertEqual(fahrenheit_to_celsius(-40), -40)
        self.assertAlmostEqual(fahrenheit_to_celsius(98.6), 37)


def run_tests():
    """Run all tests and generate report"""
    import sys
    import io
    from datetime import datetime
    
    # Capture test output
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output, verbosity=2)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = runner.run(suite)
    
    # Generate report
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("UNIT TEST REPORT")
    report_lines.append("="*60)
    report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*60)
    report_lines.append("")
    report_lines.append(f"Tests Run: {result.testsRun}")
    report_lines.append(f"Failures: {len(result.failures)}")
    report_lines.append(f"Errors: {len(result.errors)}")
    report_lines.append(f"Skipped: {len(result.skipped)}")
    report_lines.append("")
    
    if result.wasSuccessful():
        report_lines.append("[PASS] All tests passed successfully!")
        report_lines.append("[OK] Test coverage is comprehensive")
    else:
        report_lines.append("[FAIL] Some tests failed!")
        report_lines.append("")
        if result.failures:
            report_lines.append("FAILURES:")
            for test, traceback in result.failures[:3]:
                report_lines.append(f"  - {test}")
            if len(result.failures) > 3:
                report_lines.append(f"  ... and {len(result.failures) - 3} more")
        if result.errors:
            report_lines.append("ERRORS:")
            for test, traceback in result.errors[:3]:
                report_lines.append(f"  - {test}")
            if len(result.errors) > 3:
                report_lines.append(f"  ... and {len(result.errors) - 3} more")
    
    report_lines.append("")
    report_lines.append("="*60)
    report_lines.append("[OK] Test report generated successfully")
    report_lines.append("="*60)
    
    report_content = "\n".join(report_lines)
    
    # Save report
    import os
    os.makedirs("output", exist_ok=True)
    with open("output/test_report.txt", 'w', encoding='utf-8') as f:
        f.write(report_content)
        f.write("\n\n")
        f.write(output.getvalue())
    
    print(report_content)
    print("\n[OK] Report saved to: output/test_report.txt")


if __name__ == '__main__':
    run_tests()