"""
Image Processor Module
Basic image processing operations using Pillow
"""

import os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from datetime import datetime
from typing import Tuple, Optional


class ImageProcessor:
    """Image processing operations"""
    
    def __init__(self):
        self.image = None
        self.filename = None
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_image(self, filepath: str) -> bool:
        """
        Load an image from file
        
        Args:
            filepath: Path to image file
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.image = Image.open(filepath)
            self.filename = os.path.basename(filepath)
            print(f"[OK] Loaded image: {filepath}")
            print(f"  Size: {self.image.size}")
            print(f"  Mode: {self.image.mode}")
            return True
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to load image: {e}")
            return False
    
    def save_image(self, filename: str = None, format: str = None) -> bool:
        """
        Save processed image
        
        Args:
            filename: Output filename (optional)
            format: Image format (optional)
        
        Returns:
            True if saved successfully, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        if filename is None:
            name, ext = os.path.splitext(self.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_processed_{timestamp}.jpg"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            self.image.save(filepath, format=format)
            print(f"[OK] Saved: {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save image: {e}")
            return False
    
    def resize(self, width: int, height: int) -> bool:
        """
        Resize image
        
        Args:
            width: New width
            height: New height
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            original_size = self.image.size
            self.image = self.image.resize((width, height))
            print(f"[OK] Resized: {original_size} -> {self.image.size}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to resize: {e}")
            return False
    
    def resize_by_percent(self, percent: int) -> bool:
        """
        Resize image by percentage
        
        Args:
            percent: Percentage to resize (e.g., 50 for half)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            width = int(self.image.width * percent / 100)
            height = int(self.image.height * percent / 100)
            return self.resize(width, height)
        except Exception as e:
            print(f"[ERROR] Failed to resize: {e}")
            return False
    
    def rotate(self, angle: float) -> bool:
        """
        Rotate image
        
        Args:
            angle: Rotation angle in degrees
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image = self.image.rotate(angle, expand=True)
            print(f"[OK] Rotated: {angle}°")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to rotate: {e}")
            return False
    
    def flip(self, direction: str = 'horizontal') -> bool:
        """
        Flip image
        
        Args:
            direction: 'horizontal' or 'vertical'
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            if direction.lower() == 'horizontal':
                self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                print("[OK] Flipped horizontally")
            elif direction.lower() == 'vertical':
                self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
                print("[OK] Flipped vertically")
            else:
                print(f"[ERROR] Invalid direction: {direction}")
                return False
            return True
        except Exception as e:
            print(f"[ERROR] Failed to flip: {e}")
            return False
    
    def crop(self, left: int, top: int, right: int, bottom: int) -> bool:
        """
        Crop image
        
        Args:
            left: Left coordinate
            top: Top coordinate
            right: Right coordinate
            bottom: Bottom coordinate
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image = self.image.crop((left, top, right, bottom))
            print(f"[OK] Cropped: ({left}, {top}, {right}, {bottom})")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to crop: {e}")
            return False
    
    def convert_to_grayscale(self) -> bool:
        """Convert image to grayscale"""
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image = self.image.convert('L')
            print("[OK] Converted to grayscale")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to convert: {e}")
            return False
    
    def blur(self, radius: int = 2) -> bool:
        """
        Apply blur filter
        
        Args:
            radius: Blur radius
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
            print(f"[OK] Applied blur: radius={radius}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to blur: {e}")
            return False
    
    def sharpen(self) -> bool:
        """Apply sharpen filter"""
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            print("[OK] Applied sharpen")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to sharpen: {e}")
            return False
    
    def adjust_brightness(self, factor: float) -> bool:
        """
        Adjust brightness
        
        Args:
            factor: Brightness factor (0.0 - 2.0)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)
            print(f"[OK] Adjusted brightness: {factor}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to adjust brightness: {e}")
            return False
    
    def adjust_contrast(self, factor: float) -> bool:
        """
        Adjust contrast
        
        Args:
            factor: Contrast factor (0.0 - 2.0)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(factor)
            print(f"[OK] Adjusted contrast: {factor}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to adjust contrast: {e}")
            return False
    
    def adjust_saturation(self, factor: float) -> bool:
        """
        Adjust saturation
        
        Args:
            factor: Saturation factor (0.0 - 2.0)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(factor)
            print(f"[OK] Adjusted saturation: {factor}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to adjust saturation: {e}")
            return False
    
    def adjust_sharpness(self, factor: float) -> bool:
        """
        Adjust sharpness
        
        Args:
            factor: Sharpness factor (0.0 - 2.0)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(factor)
            print(f"[OK] Adjusted sharpness: {factor}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to adjust sharpness: {e}")
            return False
    
    def add_watermark(self, text: str, position: str = 'bottom-right') -> bool:
        """
        Add text watermark
        
        Args:
            text: Watermark text
            position: Position (top-left, top-right, bottom-left, bottom-right, center)
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            # Create a copy for drawing
            img = self.image.copy()
            draw = ImageDraw.Draw(img)
            
            # Try to use a font
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            # Calculate text size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            margin = 20
            if position == 'top-left':
                x, y = margin, margin
            elif position == 'top-right':
                x = img.width - text_width - margin
                y = margin
            elif position == 'bottom-left':
                x = margin
                y = img.height - text_height - margin
            elif position == 'bottom-right':
                x = img.width - text_width - margin
                y = img.height - text_height - margin
            elif position == 'center':
                x = (img.width - text_width) / 2
                y = (img.height - text_height) / 2
            else:
                x = margin
                y = margin
            
            # Draw text
            draw.text((x, y), text, fill=(255, 255, 255, 128), font=font)
            draw.text((x+1, y+1), text, fill=(0, 0, 0, 128), font=font)
            
            self.image = img
            print(f"[OK] Added watermark: '{text}' at {position}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to add watermark: {e}")
            return False
    
    def get_info(self) -> dict:
        """Get image information"""
        if self.image is None:
            return {"error": "No image loaded"}
        
        return {
            "filename": self.filename,
            "size": self.image.size,
            "width": self.image.width,
            "height": self.image.height,
            "mode": self.image.mode,
            "format": self.image.format,
            "info": self.image.info
        }
    
    def create_thumbnail(self, size: Tuple[int, int] = (200, 200)) -> bool:
        """
        Create thumbnail
        
        Args:
            size: Thumbnail size
        
        Returns:
            True if successful, False otherwise
        """
        if self.image is None:
            print("[ERROR] No image loaded")
            return False
        
        try:
            self.image.thumbnail(size)
            print(f"[OK] Created thumbnail: {self.image.size}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to create thumbnail: {e}")
            return False
