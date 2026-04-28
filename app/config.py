from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from typing import List

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_URL: str = "redis://localhost:6379/0"
    POSTGRES_PASSWORD: str = "1234"
    # Comma-separated in .env, e.g.: ALLOWED_ORIGINS=http://localhost:3000,https://myapp.com
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_scheme(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

settings = Settings()