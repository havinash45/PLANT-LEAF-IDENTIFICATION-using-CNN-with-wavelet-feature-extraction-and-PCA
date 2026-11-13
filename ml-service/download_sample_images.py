"""
Script to download sample plant leaf images for testing.
Downloads images from public sources for testing the batch upload feature.
"""

import os
import requests
from urllib.parse import urlparse
import time

# Sample plant leaf image URLs (you can replace these with actual plant leaf images)
# These are placeholder URLs - you'll need to replace with actual image URLs
SAMPLE_IMAGES = [
    # You can add actual image URLs here
    # Example format:
    # "https://example.com/plant1.jpg",
    # "https://example.com/plant2.jpg",
]

def download_image(url, save_path):
    """Download an image from URL and save it."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ Downloaded: {save_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def create_sample_images_folder():
    """Create a folder for sample images."""
    folder = "sample_test_images"
    os.makedirs(folder, exist_ok=True)
    return folder

def main():
    print("=" * 50)
    print("Sample Plant Leaf Images Downloader")
    print("=" * 50)
    print("\nThis script helps you get sample images for testing.")
    print("\nOptions:")
    print("1. Download from PlantVillage dataset")
    print("2. Use local images from a folder")
    print("3. Generate placeholder images")
    print("\nFor best results, use actual plant leaf images from:")
    print("- PlantVillage dataset: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")
    print("- Flavia dataset")
    print("- Your own collection")
    print("\n" + "=" * 50)
    
    folder = create_sample_images_folder()
    
    if len(SAMPLE_IMAGES) > 0:
        print(f"\nDownloading {len(SAMPLE_IMAGES)} images to {folder}/...")
        for i, url in enumerate(SAMPLE_IMAGES, 1):
            filename = f"plant_{i:02d}.jpg"
            save_path = os.path.join(folder, filename)
            download_image(url, save_path)
            time.sleep(0.5)  # Be nice to servers
    else:
        print("\n⚠ No image URLs configured.")
        print("\nTo use this script:")
        print("1. Add image URLs to SAMPLE_IMAGES list")
        print("2. Or manually copy 20-30 plant leaf images to 'sample_test_images' folder")
        print("\nYou can find free plant images at:")
        print("- Unsplash: https://unsplash.com/s/photos/plant-leaf")
        print("- Pexels: https://www.pexels.com/search/leaf/")
        print("- Your own photos")
    
    print(f"\n✓ Sample images folder created: {folder}/")
    print("\nYou can now use these images to test batch upload!")

if __name__ == "__main__":
    main()


