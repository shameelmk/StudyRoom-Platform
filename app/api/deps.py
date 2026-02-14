from core.db import AsyncSessionLocal


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
