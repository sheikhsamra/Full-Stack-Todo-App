from app.models.user import User, UserCreate, pwd_context
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import tempfile
import os

# Create a temporary SQLite database for testing
temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
temp_db.close()

# Create an in-memory database engine for testing
engine = create_engine(f"sqlite:///{temp_db.name}", connect_args={"check_same_thread": False})

# Create tables
SQLModel.metadata.create_all(engine)

def test_user_creation():
    # Create user data
    user_data = UserCreate(name="Test User", email="test@example.com", password="password123")
    
    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create new user with hashed password
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    print("User object created successfully:")
    print(f"  Email: {user.email}")
    print(f"  Name: {user.name}")
    print(f"  Has hashed password: {bool(user.hashed_password)}")
    print(f"  Password verifies: {user.verify_password('password123')}")
    
    # Try to save to database
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        
        print(f"  User saved with ID: {user.id}")
    
    # Clean up
    os.unlink(temp_db.name)

if __name__ == "__main__":
    test_user_creation()
    print("Test completed successfully!")