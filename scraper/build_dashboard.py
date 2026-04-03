"""
Phase 3: Generate index.html dashboard from data/apartments.json
Embeds all apartment data directly into a Leaflet + OpenStreetMap HTML file.

Google Maps links use lat/lng format for universal mobile + desktop support:
  https://www.google.com/maps/search/?api=1&query=LAT,LNG

Usage:
    python build_dashboard.py
"""

import json
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")


def escape_js(s):
    """Escape a string for safe embedding in JavaScript."""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'").replace("\n", " ").replace("\r", "")


def build():
    with open(os.path.join(BASE_DIR, "data", "apartments.json")) as f:
        apartments = json.load(f)

    # Build JS array entries
    js_entries = []
    for a in apartments:
        name = escape_js(a.get("name", ""))
        address = escape_js(a.get("address", ""))
        city = escape_js(a.get("city", ""))
        phone = escape_js(a.get("phone", ""))
        website = a.get("website") or ""
        place_id = a.get("place_id", "")
        price = a.get("price_1br")
        rating = a.get("rating") or 0
        reviews = a.get("reviews") or 0
        lat = a.get("lat", 0)
        lng = a.get("lng", 0)
        transit = escape_js(a.get("transit", ""))

        price_str = f'"${price:,}/mo"' if price else "null"
        website_str = f'"{escape_js(website)}"' if website else "null"
        phone_str = f'"{phone}"' if phone else "null"
        place_id_str = f'"{place_id}"' if place_id else '""'

        js_entries.append(
            f'{{n:"{name}",a:"{address}",c:"{city}",'
            f'r:{rating},v:{reviews},'
            f'p:{phone_str},t:"{transit}",'
            f'lt:{lat},ln:{lng},'
            f'id:{place_id_str},w:{website_str},pr:{price_str}}}'
        )

    js_array = "const D=[\n  " + ",\n  ".join(js_entries) + "\n];"

    # Read template and inject data
    template_path = os.path.join(BASE_DIR, "template.html")
    if not os.path.exists(template_path):
        # If no template, use the current index.html as template
        template_path = os.path.join(BASE_DIR, "index.html")

    with open(template_path) as f:
        template = f.read()

    html = template.replace("/* __APARTMENT_DATA__ */", js_array)

    # Ensure Google Maps links use lat/lng format (works on mobile + desktop)
    html = html.replace(
        'https://www.google.com/maps/place/?q=place_id:${a.id}',
        'https://www.google.com/maps/search/?api=1&query=${a.lt},${a.ln}'
    )

    with open(os.path.join(BASE_DIR, "index.html"), "w") as f:
        f.write(html)

    print(f"Built index.html with {len(apartments)} apartments")
    print("Google Maps links use lat/lng (works on mobile + desktop)")


if __name__ == "__main__":
    build()
