from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Generator
from ..database import get_session
from ..core.security import decode_token_user_id

security = HTTPBearer()


def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract and return the JWT token from the Authorization header
    """
    return credentials.credentials


def get_current_user_id(token: str = Depends(get_current_user_token)) -> int:
    """
    Get the current user ID from the JWT token
    """
    try:
        user_id = decode_token_user_id(token)
        return user_id
    except HTTPException:
        raise


def verify_user_owns_resource(current_user_id: int, requested_user_id: int):
    """
    Verify that the current user ID matches the requested user ID
    """
    if current_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )


def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session dependency
    """
    yield from get_session()