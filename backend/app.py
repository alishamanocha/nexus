"""Main FastAPI application entrypoint."""

from datetime import timedelta
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                          create_access_token, get_current_user,
                          get_password_hash, set_access_token_cookie,
                          validate_username)
from backend.graph.builder import build_graph
from backend.graph.utils import get_course_subgraph
from backend.models.concepts import Concept
from backend.models.courses import Course
from backend.models.graph import CourseGraph
from backend.models.users import User, UserCreate
from backend.sample_data import concepts, courses, fake_users_db

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


@app.post("/signup")
def signup(user: UserCreate) -> JSONResponse:
    """Register a new user and issue an access token.

    This endpoint validates the username, hashes the password, stores the user in the database, and returns a response with a session cookie set.

    Args:
        user (UserCreate): The user signup data including username, full name, email, and password.

    Returns:
        JSONResponse: A response indicating success, with an access token set as a secure cookie.

    Raises:
        HTTPException: If the username is already registered.

    """
    if not validate_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(user.password)

    new_user = {
        "id": str(uuid4()),
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": hashed_password,
    }

    fake_users_db.append(new_user)

    access_token = create_access_token(data={"sub": new_user["id"]})
    response = JSONResponse({"message": "User created"})
    set_access_token_cookie(response, access_token)
    return response


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """Log in an existing user and issue an access token.

    This endpoint verifies the provided username and password. If valid, it creates a new access token, sets it as a secure cookie, and returns a success response.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data containing username and password.

    Returns:
        JSONResponse: A response indicating success, with an access token set as a secure cookie.

    Raises:
        HTTPException: If authentication fails due to invalid username or password.

    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    response = JSONResponse(content={"message": "Login successful"})
    set_access_token_cookie(response, access_token)
    return response


@app.post("/logout")
def logout() -> JSONResponse:
    """Log out a user by clearing the access token cookie.

    Returns:
        JSONResponse: A response confirming that the user has been logged out.
    """
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("access_token")
    return response


@app.get("/me")
def me(current_user: User = Depends(get_current_user)) -> User:
    """Retrieve user info for currently logged in user.

    Args:
        current_user (User): The currently authenticated user, injected via dependency.

    Returns:
        User: Information on the currently logged in user.
    """
    return User(**current_user.dict())


@app.get("/courses")
def get_courses(user: User = Depends(get_current_user)) -> list[Course]:
    """Retrieve the list of available courses.

    Args:
        user (User): The currently authenticated user, injected via dependency.

    Returns:
        list[Course]: A list of all available courses.
    """
    return COURSES


@app.get("/courses/{course_id}")
def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
) -> Course:
    """Retrieve course information by ID.

    Args:
        course_id (str): The ID of the course to retrieve.
        current_user (User): The currently authenticated user, injected via dependency.

    Returns:
        Course: The course object containing course details.

    Raises:
        HTTPException: If the course does not exist.
    """
    course = next((c for c in COURSES if c.id == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/{course_id}/graph")
def get_course_graph(
    course_id: str,
    current_user: User = Depends(get_current_user),
) -> CourseGraph:
    """Retrieve the concept graph for a course by ID.

    Args:
        course_id (str): The ID of the course for which to retrieve the graph.
        current_user (User): The currently authenticated user, injected via dependency.

    Returns:
        CourseGraph: A graph object representing all concepts and their relationships within the course.

    Raises:
        HTTPException: If the course does not exist or has no concepts.
    """
    course = next((c for c in COURSES if c.id == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    subG = get_course_subgraph(CONCEPT_GRAPH, course_id)
    if subG.number_of_nodes() == 0:
        raise HTTPException(status_code=404, detail="No concepts found for this course")

    return CourseGraph.from_networkx(course_id, subG)


@app.get("/concepts/{concept_id}")
def get_concept(
    concept_id: str,
    current_user: User = Depends(get_current_user),
) -> Concept:
    """Get information on a concept."""
    concept = next((c for c in CONCEPTS if c.id == concept_id), None)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept
