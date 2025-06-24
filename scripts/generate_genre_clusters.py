# scripts/generate_genre_clusters.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the pre-aggregated mood feature dataset
# Each row represents a music genre with its averaged audio characteristics
df = pd.read_csv("data/mood_by_genre.csv")

# Select the mood-related audio features to use for clustering
# These features describe the general vibe or structure of each genre
features = ["valence", "energy", "danceability", "tempo",
            "acousticness", "instrumentalness", "liveness", "speechiness"]

# Standardize feature values so that all features contribute equally to clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Apply KMeans clustering to group similar genres based on their mood profiles
# We specify 6 clusters arbitrarily, which can be tuned later for better separation
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# Assign a readable name to each cluster based on the most common genre within it
# This helps in making the clusters interpretable in charts or dashboards
cluster_names = df.groupby("cluster")["track_genre"].agg(lambda x: x.mode().iloc[0])
df["cluster_name"] = df["cluster"].map(cluster_names)

# Save the clustered data for use in Streamlit visualizations and ML predictions
output_path = "data/genre_clusters.csv"
df.to_csv(output_path, index=False)
print(f"Saved clustered genre data to {output_path}")