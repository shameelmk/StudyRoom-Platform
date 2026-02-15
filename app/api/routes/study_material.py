import os
import uuid
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import LimitOffsetPage
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from app.api.deps import CurrentUser, SessionDep
from app.schemas.study_material import MaterialResponse, StudyMaterialReportCreate, StudyMaterialReportResponse, StudyMaterialReportResponse
from app.models import room as study_room, study_material
from app.core.config import settings

router = APIRouter(tags=["Study Materials"])


@router.post("/{room_id}/materials", summary="Upload study material")
async def upload_study_material(current_user: CurrentUser, session: SessionDep, room_id: uuid.UUID, file: UploadFile = File(...)) -> MaterialResponse:
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

    file_size = 0

    try:
        with open(file_path, "wb") as buffer:
            # Checking the file size while reading it in chunks to avoid loading large files into memory
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)

                if file_size > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="File size exceeds 10MB limit"
                    )
                buffer.write(chunk)

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
    except Exception:
        # Cleanup on failure
        if os.path.exists(file_path):
            os.remove(file_path)
        session.rollback()
        raise


@router.get("/{room_id}/materials", summary="List study materials", response_model=LimitOffsetPage[MaterialResponse])
async def list_study_materials(current_user: CurrentUser, session: SessionDep, room_id: uuid.UUID) -> LimitOffsetPage[MaterialResponse]:
    """List all study materials for a specific study room."""

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

    query = (
        session.query(study_material.StudyMaterial)
        .options(joinedload(study_material.StudyMaterial.uploader))
        .filter(study_material.StudyMaterial.room_id == room_id)
        .order_by(study_material.StudyMaterial.created_at.desc())
    )
    return paginate(session, query)

# TODO - Optional Add endpoints for downloading and deleting materials (only by uploader or room owner)


@router.post("/materials/{material_id}/reports", summary="Report a study material", response_model=StudyMaterialReportResponse, status_code=status.HTTP_201_CREATED)
async def report_study_material(current_user: CurrentUser, session: SessionDep, report: StudyMaterialReportCreate, material_id: uuid.UUID) -> StudyMaterialReportResponse:
    """Report a study material, Only members of the study room can report materials in a room."""

    material = session.query(study_material.StudyMaterial).filter(
        study_material.StudyMaterial.id == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study material not found")

    is_member = session.query(
        exists().where(
            study_room.StudyRoomMember.study_room_id == material.room_id,
            study_room.StudyRoomMember.user_id == current_user.id
        )
    ).scalar()
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You must be a member of the study room to report materials")

    report = study_material.StudyMaterialReport(
        material_id=material_id,
        reported_by=current_user.id,
        comment=report.comment
    )
    session.add(report)
    session.commit()
    return report


@router.get("/materials/{material_id}/reports", summary="List reports for a study material", response_model=LimitOffsetPage[StudyMaterialReportResponse])
async def list_material_reports(current_user: CurrentUser, session: SessionDep, material_id: uuid.UUID) -> LimitOffsetPage[StudyMaterialReportResponse]:
    """List all reports for a specific study material, Only room owners can view reports for materials in their rooms."""

    material = session.query(study_material.StudyMaterial).filter(
        study_material.StudyMaterial.id == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study material not found")

    is_room_owner = session.query(
        exists().where(
            study_room.StudyRoom.id == material.room_id,
            study_room.StudyRoom.created_by == current_user.id
        )
    ).scalar()
    if not is_room_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only room owners can view reports for materials in their rooms")

    query = (
        session.query(study_material.StudyMaterialReport)
        .options(joinedload(study_material.StudyMaterialReport.reporter))
        .filter(study_material.StudyMaterialReport.material_id == material_id)
        .order_by(study_material.StudyMaterialReport.created_at.desc())
    )
    return paginate(session, query)
