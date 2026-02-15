import uuid
from app.core.base import Base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    UniqueConstraint,
    func,
    UUID,
)
from sqlalchemy.orm import relationship


class StudyRoom(Base):
    __tablename__ = "study_rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    max_members = Column(Integer, nullable=False, default=10)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    creator = relationship("User", back_populates="created_study_rooms")
    members = relationship(
        "StudyRoomMember", back_populates="study_room", cascade="all, delete-orphan"
    )
    materials = relationship(
        "StudyMaterial", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<StudyRoom id={self.id} name={self.name}>"


class StudyRoomMember(Base):
    __tablename__ = "study_room_members"
    __table_args__ = (
        UniqueConstraint("study_room_id", "user_id", name="uix_study_room_user"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    study_room_id = Column(
        UUID(as_uuid=True),
        ForeignKey("study_rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    study_room = relationship("StudyRoom", back_populates="members")
    user = relationship("User", back_populates="study_rooms_memberships")

    def __repr__(self):
        return f"<StudyRoomMember id={self.id} study_room_id={self.study_room_id} user_id={self.user_id}>"
