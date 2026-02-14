from fastapi import APIRouter, HTTPException
from app.api.deps import CurrentUser, SessionDep
from app.schemas import room as room_schemas
from app.models import study_room
from uuid import UUID

router = APIRouter(tags=["study_rooms"])


@router.post("/", summary="Create a new study room")
async def create_study_room(room_data: room_schemas.StudyRoomCreate, current_user: CurrentUser, session: SessionDep) -> room_schemas.StudyRoomBase:
    """Create a new study room with the given details. The current user will be set as the owner of the room."""
    room = study_room.StudyRoom(
        name=room_data.name,
        description=room_data.description,
        max_members=room_data.max_members,
        created_by=current_user.id,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@router.get("/{room_id}", summary="Get details of a study room")
async def get_study_room(room_id: str, session: SessionDep) -> room_schemas.StudyRoomBase:
    """Retrieve details of a study room by its ID."""
    room = session.query(study_room.StudyRoom).filter(
        study_room.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Study room not found")
    return room
