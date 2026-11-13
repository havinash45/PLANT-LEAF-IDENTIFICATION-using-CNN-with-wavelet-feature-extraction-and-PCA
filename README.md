<<<<<<< HEAD
# LeafAI Hub – Intelligent Plant Species Identification Platform

A full-stack AI-powered platform for identifying plant species and diagnosing leaf diseases from images using deep learning, FastAPI, React, and MongoDB.

---

## 🏗️ Architecture

```
LeafAI Hub/
├── backend-python/   # FastAPI REST API Backend (Port 8081)
├── frontend/         # React 18 + Vite + Tailwind CSS (Port 5173)
├── ml-service/       # Python Flask + TensorFlow CNN Service (Port 5000)
├── dataset/          # Botanical & Plant Disease Training Datasets
└── README.md
```

---

## 🚀 Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI**: Modern, high-performance web framework for building APIs
- **Uvicorn**: Asynchronous ASGI web server
- **Motor & Beanie ODM**: Asynchronous MongoDB driver and object-document mapper built on Pydantic
- **PyJWT**: Secure JSON Web Token authentication (`HS256`)
- **BCrypt**: Password hashing and verification
- **HTTPX**: Async HTTP client for ML service communication
- **Pydantic**: Robust data validation and schema serialization

### Frontend
- **React 18**
- **Vite**: Next-generation frontend tooling and build server
- **Tailwind CSS**: Utility-first styling framework
- **Axios**: HTTP client for API requests (configured for `http://localhost:8081`)
- **Chart.js & React-Chartjs-2**: Interactive data visualizations and analytics
- **React Router 6**: Client-side routing with role-protected routes

### AI / Machine Learning
- **Python 3.8+**
- **Flask**: Lightweight REST inference microservice
- **TensorFlow / Keras**: MobileNetV2 convolutional neural network (transfer learning)
- **OpenCV & Pillow**: Image preprocessing and augmentation
- **NumPy**: Numerical operations and tensor manipulation

---

## 📋 Features

### User Portal
- **Single Image Upload**: Upload leaf photos via file picker or camera capture
- **Batch Image Upload**: Process up to 30 images simultaneously with aggregated results
- **Real-Time Identification**: Species prediction, health status (`Healthy` / `Unhealthy`), and disease identification
- **Confidence Scoring & Levels**: Percentage score and categorization (`High Chances` / `Low Chances`)
- **Treatment Recommendations**: Context-aware pesticide suggestions for identified diseases
- **Botanical Metadata**: Scientific names, leaf types, and geographical distribution
- **Prediction History**: Searchable and filterable archive of past user predictions

### Admin Portal
- **Platform Analytics**: Total users, total predictions, unverified counts, and popularity charts
- **User Management**: Paginated user directory with real-time role modification (`USER`, `ADMIN`, `RESEARCHER`)
- **Prediction Monitoring**: Recent platform-wide predictions and admin verification controls

### Researcher Portal
- **Verification Queue**: Dedicated list of unverified predictions requiring expert inspection
- **Species & Disease Correction**: Update misdiagnosed predictions to maintain ground-truth quality
- **Feedback Loop**: Annotations and verification records to improve dataset training quality

---

## 🎨 Design

**Color Palette:**
- Primary: `#2E7D32` (Forest Green)
- Secondary: `#A5D6A7` (Mint Green)
- Accent: `#FBC02D` (Sunflower Yellow)
- Background: `#F5F7F6` (Off-White)
- Text: `#263238` (Charcoal)

---

## 🔧 Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**
- **MongoDB** (running locally on `localhost:27017` or a MongoDB Atlas URI)

### 2. Backend Setup (FastAPI)
```bash
cd backend-python

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --port 8081 --reload
```
✅ Backend running on **http://localhost:8081**  
📚 Interactive Swagger UI: **http://localhost:8081/docs**

### 3. Frontend Setup (React)
```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
✅ Frontend running on **http://localhost:5173**

### 4. ML Service Setup (Flask)
```bash
cd ml-service

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the inference server
python app.py
```
✅ ML Service running on **http://localhost:5000**

---

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new account (`name`, `email`, `password`, `role`)
- `POST /api/auth/login` - Authenticate and receive a JWT Bearer token

### Predictions
- `POST /api/predict` - Upload a single leaf image for species/disease identification
- `POST /api/predict/batch` - Upload multiple leaf images (up to 30) for batch identification
- `GET /api/predict/history` - Retrieve authenticated user's prediction history

### Admin
- `GET /api/admin/stats` - Platform-wide statistics and top plant counts
- `GET /api/admin/users` - Retrieve recent users list
- `GET /api/admin/users/page` - Paginated user management with optional role filtering
- `PATCH /api/admin/users/{id}/role` - Update a user's role (`USER`, `ADMIN`, `RESEARCHER`)
- `GET /api/admin/predictions` - Retrieve platform-wide recent predictions
- `PATCH /api/admin/predictions/{id}/verify` - Mark a prediction as verified

### Researcher
- `GET /api/researcher/unverified` - Fetch all unverified predictions for review
- `POST /api/researcher/verify/{predictionId}` - Verify or correct identified plant species

---

## 📚 Documentation Links

- [QUICKSTART.md](QUICKSTART.md) - Fast 5-minute setup and execution guide
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed directory structure and component breakdown
- [SETUP.md](SETUP.md) - Complete configuration, training, and production deployment guide
- [FEATURES.md](FEATURES.md) - Full feature matrix and functional specifications
- [QUICK_IMAGE_GUIDE.md](QUICK_IMAGE_GUIDE.md) - Generating and testing sample leaf images

---

## 🎯 Target Accuracy
90%+ plant species identification and leaf disease classification accuracy using transfer learning.
=======
# PLANT-LEAF-IDENTIFICATION-using-CNN-with-wavelet-feature-extraction-and-PCA
>>>>>>> fa0e2f067ff664d9ba5f4051270712ee04a11b62
