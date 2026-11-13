# ML Service - Nematode Genus Classification

Python Flask service for **plant-parasitic nematode genus identification** from microscopic images using a CNN (MobileNetV2 transfer learning).

## Dataset

The project uses the **Microscopic Image Dataset of Plant-Parasitic Nematodes** (11 genera):

- Genus Criconema, Criconemoides, Helicotylenchus, Hemicycliophora, Hirschmaniella  
- Genus Hoplolaimus, Meloidogyne, Pratylenchus, Radopholus, Trichodorus, Xiphinema  

Dataset folder: `Microscopic Image Dataset of Plant-Parasitic Nematodes/` (each subfolder = one genus, containing `.jpg` images).

## Setup

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
python app.py
```

The service runs on `http://localhost:5000`.

## Training a Model

1. Ensure the dataset folder **Microscopic Image Dataset of Plant-Parasitic Nematodes** is inside `ml-service/` (it contains subfolders like `Genus Criconema`, `Genus Meloidogyne`, etc., each with `.jpg` images).

2. Train the model (defaults use the nematode dataset):
```bash
python train_model.py
```

   Or with custom options:
```bash
python train_model.py --data_dir "Microscopic Image Dataset of Plant-Parasitic Nematodes" --epochs 50 --batch_size 32
```

3. The trained model is saved to `models/nematode_classifier.h5` and class names to `models/class_names.txt`.

## API Endpoints

- `GET /health` - Health check  
- `POST /predict` - Predict nematode genus from a microscopic image  

### Predict Request
```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@microscope_image.jpg"
```

### Predict Response
```json
{
  "plantName": "Genus Meloidogyne",
  "confidence": 0.92
}
```

(`plantName` holds the predicted **genus** label for backend compatibility.)