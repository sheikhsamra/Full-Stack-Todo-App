from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from jose import jwt
from ..utils.jwt_utils import verify_token, verify_user_access
from ..config import settings


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get the current user from the JWT token in the Authorization header.

    This function will:
    1. Extract the JWT token from the Authorization header
    2. Verify the token using the shared secret
    3. Return the user information if the token is valid

    Raises:
        HTTPException: If the token is invalid, expired, or missing required claims
    """
    try:
        # Decode and verify the token
        payload = verify_token(credentials.credentials)

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        # Return the user information extracted from the token
        return {
            "user_id": user_id,
            "email": payload.get("email"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Optional dependency to get the current user. Doesn't raise an exception if no token is provided.

    Returns:
        Dict: User information if token is valid, None otherwise
    """
    try:
        # Decode and verify the token
        payload = verify_token(credentials.credentials)

        user_id = payload.get("user_id")
        if user_id is None:
            return None

        # Return the user information extracted from the token
        return {
            "user_id": user_id,
            "email": payload.get("email"),
        }
    except:
        return None


def verify_user_access_dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Dependency to ensure that the current user has access to the requested resource.
    This is a simplified version that just ensures the user is authenticated.
    More specific authorization logic can be added as needed.
    """
    return current_user