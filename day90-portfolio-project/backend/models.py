"""
Database models for Portfolio Project
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from datetime import datetime
from backend.database import Base

class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    tech_stack = Column(String(200))
    github_url = Column(String(200))
    live_url = Column(String(200))
    image_url = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Skill(Base):
    """Skill model"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50))
    level = Column(Integer, default=3)  # 1-5
    icon = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Experience(Base):
    """Experience model"""
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(String(20))
    end_date = Column(String(20))
    description = Column(Text)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
