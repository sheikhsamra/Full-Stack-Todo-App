from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using environment variable for Neon PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure your .env file.")

# Ensure we're using psycopg3 driver
if DATABASE_URL.startswith("postgresql://"):
    # Convert to psycopg3 format if needed
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Ensure SSL mode is properly configured for Neon
if "sslmode=" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Create the engine with connection pooling settings
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session
    """
    with Session(engine) as session:
        yield session