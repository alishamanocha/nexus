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


# Token models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: UUID


# Username/password helpers
def validate_username(username: str) -> bool:
    return all(u["username"] != username for u in fake_users_db)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# User lookup
def get_user_by_username(db: list[dict], username: str) -> UserInDB | None:
    for u in db:
        if u.get("username") == username:
            return UserInDB(**u)
    return None


def get_user_by_id(db: list[dict], user_id: UUID) -> UserInDB | None:
    for u in db:
        if u.get("id") == str(user_id):
            return UserInDB(**u)
    return None


# Auth helpers
def authenticate_user(db: list[dict], username: str, password: str) -> UserInDB | None:
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=30),
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def set_access_token_cookie(response: JSONResponse, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# Dependency to get current user
async def get_current_user(request: Request) -> UserInDB:
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(fake_users_db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
