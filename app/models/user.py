import uuid
from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.core.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now())

    created_study_rooms = relationship(
        "StudyRoom", back_populates="creator")
    study_rooms_memberships = relationship(
        "StudyRoomMember", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
