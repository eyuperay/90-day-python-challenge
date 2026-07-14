"""
CRUD operations for Portfolio Project
"""

from sqlalchemy.orm import Session
from backend import models, schemas

# Project CRUD
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    for key, value in project_update.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    db.delete(db_project)
    db.commit()
    return True

# Skill CRUD
def get_skill(db: Session, skill_id: int):
    return db.query(models.Skill).filter(models.Skill.id == skill_id).first()

def get_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Skill).offset(skip).limit(limit).all()

def create_skill(db: Session, skill: schemas.SkillCreate):
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def update_skill(db: Session, skill_id: int, skill_update: schemas.SkillUpdate):
    db_skill = get_skill(db, skill_id)
    if not db_skill:
        return None
    for key, value in skill_update.model_dump(exclude_unset=True).items():
        setattr(db_skill, key, value)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int):
    db_skill = get_skill(db, skill_id)
    if not db_skill:
        return False
    db.delete(db_skill)
    db.commit()
    return True

# Experience CRUD
def get_experience(db: Session, experience_id: int):
    return db.query(models.Experience).filter(models.Experience.id == experience_id).first()

def get_experiences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Experience).offset(skip).limit(limit).all()

def create_experience(db: Session, experience: schemas.ExperienceCreate):
    db_experience = models.Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

def update_experience(db: Session, experience_id: int, experience_update: schemas.ExperienceUpdate):
    db_experience = get_experience(db, experience_id)
    if not db_experience:
        return None
    for key, value in experience_update.model_dump(exclude_unset=True).items():
        setattr(db_experience, key, value)
    db.commit()
    db.refresh(db_experience)
    return db_experience

def delete_experience(db: Session, experience_id: int):
    db_experience = get_experience(db, experience_id)
    if not db_experience:
        return False
    db.delete(db_experience)
    db.commit()
    return True
