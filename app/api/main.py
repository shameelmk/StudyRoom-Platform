from fastapi import APIRouter

from app.api.routes import auth, users, rooms, study_material

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(rooms.router, prefix="/rooms")
api_router.include_router(study_material.router, prefix="/rooms")