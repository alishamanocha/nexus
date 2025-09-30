"""Data models for users."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Represents a user in the system."""

    id: UUID
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    """Represents a user stored in the database, including password hash."""

    hashed_password: str


class UserCreate(BaseModel):
    """Represents the data required to create a new user."""

    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    password: str
