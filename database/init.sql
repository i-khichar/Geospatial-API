-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the table to store geospatial data
CREATE TABLE IF NOT EXISTS geospatial_data (
    id SERIAL PRIMARY KEY,                                -- Auto-incrementing ID
    fill VARCHAR(10) NOT NULL,                           -- To store the 'fill' property
    geometry GEOMETRY(Polygon, 4326) NOT NULL            -- Geometry column in EPSG:4326
);
