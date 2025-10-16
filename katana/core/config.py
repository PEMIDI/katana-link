from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="Katana Link")
    VERSION: str = Field(default="0.1.0")
    ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    ENABLE_DOCS: bool = Field(default=True)

    LOG_LEVEL: str = Field(default="INFO")

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./app.db")
    SQL_ECHO: bool = Field(default=False)
    SQL_POOL_SIZE: int = Field(default=5)
    SQL_MAX_OVERFLOW: int = Field(default=10)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
