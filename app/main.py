from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.limiter import limiter
from starlette.responses import JSONResponse
from app.core.security import O2AuthMiddleware
from app.routes import auth, subscription, ai, demo
from app.models.db import Base, engine
from fastapi.responses import FileResponse, RedirectResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e, ValueError) and "Rate limit" in str(e):
                 return JSONResponse(status_code=429, content={'detail': str(e)})
            raise e

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(RateLimitMiddleware)

# Inisialisasi database
Base.metadata.create_all(bind=engine)

# Tambahkan O2AuthMiddleware
app.add_middleware(O2AuthMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(subscription.router)
app.include_router(ai.router)
app.include_router(demo.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/demo", include_in_schema=False)
async def read_demo_page():
    return FileResponse('static/index.html') 