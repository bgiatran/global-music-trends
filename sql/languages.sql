-- Drop the existing view if it exists to avoid errors when re-running the script
DROP VIEW IF EXISTS languages;

-- Create a view that summarizes how many tracks appear in each language,
-- by region and year, based on chart performance data
CREATE VIEW languages AS
SELECT
    ld.language AS language,               -- Detected language of the track
    c.region AS region,                    -- Country or region where the track charted
    strftime('%Y', c.date) AS year,        -- Extract the year from the chart date for trend analysis
    COUNT(*) AS track_count                -- Count of tracks matching this language-region-year combo
FROM charts c
JOIN lang_detect ld
    -- Join on both track name and artist name to accurately match language detection results
    ON c.track_name = ld.name AND c.artist_name = ld.artist_name
WHERE ld.language IS NOT NULL              -- Exclude rows with undetected or null language values
GROUP BY ld.language, c.region, year;      -- Aggregate results by language, region, and year