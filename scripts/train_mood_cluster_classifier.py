import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset containing genre mood clusters and audio features
df = pd.read_csv("data/genre_clusters.csv")

# Select audio-related features used for predicting the cluster
X = df[[
    "valence", "danceability", "energy", "tempo",
    "acousticness", "instrumentalness", "liveness", "speechiness"
]]

# Target variable: cluster number each genre belongs to
y = df["cluster"]

# Split data into training and testing sets for validation
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the training data
clf.fit(X_train, y_train)

# Save the trained model to disk for use in the Streamlit dashboard
joblib.dump(clf, "models/mood_cluster_classifier.pkl")
print("Saved model to models/mood_cluster_classifier.pkl")