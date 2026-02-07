from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using environment variable for Neon PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tasks_db")

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