# LeafAI Hub - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Start MongoDB
Ensure MongoDB is running locally or use a MongoDB Atlas connection string configured in `backend-python/.env`:

```bash
# Windows (Command Prompt as Administrator)
net start MongoDB

# Linux / macOS
sudo systemctl start mongod
```

### Step 2: Start ML Service (Python / Flask)
```bash
cd ml-service

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies and start server
pip install -r requirements.txt
python app.py
```
✅ ML Service running on **http://localhost:5000**

### Step 3: Start Backend (Python / FastAPI)
```bash
cd backend-python

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies and start server
pip install -r requirements.txt
uvicorn main:app --port 8081 --reload
```
✅ Backend running on **http://localhost:8081**  
📚 Interactive Swagger API Docs: **http://localhost:8081/docs**

### Step 4: Start Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
✅ Frontend running on **http://localhost:5173**

---

## 🎯 First Steps

1. **Open Browser**: Navigate to [http://localhost:5173](http://localhost:5173).
2. **Register**: Create a new account with your preferred role (**USER**, **ADMIN**, or **RESEARCHER**).
3. **Login**: Authenticate using your registered email and password.
4. **Identify Plants**:
   - **Single Upload**: Upload a leaf image from your file system or take a photo with your camera to view instant species identification, disease diagnosis, health status, and pesticide recommendations.
   - **Batch Upload**: Switch to "Batch Upload (20-30 images)", select multiple leaf images from `ml-service/sample_test_images/`, and identify them all simultaneously.

---

## 📝 User Roles & Test Accounts

You can register accounts with the following roles:
- **USER**: Standard access for leaf image upload, plant identification, disease analysis, and viewing prediction history.
- **ADMIN**: Access to the Admin Analytics Dashboard, system metrics, top identified plants, recent predictions, and the user management portal with role reassignment.
- **RESEARCHER**: Access to the Researcher Dashboard to inspect unverified predictions, review leaf images, and confirm or correct identified plant species and disease diagnoses.

---

## 🔧 Troubleshooting

### Port Already in Use
- **Backend (Port 8081)**: Change `SERVER_PORT` in `backend-python/.env` or specify a custom port in the uvicorn command:
  ```bash
  uvicorn main:app --port 8082 --reload
  ```
  *(Note: If changing backend port, also update `baseURL` in `frontend/src/services/api.js`)*
- **Frontend (Port 5173)**: Change port in `frontend/vite.config.js`.
- **ML Service (Port 5000)**: Change port in `ml-service/app.py` and update `ML_SERVICE_URL` in `backend-python/.env`.

### MongoDB Connection Error
- Ensure the MongoDB service is active (`net start MongoDB` or `sudo systemctl status mongod`).
- Verify the connection string in `backend-python/.env`:
  ```ini
  MONGODB_URI=mongodb://localhost:27017
  MONGODB_DATABASE=leafai_hub
  ```

### ML Service Not Responding
- Verify Python virtual environment dependencies are installed (`pip install -r requirements.txt`).
- Verify model files exist in `ml-service/models/` (`plant_classifier.h5` and `class_names.txt`). If absent, a fallback placeholder model will load automatically for testing.
- Check terminal logs for inference or memory errors.

---

## 🎓 For Development

### Generating Test Images for Batch Upload
```bash
cd ml-service
python create_test_images.py
```
This generates 30 sample leaf images in `ml-service/sample_test_images/` ready for batch upload testing in the UI.

### Training Your Own Model
```bash
cd ml-service
python train_model.py --epochs 30 --batch_size 32
# Or with a custom dataset directory:
python train_model.py --data_dir ../dataset --epochs 30
```

### Running Backend Unit Tests
```bash
cd backend-python
pytest tests/
```

### Production Deployment
```bash
# 1. Build Frontend
cd frontend
npm run build

# 2. Deploy FastAPI Backend with Uvicorn / Gunicorn
cd backend-python
uvicorn main:app --host 0.0.0.0 --port 8081 --workers 4
# Or with Gunicorn:
# gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8081

# 3. Deploy ML Service
cd ml-service
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 💡 Tips

- The backend automatically serves uploaded images via static files at `http://localhost:8081/uploads/<filename>`.
- Interactive OpenAPI / Swagger documentation is available at `http://localhost:8081/docs` and ReDoc at `http://localhost:8081/redoc`.
- Researchers can verify predictions directly from the Researcher Dashboard to enrich the database and improve prediction accuracy.
