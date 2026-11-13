"""
Prediction document model for MongoDB collection: "predictions".
"""

from datetime import datetime
from typing import Optional, List
from beanie import Document


class Prediction(Document):
    userId: Optional[str] = None
    plantName: Optional[str] = None
    confidence: Optional[float] = None
    imageUrl: Optional[str] = None
    imagePath: Optional[str] = None
    timestamp: Optional[datetime] = None
    verified: Optional[bool] = False
    verifiedBy: Optional[str] = None
    feedback: Optional[str] = None

    # Enhanced output fields
    diseaseName: Optional[str] = None
    status: Optional[str] = None  # Healthy, Unhealthy
    pesticides: Optional[List[str]] = None
    confidenceLevel: Optional[str] = None  # High Chances, Low Chances
    scientificName: Optional[str] = None

    class Settings:
        name = "predictions"
        use_state_management = True
