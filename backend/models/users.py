from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    password: str
