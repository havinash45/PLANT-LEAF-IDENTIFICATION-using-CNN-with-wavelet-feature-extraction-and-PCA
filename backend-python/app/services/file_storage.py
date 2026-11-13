"""
File storage service for saving uploaded leaf images.
"""

import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.config import settings

def store_file(file: UploadFile) -> str:
    """
    Stores an uploaded file using a unique UUID.
    """
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = upload_path / file_name
    
    # Write to disk
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return str(file_path)

def get_file_url(file_path: str) -> str:
    """
    Generates public URL path for the uploaded file.
    """
    filename = Path(file_path).name
    return f"/uploads/{filename}"
