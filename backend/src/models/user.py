from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None