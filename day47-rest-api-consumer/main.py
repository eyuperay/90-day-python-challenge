#!/usr/bin/env python3
"""
Day 47 - REST API Consumer
Consume REST APIs for exchange rates and weather data
"""

import os
import json
import pandas as pd
from datetime import datetime
from api_client import APIClient


def display_exchange_rates(rates: dict, base_currency: str):
    """Display exchange rates in a formatted table"""
    print("\n" + "="*60)
    print(f"EXCHANGE RATES (Base: {base_currency})")
    print("="*60)
    print(f"{'Currency':<10} {'Rate':>15} {'Converted (1 USD)':>20}")
    print("-"*60)
    
    for currency, rate in sorted(rates.items()):
        if rate:
            converted = round(1 * rate, 2)
            print(f"{currency:<10} {rate:>15,.4f} {converted:>20,.2f}")
        else:
            print(f"{currency:<10} {'N/A':>15} {'N/A':>20}")
    
    print("="*60 + "\n")


def save_rates_to_csv(rates: dict, base_currency: str, filename: str = None):
    """Save exchange rates to CSV file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exchange_rates_{base_currency}_{timestamp}.csv"
    
    os.makedirs("output", exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame([
        {"Currency": curr, "Rate": rate, "Base": base_currency}
        for curr, rate in rates.items() if rate is not None
    ])
    
    # Add converted column
    df["Converted (1 USD)"] = df["Rate"].apply(lambda x: round(1 * x, 2))
    
    # Sort by rate
    df = df.sort_values("Rate", ascending=False)
    
    # Save to CSV
    filepath = f"output/{filename}"
    df.to_csv(filepath, index=False)
    print(f"[OK] Rates saved to: {filepath}")
    
    return df


def perform_currency_conversions(api_client: APIClient):
    """Perform and display currency conversions"""
    print("\n" + "="*60)
    print("CURRENCY CONVERSIONS")
    print("="*60)
    
    conversions = [
        ("USD", "TRY", 100),
        ("EUR", "USD", 100),
        ("TRY", "EUR", 1000),
        ("GBP", "USD", 50),
        ("USD", "EUR", 200),
    ]
    
    print(f"{'From':<10} {'To':<10} {'Amount':>12} {'Converted':>15}")
    print("-"*60)
    
    for from_curr, to_curr, amount in conversions:
        result = api_client.get_currency_conversion(from_curr, to_curr, amount)
        if result:
            print(f"{from_curr:<10} {to_curr:<10} {amount:>12,.2f} {result:>15,.2f}")
        else:
            print(f"{from_curr:<10} {to_curr:<10} {amount:>12,.2f} {'N/A':>15}")
    
    print("="*60 + "\n")


def display_weather_data(weather_data: dict):
    """Display weather data in formatted output"""
    print("\n" + "="*60)
    print("WEATHER DATA (Demo)")
    print("="*60)
    
    print(f"City: {weather_data.get('city', 'Unknown')}")
    print(f"Temperature: {weather_data.get('temperature', 'N/A')}°C")
    print(f"Condition: {weather_data.get('condition', 'N/A')}")
    print(f"Humidity: {weather_data.get('humidity', 'N/A')}%")
    print(f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} km/h")
    print(f"Timestamp: {weather_data.get('timestamp', 'N/A')}")
    
    print("="*60 + "\n")
    
    # Save weather data
    os.makedirs("data", exist_ok=True)
    with open("data/weather_demo.json", 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2)
    print("[OK] Weather data saved to: data/weather_demo.json\n")


def main():
    print("=" * 60)
    print("DAY 47 - REST API CONSUMER")
    print("=" * 60 + "\n")
    
    # Initialize API client
    api_client = APIClient()
    
    # 1. Get exchange rates for USD
    print("[1] Fetching Exchange Rates...")
    usd_rates = api_client.get_exchange_rates("USD")
    
    if usd_rates:
        # Extract rates for specific currencies
        target_currencies = ["TRY", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "RUB", "BRL"]
        
        rates = {}
        for currency in target_currencies:
            if currency in usd_rates['rates']:
                rates[currency] = usd_rates['rates'][currency]
            else:
                rates[currency] = None
        
        # Display rates
        display_exchange_rates(rates, "USD")
        
        # Save to CSV
        df = save_rates_to_csv(rates, "USD")
        
        # Save raw JSON
        api_client.save_response(usd_rates, "usd_exchange_rates.json")
        
        # Perform conversions
        perform_currency_conversions(api_client)
    
    # 2. Get exchange rates for EUR
    print("\n[2] Fetching Exchange Rates for EUR...")
    eur_rates = api_client.get_exchange_rates("EUR")
    
    if eur_rates:
        # Extract TRY and USD rates
        rates = {
            "USD": eur_rates['rates'].get("USD"),
            "TRY": eur_rates['rates'].get("TRY"),
            "GBP": eur_rates['rates'].get("GBP")
        }
        
        display_exchange_rates(rates, "EUR")
        api_client.save_response(eur_rates, "eur_exchange_rates.json")
    
    # 3. Get weather data (demo)
    print("\n[3] Fetching Weather Data (Demo)...")
    weather = api_client.get_weather_data("Istanbul")
    display_weather_data(weather)
    
    # 4. Generate summary report
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    print("API Operations Completed:")
    print("  - Fetch exchange rates for USD and EUR")
    print("  - Extract rates for 10 currencies")
    print("  - Perform currency conversions")
    print("  - Save data to CSV and JSON")
    print("  - Weather data demo")
    print("\nOutput Files:")
    print("  - output/exchange_rates_USD_*.csv")
    print("  - output/exchange_rates_EUR_*.csv")
    print("  - data/usd_exchange_rates.json")
    print("  - data/eur_exchange_rates.json")
    print("  - data/weather_demo.json")
    print("="*60 + "\n")
    
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
    