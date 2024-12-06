from pydantic import BaseModel

class GeoJSONFeature(BaseModel):
    id: int
    geometry: dict
    properties: dict
