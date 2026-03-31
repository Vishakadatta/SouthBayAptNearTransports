"""
Phase 2: Scrape 1BR/1BA pricing from apartment websites.
Reads data/discovered.json, attempts to find pricing, outputs data/apartments.json

Usage:
    python scrape_prices.py

Handles common platforms: RentCafe, Yardi, Entrata, custom sites.
Falls back gracefully — website + phone are always kept even if price can't be found.
"""

import json
import re
import time
import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Price patterns to look for
PRICE_PATTERNS = [
    # $2,450 or $2450
    r'\$[\s]?([\d,]+)\s*[-–/]\s*\$?([\d,]+)',  # Range: $2,450 - $3,200
    r'\$[\s]?([\d,]+)\s*(?:per\s*month|/\s*mo|/mo)',  # $2,450/mo
    r'(?:starting\s*(?:at|from)\s*)\$[\s]?([\d,]+)',  # Starting at $2,450
    r'(?:from\s*)\$[\s]?([\d,]+)',  # From $2,450
    r'\$[\s]?([\d,]+)',  # Plain $2,450
]

# Keywords that indicate 1BR content
BR1_KEYWORDS = [
    "1 bed", "1bed", "1-bed", "one bed", "1 br", "1br", "1-br",
    "one bedroom", "1 bedroom", "1-bedroom", "studio",  # Include studio as fallback
]


def extract_prices_from_text(text):
    """Find all dollar amounts in text that look like monthly rent."""
    prices = []
    for pattern in PRICE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                for m in match:
                    if m:
                        price = int(m.replace(",", ""))
                        if 800 <= price <= 8000:  # Reasonable rent range
                            prices.append(price)
            else:
                price = int(match.replace(",", ""))
                if 800 <= price <= 8000:
                    prices.append(price)
    return prices


def find_1br_price(text):
    """Try to find a 1BR-specific price in the page text."""
    text_lower = text.lower()

    # Look for 1BR section and grab nearby prices
    for keyword in BR1_KEYWORDS:
        idx = text_lower.find(keyword)
        if idx != -1:
            # Extract ~500 chars around the keyword
            context = text[max(0, idx - 100):idx + 400]
            prices = extract_prices_from_text(context)
            if prices:
                return min(prices)  # Return lowest (starting price)

    # Fallback: just grab all prices and return the lowest reasonable one
    all_prices = extract_prices_from_text(text)
    if all_prices:
        return min(all_prices)

    return None


def scrape_website(url):
    """Attempt to scrape pricing from an apartment website."""
    if not url:
        return None

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        if resp.status_code != 200:
            return None

        text = resp.text

        # Check for common floor plan / pricing page links
        pricing_paths = ["/floor-plans", "/floorplans", "/pricing", "/apartments", "/availability"]
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        # Try the main page first
        price = find_1br_price(text)
        if price:
            return price

        # Try common pricing subpages
        for path in pricing_paths:
            try:
                resp2 = requests.get(base + path, headers=HEADERS, timeout=8, allow_redirects=True)
                if resp2.status_code == 200:
                    price = find_1br_price(resp2.text)
                    if price:
                        return price
            except Exception:
                continue

    except Exception as e:
        print(f"    Error scraping {url}: {e}")

    return None


def city_from_address(address):
    """Extract city from address string."""
    cities = [
        "Milpitas", "Fremont", "Hayward", "Santa Clara", "San Jose",
        "Mountain View", "Sunnyvale", "Palo Alto", "Menlo Park",
    ]
    for city in cities:
        if city.lower() in address.lower():
            return city
    return "Unknown"


def scrape_all():
    # Load discovered data
    with open("data/discovered.json") as f:
        apartments = json.load(f)

    print(f"Scraping prices for {len(apartments)} apartments...\n")

    results = []
    found_count = 0

    for i, apt in enumerate(apartments):
        website = apt.get("website")
        price = None

        if website:
            print(f"  [{i+1}/{len(apartments)}] {apt['name']} — {website}")
            price = scrape_website(website)
            if price:
                found_count += 1
                print(f"    Found: ${price:,}/mo")
            else:
                print(f"    No price found (website link saved)")
            time.sleep(1)  # Be polite
        else:
            print(f"  [{i+1}/{len(apartments)}] {apt['name']} — no website")

        results.append({
            "name": apt["name"],
            "address": apt.get("address", ""),
            "city": city_from_address(apt.get("address", "")),
            "rating": apt.get("rating"),
            "reviews": apt.get("reviews", 0),
            "phone": apt.get("phone"),
            "transit": apt.get("transit", ""),
            "lat": apt["lat"],
            "lng": apt["lng"],
            "place_id": apt["place_id"],
            "website": website,
            "price_1br": price,
        })

    # Save final data
    with open("data/apartments.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone! {found_count}/{len(apartments)} prices found")
    print(f"Saved to data/apartments.json")


if __name__ == "__main__":
    scrape_all()
