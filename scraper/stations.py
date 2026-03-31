"""
All transit station coordinates along the South Bay corridor.
Used for radius-based apartment discovery via Google Places API.
"""

STATIONS = {
    # BART stations (Hayward → Milpitas)
    "Hayward BART": {"lat": 37.6700, "lng": -122.0870, "transit": "BART"},
    "South Hayward BART": {"lat": 37.6348, "lng": -122.0571, "transit": "BART"},
    "Union City BART": {"lat": 37.5910, "lng": -122.0175, "transit": "BART"},
    "Fremont BART": {"lat": 37.5574, "lng": -121.9764, "transit": "BART"},
    "Warm Springs BART": {"lat": 37.5024, "lng": -121.9395, "transit": "BART"},
    "Milpitas BART": {"lat": 37.4104, "lng": -121.8910, "transit": "BART"},
    "Berryessa BART": {"lat": 37.3685, "lng": -121.8746, "transit": "BART"},

    # Caltrain stations (San Jose Diridon → Menlo Park)
    "San Jose Diridon": {"lat": 37.3297, "lng": -121.9022, "transit": "Caltrain/BART"},
    "Santa Clara Caltrain": {"lat": 37.3531, "lng": -121.9365, "transit": "Caltrain"},
    "Lawrence Caltrain": {"lat": 37.3706, "lng": -121.9970, "transit": "Caltrain"},
    "Sunnyvale Caltrain": {"lat": 37.3784, "lng": -122.0308, "transit": "Caltrain"},
    "Mountain View Caltrain": {"lat": 37.3946, "lng": -122.0764, "transit": "Caltrain"},
    "San Antonio Caltrain": {"lat": 37.4069, "lng": -122.1071, "transit": "Caltrain"},
    "California Ave Caltrain": {"lat": 37.4291, "lng": -122.1422, "transit": "Caltrain"},
    "Palo Alto Caltrain": {"lat": 37.4434, "lng": -122.1648, "transit": "Caltrain"},
    "Menlo Park Caltrain": {"lat": 37.4547, "lng": -122.1825, "transit": "Caltrain"},

    # Key VTA Light Rail stops
    "VTA Milpitas": {"lat": 37.4163, "lng": -121.8892, "transit": "VTA"},
    "VTA Great Mall": {"lat": 37.4157, "lng": -121.8984, "transit": "VTA"},
    "VTA Baypointe": {"lat": 37.3824, "lng": -121.9458, "transit": "VTA"},
    "VTA Convention Center": {"lat": 37.3298, "lng": -121.8882, "transit": "VTA"},
    "VTA Capitol": {"lat": 37.3160, "lng": -121.8660, "transit": "VTA"},
    "VTA Curtner": {"lat": 37.2929, "lng": -121.8480, "transit": "VTA"},
    "VTA Oakridge": {"lat": 37.2570, "lng": -121.8165, "transit": "VTA"},
}

SEARCH_RADIUS_METERS = 1500  # 1.5 km radius around each station
