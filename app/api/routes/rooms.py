from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import func
from app.api.deps import CurrentUser, SessionDep
from app.schemas import room as room_schemas
from app.models import room as room_models

router = APIRouter(tags=["study_rooms"])


@router.post("/", summary="Create a new study room", status_code=status.HTTP_201_CREATED)
async def create_study_room(room_data: room_schemas.StudyRoomCreate, current_user: CurrentUser, session: SessionDep) -> room_schemas.StudyRoomBase:
    """Create a new study room with the given details. The current user will be set as the owner of the room."""
    room = room_models.StudyRoom(
        name=room_data.name,
        description=room_data.description,
        max_members=room_data.max_members,
        created_by=current_user.id,
    )
    # append a StudyRoomMember so the owner is part of the members list
    room.members.append(room_models.StudyRoomMember(user_id=current_user.id))

    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@router.get("/{room_id}", summary="Get details of a study room")
async def get_study_room(room_id: str, session: SessionDep) -> room_schemas.StudyRoomBase:
    """Retrieve details of a study room by its ID."""
    room = session.query(room_models.StudyRoom).filter(
        room_models.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")
    return room


@router.get("/", summary="List all study rooms")
async def list_study_rooms(session: SessionDep) -> list[room_schemas.StudyRoomBase]:
    """List all available study rooms."""
    # TODO: Add pagination and search functionality.
    rooms = session.query(room_models.StudyRoom).all()
    return rooms


@router.delete("/{room_id}", summary="Delete a study room")
async def delete_study_room(room_id: str, current_user: CurrentUser, session: SessionDep):
    """Delete a study room by its ID. Only the owner of the room can delete it."""
    room = session.query(room_models.StudyRoom).filter(
        room_models.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")
    if room.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only the owner can delete this study room")
    session.delete(room)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{room_id}/join", summary="Join a study room")
async def join_study_room(room_id: str, current_user: CurrentUser, session: SessionDep):
    """Join a study room by its ID. The user will be added to the members list of the room."""
    room = session.query(room_models.StudyRoom).filter(
        room_models.StudyRoom.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")

    member_count = (
        session.query(func.count(room_models.StudyRoomMember.id))
        .filter(room_models.StudyRoomMember.study_room_id == room_id)
        .scalar()
    )

    if member_count >= room.max_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Study room is full")

    existing_member = (
        session.query(room_models.StudyRoomMember)
        .filter_by(study_room_id=room_id, user_id=current_user.id)
        .first()
    )
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are already a member of this study room")

    new_member = room_models.StudyRoomMember(user_id=current_user.id)
    
    room.members.append(new_member)
    session.add(new_member)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{room_id}/leave", summary="Leave a study room")
async def leave_study_room(room_id: str, current_user: CurrentUser, session: SessionDep):
    """Leave a study room by its ID. The user will be removed from the members list of the room."""
    room = session.query(room_models.StudyRoom).filter(
        room_models.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")
    member = (
        session.query(room_models.StudyRoomMember)
        .filter_by(study_room_id=room_id, user_id=current_user.id)
        .first()
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of this study room")
    if room.created_by == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Owner cannot leave their own study room. Consider deleting the room instead.")
    session.delete(member)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
