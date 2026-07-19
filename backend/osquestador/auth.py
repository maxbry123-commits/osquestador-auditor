"""Auth module: JWT with HttpOnly cookies (best practice 2026)
REGLA #0: OpenClaw INTACTO - this auth is local to osquestador-auditor only.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import hashlib, hmac, secrets, time, base64, json

SECRET = b"osquestador-auditor-secret-CHANGE-IN-PROD"
TOKEN_TTL = 60 * 60 * 24  # 24h

class User(BaseModel):
    id: str
    name: str
    plan: str = "free"

# In-memory user store (single demo user)
USERS = {
    "max": User(id="max", name="Maxbry Odreman", plan="Plus Plan")
}

def hash_password(pw: str, salt: str = "osq-salt") -> str:
    return hashlib.sha256(f"{salt}:{pw}".encode()).hexdigest()

def verify_password(pw: str, hash_: str) -> bool:
    return hmac.compare_digest(hash_password(pw), hash_)

# JWT (simple HS256 - for demo, swap to python-jose in prod)
def make_token(user_id: str) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({
        "sub": user_id, "iat": int(time.time()), "exp": int(time.time()) + TOKEN_TTL
    }).encode()).rstrip(b"=").decode()
    sig = hmac.new(SECRET, f"{header}.{payload}".encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
    return f"{header}.{payload}.{sig_b64}"

def verify_token(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3: return None
        header, payload, sig = parts
        expected = hmac.new(SECRET, f"{header}.{payload}".encode(), hashlib.sha256).digest()
        actual = base64.urlsafe_b64decode(sig + "==")
        if not hmac.compare_digest(expected, actual): return None
        data = json.loads(base64.urlsafe_b64decode(payload + "=="))
        if data.get("exp", 0) < time.time(): return None
        return data
    except Exception:
        return None

def get_current_user_optional(request: Request) -> Optional[User]:
    """Get user from cookie OR Authorization header (for API clients)."""
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        return None
    payload = verify_token(token)
    if not payload:
        return None
    return USERS.get(payload["sub"])

def get_current_user(request: Request) -> User:
    user = get_current_user_optional(request)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user
