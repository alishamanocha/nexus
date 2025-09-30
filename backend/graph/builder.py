"""Graph builder utilities for constructing concept dependency DAGs, where nodes represent concepts and edges represent prerequisite relationships."""

import networkx as nx

from backend.models.concepts import Concept


def build_graph(concepts: list[Concept]) -> nx.DiGraph:
    """Construct a DAG of concepts.

    Each concept is added as a node in the graph, and edges are added from prerequisite concepts to dependent concepts, representing prerequisite relationships.

    Args:
        concepts (list[Concept]): A list of `Concept` objects to include in the graph. Each concept should have a unique `id` and may list other concept IDs in `prerequisites`.

    Returns:
        nx.DiGraph: A directed graph representing the concept dependency relationships. Nodes are concept IDs with a `concept` attribute storing the original `Concept` object. Edges point from a prerequisite concept to its dependent concept.

    Raises:
        ValueError: If a concept references a prerequisite ID that does not exist in the provided list of concepts.
    """
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
