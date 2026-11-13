"""
Prediction Pydantic schemas.
"""

from typing import List, Optional
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predictionId: str
    plantName: str
    confidence: float
    imageUrl: str
    scientificName: str
    description: str
    leafType: str
    region: str
    
    # Enhanced output fields
    diseaseName: str
    status: str
    pesticides: List[str]
    confidenceLevel: str
