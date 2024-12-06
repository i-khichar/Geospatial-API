from fastapi import FastAPI, HTTPException
from app.crud import get_features, get_feature_by_id, create_feature, update_feature, delete_feature
from app.models import FeatureCreate, FeaturePartialUpdate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/features")
def read_features():
    """Retrieve all features."""
    return get_features()

@app.get("/features/{feature_id}")
def read_feature(feature_id: int):
    """Retrieve a single feature by its ID."""
    feature = get_feature_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature

@app.post("/features")
def add_feature(feature: FeatureCreate):
    """Add a new feature to the database."""
    create_feature(feature.fill, feature.geometry)
    return {"message": "Feature added successfully"}

@app.put("/features/{feature_id}")
def modify_feature(feature_id: int, feature: FeaturePartialUpdate):
    """Update an existing feature."""
    existing_feature = get_feature_by_id(feature_id)
    if not existing_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    fill = feature.fill if feature.fill is not None else existing_feature["fill"]
    geometry = feature.geometry if feature.geometry is not None else existing_feature["geometry"]

    # Perform the update
    update_feature(feature_id, fill, geometry)
    return {"message": "Feature updated successfully"}

@app.delete("/features/{feature_id}")
def remove_feature(feature_id: int):
    """Delete a feature."""
    feature = get_feature_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    delete_feature(feature_id)
    return {"message": "Feature deleted successfully"}
