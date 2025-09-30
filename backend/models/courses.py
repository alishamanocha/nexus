"""Data models for courses."""

from pydantic import BaseModel

from backend.models.concepts import Concept


class Course(BaseModel):
    """Represents a course containing multiple concepts."""

    id: str
    name: str
    description: str
    concepts: list[Concept]
