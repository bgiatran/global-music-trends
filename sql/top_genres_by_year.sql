-- Drop the view if it already exists to allow safe recreation without errors
DROP VIEW IF EXISTS top_genres_by_year;

-- Create a view that shows the number of charting tracks per genre by year
-- This helps analyze genre trends in global music popularity over time
CREATE VIEW top_genres_by_year AS
SELECT
    strftime('%Y', c.date) AS year,         -- Extract the year from the chart date
    af.track_genre,                         -- Genre classification from the audio features table
    COUNT(*) AS track_count                 -- Total number of tracks for this genre in that year
FROM charts c
JOIN audio_features af
    -- Join on track name and artist name to accurately map chart entries to their audio features
    ON c.track_name = af.track_name AND c.artist_name = af.artist_name
WHERE af.track_genre IS NOT NULL            -- Exclude tracks without genre information
GROUP BY year, af.track_genre;              -- Group results by year and genre for aggregation