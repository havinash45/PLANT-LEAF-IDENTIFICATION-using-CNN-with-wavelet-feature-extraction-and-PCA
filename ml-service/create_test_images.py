"""
Quick script to create 30 placeholder test images for batch upload testing.
These are simple colored images that you can use to test the UI.
"""

from PIL import Image, ImageDraw
import os

def create_test_images(count=30):
    """Create placeholder test images."""
    folder = "sample_test_images"
    os.makedirs(folder, exist_ok=True)
    
    # Different colors for variety
    colors = [
        (34, 125, 50),   # Green
        (76, 175, 80),    # Light Green
        (27, 94, 32),     # Dark Green
        (129, 199, 132),  # Pale Green
        (56, 142, 60),    # Medium Green
    ]
    
    print(f"Creating {count} test images...")
    print("=" * 50)
    
    for i in range(1, count + 1):
        # Create image with leaf-like color
        color = colors[i % len(colors)]
        img = Image.new('RGB', (400, 400), color=color)
        draw = ImageDraw.Draw(img)
        
        # Draw a simple leaf shape (ellipse)
        draw.ellipse([50, 50, 350, 350], fill=color, outline=(27, 94, 32), width=5)
        
        # Add text
        try:
            # Try to use a nice font
            draw.text((150, 180), f"Leaf {i}", fill=(255, 255, 255))
        except:
            draw.text((150, 180), f"Leaf {i}", fill=(255, 255, 255))
        
        filename = os.path.join(folder, f"test_leaf_{i:02d}.jpg")
        img.save(filename, quality=85)
        print(f"✓ Created: {filename}")
    
    print("=" * 50)
    print(f"\n✅ Successfully created {count} test images in '{folder}/' folder!")
    print(f"\n📁 Location: {os.path.abspath(folder)}")
    print("\n💡 You can now:")
    print("   1. Open the frontend dashboard")
    print("   2. Click 'Batch Upload (20-30 images)'")
    print("   3. Select all images from this folder")
    print("   4. Test the batch upload feature!")
    print("\n⚠️  Note: These are placeholder images.")
    print("   For real predictions, use actual plant leaf photos.")

if __name__ == "__main__":
    create_test_images(30)


