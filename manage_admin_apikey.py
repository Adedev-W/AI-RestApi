import sys
import secrets
from datetime import datetime, timedelta, UTC
from app.models.db import SessionLocal
from app.models.user import User

def print_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("Admin user not found!")
    else:
        print(f"Admin email: {admin.email}")
        print(f"API key: {admin.api_key}")
        print(f"API key expires: {admin.api_key_expires}")
    db.close()

def reset_admin_key(seconds=1):
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("Admin user not found!")
    else:
        new_key = secrets.token_urlsafe(32)
        admin.api_key = new_key
        admin.api_key_expires = datetime.now(UTC) + timedelta(seconds=seconds)
        db.commit()
        print(f"API key admin direset!")
        print(f"API key baru: {new_key}")
        print(f"Expired: {admin.api_key_expires}")
    db.close()

def set_admin_expiry(seconds):
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("Admin user not found!")
    else:
        admin.api_key_expires = datetime.now(UTC) + timedelta(seconds=seconds)
        db.commit()
        print(f"API key admin expiry di-set ke {admin.api_key_expires}")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python manage_admin_apikey.py [print|reset|set-expiry <seconds>]")
    elif sys.argv[1] == "print":
        print_admin()
    elif sys.argv[1] == "reset":
        seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        reset_admin_key(seconds)
    elif sys.argv[1] == "set-expiry" and len(sys.argv) > 2:
        set_admin_expiry(int(sys.argv[2]))
    else:
        print("Unknown command. Usage: python manage_admin_apikey.py [print|reset|set-expiry <seconds>]") 