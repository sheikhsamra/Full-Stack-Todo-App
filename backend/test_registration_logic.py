import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine
from app.models.user import User, UserCreate, pwd_context
from sqlmodel import select, Session

def test_registration_logic():
    print("Testing registration logic step by step...")
    
    # Simulate the registration process
    user_data = UserCreate(
        name="Test User",
        email="testlogic@example.com",
        password="password123"
    )
    
    print(f"1. User data created: {user_data.name}, {user_data.email}")
    
    # Check if user already exists
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            print(f"2. User already exists: {existing_user.email}")
            # Delete for test purposes
            session.delete(existing_user)
            session.commit()
            print("   Deleted existing user for test")
        else:
            print("2. No existing user found")
    
    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)
    print(f"3. Password hashed successfully")
    
    # Create new user with hashed password
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    print(f"4. User object created: {user.email}, {user.name}")
    
    # Save to database
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"5. User saved to database with ID: {user.id}")
        
        # Verify the user can be retrieved
        retrieved_user = session.exec(select(User).where(User.email == user_data.email)).first()
        print(f"6. Retrieved user from DB: {retrieved_user.email}, ID: {retrieved_user.id}")
        print(f"   Password verification: {retrieved_user.verify_password('password123')}")
    
    print("\nRegistration logic test completed successfully!")

if __name__ == "__main__":
    test_registration_logic()