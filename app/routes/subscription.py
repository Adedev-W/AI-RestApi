from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserRead
from app.models.db import SessionLocal
from app.core.email_utils import send_verification_email
from app.core.jwt_utils import get_current_user

router = APIRouter(prefix="/subscription", tags=["subscription"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subscribe/{user_id}")
def subscribe(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_subscribed = True
    db.commit()
    return {"msg": "Subscribed to notifications"}

@router.post("/unsubscribe/{user_id}")
def unsubscribe(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_subscribed = False
    db.commit()
    return {"msg": "Unsubscribed from notifications"}

@router.post("/notify")
def notify_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscribers = db.query(User).filter(User.is_subscribed == True).all()
    for user in subscribers:
        # Kirim email notifikasi (asynchronous di production)
        await send_verification_email(user.email, "Notification", "This is a notification email.")
        pass
    return {"msg": f"Notification sent to {len(subscribers)} subscribers"} 