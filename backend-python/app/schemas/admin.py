"""
Admin Pydantic schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.user import User


class AdminUserDto(BaseModel):
    id: str
    email: str
    name: str
    role: Optional[str]
    createdAt: Optional[datetime]
    lastLogin: Optional[datetime]

    @classmethod
    def from_user(cls, user: User) -> "AdminUserDto":
        return cls(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role.value if user.role else None,
            createdAt=user.createdAt,
            lastLogin=user.lastLogin
        )


class UpdateRoleRequest(BaseModel):
    role: str  # USER, ADMIN, RESEARCHER
