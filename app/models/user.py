from sqlalchemy import Column, String, Boolean, DateTime
from app.models.db import Base
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_subscribed = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_token_expires = Column(DateTime, nullable=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_subscribed: bool

    class Config:
        orm_mode = True 