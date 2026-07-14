"""
Password Utilities Module
Password generation, hashing, and validation functions
"""

import hashlib
import secrets
import string
import re
from typing import Tuple, Optional


class PasswordUtils:
    """Password utilities for generation and validation"""
    
    @staticmethod
    def generate_password(length: int = 16, 
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True) -> str:
        """Generate a secure random password"""
        characters = ""
        
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not characters:
            raise ValueError("At least one character type must be selected")
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
        """Hash a password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        salted = password + salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()
        
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify a password against hash and salt"""
        test_hash, _ = PasswordUtils.hash_password(password, salt)
        return test_hash == hashed
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Validate password strength"""
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Password should contain at least one uppercase letter")
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Password should contain at least one lowercase letter")
        
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Password should contain at least one digit")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        else:
            feedback.append("Password should contain at least one special character")
        
        strength = {
            0: "Very Weak",
            1: "Weak",
            2: "Moderate",
            3: "Strong",
            4: "Very Strong",
            5: "Excellent"
        }
        
        return {
            "score": score,
            "strength": strength.get(score, "Unknown"),
            "feedback": feedback,
            "is_strong": score >= 3
        }
    
    @staticmethod
    def generate_master_password() -> str:
        """Generate a strong master password"""
        return PasswordUtils.generate_password(20, True, True, True, True)
    
    @staticmethod
    def generate_pin() -> str:
        """Generate a 4-6 digit PIN"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))
