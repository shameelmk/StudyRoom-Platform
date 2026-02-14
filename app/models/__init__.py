"""This file is used to import all the models in the app/models directory 
for alembic to recognize them when generating migrations."""

from .user import User
from .room import StudyRoom, StudyRoomMember
from .study_material import StudyMaterial

__all__ = ["User", "StudyRoom", "StudyRoomMember", "StudyMaterial"]
