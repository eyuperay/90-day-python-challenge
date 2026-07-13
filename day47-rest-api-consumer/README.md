# Day 47 - REST API Consumer

## About This Project
This project demonstrates consuming REST APIs in Python. It fetches real-time exchange rates from ExchangeRate-API and simulates weather data retrieval.

## Features
- Fetch real-time exchange rates
- Extract rates for specific currencies
- Perform currency conversions
- Save data to CSV and JSON
- Display formatted reports

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Check outputs
- CSV reports: output/exchange_rates_*.csv
- JSON data: data/*.json

## API Endpoints Used

### ExchangeRate-API (Free)
- Endpoint: https://api.exchangerate-api.com/v4/latest/{BASE}
- Method: GET
- Response: Exchange rates for all currencies

## Output Files

### CSV Reports
- exchange_rates_USD_*.csv - USD base rates
- exchange_rates_EUR_*.csv - EUR base rates

### JSON Data
- usd_exchange_rates.json - Raw API response
- eur_exchange_rates.json - Raw API response
- weather_demo.json - Demo weather data

## Features Demonstrated
- GET requests with requests library
- JSON response parsing
- Error handling for API calls
- Data extraction and transformation
- CSV and JSON export

## Libraries Used
- requests - HTTP client
- pandas - Data processing and CSV export

## API Documentation
- ExchangeRate-API: https://exchangerate-api.com/documentation
- OpenWeatherMap: https://openweathermap.org/api

## Learning Objectives
- REST API concepts
- Making HTTP requests in Python
- Handling JSON responses
- Error handling for APIs
- Data export and reporting