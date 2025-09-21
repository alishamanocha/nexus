import json
from pathlib import Path

from fastapi import FastAPI

from backend.models.concepts import Concept

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/concepts")
def concepts():
    data = json.loads(Path("sample_data/calculus/concepts.json").read_text())
    concepts = [Concept(**item) for item in data]
    return {"concepts": concepts}
