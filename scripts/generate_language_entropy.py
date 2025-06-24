# scripts/generate_language_entropy.py

import pandas as pd
import numpy as np
import os

# Load the language detection results and the cleaned chart data
lang_df = pd.read_csv("data/lang_detect.csv")
charts_df = pd.read_csv("data/charts_2017_2023_clean.csv")

# Rename 'name' to 'track_name' to ensure consistent column names for merging
lang_df = lang_df.rename(columns={"name": "track_name"})

# Merge language data with chart data using track name and artist name
# This ensures we're matching language info with specific charted songs
merged = charts_df.merge(lang_df, on=["track_name", "artist_name"], how="inner")

# Drop any rows where region or language is missing
merged = merged.dropna(subset=["region", "language"])

# Define a function to calculate Shannon entropy
# Entropy measures how evenly languages are distributed in a region
def shannon_entropy(series):
    proportions = series.value_counts(normalize=True)
    return -np.sum(proportions * np.log2(proportions))

# Group by region and calculate:
# - language entropy (diversity score)
# - total number of charted tracks
# - number of unique languages detected
entropy_df = (
    merged.groupby("region")
    .agg(
        entropy_score=("language", shannon_entropy),
        total_tracks=("track_name", "count"),
        unique_languages=("language", "nunique")
    )
    .reset_index()
    .sort_values("entropy_score", ascending=False)
)

# Save the results to a CSV file for use in visualizations
output_path = os.path.join("data", "language_entropy.csv")
entropy_df.to_csv(output_path, index=False)
print(f"Saved entropy-based diversity scores to {output_path}")