from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    DEBUG: bool = True
    APP_NAME: str = "Study Room API"
    APP_DESCRIPTION: str = "Study Room API"
    API_V1_STR: str = "/api/v1"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"


settings = Settings()
