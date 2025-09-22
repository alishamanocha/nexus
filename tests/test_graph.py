from typing import List

import pytest

from backend.graph.builder import build_graph
from backend.graph.utils import get_course_subgraph
from backend.models.concepts import Concept
from backend.models.graph import ConceptEdge, ConceptNode, CourseGraph

valid_concepts: List[Concept] = [
    Concept(
        id="A", name="A", course_id="course1", description="concept A", prerequisites=[]
    ),
    Concept(
        id="B",
        name="B",
        course_id="course1",
        description="concept B",
        prerequisites=["A"],
    ),
    Concept(
        id="C",
        name="C",
        course_id="course1",
        description="concept C",
        prerequisites=["A", "B"],
    ),
    Concept(
        id="D",
        name="D",
        course_id="course2",
        description="concept D",
        prerequisites=[],
    )
]

valid_prereq_edges = [
    ConceptEdge(source="A", target="B"),
    ConceptEdge(source="A", target="C"),
    ConceptEdge(source="B", target="C"),
]


def test_build_graph_creates_nodes_and_edges():
    G = build_graph(valid_concepts)

    assert len(G.nodes) == len(valid_concepts)
    assert set(G.nodes) == {c.id for c in valid_concepts}
    assert len(G.edges) == len(valid_prereq_edges)
    assert set(G.edges) == {(e.source, e.target) for e in valid_prereq_edges}

    for c in valid_concepts:
        assert isinstance(G.nodes[c.id]["concept"], Concept)
        assert G.nodes[c.id]["concept"] == c


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


def test_get_course_subgraph():
    G = build_graph(valid_concepts)

    def check_concepts_in_course_subgraph(G, course_id):
        expected_concepts = sorted(
            [c for c in valid_concepts if c.course_id == course_id],
            key=lambda n: n.id,
        )
        assert len(G.nodes) == len(expected_concepts)
        assert set(G.nodes) == {c.id for c in expected_concepts}

    course_id = "course1"
    subG = get_course_subgraph(G, course_id)

    check_concepts_in_course_subgraph(subG, course_id)

    assert len(subG.edges) == len(valid_prereq_edges)
    assert set(subG.edges) == {(e.source, e.target) for e in valid_prereq_edges}

    course_id = "course2"
    subG = get_course_subgraph(G, course_id)

    check_concepts_in_course_subgraph(subG, course_id)
    assert len(subG.edges) == 0


def test_coursegraph_from_networkx():
    G = build_graph(valid_concepts)

    course_id = "course1"
    subG = get_course_subgraph(G, course_id)

    course_graph = CourseGraph.from_networkx(course_id, subG)

    assert course_graph.course_id == course_id

    expected_nodes = sorted(
        [ConceptNode(id=c.id, concept=c) for c in valid_concepts if c.course_id == course_id],
        key=lambda n: n.id,
    )
    assert sorted(course_graph.nodes, key=lambda n: n.id) == expected_nodes

    assert sorted(course_graph.links, key=lambda link: (link.source, link.target)) == sorted(valid_prereq_edges, key=lambda e: (e.source, e.target))
