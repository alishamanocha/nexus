from fastapi import FastAPI, HTTPException

from backend.graph.builder import build_graph
from backend.graph.utils import get_course_subgraph
from backend.models.concepts import Concept
from backend.models.courses import Course
from backend.models.graph import CourseGraph
from backend.sample_data import concepts, courses

app = FastAPI()

CONCEPTS = [Concept.model_validate(c) for c in concepts]
COURSES = [Course.model_validate(c) for c in courses]
CONCEPT_GRAPH = build_graph(CONCEPTS)


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
