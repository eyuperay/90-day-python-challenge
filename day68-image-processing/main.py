#!/usr/bin/env python3
"""
Day 68 - Image Processing
Demonstrates basic image processing operations
"""

import os
import sys
from image_processor import ImageProcessor


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def select_image():
    """Select image file"""
    print("\nAvailable images in 'input' folder:")
    
    if not os.path.exists("input"):
        os.makedirs("input", exist_ok=True)
        print("  (No images found. Please place images in 'input' folder)")
        return None
    
    images = [f for f in os.listdir("input") if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    
    if not images:
        print("  (No images found. Please place images in 'input' folder)")
        return None
    
    for i, img in enumerate(images, 1):
        print(f"  {i}. {img}")
    
    try:
        choice = int(input("\nSelect image number: "))
        if 1 <= choice <= len(images):
            return os.path.join("input", images[choice-1])
        else:
            print("Invalid choice")
            return None
    except ValueError:
        print("Invalid input")
        return None


def demo_basic_operations(processor: ImageProcessor):
    """Demonstrate basic operations"""
    print_section("1. BASIC OPERATIONS")
    
    print("\nPerforming basic operations on loaded image...")
    
    # Resize
    processor.resize_by_percent(50)
    processor.save_image("resized_50.jpg")
    
    # Rotate
    processor.rotate(45)
    processor.save_image("rotated_45.jpg")
    
    # Flip
    processor.flip('horizontal')
    processor.save_image("flipped_horizontal.jpg")


def demo_filter_operations(processor: ImageProcessor):
    """Demonstrate filter operations"""
    print_section("2. FILTER OPERATIONS")
    
    print("\nApplying filters...")
    
    # Blur
    processor.blur(3)
    processor.save_image("blurred.jpg")
    
    # Sharpen
    processor.sharpen()
    processor.save_image("sharpened.jpg")


def demo_color_operations(processor: ImageProcessor):
    """Demonstrate color operations"""
    print_section("3. COLOR OPERATIONS")
    
    print("\nAdjusting colors...")
    
    # Grayscale
    processor.convert_to_grayscale()
    processor.save_image("grayscale.jpg")
    
    # Brightness
    processor.adjust_brightness(1.5)
    processor.save_image("brightness_1.5.jpg")
    
    # Contrast
    processor.adjust_contrast(1.5)
    processor.save_image("contrast_1.5.jpg")
    
    # Saturation
    processor.adjust_saturation(1.5)
    processor.save_image("saturation_1.5.jpg")


def demo_watermark(processor: ImageProcessor):
    """Demonstrate watermark"""
    print_section("4. WATERMARK")
    
    print("\nAdding watermark...")
    
    watermark_text = input("Enter watermark text (default: Python): ").strip()
    if not watermark_text:
        watermark_text = "Python"
    
    processor.add_watermark(watermark_text)
    processor.save_image("watermarked.jpg")


def demo_thumbnail(processor: ImageProcessor):
    """Demonstrate thumbnail"""
    print_section("5. THUMBNAIL")
    
    print("\nCreating thumbnail...")
    
    size_input = input("Enter thumbnail size (width height, default: 200 200): ").strip()
    if size_input:
        try:
            w, h = map(int, size_input.split())
            size = (w, h)
        except:
            size = (200, 200)
    else:
        size = (200, 200)
    
    processor.create_thumbnail(size)
    processor.save_image("thumbnail.jpg")


def demo_image_info(processor: ImageProcessor):
    """Demonstrate image info"""
    print_section("6. IMAGE INFO")
    
    info = processor.get_info()
    print("\nImage Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")


def main():
    print("=" * 60)
    print("DAY 68 - IMAGE PROCESSING")
    print("=" * 60 + "\n")
    
    print("NOTE: Place an image in the 'input' folder first.")
    print("Supported formats: JPG, PNG, BMP, GIF\n")
    
    # Select image
    image_path = select_image()
    if not image_path:
        print("\n[ERROR] No image selected. Exiting...")
        return
    
    # Initialize processor
    processor = ImageProcessor()
    
    # Load image
    if not processor.load_image(image_path):
        return
    
    # Show info
    demo_image_info(processor)
    
    # Process image
    while True:
        print("\n" + "="*60)
        print("IMAGE PROCESSING MENU")
        print("="*60)
        print("1. Basic Operations (Resize, Rotate, Flip)")
        print("2. Filter Operations (Blur, Sharpen)")
        print("3. Color Operations (Grayscale, Brightness, Contrast, Saturation)")
        print("4. Add Watermark")
        print("5. Create Thumbnail")
        print("6. Show Image Info")
        print("7. Save Image")
        print("8. Exit")
        print("="*60)
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice == "1":
            demo_basic_operations(processor)
        elif choice == "2":
            demo_filter_operations(processor)
        elif choice == "3":
            demo_color_operations(processor)
        elif choice == "4":
            demo_watermark(processor)
        elif choice == "5":
            demo_thumbnail(processor)
        elif choice == "6":
            demo_image_info(processor)
        elif choice == "7":
            filename = input("Enter filename (default: processed.jpg): ").strip()
            if not filename:
                filename = "processed.jpg"
            processor.save_image(filename)
        elif choice == "8":
            print("\n[OK] Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for processed images")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
