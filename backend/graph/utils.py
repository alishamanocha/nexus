"""Graph utility functions for concept and course subgraphs."""

from typing import cast

import networkx as nx


def get_course_subgraph(G: nx.DiGraph, course_id: str) -> nx.DiGraph:
    """Return a subgraph containing only the concepts for a given course.

    Args:
        G (nx.DiGraph): The full concept dependency graph.
        course_id (str): The ID of the course for which to extract the subgraph.

    Returns:
        nx.DiGraph: A directed graph containing only the nodes (concepts) that belong to the specified course, with edges preserved.
    """
    nodes = [
        n for n, attr in G.nodes(data=True) if attr["concept"].course_id == course_id
    ]
    return cast("nx.DiGraph", G.subgraph(nodes).copy())
