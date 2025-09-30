"""Data models for course graphs."""

import networkx as nx
from pydantic import BaseModel

from backend.models.concepts import Concept


class ConceptNode(BaseModel):
    """Represents a single node in a course graph."""

    id: str
    concept: Concept


class ConceptEdge(BaseModel):
    """Represents a directed edge between two concept nodes."""

    source: str
    target: str


class CourseGraph(BaseModel):
    """Represents a course as a graph of concepts."""

    course_id: str
    nodes: list[ConceptNode]
    links: list[ConceptEdge]

    @classmethod
    def from_networkx(cls, course_id: str, G: nx.DiGraph) -> "CourseGraph":
        """Convert a networkx DiGraph with Concept nodes into a CourseGraph.

        Args:
            course_id (str): The ID of the course.
            G (nx.DiGraph): A DAG where nodes have a 'concept' attribute containing a `Concept` object and edges represent prerequisites.

        Returns:
            CourseGraph: A CourseGraph instance representing the course graph with nodes and edges extracted from the networkx graph.
        """
        nodes = [
            ConceptNode(id=node_id, concept=attr["concept"])
            for node_id, attr in G.nodes(data=True)
        ]
        links = [ConceptEdge(source=u, target=v) for u, v in G.edges()]
        return cls(course_id=course_id, nodes=nodes, links=links)
