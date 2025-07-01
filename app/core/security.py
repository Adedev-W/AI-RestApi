from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, Header, HTTPException, Depends
from app.models.user import User
from app.models.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
import secrets
from datetime import datetime, timedelta
from app.core.email_utils import send_verification_email, general_notification_template
import os

class O2AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Tambahkan logika autentikasi O2Auth dan pengiriman email verifikasi
        response = await call_next(request)
        return response 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)

EXPIRED_ADMIN_TOKEN_DAYS = int(os.getenv("EXPIRED_ADMIN_TOKEN_DAYS", 30))

def get_current_user_by_api_key(x_api_key: str = Depends(api_key_scheme), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive API Key")
    # Cek expiry
    if user.api_key_expires and user.api_key_expires < datetime.utcnow():
        new_key = secrets.token_urlsafe(32)
        user.api_key = new_key
        user.api_key_expires = datetime.utcnow() + timedelta(days=EXPIRED_ADMIN_TOKEN_DAYS)
        db.commit()
        subject, body = general_notification_template(user.email, f"API key Anda telah expired. Berikut API key baru Anda: {new_key}")
        try:
            import asyncio
            asyncio.create_task(send_verification_email(user.email, subject, body))
        except RuntimeError:
            # fallback jika di context sync
            import threading
            threading.Thread(target=asyncio.run, args=(send_verification_email(user.email, subject, body),)).start()
        raise HTTPException(status_code=401, detail="API Key expired. New key sent to your email.")
    return user

def api_key_header(x_api_key: str = Depends(api_key_scheme)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header missing")
    return x_api_key 