import numpy as np
import cv2
from PIL import Image
import io
import os
import tensorflow as tf
from tensorflow import keras

# Default class names when no trained model - placeholder only
DEFAULT_CLASS_NAMES = ["Unknown_Plant"]

def load_model():
    """
    Load the trained plant identification model.
    Uses plant_classifier.h5 (trained on leaf_dataset + plantvillage).
    Falls back to nematode_classifier.h5 for backward compatibility.
    """
    base = os.path.dirname(__file__)
    model_path = os.path.join(base, 'models', 'plant_classifier.h5')
    if not os.path.exists(model_path):
        model_path = os.path.join(base, 'models', 'nematode_classifier.h5')

    if os.path.exists(model_path):
        model = keras.models.load_model(model_path)
        class_names_file = os.path.join(base, 'models', 'class_names.txt')
        if os.path.exists(class_names_file):
            with open(class_names_file, 'r') as f:
                class_names = [line.strip() for line in f.readlines()]
        else:
            class_names = DEFAULT_CLASS_NAMES
    else:
        print("Warning: No trained model found. Run: python train_model.py")
        model = create_placeholder_model()
        class_names = DEFAULT_CLASS_NAMES

    return model, class_names

def create_placeholder_model():
    """
    Creates a simple CNN model structure for development/testing.
    In production, this should be replaced with a trained model.
    """
    model = keras.Sequential([
        keras.layers.Input(shape=(224, 224, 3)),
        keras.layers.Conv2D(32, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(len(DEFAULT_CLASS_NAMES), activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def preprocess_image(image_bytes):
    """
    Preprocess image for model input.
    Resizes to 224x224 and normalizes pixel values.
    """
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to numpy array
    image_array = np.array(image)
    
    # Resize to 224x224
    image_resized = cv2.resize(image_array, (224, 224))
    
    # Normalize pixel values to [0, 1]
    image_normalized = image_resized.astype('float32') / 255.0
    
    # Add batch dimension
    image_batch = np.expand_dims(image_normalized, axis=0)
    
    return image_batch

def predict_plant(model, processed_image, class_names):
    """
    Predict plant/class from preprocessed image.
    Returns plant name (for API as plantName) and confidence score.
    """
    predictions = model.predict(processed_image, verbose=0)
    top_index = np.argmax(predictions[0])
    confidence = float(predictions[0][top_index])
    name = class_names[top_index] if top_index < len(class_names) else "Unknown"
    return name, confidence

