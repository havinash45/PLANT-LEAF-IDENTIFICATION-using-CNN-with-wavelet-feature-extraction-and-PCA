"""
Authentication API router for user registration and login.
"""

from fastapi import APIRouter
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    return await auth_service.register(request)

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    return await auth_service.login(request)
