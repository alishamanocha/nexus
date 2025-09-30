import networkx as nx
from pydantic import BaseModel

from backend.models.concepts import Concept


class ConceptNode(BaseModel):
    id: str
    concept: Concept


class ConceptEdge(BaseModel):
    source: str
    target: str


class CourseGraph(BaseModel):
    course_id: str
    nodes: list[ConceptNode]
    links: list[ConceptEdge]

    @classmethod
    def from_networkx(cls, course_id: str, G: nx.DiGraph) -> "CourseGraph":
        """Convert a networkx DiGraph with Concept nodes into a CourseGraph."""
        nodes = [
            ConceptNode(id=node_id, concept=attr["concept"])
            for node_id, attr in G.nodes(data=True)
        ]
        links = [ConceptEdge(source=u, target=v) for u, v in G.edges()]
        return cls(course_id=course_id, nodes=nodes, links=links)
