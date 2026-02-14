from fastapi import APIRouter, Depends, status
from app import schemas, models
from app.api.deps import get_db, CurrentUser
from fastapi import HTTPException, status

router = APIRouter(tags=["users"])



@router.get("/me")
def get_current_user(current_user: CurrentUser) -> schemas.user.UserBase:
    return current_user


@router.put("/me")
def update_current_user(user_in: schemas.user.UserUpdate, current_user: CurrentUser, db=Depends(get_db)) -> schemas.user.UserBase:
    if user_in.name is not None:
        current_user.name = user_in.name

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=schemas.user.UserBase)
def get_user(user_id: str, db=Depends(get_db)) -> schemas.user.UserBase:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
