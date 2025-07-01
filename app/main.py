from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.limiter import limiter
from starlette.responses import JSONResponse
from app.core.security import O2AuthMiddleware, get_current_user_by_api_key
from app.routes import auth, ai, demo
from app.models.db import Base, engine
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.responses import HTMLResponse
import json
import os

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e, ValueError) and "Rate limit" in str(e):
                 return JSONResponse(status_code=429, content={'detail': str(e)})
            raise e

from fastapi import FastAPI

app = FastAPI(
    title="Authentication & User Management API",
    description="""
This API provides endpoints for user registration, authentication, password management, 
role-based access control (RBAC). Only administrators can create new users and API keys.
Web Demo: http://127.0.0.1:8080/demo
""",
    version="1.0.0",
    contact={
        "name": "Your Team Name",
        "email": "support@yourdomain.com",
        "url": "https://yourdomain.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,      # Swagger UI
    redoc_url=None,    # ReDoc
    openapi_url="/openapi.json"
)
app.state.limiter = limiter
app.add_middleware(RateLimitMiddleware)

# Inisialisasi database
Base.metadata.create_all(bind=engine)

# Tambahkan O2AuthMiddleware
app.add_middleware(O2AuthMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(demo.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/demo", include_in_schema=False)
async def read_demo_page():
    return FileResponse('static/index.html') 

@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_docs():
    return HTMLResponse("""
    <!doctype html>
    <html>
        <head>
        <title>RapiDoc</title>
        <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
        </head>
        <body>
        <rapi-doc
            spec-url="/openapi.json"
            render-style="read"
            allow-server-selection="false"
            allow-authentication="true"
            allow-try="true"
            show-header="true"
            layout="column"
        > </rapi-doc>
        </body>
    </html>
    """)

@app.get("/admin-openapi.json", include_in_schema=False)
async def admin_openapi(request: Request):
    admin_api_key = request.query_params.get("admin_api_key")
    from app.models.db import SessionLocal
    from app.models.user import User
    from datetime import datetime, timedelta
    import secrets
    from app.core.email_utils import send_verification_email, general_notification_template
    import asyncio
    EXPIRED_ADMIN_TOKEN_DAYS = int(os.getenv("EXPIRED_ADMIN_TOKEN_DAYS", 30))
    db = SessionLocal()
    admin = db.query(User).filter(User.api_key == admin_api_key, User.role == "admin").first()
    if not admin or not admin.is_active:
        db.close()
        return JSONResponse(status_code=403, content={"detail": "Not authorized"})
    # Jika expired, reset API key, update expiry, kirim email
    if admin.api_key_expires and admin.api_key_expires < datetime.utcnow():
        new_key = secrets.token_urlsafe(32)
        admin.api_key = new_key
        admin.api_key_expires = datetime.utcnow() + timedelta(days=EXPIRED_ADMIN_TOKEN_DAYS)
        db.commit()
        subject, body = general_notification_template(admin.email, f"API key admin Anda telah expired dan direset. Berikut API key baru: {new_key}")
        try:
            asyncio.create_task(send_verification_email(admin.email, subject, body))
        except RuntimeError:
            import threading
            threading.Thread(target=asyncio.run, args=(send_verification_email(admin.email, subject, body),)).start()
        db.close()
        return JSONResponse(status_code=401, content={"detail": "API Key expired. New key sent to your email."})
    db.close()
    # Baca file openapi_adminstrator.json
    with open("app/openapi_adminstrator.json", "r") as f:
        raw_openapi = json.load(f)
    # Filter hanya endpoint admin
    admin_paths = {}
    for path in ["/auth/register", "/auth/admin-reset-apikey"]:
        if path in raw_openapi["paths"]:
            admin_paths[path] = raw_openapi["paths"][path]
    # Siapkan hasil akhir
    admin_openapi = {
        "openapi": raw_openapi["openapi"],
        "info": raw_openapi["info"],
        "paths": admin_paths,
        "components": raw_openapi.get("components", {}),
        "tags": raw_openapi.get("tags", [])
    }
    return JSONResponse(admin_openapi)