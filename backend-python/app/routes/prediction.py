"""
Prediction API router for single/batch leaf image classification and history.
"""

from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas.prediction import PredictionResponse
from app.models.prediction import Prediction
from app.services import prediction_service
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/predict", tags=["prediction"])

@router.post("", response_model=PredictionResponse)
async def predict(
    image: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    return await prediction_service.predict(user["sub"], image)

@router.post("/batch", response_model=List[PredictionResponse])
async def predict_batch(
    images: List[UploadFile] = File(...),
    user: dict = Depends(get_current_user)
):
    return await prediction_service.predict_batch(user["sub"], images)

@router.get("/history", response_model=List[Prediction])
async def get_history(user: dict = Depends(get_current_user)):
    return await prediction_service.get_history(user["sub"])
