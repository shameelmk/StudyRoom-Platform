from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from app.schemas import user as user_schemas


class StudyRoomCreate(BaseModel):
    name: str = Field(..., example="Math Study Group")
    description: str = Field(
        None, example="A group for studying math together.")
    max_members: int = Field(10, example=10)


class StudyRoomUpdate(BaseModel):
    name: str = Field(None, example="Math Study Group")
    description: str = Field(
        None, example="A group for studying math together.")
    max_members: int = Field(None, example=10)


class StudyRoomBase(BaseModel):
    id: UUID
    name: str
    description: str = None
    max_members: int
    created_at: datetime
    updated_at: datetime
    creator: user_schemas.UserOut


    model_config = ConfigDict(from_attributes=True)
