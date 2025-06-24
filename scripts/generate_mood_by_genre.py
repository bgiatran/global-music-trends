# scripts/generate_mood_by_genre.py

import pandas as pd
import os

# Define input and output file paths
AUDIO_PATH = os.path.join("data", "audio_features_cleaned.csv")
OUTPUT_PATH = os.path.join("data", "mood_by_genre.csv")

# Load the cleaned audio features dataset
df = pd.read_csv(AUDIO_PATH)

# Keep only rows with valid, non-empty genre labels
df = df[df["track_genre"].notna() & (df["track_genre"] != "")]

# Calculate the average value of mood-related audio features for each genre
# These metrics give insight into the overall sound and emotion of each genre
summary = df.groupby("track_genre").agg({
    "valence": "mean",
    "energy": "mean",
    "danceability": "mean",
    "tempo": "mean",
    "acousticness": "mean",
    "instrumentalness": "mean",
    "liveness": "mean",
    "speechiness": "mean"
}).reset_index()

# Save the mood profile summary per genre to a CSV file
summary.to_csv(OUTPUT_PATH, index=False)
print(f"Saved mood summary to {OUTPUT_PATH}")