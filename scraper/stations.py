"""
All transit station coordinates along the South Bay corridor.
Used for radius-based apartment discovery via Overpass API (OpenStreetMap).
"""

STATIONS = {
    # BART stations (Hayward → Santa Clara)
    "Hayward BART": {"lat": 37.6700, "lng": -122.0870, "transit": "BART"},
    "South Hayward BART": {"lat": 37.6348, "lng": -122.0571, "transit": "BART"},
    "Union City BART": {"lat": 37.5910, "lng": -122.0175, "transit": "BART"},
    "Fremont BART": {"lat": 37.5574, "lng": -121.9764, "transit": "BART"},
    "Warm Springs BART": {"lat": 37.5024, "lng": -121.9395, "transit": "BART"},
    "Milpitas BART": {"lat": 37.4104, "lng": -121.8910, "transit": "BART"},
    "Berryessa BART": {"lat": 37.3688, "lng": -121.8495, "transit": "BART"},
    "Alum Rock BART (planned)": {"lat": 37.3660, "lng": -121.8293, "transit": "BART"},
    "Downtown San Jose BART (planned)": {"lat": 37.3382, "lng": -121.8863, "transit": "BART"},
    "Diridon BART (planned)": {"lat": 37.3297, "lng": -121.9020, "transit": "BART"},
    "Santa Clara BART (planned)": {"lat": 37.3531, "lng": -121.9369, "transit": "BART"},

    # Caltrain stations (San Jose Diridon → Menlo Park)
    "San Jose Diridon": {"lat": 37.3297, "lng": -121.9020, "transit": "Caltrain"},
    "Santa Clara Caltrain": {"lat": 37.3531, "lng": -121.9369, "transit": "Caltrain"},
    "Lawrence Caltrain": {"lat": 37.3708, "lng": -121.9970, "transit": "Caltrain"},
    "Sunnyvale Caltrain": {"lat": 37.3783, "lng": -122.0308, "transit": "Caltrain"},
    "Mountain View Caltrain": {"lat": 37.3946, "lng": -122.0764, "transit": "Caltrain"},
    "San Antonio Caltrain": {"lat": 37.4069, "lng": -122.1070, "transit": "Caltrain"},
    "California Ave Caltrain": {"lat": 37.4292, "lng": -122.1422, "transit": "Caltrain"},
    "Palo Alto Caltrain": {"lat": 37.4432, "lng": -122.1649, "transit": "Caltrain"},
    "Menlo Park Caltrain": {"lat": 37.4547, "lng": -122.1823, "transit": "Caltrain"},

    # VTA Light Rail stations
    "VTA Great Mall/Milpitas": {"lat": 37.4153, "lng": -121.8985, "transit": "VTA"},
    "VTA Hostetter": {"lat": 37.3877, "lng": -121.8772, "transit": "VTA"},
    "VTA Civic Center": {"lat": 37.3300, "lng": -121.8889, "transit": "VTA"},
    "VTA Convention Center": {"lat": 37.3298, "lng": -121.8861, "transit": "VTA"},
    "VTA Paseo de San Antonio": {"lat": 37.3335, "lng": -121.8840, "transit": "VTA"},
    "VTA Santa Teresa": {"lat": 37.2539, "lng": -121.8027, "transit": "VTA"},
    "VTA Cottle": {"lat": 37.2634, "lng": -121.7969, "transit": "VTA"},
    "VTA Snell": {"lat": 37.2700, "lng": -121.8008, "transit": "VTA"},
    "VTA Branham": {"lat": 37.2820, "lng": -121.8278, "transit": "VTA"},
    "VTA Ohlone/Chynoweth": {"lat": 37.2897, "lng": -121.8429, "transit": "VTA"},
    "VTA Blossom Hill": {"lat": 37.2527, "lng": -121.7977, "transit": "VTA"},
    "VTA Capitol": {"lat": 37.2875, "lng": -121.8363, "transit": "VTA"},
    "VTA Curtner": {"lat": 37.3097, "lng": -121.8867, "transit": "VTA"},
    "VTA Tamien": {"lat": 37.3118, "lng": -121.8834, "transit": "VTA"},
    "VTA Baypointe": {"lat": 37.4019, "lng": -121.9130, "transit": "VTA"},
    "VTA Lick Mill": {"lat": 37.3932, "lng": -121.9265, "transit": "VTA"},
    "VTA Old Ironsides": {"lat": 37.3893, "lng": -121.9502, "transit": "VTA"},
    "VTA Great America": {"lat": 37.4066, "lng": -121.9766, "transit": "VTA"},
    "VTA Reamwood": {"lat": 37.3982, "lng": -121.9471, "transit": "VTA"},
    "VTA Champion": {"lat": 37.4019, "lng": -121.9130, "transit": "VTA"},
}

SEARCH_RADIUS_METERS = 3000  # 3 km radius around each station
