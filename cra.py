import uuid
import secrets
from app.models.db import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

admin_email = "exampleadmin@gmail.com"
admin_password = "SuperSecurePassword123!"

hashed_password = pwd_context.hash(admin_password)
api_key = secrets.token_urlsafe(32)
admin_user = User(
    id=str(uuid.uuid4()),
    email=admin_email,
    hashed_password=hashed_password,
    is_active=True,
    is_verified=True,
    role="admin",
    api_key=api_key
)
db.add(admin_user)
db.commit()
db.close()
print("Admin user created!")
print(f"API Key: {api_key}")
