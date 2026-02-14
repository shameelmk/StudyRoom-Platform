from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """Shared fields for user schemas."""

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Data required to create a new user via the API or initial setup."""
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Data for updating the current user's profile."""
    name: str | None = None


class UserOut(UserBase):
    """Public user fields returned in responses."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
