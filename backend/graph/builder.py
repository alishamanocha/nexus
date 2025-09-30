import networkx as nx

from backend.models.concepts import Concept


def build_graph(concepts: list[Concept]) -> nx.DiGraph:
    """Build a DAG of concepts, where nodes represent concepts and edges represent prerequisite relationships."""
    G: nx.DiGraph = nx.DiGraph()

    for c in concepts:
        G.add_node(c.id, concept=c)

    for c in concepts:
        for prereq_id in c.prerequisites:
            if prereq_id in G:
                G.add_edge(prereq_id, c.id)
            else:
                raise ValueError(
                    f"Prerequisite {prereq_id} not found for concept {c.id}",
                )

    return G
