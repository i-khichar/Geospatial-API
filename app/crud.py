from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/karnataka_db"

engine = create_engine(DATABASE_URL)

def get_features():
    """Retrieve all features from the geojson_data table."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, fill, ST_AsGeoJSON(geometry) AS geometry FROM geojson_data;"))
        return [row for row in result.mappings()]

def get_feature_by_id(feature_id):
    """Retrieve a single feature by its ID."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, fill, ST_AsGeoJSON(geometry) AS geometry FROM geojson_data WHERE id = :id"),{"id": feature_id})
        # Convert the result to a dictionary
        row = result.mappings().first()  # Get the first (and only) result row as a dictionary
        return row

def create_feature(fill, geometry):
    """Insert a new feature into the geojson_data table."""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO geojson_data (fill, geometry)
            VALUES (:fill, ST_GeomFromGeoJSON(:geometry))
        """), {"fill": fill, "geometry": geometry})
        conn.commit()

def update_feature(feature_id, fill, geometry):
    """Update an existing feature by its ID."""
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE geojson_data
                SET fill = :fill,
                    geometry = ST_GeomFromGeoJSON(:geometry)
                WHERE id = :id
            """),
            {"id": feature_id, "fill": fill, "geometry": geometry}
        )
        conn.commit()

def delete_feature(feature_id):
    """Delete a feature by its ID."""
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM geojson_data WHERE id = :id"), {"id": feature_id})
        conn.commit()
