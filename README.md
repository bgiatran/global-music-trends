# Global Music Trends Dashboard

> **⚠️ Important Notice:**  
> Due to file size limits and licensing, full datasets and the SQLite database are not uploaded.  
> However, the full project structure, scripts, and documentation are provided to support reproducibility.

## Project Summary

This project analyzes **global music trends from 2017 to 2023**, offering insights into genre evolution, mood metrics, language diversity, and artist geography. It combines data from **Kaggle**, **Spotify Charts**, **language detection APIs**, and custom ML clustering tools to explore the worldwide music landscape.

Due to **limited access to Spotify’s audio features API** and an inactive SoundCloud key, I worked with **public datasets**, **archived feature exports**, and **preloaded metadata** instead of live APIs. I built this dashboard around a large SQLite database (~3GB), which cannot be uploaded to GitHub—but all scripts and screenshots have been shared to show the full pipeline and outcomes.

---

### Technical Stack

| Category         | Tools & Technologies                                                                 |
|------------------|----------------------------------------------------------------------------------------|
| **Languages**     | Python, SQL                                                                          |
| **Libraries**     | pandas, scikit-learn, langdetect, sqlite3                                             |
| **Visualization** | Streamlit, Altair, Plotly, Mapbox                                                    |
| **Machine Learning** | KMeans Clustering                                                                 |
| **Data Sources**  | Kaggle, SpotifyCharts.com, LangDetect                                                |

---

## Project Goals

- Track **genre trends and mood shifts** over time
- Analyze **valence, energy, danceability** across genres and countries
- Examine **language entropy** to gauge musical diversity
- Identify **top contributing countries and unique artists**
- Visualize **artist origins on a world map**
- Build a basic **ML genre prediction tool** based on mood clusters

---

## Development Process

This project required:

- Gathering and cleaning large, noisy datasets from **Kaggle**, **SpotifyCharts**, and language detection APIs
- Merging datasets with inconsistent naming conventions, missing keys, and messy formats
- Designing SQL schemas but shifting much of the pipeline to Python due to JOIN and memory limitations
- Building modular scripts to support language detection, country geocoding, feature aggregation, clustering, and Streamlit layout

---

## Feature Walkthrough

Each section of the dashboard reveals a different dimension of global music evolution. The charts were designed with storytelling and real-world business applications in mind—such as talent scouting, cultural strategy, or platform localization.

### Genre Trends Over Time & Mood Metrics

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>What it includes:</h3>
    <ul>
      <li><strong>Top Genres Over Time (2017–2023):</strong> Stacked line chart shows how genres like pop, hip-hop, and reggaeton shifted globally. This reveals seasonality and rise/fall of trends.</li>
      <li><strong>Mood Metrics by Genre:</strong> A horizontal bar chart comparing average valence, energy, and danceability for each genre.</li>
    </ul>

  <p><strong>Why it matters:</strong>  
  This section shows the evolution of consumer taste and helps identify fast-growing or fading genres—insights that are key for music labels and playlist curators.</p>

  <p><strong>Real-world application:</strong>  
  Platforms like Spotify can use this to time promotions or tailor editorial strategies by genre-mood shifts.</p>

  <img src="images/Screenshot (106).png" width="100%">
  </div>
</div>

---

### Mood Landscape & Genre Clusters

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>What it includes:</h3>
    <ul>
      <li><strong>Valence vs. Danceability Scatterplot:</strong> Genres plotted in a 2D space based on emotion (valence) and movement (danceability). Top-right = happy and danceable.</li>
      <li><strong>Genre Mood Clusters:</strong> Using KMeans clustering, genres are grouped into mood-based categories (e.g. calm, energetic, dark).</li>
    </ul>

  <p><strong>Why it matters:</strong>  
  Understanding emotional space helps build mood-specific playlists, music recommendation engines, and marketing segments.</p>

  <p><strong>Real-world application:</strong>  
  Streaming platforms or A&R teams can segment listener profiles based on these mood clusters to enhance user personalization.</p>

  <img src="images/Screenshot (107).png" width="100%">
  </div>
</div>

---

### Top Music Countries & Unique Artist Counts

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>What it includes:</h3>
    <ul>
      <li><strong>Top Countries by Chart Appearances:</strong> Ranked bar chart of countries whose artists appear most in top charts globally.</li>
      <li><strong>Top Countries by Unique Artists:</strong> Highlights artist diversity per country, not just total appearances.</li>
    </ul>

  <p><strong>Why it matters:</strong>  
  This identifies **global hubs** of musical influence and **rising markets** where platforms can invest in outreach or localization.</p>

  <p><strong>Real-world application:</strong>  
  Useful for international expansion planning, talent scouting, and understanding music export markets.</p>

  <img src="images/Screenshot (108).png" width="100%">
  </div>
</div>

---

### Language Entropy by Region

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>What it includes:</h3>
    <ul>
      <li><strong>Language Entropy Score:</strong> Measures linguistic diversity in charts by country. Higher entropy = more languages used.</li>
    </ul>

  <p><strong>Why it matters:</strong>  
  Language entropy reveals **how open regions are to multilingual content**, which is critical for localization and translation strategies.</p>

  <p><strong>Real-world application:</strong>  
  Streaming platforms can prioritize subtitling, lyrics translation, or even UI localization based on entropy scores.</p>
<img src="images/Screenshot (109).png" width="100%">  
</div>
</div>

---

### Artist Origin Map & Genre Cluster Predictor

<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>What it includes:</h3>
    <ul>
      <li><strong>Artist Origin Map:</strong> A Mapbox visualization showing the birthplaces of charting artists.</li>
      <li><strong>Genre Cluster Predictor:</strong> Interactive sliders to input mood features (valence, energy, etc.) and get back a genre cluster prediction.</li>
    </ul>

  <p><strong>Why it matters:</strong>  
  Helps visualize **global creative hotspots** and empowers users or developers to explore how musical traits map to genre clusters.</p>

  <p><strong>Real-world application:</strong>  
  This tool could support playlist automation, discovery algorithms, or artist mood branding strategies.</p>

  <img src="images/Screenshot (111).png" width="100%">
  </div>
</div>

---

## What I Learned

- How to join and reconcile multiple **schema-incompatible datasets**
- Strategies for handling **large-scale preprocessing** and memory constraints
- How to use **language detection**, geocoding, and ML clustering in music analytics
- Importance of **project architecture** when dealing with many scripts, modules, and files
- The value of **data visualization** to tell meaningful stories with numbers

---

## Challenges

- The Spotify Audio Features API was unavailable, so I relied on archived datasets and public metadata
- My **SoundCloud API key stopped working**, limiting platform coverage
- The **database size (~1GB)** was too large to upload or load in-memory for real-time interaction
- Originally planned SQL queries were replaced by Python due to JOIN failures, memory overload, and indexing issues
- Significant effort was spent aligning inconsistent column names and resolving dataset mismatches

---

## Future Plans

- Create a **cleaner modular folder structure** with better naming and deduplication
- Implement a **user-friendly config system** to re-run the pipeline with custom data
- Rebuild the app with **streamlined SQL + DuckDB** for faster join performance
- Add SoundCloud + YouTube support when keys/API access become available
- Expand the ML predictor to include **genre evolution** and **cross-country mood shifts**

---

## Author

**Bria Tran**  
GitHub: [@bgiatran](https://github.com/bgiatran)  
Made with passion for music, data, and global storytelling.
