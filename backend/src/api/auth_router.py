from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from datetime import timedelta
from typing import Dict, Any
from ..services.user_service import UserService
from ..models.user import UserCreate, UserRead
from ..db import get_session
from ..utils.jwt_utils import create_access_token, create_user_token_payload
from ..config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
user_service = UserService()


@router.post("/signup", response_model=UserRead)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    """
    Register a new user with email and password.

    Args:
        user_create: User creation data containing email and password
        session: Database session dependency

    Returns:
        UserRead: Created user data (without password)

    Raises:
        HTTPException: If user with email already exists
    """
    try:
        # Create the user using the user service
        db_user = user_service.create_user(session=session, user_create=user_create)

        # Return user data (without password)
        return UserRead(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions from the service
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user registration"
        )


@router.post("/login")
def login_user(email: str, password: str, session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    Authenticate user with email and password and return JWT token.

    Args:
        email: User's email address
        password: User's password
        session: Database session dependency

    Returns:
        Dict: Contains access token and token type

    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate the user using the user service
    user = user_service.authenticate_user(session=session, email=email, password=password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a payload for the token
    token_payload = create_user_token_payload(user.id, user.email)

    # Create access token with a 30-minute expiration
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data=token_payload, expires_delta=access_token_expires
    )

    # Return the token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/logout")
def logout_user():
    """
    Logout user (currently a placeholder, as JWT tokens are stateless).

    In a real implementation, this might add the token to a blacklist.
    """
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: Dict[str, Any] = Depends(user_service.get_current_user)) -> UserRead:
    """
    Get current user's information based on the JWT token.

    Args:
        current_user: User information extracted from the JWT token

    Returns:
        UserRead: Current user's information
    """
    # This endpoint would typically fetch the full user record from the database
    # using the user_id from the token, but we'll return the information from the token for now
    return UserRead(
        id=current_user["user_id"],
        email=current_user["email"],
        is_active=True,
        created_at=None,  # Would come from DB in a real implementation
        updated_at=None   # Would come from DB in a real implementation
    )