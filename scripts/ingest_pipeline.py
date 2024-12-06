import requests
import json
import psycopg2
from psycopg2.extras import execute_values
from pyproj import Transformer
from datetime import datetime

# Database connection
DB_CONFIG = {
    "dbname": "karnataka_db",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": 5432,
}

# GeoJSON URL
GEOJSON_URL = "http://example.com/karnataka.geojson"

transformer = Transformer.from_crs("EPSG:2000", "EPSG:4326", always_xy=True)
output_file = "transformed.json"

def fetch_geojson():
    """Fetch GeoJSON data from the URL."""
    response = requests.get(GEOJSON_URL)
    response.raise_for_status()
    return response.json()

# Transform coordinates in GeoJSON
def transform_coordinates(geometry):
    if geometry["type"] == "Point":
        # Transform a single point
        return list(transformer.transform(*geometry["coordinates"]))
    elif geometry["type"] in ["LineString", "MultiPoint"]:
        # Transform a list of points
        return [list(transformer.transform(*coords)) for coords in geometry["coordinates"]]
    elif geometry["type"] in ["Polygon", "MultiLineString"]:
        # Transform a list of rings or lines
        return [[list(transformer.transform(*coords)) for coords in ring] for ring in geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        # Transform a list of polygons
        return [[[list(transformer.transform(*coords)) for coords in ring] for ring in polygon] for polygon in geometry["coordinates"]]
    else:
        raise ValueError(f"Geometry type {geometry['type']} is not supported")

def transform_geojson(input_file):
    with open(input_file, 'r') as f:
        geojson_data = json.load(f)
    for feature in geojson_data["features"]:
        feature["geometry"]["coordinates"] = transform_coordinates(feature["geometry"])
    with open(output_file, 'w') as f:
        json.dump(geojson_data, f, indent=4)
    return geojson_data


def ingest_to_db(features):
    """Ingest transformed GeoJSON into the database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for feature in features["features"]:
            geom = json.dumps(feature["geometry"])  # Convert geometry to GeoJSON string
            fill = feature["properties"].get("fill", "#000")  # Default to "#000" if not provided

        # Insert into the database
            sql = """
            INSERT INTO geojson_data (fill, geometry)
            VALUES (%s, ST_GeomFromGeoJSON(%s));
            """
            cursor.execute(sql, (fill, geom))

        conn.commit()
        print("Data ingested successfully!")
    except Exception as e:
        print(f"Error ingesting data: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    # geojson = fetch_geojson()
    geojson = "karnataka_data.json"
    features = transform_geojson(geojson)
    ingest_to_db(features)

if __name__ == "__main__":
    main()
