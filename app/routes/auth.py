from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserRead
from app.models.db import SessionLocal
from passlib.context import CryptContext
from app.core.jwt_utils import create_access_token, get_current_user, verify_access_token
from app.core.email_utils import send_verification_email, email_verification_template, general_notification_template, password_reset_template, admin_register_template
import uuid, random, string, secrets
from datetime import datetime, timedelta
from pydantic import EmailStr, BaseModel
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user_by_api_key, api_key_header

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

@router.post("/register", response_model=UserRead, include_in_schema=False)
async def register(data: UserCreate, db: Session = Depends(get_db), x_api_key: str = Depends(api_key_header), current_user: User = Depends(get_current_user_by_api_key)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create new users.")
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        subject, body = email_verification_template(user.email, "sdsdhsudhquidg3r3")
        await send_verification_email(user.email, subject, body)
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)
    code = ''.join(random.choices(string.digits, k=6))
    api_key = secrets.token_urlsafe(32)
    api_key_expires = datetime.utcnow() + timedelta(days=30)
    new_user = User(id=str(uuid.uuid4()), email=data.email, hashed_password=hashed_password, verification_code=code, api_key=api_key, api_key_expires=api_key_expires)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    subject, body = admin_register_template(new_user.email, api_key, code)
    await send_verification_email(new_user.email, subject, body)
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
    return {"msg": "Email verified"}

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
        *password_reset_template(user.email, token)
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
def login(
    Authorization: str = Header(...),
    x_api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = Authorization.split(" ", 1)[1]
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email, "role": user.role, "is_active": user.is_active, "is_verified": user.is_verified}

@router.post("/admin-reset-apikey", include_in_schema=False)
def admin_reset_apikey(
    current_user: User = Depends(get_current_user_by_api_key),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can reset API key here")
    # Generate API key baru
    new_key = secrets.token_urlsafe(32)
    current_user.api_key = new_key
    current_user.api_key_expires = datetime.utcnow() + timedelta(days=30)
    db.commit()
    # Kirim email ke admin
    subject, body = general_notification_template(current_user.email, f"API key admin Anda telah direset. Berikut API key baru: {new_key}")
    import asyncio
    try:
        asyncio.create_task(send_verification_email(current_user.email, subject, body))
    except RuntimeError:
        import threading
        threading.Thread(target=asyncio.run, args=(send_verification_email(current_user.email, subject, body),)).start()
    return {"msg": "API key admin berhasil direset. Silakan cek email Anda."}

def get_user_by_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive API Key")
    return user