"""
Prediction service for leaf image classification, botanical enrichment, and prediction history.
"""

import logging
from datetime import datetime
from typing import List, Tuple
from fastapi import UploadFile, HTTPException

from app.models.user import User
from app.models.plant import Plant
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionResponse

# Import initialized service dependencies
from app.services import file_storage, ml_client

logger = logging.getLogger(__name__)

def parse_prediction_label(label: str) -> Tuple[str, str, str]:
    """
    Parses ML prediction label into plant name, disease name, and health status.
    Returns (plantData, diseaseName, status)
    """
    try:
        if not label:
            return "Unknown", "Unknown", "Unknown"
            
        parts = label.split("___")
        plant_data = parts[0]
        
        # Format plant name
        plant_data = plant_data.replace("_", " ")
        if len(plant_data) > 0:
            plant_data = plant_data[0].upper() + plant_data[1:]
            
        if len(parts) == 1:
            # Simple plant name
            disease_name = "Healthy"
            status = "Healthy"
        else:
            disease_data = parts[1]
            if "Healthy" in disease_data or "healthy" in disease_data:
                disease_name = "Healthy"
                status = "Healthy"
            else:
                disease_name = disease_data.replace("_", " ")
                status = "Unhealthy"
                
        return plant_data, disease_name, status
    except Exception as e:
        logger.error(f"Error parsing label {label}: {e}")
        return "Error", "Error", "Error"


def get_pesticides(disease_name: str) -> List[str]:
    """
    Retrieves recommended pesticides for a given plant disease.
    """
    pesticide_map = {
        "Late blight": ["Mancozeb", "Chlorothalonil"],
        "Early blight": ["Copper fungicide"],
        "Leaf Mold": ["Chlorothalonil"],
        "Septoria leaf spot": ["Chlorothalonil", "Copper-based fungicides"],
        "Spider mites Two-spotted spider mite": ["Neem oil", "Insecticidal soap"],
        "Target Spot": ["Chlorothalonil"],
        "Yellow Leaf Curl Virus": ["Control whiteflies with Imidacloprid"],
        "Mosaic virus": ["Remove infected plants", "Control aphids"],
        "Bacterial spot": ["Copper-based bactericides"],
        "Powdery mildew": ["Sulfur", "Neem oil"],
        "Healthy": []
    }
    
    return pesticide_map.get(disease_name, ["Not Available in Database"])


async def predict(user_email: str, image_file: UploadFile) -> PredictionResponse:
    # Validate user
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Store file
    try:
        image_path = file_storage.store_file(image_file)
        image_url = file_storage.get_file_url(image_path)
    except Exception as e:
        logger.error(f"File store error: {e}")
        raise HTTPException(status_code=500, detail="Could not store file")
        
    # Call ML
    try:
        ml_response = await ml_client.predict(image_file)
    except Exception as e:
        logger.error(f"ML Service error: {e}")
        raise HTTPException(status_code=500, detail="ML Service error")
        
    plant_name_raw = ml_response.get("plantName", "")
    confidence = ml_response.get("confidence", 0.0)
    
    # DB Queries
    plant = await Plant.find_one(Plant.plantName == plant_name_raw)
    if not plant:
        plant = Plant()  # Default empty plant
        
    extracted_plant, disease_name, status = parse_prediction_label(plant_name_raw)
    pesticides = get_pesticides(disease_name)
    confidence_level = "High Chances" if confidence >= 0.50 else "Low Chances"
    
    # Save Prediction
    prediction = Prediction(
        userId=str(user.id),
        plantName=plant_name_raw,
        confidence=confidence,
        imageUrl=image_url,
        imagePath=image_path,
        timestamp=datetime.utcnow(),
        verified=False,
        diseaseName=disease_name,
        status=status,
        pesticides=pesticides,
        confidenceLevel=confidence_level,
        scientificName=plant.scientificName
    )
    await prediction.insert()
    
    return PredictionResponse(
        predictionId=str(prediction.id),
        plantName=plant_name_raw,
        confidence=confidence,
        imageUrl=image_url,
        scientificName=plant.scientificName or "",
        description=plant.description or "",
        leafType=plant.leafType or "",
        region=plant.region or "",
        diseaseName=disease_name,
        status=status,
        pesticides=pesticides,
        confidenceLevel=confidence_level
    )


async def predict_batch(user_email: str, image_files: List[UploadFile]) -> List[PredictionResponse]:
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    responses = []
    
    for image_file in image_files:
        try:
            image_path = file_storage.store_file(image_file)
            image_url = file_storage.get_file_url(image_path)
            
            ml_response = await ml_client.predict(image_file)
            plant_name_raw = ml_response.get("plantName", "")
            confidence = ml_response.get("confidence", 0.0)
            
            plant = await Plant.find_one(Plant.plantName == plant_name_raw)
            if not plant:
                plant = Plant()
                
            extracted_plant, disease_name, status = parse_prediction_label(plant_name_raw)
            pesticides = get_pesticides(disease_name)
            confidence_level = "High Chances" if confidence >= 0.50 else "Low Chances"
            
            prediction = Prediction(
                userId=str(user.id),
                plantName=plant_name_raw,
                confidence=confidence,
                imageUrl=image_url,
                imagePath=image_path,
                timestamp=datetime.utcnow(),
                verified=False,
                diseaseName=disease_name,
                status=status,
                pesticides=pesticides,
                confidenceLevel=confidence_level,
                scientificName=plant.scientificName
            )
            await prediction.insert()
            
            responses.append(
                PredictionResponse(
                    predictionId=str(prediction.id),
                    plantName=plant_name_raw,
                    confidence=confidence,
                    imageUrl=image_url,
                    scientificName=plant.scientificName or "",
                    description=plant.description or "",
                    leafType=plant.leafType or "",
                    region=plant.region or "",
                    diseaseName=disease_name,
                    status=status,
                    pesticides=pesticides,
                    confidenceLevel=confidence_level
                )
            )
        except Exception as e:
            logger.error(f"Error processing image {image_file.filename}: {e}")
            
    return responses


async def get_history(user_email: str) -> List[Prediction]:
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    predictions = await Prediction.find(
        Prediction.userId == str(user.id)
    ).sort("-timestamp").to_list()
    
    return predictions
