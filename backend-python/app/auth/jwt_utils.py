"""
JWT utilities for token generation and verification.
"""

import jwt
from datetime import datetime, timedelta
from app.config import settings

ALGORITHM = "HS256"


def create_token(email: str, role: str) -> str:
    """
    Generate JWT Token with subject=email and role claim.
    """
    expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expiration_seconds)
    to_encode = {
        "sub": email,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode JWT and verify signature and expiration.
    """
    try:
        decoded_token = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token is expired")
    except jwt.InvalidTokenError:
        raise ValueError("Token is invalid")
