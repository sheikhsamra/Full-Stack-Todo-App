from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Tasks API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tasks_db")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS settings
    allowed_origins: list = ["*"]  # Should be restricted in production

    class Config:
        env_file = ".env"


settings = Settings()