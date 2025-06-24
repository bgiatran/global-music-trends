import sys, os

# Allow importing from the parent directory (useful for utils and shared code)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import requests
from utils.spotify_auth import get_token

# Spotify API endpoint for retrieving audio features by track ID
BASE_URL = "https://api.spotify.com/v1/audio-features"

# Fetches audio features in batches of up to 100 track IDs
# Returns a list of feature dictionaries for all valid tracks
def fetch_audio_features(track_ids):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    all_audio_features = []

    print(f"🔍 Fetching audio features for {len(track_ids)} tracks...")

    # Spotify allows up to 100 track IDs per request, so we batch the input list
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        ids_param = ','.join(batch)
        res = requests.get(BASE_URL, headers=headers, params={"ids": ids_param})

        # If the request succeeds, collect all valid feature entries
        if res.status_code == 200:
            features = res.json().get("audio_features", [])
            valid_features = [f for f in features if f is not None]
            all_audio_features.extend(valid_features)
            print(f"Batch {i//100 + 1}: Fetched {len(valid_features)} tracks")
        else:
            # Print the error message if the batch fails
            print(f"Error in batch {i//100 + 1}:", res.json())

    return all_audio_features

# If the script is run directly, fetch and save audio features to CSV
if __name__ == "__main__":
    # Ensure the output directory exists
    os.makedirs("data", exist_ok=True)

    # Load track IDs from the dataset (must contain a 'track_id' column)
    df_tracks = pd.read_csv("data/tracks_2020.csv")
    track_ids = df_tracks["track_id"].dropna().unique().tolist()

    # Retrieve audio features using Spotify API
    audio_data = fetch_audio_features(track_ids)
    df_audio = pd.DataFrame(audio_data)

    # Save the result to a CSV file for reuse
    df_audio.to_csv("data/audio_features.csv", index=False)
    print(f"Done. Saved {len(df_audio)} audio features to data/audio_features.csv")