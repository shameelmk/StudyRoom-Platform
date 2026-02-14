from fastapi import FastAPI
from app.core.config import settings
from app.api.main import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    api_version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(
    prefix=settings.API_V1_STR,
    router=api_router
)
