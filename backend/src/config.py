from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-change-in-production")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    api_v1_prefix: str = "/api/v1"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"


settings = Settings()