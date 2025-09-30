from pydantic import BaseModel

from backend.models.concepts import Concept


class Course(BaseModel):
    id: str
    name: str
    description: str
    concepts: list[Concept]
