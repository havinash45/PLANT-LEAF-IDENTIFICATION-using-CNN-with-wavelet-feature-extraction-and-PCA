# Quick Guide: Get 20-30 Test Leaf Images

This guide explains how to generate, collect, and use 20–30 test leaf images to test the single upload and batch identification features in LeafAI Hub.

---

## 🚀 Fastest Method (Under 30 Seconds)

Run the automated image generation script inside the `ml-service` directory:

```bash
cd ml-service
python create_test_images.py
```

This creates 30 synthetic leaf test images in the `ml-service/sample_test_images/` folder:
- Files generated: `test_leaf_01.jpg` through `test_leaf_30.jpg`.

---

## 📸 Sourcing Real Plant Leaf Images

If you prefer testing with real botanical photographs:

### Option 1: Unsplash (Free High-Resolution Photos)
1. Visit: [https://unsplash.com/s/photos/plant-leaf](https://unsplash.com/s/photos/plant-leaf)
2. Download 20–30 diverse plant leaf photos.
3. Save or copy them into `ml-service/sample_test_images/`.

### Option 2: Public Datasets
- **PlantVillage Dataset**: [Kaggle PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset)  
  Extract sample leaves from various plant disease folders (e.g., Tomato, Potato, Apple, Pepper).
- **Flavia Leaf Dataset**: Search online for "Flavia leaf dataset" for clean, segmented leaf specimens.

### Option 3: Phone Photos
1. Take well-lit photos of 20–30 different leaves in your garden or local park.
2. Transfer them to your computer.
3. Place them into `ml-service/sample_test_images/`.

---

## 🔄 End-to-End Batch Testing Workflow

### 1. Ensure All Services Are Running

| Service | Technology | Address |
| :--- | :--- | :--- |
| **MongoDB** | Database Engine | `mongodb://localhost:27017` |
| **ML Service** | Python / Flask / TensorFlow | `http://localhost:5000` |
| **Backend API** | Python / FastAPI / Uvicorn | `http://localhost:8081` |
| **Frontend UI** | React 18 / Vite / Tailwind | `http://localhost:5173` |

### 2. Test in the Frontend

1. Open your browser and navigate to [http://localhost:5173](http://localhost:5173).
2. Log in with your user account (or register a new user).
3. On the **User Dashboard**, click the **"Batch Upload (20-30 images)"** toggle button.
4. Click the upload zone and select all 20–30 images from `ml-service/sample_test_images/` (use `Ctrl + A` or `Cmd + A`).
5. Click **"Identify Plants"**.
6. The frontend sends a multipart request to FastAPI's batch endpoint: `POST /api/predict/batch`.
7. Each image is processed through the ML service, stored in `backend-python/uploads/`, enriched with disease status and pesticide recommendations, and logged to MongoDB.
8. View the batch prediction results grid displaying plant species, health condition, confidence score, and treatment advice.

---

## 📁 Recommended Folder Layout

```
ml-service/
  └── sample_test_images/
      ├── test_leaf_01.jpg
      ├── test_leaf_02.jpg
      ├── test_leaf_03.jpg
      ...
      └── test_leaf_30.jpg
```

---

## 💡 Image Best Practices

- **Formats**: `.jpg`, `.jpeg`, `.png`
- **Max File Size**: Up to 10MB per image (validated by FastAPI backend)
- **Lighting**: Clear, evenly lit leaf photos yield the highest prediction confidence
- **Batch Limit**: The UI accepts up to 30 images per batch run
