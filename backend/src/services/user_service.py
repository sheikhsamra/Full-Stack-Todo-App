from sqlmodel import Session, select
from typing import Optional
from passlib.context import CryptContext
from ..models.user import User, UserCreate, UserUpdate
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from ..config import settings
from ..utils.jwt_utils import verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Service class for handling user-related operations.
    """

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for the given password.
        """
        return pwd_context.hash(password)

    def create_user(self, *, session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        # Check if user with this email already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password
        password_hash = self.get_password_hash(user_create.password)

        # Create the user instance
        db_user = User(
            name=user_create.name,
            email=user_create.email,
            hashed_password=password_hash,
            is_active=True # Default to active for new users
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    def get_user_by_email(self, *, session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    def get_user_by_id(self, *, session: Session, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID.
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    def authenticate_user(self, *, session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        user = self.get_user_by_email(session=session, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

    def update_user(self, *, session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information.
        """
        db_user = self.get_user_by_id(session=session, user_id=user_id)
        if not db_user:
            return None

        # Update fields if provided
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = self.get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def delete_user(self, *, session: Session, user_id: str) -> bool:
        """
        Delete a user by ID.
        """
        db_user = self.get_user_by_id(session=session, user_id=user_id)
        if not db_user:
            return False

        session.delete(db_user)
        session.commit()
        return True

    def get_current_user(self, token: str, session: Session) -> User:
        """
        Get current user from JWT token.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = verify_token(token)
            user_id: str = payload.get("sub")  # Token uses "sub" field for user ID
            if user_id is None:
                raise credentials_exception
        except HTTPException:
            raise credentials_exception
        
        user = self.get_user_by_id(session=session, user_id=int(user_id))
        if user is None:
            raise credentials_exception
        
        return user