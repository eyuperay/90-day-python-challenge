"""
QR Code Generator Module
Generates QR codes using qrcode library
"""

import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from datetime import datetime
from typing import Optional, Tuple
import json


class QRGenerator:
    """QR code generator"""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_basic_qr(self, data: str, filename: str = None, 
                          size: int = 10, border: int = 4) -> str:
        """
        Generate a basic QR code
        
        Args:
            data: Data to encode
            filename: Output filename (optional)
            size: QR code size (box_size)
            border: Border size
        
        Returns:
            Path to generated QR code
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_code_{timestamp}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
        
        print(f"[OK] QR code generated: {filepath}")
        print(f"  Data: {data[:50]}..." if len(data) > 50 else f"  Data: {data}")
        print(f"  Size: {img.size}")
        
        return filepath
    
    def generate_colored_qr(self, data: str, fill_color: str = "#3498db", 
                            back_color: str = "white", filename: str = None,
                            size: int = 10) -> str:
        """
        Generate a colored QR code
        
        Args:
            data: Data to encode
            fill_color: Fill color (hex or name)
            back_color: Background color (hex or name)
            filename: Output filename (optional)
            size: QR code size
        
        Returns:
            Path to generated QR code
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_colored_{timestamp}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create colored image
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filepath)
        
        print(f"[OK] Colored QR code generated: {filepath}")
        print(f"  Colors: {fill_color} / {back_color}")
        
        return filepath
    
    def generate_styled_qr(self, data: str, filename: str = None,
                           size: int = 10) -> str:
        """
        Generate a styled QR code with rounded modules
        
        Args:
            data: Data to encode
            filename: Output filename (optional)
            size: QR code size
        
        Returns:
            Path to generated QR code
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_styled_{timestamp}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create styled image
        img = StyledPilImage(
            qr,
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                back_color=(255, 255, 255),
                center_color=(52, 152, 219),
                edge_color=(46, 204, 113)
            )
        )
        img.save(filepath)
        
        print(f"[OK] Styled QR code generated: {filepath}")
        
        return filepath
    
    def generate_batch_qr(self, data_list: list, prefix: str = "qr") -> list:
        """
        Generate multiple QR codes
        
        Args:
            data_list: List of (data, filename) tuples
            prefix: Prefix for filenames
        
        Returns:
            List of generated file paths
        """
        files = []
        for i, (data, name) in enumerate(data_list):
            filename = f"{prefix}_{i+1}_{name}.png"
            filepath = self.generate_basic_qr(data, filename)
            files.append(filepath)
        
        print(f"[OK] Generated {len(files)} QR codes")
        return files
    
    def generate_vcard_qr(self, name: str, phone: str, email: str,
                          company: str = None, title: str = None,
                          filename: str = None) -> str:
        """
        Generate QR code for vCard contact
        
        Args:
            name: Full name
            phone: Phone number
            email: Email address
            company: Company name (optional)
            title: Job title (optional)
            filename: Output filename (optional)
        
        Returns:
            Path to generated QR code
        """
        # Create vCard format
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}"""
        
        if company:
            vcard += f"\nORG:{company}"
        if title:
            vcard += f"\nTITLE:{title}"
        
        vcard += "\nEND:VCARD"
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vcard_{timestamp}.png"
        
        return self.generate_basic_qr(vcard, filename)
    
    def generate_wifi_qr(self, ssid: str, password: str, 
                         security: str = "WPA", filename: str = None) -> str:
        """
        Generate QR code for WiFi connection
        
        Args:
            ssid: WiFi network name
            password: WiFi password
            security: Security type (WPA, WEP, nopass)
            filename: Output filename (optional)
        
        Returns:
            Path to generated QR code
        """
        wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};;"
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wifi_{timestamp}.png"
        
        return self.generate_basic_qr(wifi_data, filename)
    
    def generate_url_qr(self, url: str, filename: str = None) -> str:
        """
        Generate QR code for URL
        
        Args:
            url: URL to encode
            filename: Output filename (optional)
        
        Returns:
            Path to generated QR code
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"url_{timestamp}.png"
        
        return self.generate_basic_qr(url, filename)
    
    def generate_text_qr(self, text: str, filename: str = None) -> str:
        """
        Generate QR code for text
        
        Args:
            text: Text to encode
            filename: Output filename (optional)
        
        Returns:
            Path to generated QR code
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"text_{timestamp}.png"
        
        return self.generate_basic_qr(text, filename)
    
    def get_qr_info(self, filepath: str) -> dict:
        """
        Get information about a QR code image
        
        Args:
            filepath: Path to QR code image
        
        Returns:
            Dictionary with image information
        """
        try:
            from PIL import Image
            img = Image.open(filepath)
            
            return {
                "filepath": filepath,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_invoice_qr(self, invoice_data: dict, filename: str = None) -> str:
        """
        Generate QR code for invoice data
        
        Args:
            invoice_data: Dictionary with invoice data
            filename: Output filename (optional)
        
        Returns:
            Path to generated QR code
        """
        invoice_json = json.dumps(invoice_data, indent=2)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"invoice_{timestamp}.png"
        
        return self.generate_basic_qr(invoice_json, filename)
