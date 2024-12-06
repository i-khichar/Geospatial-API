from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:yourpassword@localhost/karnataka_db"

engine = create_engine(DATABASE_URL)

def get_features():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, ST_AsGeoJSON(geometry) AS geometry, properties FROM geospatial_data;"))
        return [dict(row) for row in result]
