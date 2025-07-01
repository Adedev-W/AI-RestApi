from sqlalchemy import Column, String, Boolean, DateTime
from app.models.db import Base
from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_token_expires = Column(DateTime, nullable=True)
    role = Column(String, default="user")  # 'user' or 'admin'
    api_key = Column(String, unique=True, index=True, nullable=False)
    api_key_expires = Column(DateTime, nullable=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    role: str
    api_key: str
    api_key_expires: datetime | None = None

    class Config:
        from_attributes = True