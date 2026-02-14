from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.api.deps import get_db
from app import models
from app.schemas.token import Token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["auth"])


@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    """Simple login endpoint that returns a JWT access token.

    Accepts JSON body with `email` and `password` fields.
    """
    user = db.query(models.User).filter(
        models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password")

    verified, new_hash = verify_password(
        form_data.password, user.hashed_password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password")

    if new_hash:
        user.hashed_password = new_hash
        db.add(user)
        db.commit()

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires)

    return {"access_token": access_token}
