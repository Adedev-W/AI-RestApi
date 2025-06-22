import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

rate_limit_str = os.getenv("RATE_LIMIT", "5/minute")
limiter = Limiter(key_func=get_remote_address, default_limits=[rate_limit_str]) 