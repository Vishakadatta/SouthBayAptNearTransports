# 🏠 South Bay Transit Apartments

An interactive map of apartments along BART, Caltrain & VTA corridors in the South Bay (Hayward → Menlo Park).

**Built because Zillow and Apartments.com miss the hidden gems.**

This tool uses station-radius search (1.5km around every transit stop) instead of city-level queries, catching small complexes like Sunshine Gardens that popularity-ranked platforms bury.

## 🗺️ Live Demo

**[→ Open the Map](https://YOUR_USERNAME.github.io/south-bay-apartments/)**

## Stack

| Layer | Tech | Cost |
|-------|------|------|
| Map | [Leaflet](https://leafletjs.com/) + [OpenStreetMap](https://www.openstreetmap.org/) | Free |
| Data | Google Places API (discovery) + web scraping (prices) | ~$5/run |
| Hosting | GitHub Pages | Free |
| Automation | GitHub Actions (weekly cron) | Free |

Zero servers. Zero subscriptions. Just a static HTML file with embedded data.

## Features

- **75+ apartments** across 11 cities along transit corridors
- **Interactive map** with color-coded markers (BART/Caltrain/VTA)
- **Click-to-fly** — click a card, map zooms to the apartment
- **Filters** — city, transit type, minimum rating, search
- **Direct links** to Google Maps listing for each apartment
- **Phone numbers** for every leasing office
- **Mobile responsive** — works on your phone

## How It Works

### Phase 1: Discovery (`scraper/discover.py`)
Hits Google Places Nearby Search API with a 1.5km radius around every BART, Caltrain, and VTA station on the corridor. Deduplicates by `place_id`.

### Phase 2: Pricing (`scraper/scrape_prices.py`)
For each apartment, grabs the website URL from Places Detail API, then scrapes for 1BR/1BA pricing using regex pattern matching. Falls back gracefully — you always get the website link even if price isn't found.

### Phase 3: Dashboard (`scraper/build_dashboard.py`)
Generates `index.html` with all data embedded. Pure static file, no build tools needed.

### Automation (`.github/workflows/scrape.yml`)
Runs weekly via GitHub Actions. Commits updated data back to the repo. GitHub Pages auto-deploys.

## Setup

### Quick start (just use the existing data)
```bash
# Clone and open
git clone https://github.com/YOUR_USERNAME/south-bay-apartments.git
open index.html
```

### Full pipeline (refresh data)
```bash
# 1. Get a Google Places API key
#    https://console.cloud.google.com/apis/credentials
#    Enable "Places API" and "Places API (New)"

# 2. Set your key
export GOOGLE_PLACES_API_KEY="AIza..."

# 3. Install deps
pip install -r scraper/requirements.txt

# 4. Run the pipeline
python main.py

# 5. Open the result
open index.html
```

### GitHub Actions setup (automated weekly refresh)
1. Go to repo → Settings → Secrets → Actions
2. Add `GOOGLE_PLACES_API_KEY` as a repository secret
3. Go to repo → Settings → Pages → Source: Deploy from branch (`main`, `/ (root)`)
4. The action runs every Sunday, or trigger manually from Actions tab

## Transit Stations Covered

**BART:** Hayward, South Hayward, Union City, Fremont, Warm Springs, Milpitas, Berryessa

**Caltrain:** San Jose Diridon, Santa Clara, Lawrence, Sunnyvale, Mountain View, San Antonio, California Ave, Palo Alto, Menlo Park

**VTA Light Rail:** Milpitas, Great Mall, Baypointe, Convention Center, Capitol, Curtner, Oakridge

## License

MIT — do whatever you want with it.
# SouthBayAptNearTransports
