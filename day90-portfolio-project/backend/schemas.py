"""
Pydantic schemas for Portfolio Project
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Project schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Skill schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    level: int = 3
    icon: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None
    icon: Optional[str] = None

class SkillResponse(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Experience schemas
class ExperienceBase(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    is_current: bool = False

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    is_current: Optional[bool] = None

class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
