from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.core.base import Base


engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_db(session: AsyncSession) -> None:
    # Local import to avoid circular import at module import time
    from app.models.user import User

    result = await session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    )
    user = result.scalars().first()
    if not user:
        user_in = UserCreate(
            name="Admin",
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
