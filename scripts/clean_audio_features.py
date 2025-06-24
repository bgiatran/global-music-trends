import sys, os

# Add the parent directory to Python's path to allow relative imports if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

# Define file paths for input and output
AUDIO_SRC = os.path.join("data", "audio_features_kaggle.csv")
AUDIO_DST = os.path.join("data", "audio_features_cleaned.csv")

# Cleans the raw audio features dataset for use in modeling and analysis
def clean_audio_features():
    # Check if source file exists
    if not os.path.exists(AUDIO_SRC):
        print(f"Missing input file: {AUDIO_SRC}")
        return

    # Load the raw dataset
    df = pd.read_csv(AUDIO_SRC)

    # Rename column for consistency across tables
    df = df.rename(columns={"artists": "artist_name"})

    # Keep only the relevant columns for analysis
    cols_to_keep = [
        "track_id", "track_name", "artist_name", "popularity", "duration_ms", "explicit",
        "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "time_signature", "track_genre"
    ]
    df = df[cols_to_keep]

    # Remove rows missing key identifiers
    df = df.dropna(subset=["track_id", "track_name", "artist_name"])

    # Save cleaned data to a new CSV file
    df.to_csv(AUDIO_DST, index=False)
    print(f"Cleaned audio features saved to {AUDIO_DST} ({len(df):,} rows)")

# Run cleaning when script is executed directly
if __name__ == "__main__":
    clean_audio_features()