from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from jose import JWTError
import traceback


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Global handler for HTTP exceptions.

    Args:
        request: The incoming request
        exc: The HTTP exception that occurred

    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": getattr(exc, 'error_code', None),
            "path": str(request.url),
        }
    )


async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
    """
    Handler for JWT-related errors.

    Args:
        request: The incoming request
        exc: The JWT exception that occurred

    Returns:
        JSONResponse with JWT error details
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid authentication credentials",
            "error_type": "INVALID_JWT",
            "path": str(request.url),
        }
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for validation-related errors.

    Args:
        request: The incoming request
        exc: The validation exception that occurred

    Returns:
        JSONResponse with validation error details
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error in request data",
            "errors": [{"loc": ["body"], "msg": str(exc), "type": "validation_error"}],
            "path": str(request.url),
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global handler for general exceptions.

    Args:
        request: The incoming request
        exc: The general exception that occurred

    Returns:
        JSONResponse with error details
    """
    # Log the error for debugging
    print(f"Unhandled exception in {request.url.path}: {exc}")
    traceback.print_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_type": "INTERNAL_ERROR",
            "path": str(request.url),
        }
    )


def register_error_handlers(app):
    """
    Register all error handlers with the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    # Note: JWTError is caught in the verify_token function directly
    app.add_exception_handler(Exception, general_exception_handler)