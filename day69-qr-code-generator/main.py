#!/usr/bin/env python3
"""
Day 69 - QR Code Generator
Demonstrates QR code generation
"""

import os
from qr_generator import QRGenerator


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_basic_qr(generator: QRGenerator):
    """Demonstrate basic QR code generation"""
    print_section("1. BASIC QR CODE")
    
    data = input("Enter data to encode (default: https://github.com): ").strip()
    if not data:
        data = "https://github.com"
    
    filename = input("Enter filename (default: basic_qr.png): ").strip()
    if not filename:
        filename = "basic_qr.png"
    
    generator.generate_basic_qr(data, filename)


def demo_colored_qr(generator: QRGenerator):
    """Demonstrate colored QR code generation"""
    print_section("2. COLORED QR CODE")
    
    data = input("Enter data to encode (default: https://github.com): ").strip()
    if not data:
        data = "https://github.com"
    
    fill_color = input("Enter fill color (default: #3498db): ").strip()
    if not fill_color:
        fill_color = "#3498db"
    
    back_color = input("Enter background color (default: white): ").strip()
    if not back_color:
        back_color = "white"
    
    filename = input("Enter filename (default: colored_qr.png): ").strip()
    if not filename:
        filename = "colored_qr.png"
    
    generator.generate_colored_qr(data, fill_color, back_color, filename)


def demo_styled_qr(generator: QRGenerator):
    """Demonstrate styled QR code generation"""
    print_section("3. STYLED QR CODE")
    
    data = input("Enter data to encode (default: https://github.com): ").strip()
    if not data:
        data = "https://github.com"
    
    filename = input("Enter filename (default: styled_qr.png): ").strip()
    if not filename:
        filename = "styled_qr.png"
    
    generator.generate_styled_qr(data, filename)


def demo_vcard_qr(generator: QRGenerator):
    """Demonstrate vCard QR code generation"""
    print_section("4. VCARD QR CODE")
    
    name = input("Enter full name: ").strip()
    if not name:
        name = "John Doe"
    
    phone = input("Enter phone number: ").strip()
    if not phone:
        phone = "+1234567890"
    
    email = input("Enter email address: ").strip()
    if not email:
        email = "john@example.com"
    
    company = input("Enter company (optional): ").strip()
    title = input("Enter job title (optional): ").strip()
    
    filename = input("Enter filename (default: vcard.png): ").strip()
    if not filename:
        filename = "vcard.png"
    
    generator.generate_vcard_qr(name, phone, email, company, title, filename)


def demo_wifi_qr(generator: QRGenerator):
    """Demonstrate WiFi QR code generation"""
    print_section("5. WIFI QR CODE")
    
    ssid = input("Enter WiFi SSID: ").strip()
    if not ssid:
        ssid = "MyWiFi"
    
    password = input("Enter WiFi password: ").strip()
    if not password:
        password = "password123"
    
    security = input("Enter security (WPA, WEP, nopass - default: WPA): ").strip()
    if not security:
        security = "WPA"
    
    filename = input("Enter filename (default: wifi.png): ").strip()
    if not filename:
        filename = "wifi.png"
    
    generator.generate_wifi_qr(ssid, password, security, filename)


def demo_url_qr(generator: QRGenerator):
    """Demonstrate URL QR code generation"""
    print_section("6. URL QR CODE")
    
    url = input("Enter URL (default: https://github.com): ").strip()
    if not url:
        url = "https://github.com"
    
    filename = input("Enter filename (default: url.png): ").strip()
    if not filename:
        filename = "url.png"
    
    generator.generate_url_qr(url, filename)


def demo_text_qr(generator: QRGenerator):
    """Demonstrate text QR code generation"""
    print_section("7. TEXT QR CODE")
    
    text = input("Enter text: ").strip()
    if not text:
        text = "Hello, World!"
    
    filename = input("Enter filename (default: text.png): ").strip()
    if not filename:
        filename = "text.png"
    
    generator.generate_text_qr(text, filename)


def demo_batch_qr(generator: QRGenerator):
    """Demonstrate batch QR code generation"""
    print_section("8. BATCH QR CODES")
    
    data_list = []
    print("Enter data for each QR code (type 'done' to finish):")
    
    i = 1
    while True:
        data = input(f"QR {i} data (or 'done'): ").strip()
        if data.lower() == 'done':
            break
        if data:
            name = input(f"Name for QR {i}: ").strip() or f"qr{i}"
            data_list.append((data, name))
            i += 1
    
    if data_list:
        prefix = input("Enter prefix for files (default: batch): ").strip()
        if not prefix:
            prefix = "batch"
        
        generator.generate_batch_qr(data_list, prefix)
        print(f"[OK] Generated {len(data_list)} QR codes")
    else:
        print("No data entered")


def demo_invoice_qr(generator: QRGenerator):
    """Demonstrate invoice QR code generation"""
    print_section("9. INVOICE QR CODE")
    
    invoice_data = {
        "invoice_number": "INV-001",
        "date": "2026-07-14",
        "customer": "John Doe",
        "amount": "1,000.00",
        "currency": "TRY",
        "items": [
            {"name": "Product 1", "quantity": 2, "price": 200},
            {"name": "Product 2", "quantity": 1, "price": 600}
        ]
    }
    
    print("\nInvoice Data:")
    import json
    print(json.dumps(invoice_data, indent=2))
    
    filename = input("\nEnter filename (default: invoice.png): ").strip()
    if not filename:
        filename = "invoice.png"
    
    generator.generate_invoice_qr(invoice_data, filename)


def main():
    print("=" * 60)
    print("DAY 69 - QR CODE GENERATOR")
    print("=" * 60 + "\n")
    
    generator = QRGenerator()
    
    while True:
        print("\n" + "="*60)
        print("QR CODE GENERATOR MENU")
        print("="*60)
        print("1. Basic QR Code")
        print("2. Colored QR Code")
        print("3. Styled QR Code")
        print("4. vCard QR Code (Contact)")
        print("5. WiFi QR Code")
        print("6. URL QR Code")
        print("7. Text QR Code")
        print("8. Batch QR Codes")
        print("9. Invoice QR Code")
        print("0. Exit")
        print("="*60)
        
        choice = input("Enter choice (0-9): ").strip()
        
        if choice == "1":
            demo_basic_qr(generator)
        elif choice == "2":
            demo_colored_qr(generator)
        elif choice == "3":
            demo_styled_qr(generator)
        elif choice == "4":
            demo_vcard_qr(generator)
        elif choice == "5":
            demo_wifi_qr(generator)
        elif choice == "6":
            demo_url_qr(generator)
        elif choice == "7":
            demo_text_qr(generator)
        elif choice == "8":
            demo_batch_qr(generator)
        elif choice == "9":
            demo_invoice_qr(generator)
        elif choice == "0":
            print("\n[OK] Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for QR codes")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
