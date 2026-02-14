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
