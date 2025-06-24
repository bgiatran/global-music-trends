# scripts/generate_artist_counts_by_country.py

import pandas as pd
import os

# Define paths to input and output files
CHARTS_PATH = os.path.join("data", "charts_2017_2023_clean.csv")      # Cleaned charts dataset with region and artist info
COUNTRY_PATH = os.path.join("data", "country_utils.csv")              # Contains country name, latitude, longitude
OUTPUT_PATH = os.path.join("data", "artist_counts_by_country.csv")    # Output file for merged result

# Load datasets
charts = pd.read_csv(CHARTS_PATH)
countries = pd.read_csv(COUNTRY_PATH)

# Count the number of unique artists per region in the chart dataset
# This gives us a measure of how many distinct artists appeared in each country
artist_counts = charts.groupby("region")["artist_name"].nunique().reset_index()
artist_counts = artist_counts.rename(columns={"region": "country", "artist_name": "artist_count"})

# Merge artist counts with geographic coordinates using the country name
# This allows us to later map artist origins on a world map
merged = artist_counts.merge(countries, left_on="country", right_on="country_name", how="left")

# Drop any rows where the country couldn't be geolocated (missing lat/lon)
merged = merged.dropna(subset=["latitude", "longitude"])

# Save the result to a CSV that will be used for visualizations
merged.to_csv(OUTPUT_PATH, index=False)
print(f"Saved artist origin summary to {OUTPUT_PATH}")