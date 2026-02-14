from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.core.base import Base


# Synchronous engine + sessionmaker
engine = create_engine(settings.SYNC_DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def init_db(session: Session) -> None:
    # Local import to avoid circular import at module import time
    from app.models.user import User

    result = session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    )
    user = result.scalars().first()
    if not user:
        user_in = UserCreate(
            name="Admin",
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_superuser=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
