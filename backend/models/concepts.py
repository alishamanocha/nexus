from typing import List

from pydantic import BaseModel


class Concept(BaseModel):
    id: str
    name: str
    description: str
    prerequisites: List[str]
