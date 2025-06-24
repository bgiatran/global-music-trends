import os
import pandas as pd
import streamlit as st
import altair as alt
import sqlite3

# Establishes a connection to the SQLite database used across the app.
# This is useful for reading views or tables directly into pandas DataFrames.
def connect_db():
    return sqlite3.connect("data/music.db")

DATA_DIR = os.path.join("data")

# Reads a CSV file containing aggregated genre popularity by year.
# The CSV is generated from SQL queries or offline processing to optimize speed.
# Caching ensures Streamlit doesn’t reload this on every interaction, saving performance.
@st.cache_data
def load_genre_trends():
    path = os.path.join(DATA_DIR, "genre_trends.csv")
    return pd.read_csv(path)

# Visualizes the popularity trends of the top 10 music genres over time.
# The top 10 are determined based on their total appearance count across all years.
# It uses a line chart to help users visually compare rise and fall of genres annually.
def plot_genre_over_time():
    try:
        df = load_genre_trends()
        top_genres = df.groupby("track_genre")["track_count"].sum().nlargest(10).index
        df = df[df["track_genre"].isin(top_genres)]

        chart = alt.Chart(df).mark_line(point=True).encode(
            x="year:O",  # Ordinal year value on x-axis
            y="track_count:Q",  # Quantitative count of songs
            color="track_genre:N",  # Color-coded by genre
            tooltip=["year", "track_genre", "track_count"]
        ).properties(
            title="Top 10 Genres Over Time (Based on Release Dates)",
            width=700,
            height=400
        )
        st.altair_chart(chart)
    except Exception as e:
        st.error(f"Error loading genre trends: {e}")

# Loads a CSV that contains average values of audio mood features per genre.
# These features include emotional and structural qualities like energy and tempo.
@st.cache_data
def load_mood_by_genre():
    path = os.path.join(DATA_DIR, "mood_by_genre.csv")
    return pd.read_csv(path)

# Lets users select a mood-related audio feature and displays a horizontal bar chart
# comparing the average value of that feature across different music genres.
# This helps illustrate which genres tend to be more energetic, acoustic, etc.
def plot_mood_heatmap():
    try:
        df = load_mood_by_genre()
        metric = st.selectbox("Select Mood Metric", [
            "valence", "energy", "danceability", "tempo", "acousticness",
            "instrumentalness", "liveness", "speechiness"
        ])

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("track_genre:N", sort="-y"),
            y=alt.Y(f"{metric}:Q"),
            tooltip=["track_genre", metric]
        ).properties(
            title=f"{metric.title()} by Genre",
            width=800,
            height=400
        )
        st.altair_chart(chart)
    except Exception as e:
        st.error(f"Error loading mood data: {e}")

# Reads a language detection file where each track has an associated language code.
# Groups the tracks by language to compute the frequency distribution.
@st.cache_data
def get_language_distribution():
    path = os.path.join(DATA_DIR, "lang_detect.csv")
    df = pd.read_csv(path)
    return df.groupby("language").size().reset_index(name="count").sort_values("count", ascending=False)

# Visualizes the most common detected languages in the music dataset.
# Shows a bar chart of the top 15 languages and their corresponding track counts.
def plot_language_distribution():
    try:
        df = get_language_distribution()
        chart = alt.Chart(df.head(15)).mark_bar().encode(
            x=alt.X("language:N", sort="-y"),
            y="count:Q",
            tooltip=["language", "count"]
        ).properties(
            title="Top 15 Detected Languages in Global Tracks",
            width=700,
            height=400
        )
        st.altair_chart(chart)
    except Exception as e:
        st.error(f"Error loading language data: {e}")

# Loads a precomputed CSV that maps countries to artist counts and coordinates.
# The coordinates are used for both plotting and geographic clustering.
@st.cache_data
def get_artist_origin_data():
    path = os.path.join(DATA_DIR, "artist_counts_by_country.csv")
    return pd.read_csv(path)

# Displays artist origin data using both a geographic map and a bubble chart.
# This allows users to visually identify regions that produce a high volume of unique artists.
def plot_artist_map():
    try:
        df = get_artist_origin_data()
        st.map(df[["latitude", "longitude"]])  # Basic map overlay

        chart = alt.Chart(df).mark_circle(opacity=0.7).encode(
            longitude="longitude:Q",
            latitude="latitude:Q",
            size=alt.Size("artist_count:Q", scale=alt.Scale(range=[50, 1000]), legend=None),
            tooltip=["country", "artist_count"]
        ).properties(
            title="Artist Origin Concentration (Based on Charts)",
            width=800,
            height=400
        )

        st.altair_chart(chart)
    except Exception as e:
        st.error(f"Error loading artist origin map: {e}")

# Plots a scatterplot to examine how upbeat and danceable different genres are.
# Valence and danceability are both continuous audio features ranging from 0 to 1.
# This helps explain how genres differ in mood and physical engagement.
def plot_valence_vs_danceability():
    try:
        df = load_mood_by_genre()

        chart = alt.Chart(df).mark_circle(size=100, opacity=0.6).encode(
            x=alt.X("valence:Q", title="Valence (positivity)"),
            y=alt.Y("danceability:Q", title="Danceability"),
            color="track_genre:N",
            tooltip=["track_genre", "valence", "danceability"]
        ).properties(
            title="How Danceable and Positive Is Each Genre?",
            width=700,
            height=400
        )
        st.altair_chart(chart)
        st.markdown("*Genres in the upper-right are both happy and easy to dance to.*")
    except Exception as e:
        st.error(f"Error loading scatterplot: {e}")

# A mapping between language codes (e.g., "en", "es") and their full names.
# Used for more user-friendly tooltips in language visualizations.
LANGUAGE_MAP = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh-cn": "Chinese (Simplified)",
    "ru": "Russian", "it": "Italian", "tr": "Turkish", "nl": "Dutch",
    "sv": "Swedish", "no": "Norwegian", "pl": "Polish", "unknown": "Unknown"
}

# Enhanced language distribution chart that shows full language names in tooltips.
# Useful for users unfamiliar with language codes.
def plot_language_distribution_expanded():
    try:
        df = get_language_distribution()
        df["language_full"] = df["language"].apply(lambda x: LANGUAGE_MAP.get(x, x))

        chart = alt.Chart(df.head(15)).mark_bar().encode(
            x=alt.X("language:N", sort="-y", title="Language Code"),
            y="count:Q",
            tooltip=["language_full", "count"]
        ).properties(
            title="Top 15 Languages in Global Tracks (Hover to See Full Name)",
            width=700,
            height=400
        )
        st.altair_chart(chart)
        st.markdown("*Hover over each bar to see the full language name.*")
    except Exception as e:
        st.error(f"Error loading language bar chart: {e}")

# Uses artist origin data to plot a bar chart of the top 15 countries by unique artist count.
# Helpful for understanding which countries contribute the most to global music trends.
def plot_top_artist_countries():
    try:
        df = get_artist_origin_data()
        df_sorted = df.sort_values("artist_count", ascending=False).head(15)

        chart = alt.Chart(df_sorted).mark_bar().encode(
            x=alt.X("country:N", sort="-y"),
            y="artist_count:Q",
            tooltip=["country", "artist_count"]
        ).properties(
            title="Top 15 Countries by Number of Unique Charting Artists",
            width=700,
            height=400
        )
        st.altair_chart(chart)
        st.markdown("*Which countries are launching the most artists onto the global charts?*")
    except Exception as e:
        st.error(f"Error loading country artist chart: {e}")

# Loads a pre-labeled genre cluster file.
# Each row maps a genre to a mood-based cluster determined by unsupervised learning (e.g. KMeans).
@st.cache_data
def load_genre_clusters():
    return pd.read_csv("data/genre_clusters.csv")

# Visualizes mood-based clusters of genres using a scatterplot.
# The chart shows how genres group based on similarity in valence and danceability.
def plot_genre_clusters():
    try:
        df = load_genre_clusters()

        chart = alt.Chart(df).mark_circle(size=100, opacity=0.6).encode(
            x="valence:Q",
            y="danceability:Q",
            color=alt.Color("cluster_name:N", title="Cluster (Genre Group)", legend=alt.Legend(columns=2, orient="bottom")),
            tooltip=["track_genre", "cluster_name", "valence", "danceability"]
        ).properties(
            title="Genre Clusters Based on Mood Features",
            width=700,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
        st.markdown("*Each genre is plotted individually. Clusters group them by mood similarity.*")
    except Exception as e:
        st.error(f"Error loading genre clusters: {e}")

# Loads a file containing entropy scores by region.
# Entropy here is a measure of linguistic diversity: higher means more balanced variety of languages.
@st.cache_data
def load_language_entropy():
    path = os.path.join(DATA_DIR, "language_entropy.csv")
    return pd.read_csv(path)

# Plots a bar chart of the top regions with the most balanced language representation.
# Tooltip includes supporting details like number of languages and tracks used.
def plot_language_entropy():
    try:
        df = load_language_entropy()
        chart = alt.Chart(df.head(20)).mark_bar().encode(
            x=alt.X("region:N", sort="-y"),
            y="entropy_score:Q",
            tooltip=["region", "entropy_score", "unique_languages", "total_tracks"]
        ).properties(
            title="Language Entropy by Region (Higher = More Balanced Diversity)",
            width=800,
            height=400
        )
        st.altair_chart(chart)
        st.markdown("*Entropy measures how balanced the language distribution is — higher means more equal representation of multiple languages.*")
    except Exception as e:
        st.error(f"Error loading language entropy chart: {e}")

import joblib

# Loads a trained clustering model that predicts a genre group based on mood features.
# The model is used in an interactive form within the Streamlit app.
@st.cache_resource
def load_mood_cluster_model():
    return joblib.load("models/mood_cluster_classifier.pkl")