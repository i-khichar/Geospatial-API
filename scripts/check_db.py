import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "karnataka_db",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",  # Or the IP of your PostgreSQL container
    "port": 5432          # Default PostgreSQL port
}

# SQL command to create the geo_data table
CREATE_TABLE_SQL = """
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS geo_data (
    id SERIAL PRIMARY KEY,            -- Auto-incrementing ID
    fill VARCHAR(10) NOT NULL,        -- To store the 'fill' property
    geometry GEOMETRY(Polygon, 4326) NOT NULL -- Geometry column in EPSG:4326
);
"""
QUERY_DB_SQL = """
SELECT * FROM geojson_data;
"""


def create_table():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the SQL command to create the table
        cursor.execute(QUERY_DB_SQL)
        conn.commit()

        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        # Clean up
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()
