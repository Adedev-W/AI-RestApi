import jwt
from datetime import datetime, timedelta

# Sesuaikan dengan SECRET_KEY dan ALGORITHM di project-mu
SECRET_KEY = "default_secret_key"  # ganti dengan SECRET_KEY asli dari .env
ALGORITHM = "HS256"

# Data admin (ambil dari database)
admin_id = "ISI_ID_ADMIN"  # ganti dengan id admin di database
admin_email = "admin@yourdomain.com"  # ganti dengan email admin

# Payload tanpa exp (tidak expired)
to_encode = {
    "sub": admin_id,
    "email": admin_email
}

token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print("JWT for admin (no expiry):")
print(token) 