from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from app.schemas import user as user_schemas


class MaterialResponse(BaseModel):
    id: UUID
    room_id: UUID
    file_name: str
    file_url: str
    created_at: datetime
    uploader: user_schemas.UserOut

    model_config = ConfigDict(from_attributes=True)


class MaterialOut(BaseModel):
    id: UUID
    file_name: str
    uploader: user_schemas.UserOut

    model_config = ConfigDict(from_attributes=True)


class StudyMaterialReportResponse(BaseModel):
    id: UUID
    material: MaterialOut
    reporter: user_schemas.UserOut
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudyMaterialReportCreate(BaseModel):
    comment: str
