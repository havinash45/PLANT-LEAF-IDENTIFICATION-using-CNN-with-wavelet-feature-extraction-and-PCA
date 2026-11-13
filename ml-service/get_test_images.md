# Sample Plant Leaf Images - Testing Guide

## Quick Options to Get 20-30 Test Images

### Option 1: Download from Public Datasets (Recommended)

#### PlantVillage Dataset
1. Go to: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
2. Download the dataset
3. Extract leaf images from different plant folders
4. Copy 20-30 images to `sample_test_images/` folder

#### Flavia Dataset
1. Search for "Flavia leaf dataset" online
2. Download sample images
3. Use 20-30 different plant species

### Option 2: Use Free Stock Photos

#### Unsplash
- Visit: https://unsplash.com/s/photos/plant-leaf
- Download 20-30 different leaf images
- Save them with names like: `leaf_01.jpg`, `leaf_02.jpg`, etc.

#### Pexels
- Visit: https://www.pexels.com/search/leaf/
- Download various plant leaf photos

### Option 3: Use Your Own Photos

1. Take photos of different plant leaves (20-30 different plants)
2. Save them in a folder
3. Use for testing

### Option 4: Generate Placeholder Images (For UI Testing)

If you just need to test the UI without actual predictions:

```python
# create_placeholders.py
from PIL import Image, ImageDraw
import os

os.makedirs("sample_test_images", exist_ok=True)

for i in range(1, 31):
    img = Image.new('RGB', (400, 400), color=(34, 125, 50))  # Green background
    draw = ImageDraw.Draw(img)
    draw.text((150, 180), f"Leaf {i}", fill=(255, 255, 255))
    img.save(f"sample_test_images/leaf_{i:02d}.jpg")
    print(f"Created leaf_{i:02d}.jpg")

print("✓ Created 30 placeholder images!")
```

## Recommended Folder Structure

```
ml-service/
  └── sample_test_images/
      ├── leaf_01.jpg
      ├── leaf_02.jpg
      ├── leaf_03.jpg
      ...
      └── leaf_30.jpg
```

## Using the Images

1. Copy images to `sample_test_images/` folder
2. Open frontend dashboard
3. Click "Batch Upload (20-30 images)"
4. Select all images from the folder
5. Click "Identify Plants"
6. View results!

## Image Requirements

- Format: JPG, PNG, JPEG
- Size: Max 10MB per image
- Content: Plant leaf images (clear, well-lit)
- Count: 20-30 images for batch testing

## Quick Test Script

Save this as `create_test_images.py`:

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_images(count=30):
    folder = "sample_test_images"
    os.makedirs(folder, exist_ok=True)
    
    for i in range(1, count + 1):
        # Create a simple green leaf-like shape
        img = Image.new('RGB', (400, 400), color=(240, 248, 240))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple leaf shape
        draw.ellipse([50, 50, 350, 350], fill=(34, 125, 50), outline=(27, 94, 32), width=3)
        draw.text((150, 180), f"Test {i}", fill=(255, 255, 255))
        
        filename = os.path.join(folder, f"test_leaf_{i:02d}.jpg")
        img.save(filename)
        print(f"Created {filename}")
    
    print(f"\n✓ Created {count} test images in {folder}/")

if __name__ == "__main__":
    create_test_images(30)
```

Run: `python create_test_images.py`


