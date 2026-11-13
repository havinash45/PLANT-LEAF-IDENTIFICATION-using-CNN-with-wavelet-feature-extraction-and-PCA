"""
ML Service client for sending image inference requests to the ML service.
"""

import httpx
from fastapi import UploadFile
from app.config import settings

async def predict(image_file: UploadFile) -> dict:
    """
    Makes multipart POST request to the ML inference service.
    """
    url = f"{settings.ml_service_url}/predict"
    
    # Reset cursor to 0 before reading, as it might have been saved already
    await image_file.seek(0)
    file_data = await image_file.read()
    
    files = {
        "image": (image_file.filename, file_data, image_file.content_type)
    }
    
    async with httpx.AsyncClient(timeout=settings.ml_service_timeout / 1000) as client:
        response = await client.post(url, files=files)
        response.raise_for_status()
        return response.json()
