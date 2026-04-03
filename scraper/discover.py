"""
Phase 1: Discover apartments near every transit station.
Uses Overpass API (OpenStreetMap) — completely free, no API key needed.

Strategy: batch ALL stations into a single Overpass query to avoid rate limiting,
then merge results with existing Google Places data.

Output: data/discovered.json
"""

import json
import math
import os
import re
import time
import traceback

import requests

from stations import STATIONS, SEARCH_RADIUS_METERS

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "SouthBayAptFinder/1.0 (apartment-search-tool)"}

# Patterns for generic building names to skip
GENERIC_NAME_RE = re.compile(
    r'^(building\s*[a-z0-9]{0,3}|bldg\s*[a-z0-9]{0,3}|[a-z]|[0-9]+|'
    r'unit\s*[a-z0-9]{0,3}|block\s*[a-z0-9]{0,3}|phase\s*[a-z0-9]{0,3}|'
    r'tower\s*[a-z0-9]{0,3}|lot\s*[a-z0-9]{0,3}|section\s*[a-z0-9]{0,3}|'
    r'campus village\s*\d+|parking.*|garage.*)$',
    re.IGNORECASE
)

EXCLUDE_KEYWORDS = [
    "mobile home", "rv park", "storage", "church", "school", "office",
    "hotel", "motel", " inn", "parking", "garage",
]


def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def is_valid_apartment_name(name):
    if not name or len(name) < 3:
        return False
    if GENERIC_NAME_RE.match(name.strip()):
        return False
    name_lower = name.lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in name_lower:
            return False
    return True


def get_center(element):
    if element["type"] == "node":
        return element.get("lat"), element.get("lon")
    center = element.get("center", {})
    return (center.get("lat"), center.get("lon")) if center else (None, None)


def city_from_coords(lat, lng):
    city_bounds = [
        ("Hayward", 37.60, 37.70, -122.12, -122.03),
        ("Union City", 37.57, 37.61, -122.06, -121.99),
        ("Fremont", 37.47, 37.58, -122.02, -121.90),
        ("Milpitas", 37.39, 37.47, -121.93, -121.85),
        ("San Jose", 37.24, 37.40, -121.97, -121.79),
        ("Santa Clara", 37.33, 37.41, -122.00, -121.93),
        ("Sunnyvale", 37.34, 37.41, -122.07, -121.99),
        ("Mountain View", 37.36, 37.42, -122.13, -122.05),
        ("Los Altos", 37.36, 37.40, -122.14, -122.09),
        ("Palo Alto", 37.39, 37.47, -122.19, -122.10),
        ("Menlo Park", 37.44, 37.49, -122.20, -122.14),
        ("Cupertino", 37.30, 37.34, -122.09, -121.99),
        ("Campbell", 37.27, 37.30, -121.96, -121.92),
    ]
    for city, lat_min, lat_max, lng_min, lng_max in city_bounds:
        if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
            return city
    return "Unknown"


def reverse_geocode_city(lat, lng):
    try:
        resp = requests.get("https://nominatim.openstreetmap.org/reverse", params={
            "lat": lat, "lon": lng, "format": "json", "zoom": 14,
        }, headers=HEADERS, timeout=10)
        addr = resp.json().get("address", {})
        return addr.get("city") or addr.get("town") or addr.get("suburb") or "Unknown"
    except Exception:
        return "Unknown"


def find_nearest_station(lat, lng):
    """Find the nearest transit station and its type."""
    best_name = ""
    best_type = ""
    best_dist = float("inf")
    for name, s in STATIONS.items():
        d = haversine_km(lat, lng, s["lat"], s["lng"])
        if d < best_dist:
            best_dist = d
            best_name = name
            best_type = s["transit"]
    # Collect ALL transit types within range
    transit_types = set()
    for name, s in STATIONS.items():
        d = haversine_km(lat, lng, s["lat"], s["lng"])
        if d <= SEARCH_RADIUS_METERS / 1000:
            transit_types.add(s["transit"])
    transit = "/".join(sorted(transit_types)) if transit_types else best_type
    return best_name, transit


def build_batch_query():
    """Build a single Overpass query covering the entire South Bay bounding box."""
    # Find bounding box of all stations + radius
    lats = [s["lat"] for s in STATIONS.values()]
    lngs = [s["lng"] for s in STATIONS.values()]
    # Approx 3km in degrees: ~0.027 lat, ~0.033 lng
    min_lat = min(lats) - 0.027
    max_lat = max(lats) + 0.027
    min_lng = min(lngs) - 0.033
    max_lng = max(lngs) + 0.033

    return f"""
[out:json][timeout:120];
(
  node["building"="apartments"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
  way["building"="apartments"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
  relation["building"="apartments"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
  node["building"="residential"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
  way["building"="residential"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
  relation["building"="residential"]["name"]({min_lat},{min_lng},{max_lat},{max_lng});
);
out center tags;
"""


def load_existing_data():
    """Load existing apartments.json to preserve Google Places data."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "apartments.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []


def discover():
    print(f"Discovering apartments across South Bay...")
    print(f"Search radius: {SEARCH_RADIUS_METERS}m per station ({len(STATIONS)} stations)")
    print("Using: Overpass API (OpenStreetMap) — no API key needed\n")

    # Load existing data from Google Places
    existing = load_existing_data()
    existing_names = {a["name"].lower().strip() for a in existing}
    print(f"Loaded {len(existing)} existing apartments from Google Places data")

    # Single batch query for the whole South Bay
    print("Querying Overpass API for all named apartments in South Bay...")
    query = build_batch_query()

    try:
        resp = requests.post(OVERPASS_URL, data={"data": query}, headers=HEADERS, timeout=120)
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
        print(f"Got {len(elements)} raw elements from OpenStreetMap")
    except Exception as e:
        print(f"ERROR: Overpass query failed: {e}")
        elements = []

    # Process and deduplicate
    new_apartments = {}
    for el in elements:
        lat, lng = get_center(el)
        if lat is None:
            continue

        tags = el.get("tags", {})
        apt_name = tags.get("name", "").strip()
        if not is_valid_apartment_name(apt_name):
            continue

        # Skip if already in existing Google data
        if apt_name.lower().strip() in existing_names:
            continue

        # Check if within 3km of any station
        nearest_name, transit = find_nearest_station(lat, lng)
        min_dist = min(
            haversine_km(lat, lng, s["lat"], s["lng"])
            for s in STATIONS.values()
        )
        if min_dist > SEARCH_RADIUS_METERS / 1000:
            continue

        city = city_from_coords(lat, lng)
        dedup_key = f"{apt_name.lower()}|{city}"

        if dedup_key not in new_apartments:
            addr_parts = []
            if tags.get("addr:housenumber"):
                addr_parts.append(tags["addr:housenumber"])
            if tags.get("addr:street"):
                addr_parts.append(tags["addr:street"])

            new_apartments[dedup_key] = {
                "name": apt_name,
                "address": " ".join(addr_parts),
                "city": city,
                "rating": 0,
                "reviews": 0,
                "phone": tags.get("phone") or tags.get("contact:phone"),
                "transit": transit,
                "lat": round(lat, 6),
                "lng": round(lng, 6),
                "place_id": "",
                "website": tags.get("website") or tags.get("contact:website"),
                "price_1br": None,
            }

    new_list = list(new_apartments.values())
    print(f"Found {len(new_list)} new apartments from OpenStreetMap (after filtering)")

    # Reverse geocode unknown cities
    unknown = [a for a in new_list if a.get("city") == "Unknown"]
    if unknown:
        print(f"Reverse geocoding {len(unknown)} unknown cities...")
        for i, apt in enumerate(unknown):
            apt["city"] = reverse_geocode_city(apt["lat"], apt["lng"])
            time.sleep(1.1)
            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{len(unknown)} done")

    # Merge: existing Google data + new OSM data
    merged = existing + new_list
    merged.sort(key=lambda a: (a.get("city", ""), a.get("name", "")))

    # Save
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "discovered.json")
    with open(out_path, "w") as f:
        json.dump(merged, f, indent=2)

    print(f"\nTotal: {len(existing)} (Google) + {len(new_list)} (OSM) = {len(merged)} apartments")
    print(f"Saved to {out_path}")

    # City breakdown
    from collections import Counter
    cities = Counter(a.get("city", "Unknown") for a in merged)
    print("\nBy city:")
    for city, count in cities.most_common():
        print(f"  {city}: {count}")

    return merged


if __name__ == "__main__":
    discover()
