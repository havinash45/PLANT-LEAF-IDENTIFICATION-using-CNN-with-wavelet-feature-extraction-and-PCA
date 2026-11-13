"""
Admin service for platform statistics, user management, and prediction verification.
"""

from typing import List, Dict, Any
from fastapi import HTTPException
from app.models.user import User, Role
from app.models.prediction import Prediction
from app.schemas.admin import AdminUserDto


async def get_stats() -> Dict[str, Any]:
    total_users = await User.count()
    total_predictions = await Prediction.count()
    unverified_predictions = await Prediction.find(Prediction.verified == False).count()
    
    # Top plants
    all_predictions = await Prediction.find_all().to_list()
    plant_counts = {}
    for p in all_predictions:
        name = p.plantName
        if name:
            plant_counts[name] = plant_counts.get(name, 0) + 1
            
    return {
        "totalUsers": total_users,
        "totalPredictions": total_predictions,
        "unverifiedPredictions": unverified_predictions,
        "topPlants": plant_counts
    }


async def get_recent_users(limit: int) -> List[User]:
    limit = min(limit, 100)
    users = await User.find_all().sort("-createdAt").limit(limit).to_list()
    return users


async def get_recent_predictions(limit: int) -> List[Prediction]:
    limit = min(limit, 100)
    predictions = await Prediction.find_all().sort("-timestamp").limit(limit).to_list()
    return predictions


async def verify_prediction(prediction_id: str, verified_by: str) -> Prediction:
    from beanie import PydanticObjectId
    
    try:
        obj_id = PydanticObjectId(prediction_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    p = await Prediction.get(obj_id)
    if not p:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    p.verified = True
    p.verifiedBy = verified_by
    await p.save()
    return p


async def get_users_page(page: int, size: int, role_filter: str = None) -> Dict[str, Any]:
    size = min(size, 50)
    skip = page * size
    
    query = User.find_all()
    if role_filter and role_filter.strip():
        try:
            r = Role(role_filter.strip().upper())
            query = User.find(User.role == r)
        except ValueError:
            pass
            
    total_elements = await query.count()
    user_page = await query.sort("-createdAt").skip(skip).limit(size).to_list()
    
    content = [AdminUserDto.from_user(u) for u in user_page]
    total_pages = (total_elements + size - 1) // size if size > 0 else 0
    
    return {
        "content": content,
        "totalElements": total_elements,
        "totalPages": total_pages,
        "currentPage": page,
        "size": size
    }


async def update_user_role(user_id: str, new_role: str) -> AdminUserDto:
    from beanie import PydanticObjectId
    try:
        obj_id = PydanticObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = await User.get(obj_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    try:
        role = Role(new_role.strip().upper())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    user.role = role
    await user.save()
    return AdminUserDto.from_user(user)
