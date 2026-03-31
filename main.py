"""
South Bay Transit Apartments — Full Pipeline

Runs all three phases:
  1. Discover apartments near every transit station (Google Places API)
  2. Scrape pricing from apartment websites
  3. Build the HTML dashboard

Usage:
    export GOOGLE_PLACES_API_KEY="your-key-here"
    python main.py
"""

import sys
import os

# Add scraper dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scraper"))

from discover import discover
from scrape_prices import scrape_all
from build_dashboard import build


def main():
    print("=" * 60)
    print("SOUTH BAY TRANSIT APARTMENTS — DATA PIPELINE")
    print("=" * 60)

    print("\n📍 PHASE 1: Discovering apartments near transit stations...")
    print("-" * 60)
    discover()

    print("\n\n💰 PHASE 2: Scraping pricing from websites...")
    print("-" * 60)
    scrape_all()

    print("\n\n🗺️  PHASE 3: Building HTML dashboard...")
    print("-" * 60)
    build()

    print("\n" + "=" * 60)
    print("DONE! Open index.html in your browser.")
    print("=" * 60)


if __name__ == "__main__":
    main()
