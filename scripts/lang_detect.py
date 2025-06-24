# scripts/lang_detect.py

import pandas as pd
import sqlite3
import sys, os

# Add the project root to the system path to allow importing from the utils folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.lang_utils import detect_language

# Define file paths for input and output
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRACKS_PATH = os.path.join(PROJECT_ROOT, "data", "tracks_2020.csv")          # Input: track titles
LANG_TABLE_PATH = os.path.join(PROJECT_ROOT, "data", "lang_detect.csv")      # Output: language detection CSV
DB_PATH = os.path.join(PROJECT_ROOT, "data", "music.db")                     # SQLite database path

# Load the tracks dataset and keep only relevant fields
# Dropping rows with missing values to avoid detection errors
df = pd.read_csv(TRACKS_PATH)
df = df[["track_id", "name", "artist_name"]].dropna()

# Apply language detection to each track name using langdetect
# Adds a new 'language' column to the dataframe
df["language"] = df["name"].apply(detect_language)

# Save the detection results to a CSV as a backup or reference
df.to_csv(LANG_TABLE_PATH, index=False)
print(f"Saved language detection results to {LANG_TABLE_PATH}")

# Create or replace the 'lang_detect' table in the SQLite database
# This allows other scripts to join with this language data efficiently
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS lang_detect (
        track_id TEXT,
        name TEXT,
        artist_name TEXT,
        language TEXT
    )
""")
df.to_sql("lang_detect", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print(f"lang_detect table inserted into {DB_PATH}")