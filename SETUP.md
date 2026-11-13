# LeafAI Hub - Setup Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- MongoDB (running on localhost:27017)

## Backend Setup (FastAPI)

1. Navigate to backend-python directory:
```bash
cd backend-python
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --port 8081 --reload
```

The backend will run on `http://localhost:8081`

## Frontend Setup (React)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## ML Service Setup (Python)

1. Navigate to ml-service directory:
```bash
cd ml-service
```

2. Create virtual environment (recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the service:
```bash
python app.py
```

The ML service will run on `http://localhost:5000`

## MongoDB Setup

1. Install MongoDB from https://www.mongodb.com/try/download/community

2. Start MongoDB service:
```bash
# Windows (as Administrator)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
```

3. MongoDB will run on `mongodb://localhost:27017` by default

## Training the Model

The project trains on **leaf_dataset** and **plantvillage dataset** in the `dataset/` folder. All folder names become class labels—fully dynamic.

### Dataset Structure (Expected)
```
dataset/
  leaf_dataset/
    images/lab/<plant_folder>/*.jpg
    images/field/<plant_folder>/*.jpg
    segmented/lab/<plant_folder>/*.png
    segmented/field/<plant_folder>/*.png
  plantvillage dataset/
    color/<plant_folder>/*.jpg
    grayscale/<plant_folder>/*.jpg
    segmented/<plant_folder>/*.jpg
```

### Train Command
```bash
cd ml-service
python train_model.py
# Or with options:
python train_model.py --epochs 30 --batch_size 32
python train_model.py --data_dir ../dataset  # custom path
python train_model.py --sample_ratio 0.1 --epochs 5  # quick test with 10% data
```

### Output
- Model: `ml-service/models/plant_classifier.h5`
- Class names: `ml-service/models/class_names.txt`

After training, restart the ML service. Upload any plant/leaf image to get the predicted plant name.

## Default Credentials

You can register a new account through the registration page. For testing:

- Create an Admin account: Register with role "ADMIN"
- Create a Researcher account: Register with role "RESEARCHER"
- Regular users: Register with role "USER"

## Troubleshooting

### Backend Issues
- Ensure MongoDB is running
- Check `.env` for correct MongoDB URI
- Verify Python 3.10+ is installed and dependencies are installed

### Frontend Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available

### ML Service Issues
- Ensure Python 3.8+ is installed
- Install TensorFlow dependencies: `pip install tensorflow`
- For GPU support, install TensorFlow-GPU

### Port Conflicts
- Backend: Change `--port` in the `uvicorn` command or set `SERVER_PORT` in `.env`
- Frontend: Change port in `vite.config.js`
- ML Service: Change port in `app.py`

## Production Deployment

1. Build frontend:
```bash
cd frontend
npm run build
```

2. Deploy backend using gunicorn or similar:
```bash
cd backend-python
pip install gunicorn httptools uvloop
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8081
```

3. Deploy ML service using gunicorn or similar:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

