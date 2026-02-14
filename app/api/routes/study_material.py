import os
import shutil
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from sqlalchemy import exists
from app.api.deps import CurrentUser, SessionDep
from app.schemas.study_material import MaterialResponse
from app.models import room as study_room, study_material
from app.core.config import settings

router = APIRouter(tags=["Study Materials"])


@router.post("/{room_id}/materials", summary="Upload study material")
async def upload_study_material(current_user: CurrentUser, session: SessionDep, room_id: str, file: UploadFile = File(...)) -> MaterialResponse:
    """Upload a new study material to a specific study room."""

    room = session.query(study_room.StudyRoom).filter(
        study_room.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")

    is_member = session.query(
        exists().where(
            study_room.StudyRoomMember.study_room_id == room_id,
            study_room.StudyRoomMember.user_id == current_user.id
        )
    ).scalar()
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You must be a member of the study room to upload materials")

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")

    room_dir = os.path.join(settings.MATERIAL_UPLOAD_DIR, room_id)
    os.makedirs(room_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_path = os.path.join(room_dir, f"{file_id}.pdf")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    material = study_material.StudyMaterial(
        room_id=room_id,
        uploaded_by=current_user.id,
        file_name=file.filename,
        file_url=file_path
    )
    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.get("/{room_id}/materials", summary="List study materials")
async def list_study_materials(current_user: CurrentUser, session: SessionDep, room_id: str) -> list[MaterialResponse]:
    """List all study materials for a specific study room."""
    # TODO: Add pagination.
    room = session.query(study_room.StudyRoom).filter(
        study_room.StudyRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study room not found")

    is_member = session.query(
        exists().where(
            study_room.StudyRoomMember.study_room_id == room_id,
            study_room.StudyRoomMember.user_id == current_user.id
        )
    ).scalar()
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You must be a member of the study room to view materials")

    materials = session.query(study_material.StudyMaterial).filter(
        study_material.StudyMaterial.room_id == room_id).all()
    return materials

#TODO - Optional Add endpoints for downloading and deleting materials (only by uploader or room owner)