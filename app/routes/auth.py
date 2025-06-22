from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserRead
from app.models.db import SessionLocal
from passlib.context import CryptContext
from app.core.jwt_utils import create_access_token
from app.core.email_utils import send_verification_email
import uuid, random, string, secrets
from datetime import datetime, timedelta
from pydantic import EmailStr, BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(data.password)
    code = ''.join(random.choices(string.digits, k=6))
    new_user = User(id=str(uuid.uuid4()), email=data.email, hashed_password=hashed_password, verification_code=code)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_verification_email(new_user.email, "Verify your email", f"Your code: {code}")
    return new_user

@router.post("/verify-email")
async def verify_email(email: str, code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    user.is_verified = True
    user.verification_code = None
    db.commit()
    subscribers = db.query(User).filter(User.is_subscribed == True, User.is_verified == True).all()
    for sub in subscribers:
        await send_verification_email(sub.email, "New User Verified", f"User {user.email} has just verified their email.")
    return {"msg": "Email verified and notification sent to subscribers"}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = secrets.token_urlsafe(32)
    user.reset_password_token = token
    user.reset_password_token_expires = datetime.utcnow() + timedelta(minutes=15)
    db.commit()

    await send_verification_email(
        user.email,
        "Password Reset Request",
        f"Use this token to reset your password: {token}"
    )
    return {"msg": "Password reset email sent"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_password_token == request.token).first()

    if not user or user.reset_password_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.hashed_password = pwd_context.hash(request.password)
    user.reset_password_token = None
    user.reset_password_token_expires = None
    db.commit()
    
    return {"msg": "Password has been reset successfully"}

@router.post("/login")
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token({"sub": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 