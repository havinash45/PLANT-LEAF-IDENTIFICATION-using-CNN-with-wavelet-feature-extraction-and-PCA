"""
Researcher API router for reviewing unverified predictions and verifying plant species.
"""

from typing import List, Dict,Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.models.prediction import Prediction
from app.auth.dependencies import get_current_user, require_role
from beanie import PydanticObjectId

router = APIRouter(
    prefix="/api/researcher",
    tags=["researcher"],
    dependencies=[Depends(require_role("RESEARCHER", "ADMIN"))]
)

@router.get("/unverified", response_model=List[Prediction])
async def get_unverified_predictions():
    return await Prediction.find(Prediction.verified == False).to_list()

@router.post("/verify/{predictionId}", response_model=Prediction)
async def verify_prediction(
    predictionId: str,
    request: Dict[str, Optional[str]],
    user: dict = Depends(get_current_user)
):
    try:
        obj_id = PydanticObjectId(predictionId)
    except Exception:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    prediction = await Prediction.get(obj_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    correct_plant_name = request.get("correctPlantName")
    if correct_plant_name:
        prediction.plantName = correct_plant_name
        
    prediction.verified = True
    prediction.verifiedBy = user.get("sub", "researcher")
    prediction.timestamp = datetime.utcnow()
    
    await prediction.save()
    return prediction
