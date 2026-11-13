"""
MongoDB database initialization using Motor and Beanie ODM.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings


async def init_db():
    """Initialize MongoDB connection and Beanie ODM."""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_database]

    # Import models here to avoid circular imports
    from app.models.user import User
    from app.models.prediction import Prediction
    from app.models.plant import Plant
    from app.models.feedback import Feedback

    await init_beanie(
        database=database,
        document_models=[User, Prediction, Plant, Feedback],
    )
