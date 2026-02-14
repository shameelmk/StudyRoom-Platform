import uuid
from app.core.base import Base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship


class StudyRoom(Base):
    __tablename__ = "study_rooms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    max_members = Column(Integer, nullable=False, default=10)
    created_by = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    creator = relationship("User", back_populates="created_study_rooms")
    members = relationship("StudyRoomMember", back_populates="study_room", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<StudyRoom id={self.id} name={self.name}>"


class StudyRoomMember(Base):
    __tablename__ = "study_room_members"
    __table_args__ = (
        UniqueConstraint("study_room_id", "user_id",
                         name="uix_study_room_user"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    study_room_id = Column(String, ForeignKey(
        "study_rooms.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    study_room = relationship("StudyRoom", back_populates="members")
    user = relationship("User", back_populates="study_rooms_memberships")

    def __repr__(self):
        return f"<StudyRoomMember id={self.id} study_room_id={self.study_room_id} user_id={self.user_id}>"
