"""
Tests for authentication validation and token management
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from jose import jwt
from ..src.config import settings
from ..src.main import app


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client


def test_expired_jwt_rejection(client: TestClient):
    """
    Test that expired JWT tokens are rejected with 401 status
    """
    # Create an expired token
    expired_date = datetime.utcnow() - timedelta(hours=1)  # 1 hour ago
    token_data = {
        "sub": "test_user_id",
        "email": "test@example.com",
        "exp": expired_date,
        "user_id": "test_user_id"
    }

    expired_token = jwt.encode(token_data, settings.better_auth_secret, algorithm="HS256")

    # Try to access a protected endpoint with expired token
    response = client.get(
        "/api/test_user_id/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 for expired token
    assert response.status_code == 401

    # Check that the response contains appropriate error message
    response_data = response.json()
    assert "detail" in response_data
    assert "expired" in response_data["detail"].lower()


def test_invalid_signature_jwt_rejection(client: TestClient):
    """
    Test that JWT tokens with invalid signatures are rejected with 401 status
    """
    # Create a token with a different secret (to simulate invalid signature)
    token_data = {
        "sub": "test_user_id",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    # Use a different secret to encode the token
    wrong_secret_token = jwt.encode(token_data, "wrong_secret", algorithm="HS256")

    # Try to access a protected endpoint with invalid signature token
    response = client.get(
        "/api/test_user_id/tasks",
        headers={"Authorization": f"Bearer {wrong_secret_token}"}
    )

    # Should return 401 for invalid signature
    assert response.status_code == 401

    # Check that the response contains appropriate error message
    response_data = response.json()
    assert "detail" in response_data
    assert "credentials" in response_data["detail"].lower()


def test_missing_authorization_header(client: TestClient):
    """
    Test that requests without Authorization header are rejected with 401 status
    """
    # Try to access a protected endpoint without Authorization header
    response = client.get("/api/test_user_id/tasks")

    # Should return 401 for missing authorization
    assert response.status_code == 401


def test_malformed_authorization_header(client: TestClient):
    """
    Test that requests with malformed Authorization headers are rejected
    """
    # Try to access a protected endpoint with malformed Authorization header
    response = client.get(
        "/api/test_user_id/tasks",
        headers={"Authorization": "InvalidFormatToken"}
    )

    # Should return 401 for malformed authorization
    assert response.status_code == 401