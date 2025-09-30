"""Authentication and authorization utilities for the backend."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel

from backend.models.users import UserInDB
from backend.sample_data import fake_users_db

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    """JWT authentication token model."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded JWT token payload (user identity)."""

    user_id: UUID


def validate_username(username: str) -> bool:
    """Check whether a username is available.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username is available, False if already taken.
    """
    return all(u["username"] != username for u in fake_users_db)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hashed version.

    Args:
        password (str): The plaintext password to verify.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return password_hash.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plaintext password using the recommended algorithm.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The securely hashed password.
    """
    return password_hash.hash(password)


def get_user_by_username(db: list[dict], username: str) -> UserInDB | None:
    """Retrieve a user by username from the database.

    Args:
        db (list[dict]): The database of users (will eventually use an actual db).
        username (str): The username to look up.

    Returns:
        UserInDB | None: The matching user, or None if not found.
    """
    for u in db:
        if u.get("username") == username:
            return UserInDB(**u)
    return None


def get_user_by_id(db: list[dict], user_id: UUID) -> UserInDB | None:
    """Retrieve a user by ID from the database.

    Args:
        db (list[dict]): The database of users (will eventually use an actual db).
        user_id (UUID): The ID of the user to look up.

    Returns:
        UserInDB | None: The matching user, or None if not found.
    """
    for u in db:
        if u.get("id") == str(user_id):
            return UserInDB(**u)
    return None


def authenticate_user(db: list[dict], username: str, password: str) -> UserInDB | None:
    """Authenticate a user by username and password.

    Args:
        db (list[dict]): The database of users (will eventually use an actual db).
        username (str): The username to authenticate.
        password (str): The plaintext password to verify.

    Returns:
        UserInDB | None: The authenticated user if credentials are valid, otherwise None.
    """
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=30),
) -> str:
    """Create a new JWT access token.

    Args:
        data (dict): The claims to include in the token payload.
        expires_delta (timedelta, optional): The token expiration time. Defaults to 30 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def set_access_token_cookie(response: JSONResponse, token: str) -> None:
    """Attach an access token to the response as a secure HTTP-only cookie.

    Args:
        response (JSONResponse): The HTTP response to modify.
        token (str): The JWT token to set in the cookie.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


async def get_current_user(request: Request) -> UserInDB:
    """Retrieve the currently authenticated user from the request cookies.

    Decodes the JWT token stored in the `access_token` cookie and fetches the corresponding user from the database.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        UserInDB: The authenticated user.

    Raises:
        HTTPException: If no token is provided, the token is invalid/expired, or the user does not exist.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str | None = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        token_data = TokenData(user_id=UUID(sub))
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token expired") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err

    user = get_user_by_id(fake_users_db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
