from fastapi import FastAPI
from app.crud import get_features

app = FastAPI()

@app.get("/features")
def read_features():
    return get_features()
