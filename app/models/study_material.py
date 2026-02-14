import uuid
from sqlalchemy import Column, DateTime, DateTime, ForeignKey, String, String, func
from sqlalchemy.orm import relationship
from app.core.base import Base


class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, ForeignKey("study_rooms.id",
                     ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    room = relationship("StudyRoom", back_populates="materials")
    uploader = relationship("User", back_populates="uploaded_materials")
    def __repr__(self):
        return f"<StudyMaterial id={self.id} file_name={self.file_name}>"