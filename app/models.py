from pydantic import BaseModel
from typing import Optional

class FeatureCreate(BaseModel):
    fill: str
    geometry: str

class FeaturePartialUpdate(BaseModel):
    fill: Optional[str] = None
    geometry: Optional[str] = None
