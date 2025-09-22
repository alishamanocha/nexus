from fastapi import FastAPI, HTTPException

from backend.graph.builder import build_graph
from backend.models.courses import Course
from backend.models.graph import CourseGraph
from backend.sample_data.calculus import course

app = FastAPI()


@app.get("/courses/{course_id}")
def get_course(course_id: str) -> Course:
    """Get course information given a course id."""
    # The only sample data I have created is for calculus, so far
    if course_id != "calculus":
        raise HTTPException(status_code=404, detail="Course not found")
    course_model = Course.model_validate(course)
    return course_model


@app.get("/courses/{course_id}/graph")
def get_course_graph(course_id: str) -> CourseGraph:
    """
    Get a course graph given a course id.
    This currently builds the networkx graph for each call to this endpoint, but will eventually pull from an in-memory graph cache.
    """
    # The only sample data I have created is for calculus, so far
    if course_id != "calculus":
        raise HTTPException(status_code=404, detail="Course not found")
    course_model = Course.model_validate(course)
    G = build_graph(course_model.concepts)
    return CourseGraph.from_networkx(course_id, G)
