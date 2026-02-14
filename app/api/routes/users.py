from fastapi import APIRouter, Depends, status
from app.schemas import user as user_schema
from app.models import user as user_model
from app.api.deps import SessionDep, CurrentUser
from fastapi import HTTPException, status

router = APIRouter(tags=["users"])


@router.get("/me")
def get_current_user(current_user: CurrentUser) -> user_schema.UserBase:
    return current_user


@router.put("/me")
def update_current_user(user_in: user_schema.UserUpdate, current_user: CurrentUser, session: SessionDep) -> user_schema.UserBase:
    if user_in.name is not None:
        current_user.name = user_in.name

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=user_schema.UserOut)
def get_user(user_id: str, session: SessionDep) -> user_schema.UserOut:
    user_obj = session.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_obj
