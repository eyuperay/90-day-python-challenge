"""
Authentication module tests
"""

import unittest
from features.auth import AuthManager


class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager"""
    
    def test_version(self):
        auth = AuthManager()
        self.assertEqual(auth.get_version(), "1.0.0")
    
    def test_features(self):
        auth = AuthManager()
        self.assertIn("login", auth.get_features())
        self.assertIn("logout", auth.get_features())


if __name__ == "__main__":
    unittest.main()
