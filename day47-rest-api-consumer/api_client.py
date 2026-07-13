"""
API Client module for consuming REST APIs
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class APIClient:
    """REST API client for various public APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
    
    def get_exchange_rates(self, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        """
        Fetch exchange rates from ExchangeRate-API
        
        Args:
            base_currency: Base currency code (e.g., USD, EUR, TRY)
        
        Returns:
            Dictionary with exchange rate data or None if error
        """
        try:
            url = f"{self.base_url}/{base_currency}"
            print(f"[API] Fetching rates for {base_currency}...")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"[OK] Successfully fetched rates for {base_currency}")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON response: {e}")
            return None
    
    def get_weather_data(self, city: str = "London") -> Optional[Dict[str, Any]]:
        """
        Fetch weather data from OpenWeatherMap API (demo)
        Note: This is a demo function showing the structure
        
        Args:
            city: City name
        
        Returns:
            Weather data or None
        """
        # This is a demo - real API key would be needed
        print(f"[API] Weather API demo - would fetch data for {city}")
        return {
            "city": city,
            "temperature": 22.5,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 12.3,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_response(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Save API response to JSON file
        
        Args:
            data: Dictionary data to save
            filename: Output filename
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs("data", exist_ok=True)
            filepath = f"data/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Response saved to: {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save response: {e}")
            return False
    
    def get_multiple_currencies(self, base_currency: str = "USD", 
                                target_currencies: list = None) -> Dict[str, float]:
        """
        Get specific exchange rates for multiple currencies
        
        Args:
            base_currency: Base currency code
            target_currencies: List of target currency codes
        
        Returns:
            Dictionary with currency rates
        """
        if target_currencies is None:
            target_currencies = ["TRY", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY"]
        
        data = self.get_exchange_rates(base_currency)
        
        if not data or 'rates' not in data:
            return {}
        
        rates = {}
        for currency in target_currencies:
            if currency in data['rates']:
                rates[currency] = data['rates'][currency]
            else:
                rates[currency] = None
        
        return rates
    
    def get_currency_conversion(self, from_currency: str, to_currency: str, 
                                amount: float = 1.0) -> Optional[float]:
        """
        Convert amount from one currency to another
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            amount: Amount to convert
        
        Returns:
            Converted amount or None
        """
        data = self.get_exchange_rates(from_currency)
        
        if not data or 'rates' not in data or to_currency not in data['rates']:
            return None
        
        rate = data['rates'][to_currency]
        converted = amount * rate
        return round(converted, 2)