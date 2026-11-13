"""
Admin API router for analytics, user management, and prediction verification.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from app.schemas.admin import AdminUserDto, UpdateRoleRequest
from app.models.prediction import Prediction
from app.services import admin_service
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("ADMIN"))]
)

@router.get("/stats")
async def get_stats() -> Dict[str, Any]:
    return await admin_service.get_stats()

@router.get("/users", response_model=List[AdminUserDto])
async def get_recent_users(limit: int = Query(10)):
    users = await admin_service.get_recent_users(limit)
    return [AdminUserDto.from_user(u) for u in users]

@router.get("/users/page")
async def get_users_page(
    page: int = Query(0),
    size: int = Query(10),
    role: str = Query(None)
) -> Dict[str, Any]:
    return await admin_service.get_users_page(page, size, role)

@router.patch("/users/{id}/role", response_model=AdminUserDto)
async def update_user_role(id: str, request: UpdateRoleRequest):
    return await admin_service.update_user_role(id, request.role)

@router.get("/predictions", response_model=List[Prediction])
async def get_recent_predictions(limit: int = Query(10)):
    return await admin_service.get_recent_predictions(limit)

@router.patch("/predictions/{id}/verify", response_model=Prediction)
async def verify_prediction(id: str, user: dict = Depends(get_current_user)):
    verified_by = user.get("sub", "admin")
    return await admin_service.verify_prediction(id, verified_by)
