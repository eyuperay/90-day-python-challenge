"""
Unit tests for CI/CD Demo App
"""

import unittest
import json
from app import app


class TestApp(unittest.TestCase):
    """Test cases for Flask app"""
    
    def setUp(self):
        """Set up test client"""
        self.client = app.test_client()
    
    def test_home_page(self):
        """Test home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CI/CD Demo App', response.data)
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
    
    def test_info_endpoint(self):
        """Test info endpoint"""
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['app'], 'CI/CD Demo')
        self.assertIn('version', data)
        self.assertIn('environment', data)
    
    def test_version_header(self):
        """Test version header"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
