from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import Dict, Any
from ...database import get_session
from ...models.user import User, UserCreate, UserRead, UserLogin
from ...core.security import create_access_token
from ...core.config import settings

router = APIRouter()

@router.post("/auth/register", response_model=UserRead)
def register_user(user_data: UserCreate, db_session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = db_session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = User.model_validate(user_data, update={"hashed_password": user_data.password})
    user.hashed_password = user.get_hashed_password(user_data.password)
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


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