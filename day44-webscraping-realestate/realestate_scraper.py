"""
Real Estate Scraper - Fetches property listings from specified city/neighborhood
"""

import time
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Import helpers
from utils.helpers import clean_price, clean_square_meters, clean_room_count, clean_text


class RealEstateScraper:
    """Main class for scraping real estate listings"""

    def __init__(self, city: str, neighborhood: str):
        self.city = city
        self.neighborhood = neighborhood
        self.ua = UserAgent()
        self.listings = []
        self.base_url = "https://www.sahibinden.com"  # Change as needed

    def _get_headers(self) -> dict:
        """Returns random User-Agent for each request"""
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def _fetch_page(self, url: str):
        """Fetches page from URL and returns BeautifulSoup object"""
        try:
            print(f"Fetching page: {url}")
            response = requests.get(url, headers=self._get_headers(), timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def scrape(self, page_count: int = 3):
        """Scrapes listings for the specified number of pages"""
        print(f"Searching listings for {self.city} - {self.neighborhood}...")

        for page in range(1, page_count + 1):
            # Example URL - UPDATE THIS FOR REAL WEBSITE
            url = f"{self.base_url}/search?query={self.city}+{self.neighborhood}+satilik+daire&page={page}"

            soup = self._fetch_page(url)
            if not soup:
                continue

            # UPDATE THESE SELECTORS according to target website
            listing_cards = soup.find_all("div", class_="searchResultsItem")  # Example selector

            if not listing_cards:
                print(f"No listings found on page {page}.")
                continue

            for card in listing_cards:
                try:
                    # Price
                    price_elem = card.find("span", class_="price")  # Update selector
                    price = clean_price(price_elem.text if price_elem else "")

                    # Title
                    title_elem = card.find("a", class_="title")  # Update selector
                    title = clean_text(title_elem.text if title_elem else "Not Specified")

                    # Square meters
                    sqm_elem = card.find("span", class_="size")  # Update selector
                    square_meters = clean_square_meters(sqm_elem.text if sqm_elem else "")

                    # Room count
                    room_elem = card.find("span", class_="room")  # Update selector
                    room = clean_room_count(room_elem.text if room_elem else "Unknown")

                    self.listings.append({
                        "title": title,
                        "price_try": price,
                        "square_meters": square_meters,
                        "room_count": room,
                        "city": self.city,
                        "neighborhood": self.neighborhood,
                        "source": url
                    })

                except Exception as e:
                    print(f"Error processing a listing: {e}")
                    continue

            print(f"Page {page} complete. Total listings: {len(self.listings)}")
            time.sleep(random.uniform(2, 4))  # Be polite

        print(f"Scraping finished! Total {len(self.listings)} listings collected.")
        return self.listings

    def get_statistics(self) -> dict:
        """Calculates basic statistics"""
        if not self.listings:
            return {"error": "No listings scraped yet!"}

        import statistics

        prices = [item["price_try"] for item in self.listings if item["price_try"] > 0]
        sqm_values = [item["square_meters"] for item in self.listings if item["square_meters"] > 0]

        if not prices:
            return {"total_listings": len(self.listings), "error": "No valid prices"}

        return {
            "total_listings": len(self.listings),
            "avg_price": round(statistics.mean(prices), 0),
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_sqm": round(statistics.mean(sqm_values), 1) if sqm_values else 0,
            "price_per_sqm": round(statistics.mean(prices) / statistics.mean(sqm_values), 0) if sqm_values else 0
        }