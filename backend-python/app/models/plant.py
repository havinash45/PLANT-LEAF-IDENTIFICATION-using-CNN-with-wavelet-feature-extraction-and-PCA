"""
Plant document model for MongoDB collection: "plants".
"""

from datetime import datetime
from typing import Optional, List
from beanie import Document


class Plant(Document):
    plantName: Optional[str] = None
    scientificName: Optional[str] = None
    leafType: Optional[str] = None  # Simple, Compound, etc.
    region: Optional[str] = None
    description: Optional[str] = None
    imagePaths: Optional[List[str]] = None
    sampleCount: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Settings:
        name = "plants"
