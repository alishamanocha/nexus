from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.graph.builder import build_graph
from backend.graph.utils import get_course_subgraph
from backend.models.concepts import Concept
from backend.models.courses import Course
from backend.models.graph import CourseGraph
from backend.sample_data import concepts, courses

app = FastAPI()

DEV_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONCEPTS = [Concept.model_validate(c) for c in concepts]
COURSES = [Course.model_validate(c) for c in courses]
CONCEPT_GRAPH = build_graph(CONCEPTS)


@app.get("/courses")
def get_courses() -> List[Course]:
    return COURSES


@app.get("/courses/{course_id}")
def get_course(course_id: str) -> Course:
    """Get course information given a course id."""
    course = next((c for c in COURSES if c.id == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/{course_id}/graph")
def get_course_graph(course_id: str) -> CourseGraph:
    """Get a course graph given a course id."""
    course = next((c for c in COURSES if c.id == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    subG = get_course_subgraph(CONCEPT_GRAPH, course_id)
    if subG.number_of_nodes() == 0:
        raise HTTPException(status_code=404, detail="No concepts found for this course")

    return CourseGraph.from_networkx(course_id, subG)


@app.get("/concepts/{concept_id}")
def get_concept(concept_id: str) -> Concept:
    """Get information on a concept."""
    concept = next((c for c in CONCEPTS if c.id == concept_id), None)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept
