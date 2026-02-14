from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Shared fields for user schemas."""

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Data required to create a new user via the API or initial setup."""
    password: str = Field(min_length=8, max_length=128)
