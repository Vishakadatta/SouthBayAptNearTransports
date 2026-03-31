"""
Phase 3: Generate index.html dashboard from data/apartments.json
Embeds all apartment data directly into a Leaflet + OpenStreetMap HTML file.

Usage:
    python build_dashboard.py
"""

import json

def build():
    with open("data/apartments.json") as f:
        apartments = json.load(f)

    # Build JS array entries
    js_entries = []
    for a in apartments:
        price_str = f'"${a["price_1br"]:,}/mo"' if a.get("price_1br") else "null"
        website_str = f'"{a["website"]}"' if a.get("website") else "null"
        phone_str = f'"{a["phone"]}"' if a.get("phone") else "null"

        js_entries.append(
            f'{{n:"{a["name"]}",a:"{a["address"]}",c:"{a.get("city","")}",'
            f'r:{a.get("rating") or 0},rv:{a.get("reviews",0)},'
            f'p:{phone_str},t:"{a.get("transit","")}",'
            f'lat:{a["lat"]},lng:{a["lng"]},'
            f'pid:"{a["place_id"]}",w:{website_str},pr:{price_str}}}'
        )

    js_array = "const APTS = [\n  " + ",\n  ".join(js_entries) + "\n];"

    # Read template and inject data
    with open("template.html") as f:
        template = f.read()

    html = template.replace("/* __APARTMENT_DATA__ */", js_array)

    with open("index.html", "w") as f:
        f.write(html)

    print(f"Built index.html with {len(apartments)} apartments")


if __name__ == "__main__":
    build()
