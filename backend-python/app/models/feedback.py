"""
Feedback document model for MongoDB collection: "feedback".
"""

from datetime import datetime
from typing import Optional
from beanie import Document


class Feedback(Document):
    predictionId: Optional[str] = None
    userId: Optional[str] = None
    researcherId: Optional[str] = None  # If corrected by researcher
    correctPlantName: Optional[str] = None
    comment: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Settings:
        name = "feedback"
