from fastapi import FastAPI, HTTPException

from backend.models.courses import Course
from backend.sample_data.calculus import course

app = FastAPI()


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    # The only sample data I have created is for calculus, so far
    if course_id != "calculus":
        raise HTTPException(status_code=404, detail="Course not found")
    course_model = Course.model_validate(course)
    return course_model
