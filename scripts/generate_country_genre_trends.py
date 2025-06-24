import pandas as pd
from sklearn.linear_model import LinearRegression

# Load cleaned chart data that includes track genre, region, and year
df = pd.read_csv("data/charts_2017_2023_clean.csv")

# Focus the analysis on recent years only
df = df[df["year"].between(2018, 2023)]

trend_rows = []

# For each unique combination of region and genre,
# we fit a linear model to see if the genre is trending up or down over time
for (region, genre), group in df.groupby(["region", "track_genre"]):
    # Count the number of charting tracks per year and ensure all years are present
    year_counts = group.groupby("year").size().reindex(range(2018, 2024), fill_value=0).reset_index()

    # Prepare input (X = years) and output (y = number of tracks)
    X = year_counts["year"].values.reshape(-1, 1)
    y = year_counts[0].values

    # Skip genres that are too rare to be meaningful (fewer than 10 total entries)
    if y.sum() < 10:
        continue

    # Fit a simple linear regression model to detect the trend slope
    model = LinearRegression().fit(X, y)

    # Store the slope and trend type (rising or falling)
    trend_rows.append({
        "region": region,
        "genre": genre,
        "slope": model.coef_[0],
        "trend_type": "rising" if model.coef_[0] > 0 else "falling"
    })

# Save the trend results as a CSV for use in dashboards or regional analysis
pd.DataFrame(trend_rows).to_csv("data/genre_trends_by_region.csv", index=False)
print("Saved genre trends to data/genre_trends_by_region.csv")