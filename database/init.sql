-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the table to store geojson data
CREATE TABLE IF NOT EXISTS geojson_data (
    id SERIAL PRIMARY KEY,                                -- Auto-incrementing ID
    fill VARCHAR(10) NOT NULL,                           -- To store the 'fill' property
    geometry GEOMETRY(Polygon, 4326) NOT NULL            -- Geometry column in EPSG:4326
);

-- Empty the table
TRUNCATE TABLE geojson_data;
