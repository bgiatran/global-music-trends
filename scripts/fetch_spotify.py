import sys, os

# Add parent directory to the Python path for shared utility imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import pandas as pd
from utils.spotify_auth import get_token

# Base URL for the Spotify Web API
BASE_URL = "https://api.spotify.com/v1"

# Sends a request to Spotify’s search API to retrieve tracks for a given year and country
# Uses Spotify’s query syntax: year:<year>
# Returns a list of track objects from the search result
def fetch_tracks_by_year(year, country="US", limit=50):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    query = f"year:{year}"

    params = {
        "q": query,
        "type": "track",
        "limit": limit,
        "market": country
    }

    res = requests.get(f"{BASE_URL}/search", headers=headers, params=params)

    if res.status_code == 200:
        return res.json().get("tracks", {}).get("items", [])
    else:
        print("Spotify error:", res.json())
        return []

# Extracts relevant metadata from the raw Spotify API response
# Returns a DataFrame with selected track and artist fields
def extract_track_data(tracks):
    extracted = []
    for t in tracks:
        extracted.append({
            "track_id": t["id"],
            "name": t["name"],
            "artist_id": t["artists"][0]["id"],
            "artist_name": t["artists"][0]["name"],
            "release_date": t["album"].get("release_date", ""),
            "genre": None  # Placeholder for genre; can be filled later
        })
    return pd.DataFrame(extracted)

# Entry point for running this script standalone
# Fetches tracks and saves them to a local CSV
if __name__ == "__main__":
    year = 2020
    os.makedirs("data", exist_ok=True)

    print(f"🎧 Fetching Spotify tracks for {year}...")
    tracks = fetch_tracks_by_year(year)

    if not tracks:
        print("No tracks fetched. Check your credentials or API quota.")
    else:
        df = extract_track_data(tracks)
        df.to_csv("data/tracks_2020.csv", index=False)
        print(f"Saved {len(df)} tracks to data/tracks_2020.csv")