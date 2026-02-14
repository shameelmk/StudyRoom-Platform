"""This file is used to import all the models in the app/models directory 
for alembic to recognize them when generating migrations."""

from .user import User

__all__ = ["User"]
