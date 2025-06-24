-- Drop the view if it already exists to avoid conflicts during recreation
DROP VIEW IF EXISTS artist_origin_map;

-- Create a view to map the number of unique artists per country,
-- along with their corresponding latitude and longitude for mapping
CREATE VIEW artist_origin_map AS
SELECT
    c.region AS country,  -- Rename region column to 'country' for clarity
    COUNT(DISTINCT c.artist_name) AS artist_count,  -- Count unique artists per country
    cu.latitude,
    cu.longitude
FROM charts c
JOIN country_utils cu
    -- Normalize country names (trim + lowercase) to ensure matching despite case or extra spaces
    ON LOWER(TRIM(c.region)) = LOWER(TRIM(cu.country_name))
WHERE cu.latitude IS NOT NULL AND cu.longitude IS NOT NULL  -- Exclude countries with missing coordinates
GROUP BY c.region, cu.latitude, cu.longitude;  -- Group by country and location to prepare for mapping