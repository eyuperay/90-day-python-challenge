"""
Password Manager Module
Stores and manages passwords securely
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from password_utils import PasswordUtils


class PasswordManager:
    """Secure password manager"""
    
    def __init__(self, key_file: str = "data/key.key", 
                 data_file: str = "data/passwords.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.key = None
        self.cipher = None
        self.passwords = []
        self.master_password = None
        
        os.makedirs("data", exist_ok=True)
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        """Load existing key or create new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
        
        self.cipher = Fernet(self.key)
    
    def _encrypt(self, data: str) -> bytes:
        """Encrypt data"""
        return self.cipher.encrypt(data.encode())
    
    def _decrypt(self, data: bytes) -> str:
        """Decrypt data"""
        return self.cipher.decrypt(data).decode()
    
    def load_passwords(self, master_password: str) -> bool:
        """Load passwords from file"""
        if not os.path.exists(self.data_file):
            self.passwords = []
            self.master_password = master_password
            return True
        
        try:
            with open(self.data_file, 'r') as f:
                encrypted_data = json.load(f)
            
            # Verify master password
            stored_hash = encrypted_data.get('master_hash')
            stored_salt = encrypted_data.get('master_salt')
            
            if not PasswordUtils.verify_password(master_password, stored_hash, stored_salt):
                return False
            
            # Decrypt passwords
            encrypted_passwords = encrypted_data.get('passwords', [])
            self.passwords = []
            
            for entry in encrypted_passwords:
                try:
                    decrypted = {
                        'service': self._decrypt(entry['service'].encode()),
                        'username': self._decrypt(entry['username'].encode()),
                        'password': self._decrypt(entry['password'].encode()),
                        'notes': self._decrypt(entry['notes'].encode()) if entry.get('notes') else '',
                        'created_at': entry.get('created_at', datetime.now().isoformat()),
                        'updated_at': entry.get('updated_at', datetime.now().isoformat())
                    }
                    self.passwords.append(decrypted)
                except Exception as e:
                    print(f"Error decrypting entry: {e}")
                    continue
            
            self.master_password = master_password
            print(f"[DEBUG] Loaded {len(self.passwords)} passwords")
            return True
            
        except Exception as e:
            print(f"Error loading passwords: {e}")
            return False
    
    def save_passwords(self) -> bool:
        """Save passwords to file"""
        try:
            # Hash master password
            hashed, salt = PasswordUtils.hash_password(self.master_password)
            
            # Encrypt passwords
            encrypted_passwords = []
            for entry in self.passwords:
                encrypted = {
                    'service': self._encrypt(entry['service']).decode(),
                    'username': self._encrypt(entry['username']).decode(),
                    'password': self._encrypt(entry['password']).decode(),
                    'notes': self._encrypt(entry.get('notes', '')).decode(),
                    'created_at': entry.get('created_at', datetime.now().isoformat()),
                    'updated_at': datetime.now().isoformat()
                }
                encrypted_passwords.append(encrypted)
            
            data = {
                'master_hash': hashed,
                'master_salt': salt,
                'passwords': encrypted_passwords,
                'updated_at': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving passwords: {e}")
            return False
    
    def add_password(self, service: str, username: str, password: str, 
                     notes: str = "") -> bool:
        """Add a new password entry"""
        for entry in self.passwords:
            if entry['service'].lower() == service.lower():
                print(f"Service '{service}' already exists")
                return False
        
        entry = {
            'service': service,
            'username': username,
            'password': password,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.passwords.append(entry)
        print(f"[DEBUG] Added password for {service}")
        return self.save_passwords()
    
    def get_password(self, service: str) -> Optional[Dict]:
        """Get password entry by service"""
        for entry in self.passwords:
            if entry['service'].lower() == service.lower():
                return entry
        return None
    
    def update_password(self, service: str, password: str = None, 
                        username: str = None, notes: str = None) -> bool:
        """Update a password entry"""
        for entry in self.passwords:
            if entry['service'].lower() == service.lower():
                if password:
                    entry['password'] = password
                if username:
                    entry['username'] = username
                if notes is not None:
                    entry['notes'] = notes
                entry['updated_at'] = datetime.now().isoformat()
                return self.save_passwords()
        return False
    
    def delete_password(self, service: str) -> bool:
        """Delete a password entry"""
        for i, entry in enumerate(self.passwords):
            if entry['service'].lower() == service.lower():
                del self.passwords[i]
                return self.save_passwords()
        return False
    
    def list_services(self) -> List[str]:
        """List all services"""
        return [entry['service'] for entry in self.passwords]
    
    def search(self, query: str) -> List[Dict]:
        """Search passwords by service or username"""
        query_lower = query.lower()
        results = []
        
        for entry in self.passwords:
            if (query_lower in entry['service'].lower() or 
                query_lower in entry['username'].lower()):
                results.append(entry)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get password statistics"""
        total = len(self.passwords)
        if total == 0:
            return {'total': 0}
        
        strong = 0
        weak = 0
        for entry in self.passwords:
            strength = PasswordUtils.validate_password_strength(entry['password'])
            if strength['is_strong']:
                strong += 1
            else:
                weak += 1
        
        username_count = {}
        for entry in self.passwords:
            username = entry['username']
            username_count[username] = username_count.get(username, 0) + 1
        
        return {
            'total': total,
            'strong_passwords': strong,
            'weak_passwords': weak,
            'unique_services': len(set(entry['service'] for entry in self.passwords)),
            'most_common_username': max(username_count.items(), key=lambda x: x[1])[0] if username_count else None
        }
