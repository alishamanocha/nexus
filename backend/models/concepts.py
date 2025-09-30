"""Data models for concepts in courses."""

from pydantic import BaseModel


class Concept(BaseModel):
    """Represents a concept in a course."""

    id: str
    name: str
    description: str
    course_id: str
    prerequisites: list[str]
    content: str
