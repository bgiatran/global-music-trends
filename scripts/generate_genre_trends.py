# scripts/generate_genre_trends.py

import pandas as pd
import os

# Define file paths
AUDIO_PATH = os.path.join("data", "audio_features_cleaned.csv")   # Contains genre and audio features
TRACKS_PATH = os.path.join("data", "tracks_2020.csv")             # Contains release dates
OUTPUT_PATH = os.path.join("data", "genre_trends.csv")            # Output for yearly genre counts

# Load both datasets
audio = pd.read_csv(AUDIO_PATH)
tracks = pd.read_csv(TRACKS_PATH)

# Merge audio features with release dates using track_id as the key
# This allows us to assign a release year to each genre-tagged track
merged = audio.merge(tracks[["track_id", "release_date"]], on="track_id", how="left")

# Convert release_date to datetime and extract the release year
merged["release_date"] = pd.to_datetime(merged["release_date"], errors="coerce")
merged["year"] = merged["release_date"].dt.year

# Remove entries with missing genre or release year
merged = merged.dropna(subset=["year", "track_genre"])

# Count the number of tracks per genre per year
trend = merged.groupby(["year", "track_genre"]).size().reset_index(name="track_count")

# Save the genre trend data to a CSV file for visualization or modeling
trend.to_csv(OUTPUT_PATH, index=False)
print(f"Saved genre trends to {OUTPUT_PATH}")