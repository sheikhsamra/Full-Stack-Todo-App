from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlmodel import Session, select
from datetime import timedelta
from typing import Dict, Any
from ...database import get_session
from ...models.user import User, UserCreate, UserRead, UserLogin, pwd_context
from ...core.security import create_access_token, decode_token_user_id
from ...core.config import settings

router = APIRouter()

@router.post("/auth/register", response_model=UserRead)
def register_user(user_data: UserCreate, db_session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    try:
        # Check if user already exists
        existing_user = db_session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = pwd_context.hash(user_data.password)

        # Create new user with hashed password
        user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_session)):
    """
    Login user and return access token.
    """
    # Find user by email
    user = db_session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.get("/auth/users/me", response_model=UserRead)
def get_current_user(
    token: str = Depends(HTTPBearer()),
    db_session: Session = Depends(get_session)
):
    """
    Get current authenticated user.
    """
    try:
        # Decode the token to get user ID
        user_id = decode_token_user_id(token.credentials)
        
        # Fetch user from database
        user = db_session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Get current user error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )