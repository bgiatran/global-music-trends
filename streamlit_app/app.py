import streamlit as st
from visuals import (
    plot_genre_over_time,
    plot_mood_heatmap,
    plot_valence_vs_danceability,
    plot_language_distribution_expanded,
    plot_top_artist_countries,
    plot_artist_map,
    plot_genre_clusters,
    plot_language_entropy,
    load_mood_cluster_model
)

# Set up basic configuration for the Streamlit app.
# This includes the title shown in the browser tab and layout styling.
st.set_page_config(
    page_title="Global Music Trends",
    layout="wide",
)

# Display the main title of the dashboard.
# Markdown below it gives a concise summary of what the user can explore.
st.title("Global Music Trends Dashboard")
st.markdown(
    """
    Discover how music genres, moods, languages, and artist origins evolve around the world —  
    all powered by real audio data and public charts.  
    """
)

# Create three tabs that organize the dashboard into major categories:
# 1. Genre & Mood
# 2. Languages & Regions
# 3. Artist Origins & Advanced ML Predictor
tab1, tab2, tab3 = st.tabs([
    "Genre & Mood",
    "Languages & Regions",
    "Artist Origins"
])

# Tab 1 contains four key visualizations focused on genre popularity and mood analytics.
with tab1:
    col1, col2 = st.columns(2)

    # Plot a line or area chart showing how different music genres rise and fall in popularity over time.
    with col1:
        st.subheader("Genre Trends Over Time")
        st.markdown("Explore how the popularity of different music genres evolves year over year.")
        plot_genre_over_time()

    # Show a heatmap where mood-based features like energy or valence are averaged per genre.
    with col2:
        st.subheader("Mood Metrics by Genre")
        st.markdown("Select a mood-related audio feature (like energy or valence) to compare across genres.")
        plot_mood_heatmap()

    col3, col4 = st.columns(2)

    # A scatterplot to show how genres vary in emotional and rhythmic space.
    # High valence and danceability typically means upbeat tracks.
    with col3:
        st.subheader("Mood Landscape: Valence vs Danceability")
        st.markdown("Genres in the top-right are both upbeat and danceable.")
        plot_valence_vs_danceability()

    # Clustered genres using KMeans or other unsupervised learning based on mood features.
    # Gives a higher-level view of how genres group based on shared audio characteristics.
    with col4:
        st.subheader("Genre Clusters Based on Mood Similarity")
        plot_genre_clusters()

# Tab 2 provides analysis of language usage in global music, as well as country-level artist data.
with tab2:
    st.subheader("Language and Country Trends")

    col1, col2 = st.columns(2)

    # Horizontal bar chart showing the most frequently detected languages in charted songs.
    # Based on language detection applied to track titles or metadata.
    with col1:
        st.markdown("🈷 **Top Languages in Global Music**")
        st.markdown("Which languages appear most frequently in charted track titles? Hover to see the full names.")
        plot_language_distribution_expanded()

    # Vertical bar chart showing countries with the highest number of unique artists in the dataset.
    # This gives a sense of global music diversity and artist productivity by region.
    with col2:
        st.markdown("**Top Countries by Unique Artists**")
        st.markdown("Which countries produce the most distinct artists featured in global charts?")
        plot_top_artist_countries()

    col3, col4 = st.columns(2)

    # Entropy-based metric visualized per country or region.
    # High entropy = more language diversity; low entropy = more linguistic uniformity.
    with col3:
        st.markdown("**Language Entropy by Region**")
        st.markdown("Measures how evenly languages are distributed in a region’s music charts.")
        plot_language_entropy()

# Tab 3 combines a choropleth-style map with an interactive machine learning form.
# This tab is especially useful for showcasing advanced skills like clustering and model prediction.
with tab3:
    st.subheader("Artist Origin Insights")

    col1, col2 = st.columns(2)

    # Interactive global map showing where artists in the charts are coming from.
    # Uses data from a `country_utils` table joined to artist or region info.
    with col1:
        st.markdown("**Global Artist Origin Map**")
        st.markdown("Each circle shows where artists are coming from based on chart data.")
        plot_artist_map()

    # This interactive form allows users to input audio features and predict a genre cluster.
    # Based on a trained unsupervised ML model (e.g., KMeans) on mood-based audio features.
    with col2:
        st.markdown("**Advanced Insights: Mood-Based Genre Cluster Predictor**")
        st.markdown("Enter track mood features to predict the likely genre cluster.")

        with st.form("mood_predictor_form"):
            col1_, col2_, col3_, col4_ = st.columns(4)

            # Collect user input for mood-related features commonly available via Spotify API
            valence = col1_.slider("Valence", 0.0, 1.0, 0.5)
            energy = col2_.slider("Energy", 0.0, 1.0, 0.5)
            danceability = col3_.slider("Danceability", 0.0, 1.0, 0.5)
            tempo = col4_.slider("Tempo", 50.0, 200.0, 120.0)

            acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5)
            instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.0)
            liveness = st.slider("Liveness", 0.0, 1.0, 0.2)
            speechiness = st.slider("Speechiness", 0.0, 1.0, 0.1)

            submitted = st.form_submit_button("Predict Genre Cluster")

            if submitted:
                # Load the trained clustering model from disk (e.g., using joblib or pickle)
                model = load_mood_cluster_model()

                import pandas as pd
                # Wrap user input into a DataFrame so it's compatible with the model's `.predict()` method
                input_df = pd.DataFrame([{
                    "valence": valence,
                    "danceability": danceability,
                    "energy": energy,
                    "tempo": tempo,
                    "acousticness": acousticness,
                    "instrumentalness": instrumentalness,
                    "liveness": liveness,
                    "speechiness": speechiness
                }])

                # Predict which mood-based genre cluster the input features belong to
                prediction = model.predict(input_df)[0]

                # Load precomputed genre labels for each cluster from CSV
                cluster_df = pd.read_csv("data/genre_clusters.csv")
                genres_in_cluster = cluster_df[
                    cluster_df["cluster"] == prediction
                ]["track_genre"].dropna().unique()

                # Display the result to the user
                st.success(f"Predicted Cluster: Cluster {prediction}")
                st.markdown("Likely genres in this cluster:")
                st.markdown(", ".join(f"**{genre}**" for genre in sorted(genres_in_cluster)))

# Show footer with attribution and technology stack
st.markdown("Made by Bria Tran | Powered by Spotify, Kaggle, pandas, and Streamlit")