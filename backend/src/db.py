from sqlmodel import create_engine, Session
from .config import settings
from .models.user import User  # Import all models here to register them


# Create the database engine
engine = create_engine(settings.database_url, echo=settings.debug)


def get_session():
    """
    Generator function to get a database session.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create database tables based on the defined models.
    This should be called on application startup.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)