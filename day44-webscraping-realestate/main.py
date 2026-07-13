#!/usr/bin/env python3
"""
Day 44 - Web Scraping: Real Estate Prices
A simple scraper to collect apartment listings from your neighborhood
"""

import os
import pandas as pd
from datetime import datetime
from realestate_scraper import RealEstateScraper


def main():
    print("=" * 60)
    print("NEIGHBORHOOD REAL ESTATE LISTINGS SCRAPER")
    print("=" * 60)

    # Get user input
    city = input("Enter city name (e.g., Istanbul): ").strip()
    neighborhood = input("Enter neighborhood name (e.g., Kadikoy): ").strip()
    
    pages_input = input("How many pages to scrape? (default: 3): ").strip()
    pages = 3
    if pages_input:
        try:
            pages = int(pages_input)
            if pages < 1:
                pages = 1
        except ValueError:
            print("Invalid input. Using default: 3 pages.")

    print(f"\nScraping {city} - {neighborhood} for {pages} pages...\n")

    # Initialize scraper
    scraper = RealEstateScraper(city, neighborhood)

    print("NOTE: This is a demonstration version.")
    print("Update URL and selectors in 'realestate_scraper.py' for real usage.\n")

    listings = scraper.scrape(page_count=pages)

    if not listings:
        print("No listings found. Please check URL and selectors.")
        return

    # Create DataFrame
    df = pd.DataFrame(listings)

    # Clean and sort data
    df = df.drop_duplicates(subset=["title", "price_try"])
    df = df.sort_values("price_try", ascending=False)

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/realestate_{city}_{neighborhood}_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"\n✅ Data saved: {filename}")

    # Display statistics
    stats = scraper.get_statistics()
    print("\nSUMMARY STATISTICS")
    print("-" * 50)
    print(f"Total Listings : {stats.get('total_listings', 0)}")
    print(f"Average Price  : {stats.get('avg_price', 0):,.0f} TRY")
    print(f"Lowest Price   : {stats.get('min_price', 0):,.0f} TRY")
    print(f"Highest Price  : {stats.get('max_price', 0):,.0f} TRY")
    print(f"Average SQM    : {stats.get('avg_sqm', 0)} m²")
    print(f"Price per SQM  : {stats.get('price_per_sqm', 0):,.0f} TRY/m²")

    # Show top 5
    print("\nTOP 5 MOST EXPENSIVE LISTINGS")
    print("-" * 50)
    for idx, row in df.head(5).iterrows():
        print(f"{row['title'][:35]:35} | {row['price_try']:>12,.0f} TRY | {row['square_meters']:>6} m²")

    print("\n🎉 Process completed successfully!")


if __name__ == "__main__":
    main()