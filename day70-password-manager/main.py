#!/usr/bin/env python3
"""
Day 70 - Password Manager (CLI)
Secure password manager with encryption
"""

import os
import sys
import getpass
from password_manager import PasswordManager
from password_utils import PasswordUtils


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def setup_master_password(pm: PasswordManager) -> bool:
    """Setup master password"""
    print_section("MASTER PASSWORD SETUP")
    
    print("This is the first time running the password manager.")
    print("Please create a master password to secure your passwords.\n")
    
    while True:
        master = getpass.getpass("Enter master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        
        if master != confirm:
            print("Passwords do not match. Try again.\n")
            continue
        
        strength = PasswordUtils.validate_password_strength(master)
        print(f"\nPassword Strength: {strength['strength']}")
        
        if not strength['is_strong']:
            print("\nWeak password detected!")
            for msg in strength['feedback']:
                print(f"  - {msg}")
            
            choice = input("\nContinue anyway? (y/N): ").strip().lower()
            if choice != 'y':
                continue
        
        pm.master_password = master
        pm.save_passwords()
        print("\n[OK] Master password created successfully!")
        return True


def login(pm: PasswordManager) -> bool:
    """Login with master password"""
    print_section("LOGIN")
    
    if not os.path.exists(pm.data_file):
        return setup_master_password(pm)
    
    attempts = 3
    while attempts > 0:
        master = getpass.getpass("Enter master password: ")
        
        if pm.load_passwords(master):
            print("[OK] Login successful!")
            return True
        else:
            attempts -= 1
            print(f"[ERROR] Invalid password. {attempts} attempts remaining.")
    
    print("[ERROR] Too many failed attempts. Exiting...")
    return False


def add_password(pm: PasswordManager):
    """Add a new password"""
    print_section("ADD PASSWORD")
    
    service = input("Service name: ").strip()
    if not service:
        print("Service name is required")
        return
    
    username = input("Username: ").strip()
    if not username:
        print("Username is required")
        return
    
    print("\nGenerate password? (y/N): ", end="")
    generate = input().strip().lower()
    
    if generate == 'y':
        length = input("Password length (default: 16): ").strip()
        try:
            length = int(length) if length else 16
        except:
            length = 16
        
        password = PasswordUtils.generate_password(length)
        print(f"Generated password: {password}")
        
        confirm = input("Use this password? (y/N): ").strip().lower()
        if confirm != 'y':
            password = getpass.getpass("Enter password: ")
    else:
        password = getpass.getpass("Enter password: ")
    
    strength = PasswordUtils.validate_password_strength(password)
    print(f"Password Strength: {strength['strength']}")
    if not strength['is_strong']:
        for msg in strength['feedback']:
            print(f"  - {msg}")
    
    notes = input("Notes (optional): ").strip()
    
    if pm.add_password(service, username, password, notes):
        print(f"[OK] Password for '{service}' added successfully!")
    else:
        print(f"[ERROR] Failed to add password for '{service}'")


def search_password(pm: PasswordManager):
    """Search passwords"""
    print_section("SEARCH PASSWORDS")
    
    query = input("Enter service name to search: ").strip()
    if not query:
        print("Please enter a search term")
        return
    
    results = pm.search(query)
    
    if not results:
        print(f"No results found for '{query}'")
        return
    
    print(f"\nFound {len(results)} results:\n")
    for entry in results:
        print(f"  Service : {entry['service']}")
        print(f"  Username: {entry['username']}")
        print(f"  Password: {entry['password']}")
        if entry.get('notes'):
            print(f"  Notes   : {entry['notes']}")
        print("-" * 40)


def update_password(pm: PasswordManager):
    """Update an existing password"""
    print_section("UPDATE PASSWORD")
    
    services = pm.list_services()
    if not services:
        print("No passwords saved yet.")
        return
    
    print("Services:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    try:
        choice = int(input("\nSelect service number: "))
        if 1 <= choice <= len(services):
            service = services[choice - 1]
            entry = pm.get_password(service)
            
            print(f"\nCurrent: {entry}")
            print("\nLeave blank to keep current value")
            
            username = input(f"Username (current: {entry['username']}): ").strip()
            password = getpass.getpass(f"Password (current: {entry['password']}): ").strip()
            notes = input(f"Notes (current: {entry.get('notes', '')}): ").strip()
            
            if pm.update_password(service, password or None, username or None, notes or None):
                print(f"[OK] Password for '{service}' updated successfully!")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")


def delete_password(pm: PasswordManager):
    """Delete a password"""
    print_section("DELETE PASSWORD")
    
    services = pm.list_services()
    if not services:
        print("No passwords saved yet.")
        return
    
    print("Services:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    try:
        choice = int(input("\nSelect service number to delete: "))
        if 1 <= choice <= len(services):
            service = services[choice - 1]
            confirm = input(f"Delete '{service}'? (y/N): ").strip().lower()
            
            if confirm == 'y':
                if pm.delete_password(service):
                    print(f"[OK] Password for '{service}' deleted successfully!")
            else:
                print("Cancelled")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")


def show_statistics(pm: PasswordManager):
    """Show password statistics"""
    print_section("STATISTICS")
    
    stats = pm.get_statistics()
    
    if stats['total'] == 0:
        print("No passwords saved yet.")
        return
    
    print(f"Total Passwords: {stats['total']}")
    print(f"Unique Services: {stats['unique_services']}")
    print(f"Strong Passwords: {stats['strong_passwords']}")
    print(f"Weak Passwords: {stats['weak_passwords']}")
    if stats['most_common_username']:
        print(f"Most Common Username: {stats['most_common_username']}")


def generate_password():
    """Generate a random password"""
    print_section("GENERATE PASSWORD")
    
    length = input("Password length (default: 16): ").strip()
    try:
        length = int(length) if length else 16
    except:
        length = 16
    
    use_uppercase = input("Include uppercase? (Y/n): ").strip().lower() != 'n'
    use_lowercase = input("Include lowercase? (Y/n): ").strip().lower() != 'n'
    use_digits = input("Include digits? (Y/n): ").strip().lower() != 'n'
    use_special = input("Include special characters? (Y/n): ").strip().lower() != 'n'
    
    password = PasswordUtils.generate_password(
        length, use_uppercase, use_lowercase, use_digits, use_special
    )
    
    print(f"\nGenerated Password: {password}")
    
    strength = PasswordUtils.validate_password_strength(password)
    print(f"Strength: {strength['strength']}")


def main():
    print("=" * 60)
    print("DAY 70 - PASSWORD MANAGER (CLI)")
    print("=" * 60 + "\n")
    
    pm = PasswordManager()
    
    if not login(pm):
        return
    
    while True:
        print("\n" + "="*60)
        print("PASSWORD MANAGER MENU")
        print("="*60)
        print("1. Add Password")
        print("2. Search Passwords (View Details)")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Show Statistics")
        print("6. Generate Password")
        print("7. Exit")
        print("="*60)
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            add_password(pm)
        elif choice == "2":
            search_password(pm)
        elif choice == "3":
            update_password(pm)
        elif choice == "4":
            delete_password(pm)
        elif choice == "5":
            show_statistics(pm)
        elif choice == "6":
            generate_password()
        elif choice == "7":
            print("\n[OK] Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter 1-7.")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
