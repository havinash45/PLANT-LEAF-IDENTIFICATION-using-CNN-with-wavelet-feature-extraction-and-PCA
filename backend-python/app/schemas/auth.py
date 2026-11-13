"""
Authentication Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "USER"  # USER, ADMIN, RESEARCHER


class AuthResponse(BaseModel):
    token: str
    email: str
    name: str
    role: str
