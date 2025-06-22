from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

class O2AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Tambahkan logika autentikasi O2Auth dan pengiriman email verifikasi
        response = await call_next(request)
        return response 