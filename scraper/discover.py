"""
Phase 1: Discover apartments near every transit station.
Uses Google Places Nearby Search API with station-radius methodology.

Usage:
    export GOOGLE_PLACES_API_KEY="your-key-here"
    python discover.py

Output: data/discovered.json
"""

import os
import json
import time
import requests
from stations import STATIONS, SEARCH_RADIUS_METERS

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
if not API_KEY:
    raise ValueError("Set GOOGLE_PLACES_API_KEY environment variable")

NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAIL_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def search_station(name, station):
    """Search for apartment complexes near a single station."""
    print(f"  Searching near {name}...")
    results = []
    params = {
        "location": f"{station['lat']},{station['lng']}",
        "radius": SEARCH_RADIUS_METERS,
        "type": "apartment_complex",  # Also catches apartment_building
        "key": API_KEY,
    }

    resp = requests.get(NEARBY_URL, params=params)
    data = resp.json()

    if data.get("status") != "OK":
        print(f"    Warning: {data.get('status')} - {data.get('error_message', '')}")
        return results

    for place in data.get("results", []):
        results.append({
            "place_id": place["place_id"],
            "name": place["name"],
            "address": place.get("vicinity", ""),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "rating": place.get("rating"),
            "reviews": place.get("user_ratings_total", 0),
            "types": place.get("types", []),
            "nearest_station": name,
            "transit": station["transit"],
        })

    # Handle pagination (Google returns max 20 per page)
    next_token = data.get("next_page_token")
    while next_token:
        time.sleep(2)  # Google requires delay before using next_page_token
        params["pagetoken"] = next_token
        resp = requests.get(NEARBY_URL, params=params)
        data = resp.json()
        for place in data.get("results", []):
            results.append({
                "place_id": place["place_id"],
                "name": place["name"],
                "address": place.get("vicinity", ""),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "rating": place.get("rating"),
                "reviews": place.get("user_ratings_total", 0),
                "types": place.get("types", []),
                "nearest_station": name,
                "transit": station["transit"],
            })
        next_token = data.get("next_page_token")

    print(f"    Found {len(results)} results")
    return results


def get_place_details(place_id):
    """Get website and phone from Place Details API."""
    params = {
        "place_id": place_id,
        "fields": "website,formatted_phone_number,name",
        "key": API_KEY,
    }
    resp = requests.get(DETAIL_URL, params=params)
    data = resp.json()
    result = data.get("result", {})
    return {
        "website": result.get("website"),
        "phone": result.get("formatted_phone_number"),
    }


def deduplicate(all_results):
    """Deduplicate by place_id, keeping the entry with most info."""
    seen = {}
    for r in all_results:
        pid = r["place_id"]
        if pid not in seen or (r.get("reviews", 0) > seen[pid].get("reviews", 0)):
            seen[pid] = r
    return list(seen.values())


def discover():
    print(f"Discovering apartments near {len(STATIONS)} transit stations...")
    print(f"Search radius: {SEARCH_RADIUS_METERS}m per station\n")

    all_results = []
    for name, station in STATIONS.items():
        results = search_station(name, station)
        all_results.extend(results)
        time.sleep(0.5)  # Rate limiting

    print(f"\nTotal raw results: {len(all_results)}")

    # Deduplicate
    unique = deduplicate(all_results)
    print(f"After deduplication: {len(unique)}")

    # Filter to apartment-like types
    apartments = [
        a for a in unique
        if any(t in a.get("types", []) for t in [
            "apartment_complex", "apartment_building",
            "real_estate_agency"  # Many apartments show as this
        ])
    ]
    print(f"After type filtering: {len(apartments)}")

    # Enrich with details (website + phone)
    print("\nFetching details (website + phone)...")
    for i, apt in enumerate(apartments):
        details = get_place_details(apt["place_id"])
        apt["website"] = details.get("website")
        apt["phone"] = details.get("phone")
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{len(apartments)} done")
        time.sleep(0.2)

    # Sort by rating
    apartments.sort(key=lambda a: a.get("rating", 0) or 0, reverse=True)

    # Save
    os.makedirs("data", exist_ok=True)
    with open("data/discovered.json", "w") as f:
        json.dump(apartments, f, indent=2)

    print(f"\nSaved {len(apartments)} apartments to data/discovered.json")
    return apartments


if __name__ == "__main__":
    discover()
