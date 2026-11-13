"""
User document model for MongoDB collection: "users".
"""

import enum
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field


class Role(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"


class User(Document):
    email: Indexed(str, unique=True)  # type: ignore[valid-type]
    name: str
    password: str
    role: Role = Role.USER
    createdAt: Optional[datetime] = None
    lastLogin: Optional[datetime] = None

    class Settings:
        name = "users"
        use_state_management = True
