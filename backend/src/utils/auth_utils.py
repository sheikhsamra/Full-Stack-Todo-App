from fastapi import HTTPException, status
from typing import Dict, Any


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
            detail="Access denied: Insufficient permissions to access this resource"
        )
    return True


def verify_admin_access(user: Dict[str, Any]) -> bool:
    """
    Verify if the current user has admin privileges.

    Args:
        user: Current user information from the token

    Returns:
        True if the user has admin privileges, raises HTTPException if not
    """
    # In this basic implementation, we'll check for a role in the user claims
    user_roles = user.get("roles", [])
    if "admin" not in user_roles and "superuser" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return True


def verify_resource_ownership(resource_owner_id: str, current_user_id: str) -> bool:
    """
    Verify that the current user is the owner of a specific resource.

    Args:
        resource_owner_id: ID of the resource owner
        current_user_id: ID of the currently authenticated user

    Returns:
        True if the user owns the resource, raises HTTPException if not
    """
    if resource_owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not own this resource"
        )
    return True


def validate_scopes(required_scopes: list, user_scopes: list) -> bool:
    """
    Validate that the user has the required scopes/permissions.

    Args:
        required_scopes: List of required scopes for the action
        user_scopes: List of scopes that the user possesses

    Returns:
        True if user has all required scopes, raises HTTPException if not
    """
    for scope in required_scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required scope: {scope}"
            )
    return True