import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import pycountry
import time

# Paths to the local SQLite database and output CSV
DB_PATH = "data/music.db"
CSV_PATH = "data/country_utils.csv"

# Try to resolve region names to full country names using pycountry
# This improves compatibility with geolocation services that expect official names
def resolve_country_name(region):
    try:
        # Attempt to find an exact or fuzzy match in the pycountry database
        return pycountry.countries.lookup(region).name
    except:
        # If lookup fails, return the original input as a fallback
        return region

# Main function: fetch geographic coordinates for each country in the 'charts' table
def fetch_and_save_country_coords():
    # Connect to the SQLite database and retrieve unique region names from the charts table
    conn = sqlite3.connect(DB_PATH)
    countries = pd.read_sql("SELECT DISTINCT region FROM charts", conn)
    conn.close()

    # Set up the geolocation service
    geolocator = Nominatim(user_agent="geoapi")

    records = []

    # Iterate through each unique region name
    for region in countries["region"].dropna().unique():
        # Clean and attempt to resolve region name to a recognized country
        lookup_name = resolve_country_name(region.strip())

        try:
            # Use the geocoder to get latitude and longitude
            location = geolocator.geocode(lookup_name, language="en")
            if location:
                records.append({
                    "country_name": region.strip(),      # Use original name for compatibility with chart data
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
                print(f"{region} → {lookup_name}")
            else:
                print(f"No geocode result: {region} → {lookup_name}")
        except Exception as e:
            # Handle unexpected geocoding errors gracefully
            print(f"Error for {region}: {e}")

        # Pause between requests to avoid getting rate-limited by the API
        time.sleep(1)

    # Convert results into a DataFrame and save to CSV
    df = pd.DataFrame(records)
    df.to_csv(CSV_PATH, index=False)

    # Also save the results to the 'country_utils' table in the database
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("country_utils", conn, if_exists="replace", index=False)
    conn.close()

# Run the function when this script is executed directly
if __name__ == "__main__":
    fetch_and_save_country_coords()