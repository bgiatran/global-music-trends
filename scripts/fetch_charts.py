# scripts/fetch_charts.py

import pandas as pd
import sys, os

# Add the parent directory to sys.path to enable imports from the root or utils directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Loads the chart dataset downloaded from Kaggle
# Cleans and standardizes column names to match the rest of the project
# Converts the date column to datetime format for time-based analysis
def load_kaggle_chart_data(path="data/charts_kaggle.csv"):
    df = pd.read_csv(path)

    # Rename columns for consistency across the database and scripts
    df = df.rename(columns={
        "Track Name": "name",
        "Artist": "artist_name",
        "Streams": "streams",
        "Region": "region",
        "Date": "chart_date"
    })

    # Convert chart_date to datetime format
    df["chart_date"] = pd.to_datetime(df["chart_date"])

    return df

# If this script is executed directly, load the chart data and print a success message
if __name__ == "__main__":
    df = load_kaggle_chart_data()
    print("✅ Loaded Kaggle charts with", len(df), "records")