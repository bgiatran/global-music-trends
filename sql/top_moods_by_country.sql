-- View/Table: top_moods_by_country
-- Calculates average mood-related audio features per country and year
-- This is useful for comparing how the musical "mood" shifts across regions and over time

-- Drop the view if it exists (useful if you were originally testing this as a view)
DROP VIEW IF EXISTS top_moods_by_country;

-- Instead of a view, create a persistent table to store pre-aggregated mood data
-- This can improve performance for dashboards or downstream analysis
CREATE TABLE IF NOT EXISTS top_moods_by_country AS
SELECT
    strftime('%Y', c.date)             AS year,               -- Extract the year from the chart date
    c.region                           AS country,            -- Region where the track charted (used as proxy for audience location)

    -- Calculate the average of each mood-related feature, rounded for readability
    ROUND(AVG(af.valence), 3)          AS avg_valence,        -- Valence: musical positivity
    ROUND(AVG(af.energy), 3)           AS avg_energy,         -- Energy: intensity and activity level
    ROUND(AVG(af.danceability), 3)     AS avg_danceability,   -- Danceability: rhythm suitability for dancing
    ROUND(AVG(af.tempo), 2)            AS avg_tempo,          -- Tempo: beats per minute
    ROUND(AVG(af.acousticness), 3)     AS avg_acousticness,   -- Acousticness: likelihood of acoustic instrumentation
    ROUND(AVG(af.instrumentalness), 3) AS avg_instrumentalness, -- Instrumentalness: presence of vocals
    ROUND(AVG(af.liveness), 3)         AS avg_liveness,       -- Liveness: likelihood of live audience presence
    ROUND(AVG(af.speechiness), 3)      AS avg_speechiness,    -- Speechiness: presence of spoken words

    COUNT(*)                           AS total_tracks        -- Number of tracks included in the calculation
FROM charts c
JOIN audio_features af
    -- Join tracks with their audio features using both name and artist
    ON c.track_name = af.track_name AND c.artist_name = af.artist_name
WHERE af.valence IS NOT NULL
  AND af.energy IS NOT NULL
  AND af.danceability IS NOT NULL
  AND af.tempo IS NOT NULL            -- Ensure only complete data is used in mood calculations
GROUP BY year, country;               -- Aggregate results by region and year