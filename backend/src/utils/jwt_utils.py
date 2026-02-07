from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from jose import JWTError, jwt
from fastapi import HTTPException, status
from ..config import settings


def validate_jwt_signature(token: str, secret_key: str = None) -> bool:
    """
    Validate the signature of a JWT token using the provided secret key.

    Args:
        token: The JWT token to validate
        secret_key: The secret key to use for validation (uses default if not provided)

    Returns:
        True if the signature is valid, False otherwise
    """
    if secret_key is None:
        secret_key = settings.better_auth_secret

    try:
        # This will raise an exception if the signature is invalid
        jwt.decode(token, secret_key, algorithms=["HS256"])
        return True
    except JWTError:
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with the provided data.

    Args:
        data: Dictionary containing the claims to be included in the token
        expires_delta: Optional timedelta for token expiration (defaults to 30 minutes)

    Returns:
        Encoded JWT token as a string
    """
    to_encode = data.copy()

    # Set default expiration if not provided (30 minutes)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    # Add expiration time to the token
    to_encode.update({"exp": expire})

    # Encode the token with the secret and HS256 algorithm
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return the decoded claims if valid.

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token claims if valid, None otherwise
    """
    try:
        # Decode the token with the secret
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])

        # Extract user_id from the token (using 'sub' claim as user_id by convention)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract other useful claims
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        iat: int = payload.get("iat")
        iss: str = payload.get("iss")
        aud: str = payload.get("aud")

        # Validate required claims
        if not all([exp]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing required claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token is expired
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token is not yet valid (in the future)
        if iat and datetime.fromtimestamp(iat) > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not yet valid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user_id,
            "email": email,
            "exp": exp,
            "iat": iat,
            "iss": iss,
            "aud": aud
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired without fully validating it.

    Args:
        token: The JWT token to check

    Returns:
        True if the token is expired, False otherwise
    """
    try:
        # Decode the token without verification to check expiration
        unverified_payload = jwt.get_unverified_claims(token)
        exp = unverified_payload.get("exp")

        if exp:
            return datetime.fromtimestamp(exp) < datetime.utcnow()
        return True  # Consider tokens without expiration as expired

    except JWTError:
        return True  # If we can't decode, consider it expired


def get_token_expiry_time(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a JWT token.

    Args:
        token: The JWT token to check

    Returns:
        Expiration datetime if available, None otherwise
    """
    try:
        # Decode the token without verification to get claims
        unverified_payload = jwt.get_unverified_claims(token)
        exp = unverified_payload.get("exp")

        if exp:
            return datetime.fromtimestamp(exp)
        return None

    except JWTError:
        return None


def verify_user_access(token_user_id: str, url_user_id: str) -> bool:
    """
    Verify that the user in the JWT matches the user_id in the URL.

    Args:
        token_user_id: User ID from the JWT token
        url_user_id: User ID from the URL path parameter

    Returns:
        True if the IDs match, raises HTTPException if they don't
    """
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions"
        )
    return True


def create_user_token_payload(user_id: str, email: str) -> Dict[str, Any]:
    """
    Create a standard payload for user JWT tokens.

    Args:
        user_id: The user's unique identifier
        email: The user's email address

    Returns:
        Dictionary containing the standard claims for a user token
    """
    return {
        "sub": user_id,  # Standard claim for subject (user ID)
        "user_id": user_id,  # Custom claim for user ID
        "email": email,  # User's email
        "iat": datetime.utcnow(),  # Issued at time
        "iss": "todo-app-auth",  # Issuer
        "aud": "todo-app-users"  # Audience
    }