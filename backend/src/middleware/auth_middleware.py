from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from ..utils.jwt_utils import verify_token


class AuthMiddleware:
    """
    Authentication middleware for FastAPI applications.

    This middleware intercepts incoming requests and verifies JWT tokens
    before allowing them to reach the API endpoints.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)

        # Check if the endpoint requires authentication
        # Skip authentication for public endpoints like login/register
        path = request.url.path
        if path.startswith('/auth/') or path == '/health' or path == '/':
            # Skip authentication for auth endpoints and health checks
            await self.app(scope, receive, send)
            return

        # Get authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header is missing"}
            )
            await response(scope, receive, send)
            return

        # Verify the token format
        try:
            auth_scheme, token = auth_header.split(" ", 1)
            if auth_scheme.lower() != "bearer":
                response = JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization scheme must be Bearer"}
                )
                await response(scope, receive, send)
                return
        except ValueError:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"}
            )
            await response(scope, receive, send)
            return

        # Verify the token
        try:
            payload = verify_token(token)
            # Add user info to request state for later use
            request.state.current_user = payload
        except HTTPException as e:
            await JSONResponse(
                status_code=e.status_code,
                content=e.detail if isinstance(e.detail, dict) else {"detail": e.detail}
            )(scope, receive, send)
            return

        # Continue with the request
        await self.app(scope, receive, send)