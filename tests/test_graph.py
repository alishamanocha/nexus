from typing import List

import pytest

from backend.graph.builder import build_graph
from backend.models.concepts import Concept
from backend.models.graph import ConceptEdge, ConceptNode, CourseGraph

valid_concepts: List[Concept] = [
    Concept(
        id="A", name="A", course_id="course", description="concept A", prerequisites=[]
    ),
    Concept(
        id="B",
        name="B",
        course_id="course",
        description="concept B",
        prerequisites=["A"],
    ),
    Concept(
        id="C",
        name="C",
        course_id="course",
        description="concept C",
        prerequisites=["A", "B"],
    ),
]


def test_build_graph_creates_nodes_and_edges():
    G = build_graph(valid_concepts)

    assert len(G.nodes) == 3
    assert set(G.nodes) == {"A", "B", "C"}
    assert len(G.edges) == 3
    assert set(G.edges) == {("A", "B"), ("A", "C"), ("B", "C")}

    assert isinstance(G.nodes["A"]["concept"], Concept)
    assert G.nodes["A"]["concept"].id == "A"


def test_build_graph_raises_on_missing_prereq():
    concepts = [
        Concept(
            id="A",
            name="A",
            course_id="course",
            description="concept A",
            prerequisites=["Z"],
        ),
    ]

    with pytest.raises(ValueError, match="Prerequisite Z not found"):
        build_graph(concepts)


def test_coursegraph_from_networkx():
    G = build_graph(valid_concepts)

    course_graph = CourseGraph.from_networkx("course1", G)

    assert course_graph.course_id == "course1"
    assert sorted(course_graph.nodes, key=lambda n: n.id) == sorted(
        [ConceptNode(id=c.id, concept=c) for c in valid_concepts], key=lambda n: n.id
    )
    assert sorted(course_graph.links, key=lambda link: (link.source, link.target)) == [
        ConceptEdge(source="A", target="B"),
        ConceptEdge(source="A", target="C"),
        ConceptEdge(source="B", target="C"),
    ]
