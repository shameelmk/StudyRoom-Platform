from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.api.deps import SessionDep
from app import models, schemas
from app.schemas.token import Token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError


router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.user.UserCreate, session: SessionDep) -> schemas.user.UserBase:
    new_user = models.User(
        hashed_password=get_password_hash(user_in.password),
        **user_in.dict(exclude={"password"}),
    )
    session.add(new_user)

    try:
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")


@router.post("/login", response_model=Token)
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Simple login endpoint that returns a JWT access token.

    - **email**: User's email address (used as username)
    - **password**: User's password"""
    user = session.query(models.User).filter(
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

    user.last_login = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
