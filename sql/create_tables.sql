-- Drop tables if they already exist (safe for reruns)
DROP TABLE IF EXISTS close_approaches;
DROP TABLE IF EXISTS asteroids;

-- =========================
-- Asteroids master table
-- =========================
CREATE TABLE asteroids (
    neo_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    absolute_magnitude_h NUMERIC,
    estimated_diameter_min_km NUMERIC,
    estimated_diameter_max_km NUMERIC,
    is_potentially_hazardous BOOLEAN
);

-- =========================
-- Close approach events
-- =========================
CREATE TABLE close_approaches (
    approach_id SERIAL PRIMARY KEY,
    neo_id BIGINT REFERENCES asteroids(neo_id),
    close_approach_date DATE,
    miss_distance_km NUMERIC,
    relative_velocity_km_s NUMERIC,
    orbiting_body TEXT
);
