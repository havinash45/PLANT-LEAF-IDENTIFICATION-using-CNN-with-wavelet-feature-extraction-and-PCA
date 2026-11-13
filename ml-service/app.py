from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model_loader import load_model, preprocess_image, predict_plant

app = Flask(__name__)
CORS(app)

# Load model on startup
model = None
class_names = []

def initialize_model():
    global model, class_names
    try:
        model, class_names = load_model()
        print(f"Model loaded successfully with {len(class_names)} classes")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Using placeholder model for development")

# Initialize model
initialize_model()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        image_bytes = image_file.read()
        
        # Preprocess image
        processed_image = preprocess_image(image_bytes)
        
        # Predict
        plant_name, confidence = predict_plant(model, processed_image, class_names)
        
        return jsonify({
            'plantName': plant_name,
            'confidence': float(confidence)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

