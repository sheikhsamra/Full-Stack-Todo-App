from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, UTC
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_hashed_password(self, plain_password: str) -> str:
        # Truncate password to 72 bytes if needed due to bcrypt limitations
        truncated_password = plain_password[:72] if len(plain_password.encode('utf-8')) > 72 else plain_password
        return pwd_context.hash(truncated_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)
    name: str = Field(max_length=255)  # Make name required for registration


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime