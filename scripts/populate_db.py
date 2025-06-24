import sqlite3
import pandas as pd
import sys, os

# Add project root to sys.path so we can import from parent directories if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define all necessary file paths
DB_PATH = os.path.join("data", "music.db")
AUDIO_FEATURES_PATH = os.path.join("data", "audio_features_cleaned.csv")
CHARTS_PATH = os.path.join("data", "charts_2017_2023_clean.csv")
COUNTRY_UTILS_PATH = os.path.join("data", "country_utils.csv")
LANG_DETECT_PATH = os.path.join("data", "lang_detect.csv")
SQL_FOLDER = os.path.join(os.path.dirname(__file__), "..", "sql")

# Connect to the SQLite database
def connect_db():
    print(f"Connecting to SQLite database: {DB_PATH}")
    return sqlite3.connect(DB_PATH)

# Create all required tables if they don't already exist
def create_tables(conn):
    cursor = conn.cursor()

    # Audio features table from Spotify
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_features (
            track_id TEXT,
            name TEXT,
            artist_name TEXT,
            danceability REAL,
            energy REAL,
            key INTEGER,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            acousticness REAL,
            instrumentalness REAL,
            liveness REAL,
            valence REAL,
            tempo REAL,
            duration_ms INTEGER,
            time_signature INTEGER
        )
    """)

    # Global chart data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS charts (
            track_id TEXT,
            track_name TEXT,
            artist_name TEXT,
            date TEXT,
            region TEXT,
            chart TEXT,
            trend TEXT,
            streams INTEGER,
            position INTEGER
        )
    """)

    # Country location utility table (used for mapping)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_utils (
            country_name TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    # Language detection table (applied on track titles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lang_detect (
            track_id TEXT,
            name TEXT,
            artist_name TEXT,
            language TEXT
        )
    """)

    conn.commit()
    print("Tables created")

# Load a CSV into a table only if it’s currently empty
def load_table_if_empty(conn, table_name, csv_path, display_name):
    if not os.path.exists(csv_path):
        print(f"Missing file: {csv_path}")
        return

    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cur.fetchone()[0]
        if row_count > 0:
            print(f"Skipped {display_name} (already has {row_count} rows)")
            return
    except sqlite3.OperationalError:
        print(f"Table {table_name} doesn't exist, creating and loading...")

    print(f"Reading {display_name} from {csv_path} ...")
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"{display_name} CSV has {len(df)} rows. Inserting in chunks...")

    df.to_sql(table_name, conn, if_exists="append", index=False, chunksize=1000)
    print(f"Inserted {len(df)} rows into {display_name} (chunked)")

# Loaders for specific tables
def load_audio_features(conn):
    load_table_if_empty(conn, "audio_features", AUDIO_FEATURES_PATH, "Audio Features")

def load_charts(conn):
    load_table_if_empty(conn, "charts", CHARTS_PATH, "Charts")

def load_country_utils(conn):
    load_table_if_empty(conn, "country_utils", COUNTRY_UTILS_PATH, "Country Utils")

def load_lang_detect(conn):
    load_table_if_empty(conn, "lang_detect", LANG_DETECT_PATH, "Language Detection")

# Apply all SQL view scripts from the /sql folder
def apply_sql_views(conn):
    print("📄 Applying SQL view scripts from /sql ...")
    sql_files = [
        "artist_origin_map.sql",
        "languages.sql",
        "top_genres_by_year.sql",
        "top_moods_by_country.sql"
    ]

    for file in sql_files:
        path = os.path.join(SQL_FOLDER, file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    conn.executescript(f.read())
                    print(f"View applied: {file}")
                except Exception as e:
                    print(f"Failed to apply {file}: {e}")
        else:
            print(f"File not found: {file}")

# Run the entire database setup process
if __name__ == "__main__":
    try:
        conn = connect_db()
        create_tables(conn)
        load_audio_features(conn)
        load_charts(conn)
        load_country_utils(conn)
        load_lang_detect(conn)
        apply_sql_views(conn)
        conn.close()
        print("Database built and populated successfully with views.")
    except Exception as e:
        print(f"Error during execution: {e}")