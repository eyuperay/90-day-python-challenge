"""
Configuration for Portfolio Project
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/portfolio.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///./data/portfolio.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/portfolio')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
