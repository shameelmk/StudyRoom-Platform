from fastapi import APIRouter, HTTPException, Response, status
from app.api.deps import CurrentUser, SessionDep
from app.schemas import room as room_schemas
from app.models import study_room

router = APIRouter(tags=["study_rooms"])


@router.post("/", summary="Create a new study room", status_code=status.HTTP_201_CREATED)
async def create_study_room(room_data: room_schemas.StudyRoomCreate, current_user: CurrentUser, session: SessionDep) -> room_schemas.StudyRoomBase:
    """Create a new study room with the given details. The current user will be set as the owner of the room."""
    room = study_room.StudyRoom(
        name=room_data.name,
        description=room_data.description,
        max_members=room_data.max_members,
        created_by=current_user.id,
    )
    # append a StudyRoomMember so the owner is part of the members list
    room.members.append(study_room.StudyRoomMember(user_id=current_user.id))

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")
    return room


@router.get("/", summary="List all study rooms")
async def list_study_rooms(session: SessionDep) -> list[room_schemas.StudyRoomBase]:
    """List all available study rooms."""
    # TODO: Add pagination and search functionality.
    rooms = session.query(study_room.StudyRoom).all()
    return rooms


@router.delete("/{room_id}", summary="Delete a study room")
async def delete_study_room(room_id: str, current_user: CurrentUser, session: SessionDep):
    """Delete a study room by its ID. Only the owner of the room can delete it."""
    room = session.query(study_room.StudyRoom).filter(
        study_room.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")
    if room.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only the owner can delete this study room")
    session.delete(room)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
