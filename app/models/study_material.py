import uuid
from sqlalchemy import Column, DateTime, DateTime, ForeignKey, String, String, func, UUID
from sqlalchemy.orm import relationship
from app.core.base import Base


class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("study_rooms.id",
                     ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("StudyRoom", back_populates="materials")
    uploader = relationship("User", back_populates="uploaded_materials")
    reports = relationship(
        "StudyMaterialReport", back_populates="material", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<StudyMaterial id={self.id} file_name={self.file_name}>"


class StudyMaterialReport(Base):
    __tablename__ = "study_material_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    material_id = Column(UUID(as_uuid=True), ForeignKey("study_materials.id",
                                            ondelete="CASCADE"), nullable=False)
    reported_by = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    material = relationship("StudyMaterial", back_populates="reports")
    reporter = relationship("User", back_populates="reported_materials")

    def __repr__(self):
        return f"<StudyMaterialReport id={self.id} comment={self.comment}>"