from fastapi import APIRouter, Depends, status
from app import schemas, models
from app.api.deps import get_db, get_current_user
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

router = APIRouter(tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.user.UserCreate, db=Depends(get_db)) -> schemas.user.UserBase:
    new_user = models.User(
        hashed_password=get_password_hash(user_in.password),
        **user_in.dict(exclude={"password"}),
    )
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")


@router.get("/me")
def get_current_user(current_user: models.User = Depends(get_current_user)) -> schemas.user.UserBase:
    return current_user


@router.get("/{user_id}", response_model=schemas.user.UserBase)
def get_user(user_id: str, db=Depends(get_db)) -> schemas.user.UserBase:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
