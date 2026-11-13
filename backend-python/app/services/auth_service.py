"""
Authentication service for user registration and login.
"""

from datetime import datetime
import bcrypt
from fastapi import HTTPException, status
from app.models.user import User, Role
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.auth.jwt_utils import create_token

# BCrypt password hashing helpers
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

import logging
logger = logging.getLogger(__name__)

async def register(request: RegisterRequest) -> AuthResponse:
    # Check if email exists
    existing_user = await User.find_one(User.email == request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create user
    try:
        role = Role(request.role.upper()) if request.role else Role.USER
    except ValueError:
        role = Role.USER
        
    hashed_password = hash_password(request.password)
    
    user = User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role=role,
        createdAt=datetime.utcnow()
    )
    
    await user.insert()
    
    token = create_token(user.email, user.role.value)
    
    return AuthResponse(
        token=token,
        email=user.email,
        name=user.name,
        role=user.role.value
    )

async def login(request: LoginRequest) -> AuthResponse:
    user = await User.find_one(User.email == request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
        
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
        
    # Update last login
    user.lastLogin = datetime.utcnow()
    await user.save()
    
    token = create_token(user.email, user.role.value)
    
    return AuthResponse(
        token=token,
        email=user.email,
        name=user.name,
        role=user.role.value
    )
