from typing import cast

import networkx as nx


def get_course_subgraph(G: nx.DiGraph, course_id: str) -> nx.DiGraph:
    """Return a subgraph containing the concept nodes for a given course_id."""
    nodes = [
        n for n, attr in G.nodes(data=True) if attr["concept"].course_id == course_id
    ]
    return cast("nx.DiGraph", G.subgraph(nodes).copy())
