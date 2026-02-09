from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any
from sqlmodel import Session
from pydantic import BaseModel
from datetime import timedelta

from ..models.user import UserRead, UserCreate
from ..services.user_service import UserService
from ..database import get_session
from ..app.core.security import create_access_token
from ..app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> UserRead:
    """
    Dependency to get current user from JWT token.
    """
    user_service = UserService()
    return user_service.get_current_user(token, session)

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserRead)
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    user_service = UserService() # Instantiate UserService without session initially
    db_user = user_service.get_user_by_email(session=session, email=user_create.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = user_service.create_user(session=session, user_create=user_create)
    return new_user

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user_service = UserService() # Instantiate UserService without session initially
    user = user_service.authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    return current_user