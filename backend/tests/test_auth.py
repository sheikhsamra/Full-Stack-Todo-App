"""
Tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from ..src.main import app  # Adjust the import based on your actual structure
from ..src.models.user import User
from ..src.services.user_service import UserService
from ..src.db import create_db_and_tables


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client


def test_user_registration(client: TestClient, session: Session):
    """
    Test user registration flow and JWT issuance
    """
    # Register a new user
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "is_active": True
        }
    )

    assert response.status_code == 200

    # Verify that the response contains user data
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"


def test_user_login(client: TestClient, session: Session):
    """
    Test user login flow and JWT issuance
    """
    # First register a user
    register_response = client.post(
        "/auth/signup",
        json={
            "email": "login_test@example.com",
            "password": "password123",
            "is_active": True
        }
    )

    assert register_response.status_code == 200

    # Then try to login
    login_response = client.post(
        "/auth/login",
        data={
            "email": "login_test@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    # Verify that the response contains access token
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0  # Token should not be empty