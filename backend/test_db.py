import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine
from app.models.user import User, UserCreate
from sqlmodel import select, Session
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_database_connection():
    print("Testing database connection...")
    try:
        # Try to create tables
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(bind=engine)
        print("Tables created successfully")
        
        # Try to create a user
        with get_session() as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            if existing_user:
                print("Deleting existing test user...")
                session.delete(existing_user)
                session.commit()
            
            # Hash the password
            hashed_password = pwd_context.hash("password123")
            
            # Create new user with hashed password
            user = User(
                email="test@example.com",
                name="Test User",
                hashed_password=hashed_password
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            print(f"User created successfully with ID: {user.id}")
            print(f"User email: {user.email}")
            print(f"User name: {user.name}")
            print(f"Can verify password: {user.verify_password('password123')}")
            
    except Exception as e:
        print(f"Database test error: {e}")
        import traceback
        traceback.print_exc()

def test_database_connection_fixed():
    print("Testing database connection (fixed)...")
    try:
        # Try to create tables
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(bind=engine)
        print("Tables created successfully")
        
        # Try to create a user using Session directly
        with Session(engine) as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            if existing_user:
                print("Deleting existing test user...")
                session.delete(existing_user)
                session.commit()
            
            # Hash the password
            hashed_password = pwd_context.hash("password123")
            
            # Create new user with hashed password
            user = User(
                email="test@example.com",
                name="Test User",
                hashed_password=hashed_password
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            print(f"User created successfully with ID: {user.id}")
            print(f"User email: {user.email}")
            print(f"User name: {user.name}")
            print(f"Can verify password: {user.verify_password('password123')}")
            
    except Exception as e:
        print(f"Database test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection_fixed()