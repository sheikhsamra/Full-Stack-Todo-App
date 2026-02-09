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
    database_url: str = os.getenv("DATABASE_URL")  # No default - must be set in .env

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS settings
    allowed_origins: list = [
        "http://localhost:3004",  # Your frontend
        "http://localhost:3000",  # Common Next.js default
        "http://localhost:3001",  # Alternative Next.js port
        "http://127.0.0.1:3004",  # Alternative localhost format
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://localhost:8000",  # Self-access for docs
        "http://127.0.0.1:8000",  # Self-access for docs
    ]

    class Config:
        env_file = ".env"


# Validate that database_url is set
if not Settings().database_url:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure your .env file.")

settings = Settings()