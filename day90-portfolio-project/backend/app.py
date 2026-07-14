#!/usr/bin/env python3
"""
Portfolio Project - Main Application
Combines everything learned in 90 days
"""

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os

from backend.database import engine, get_db, Base
from backend import models, schemas, crud

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio API",
    description="Portfolio project combining 90 days of learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROOT ENDPOINT ====================

@app.get("/")
async def root():
    return {
        "message": "Welcome to Portfolio API",
        "version": "1.0.0",
        "endpoints": {
            "projects": "/projects",
            "skills": "/skills",
            "experiences": "/experiences",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# ==================== PROJECT ENDPOINTS ====================

@app.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)

@app.get("/projects", response_model=List[schemas.ProjectResponse])
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return crud.get_projects(db, skip=skip, limit=limit)

@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = crud.update_project(db, project_id, project_update)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    if not crud.delete_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")

# ==================== SKILL ENDPOINTS ====================

@app.post("/skills", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    return crud.create_skill(db, skill)

@app.get("/skills", response_model=List[schemas.SkillResponse])
async def list_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return crud.get_skills(db, skip=skip, limit=limit)

@app.get("/skills/{skill_id}", response_model=schemas.SkillResponse)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = crud.get_skill(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.put("/skills/{skill_id}", response_model=schemas.SkillResponse)
async def update_skill(
    skill_id: int,
    skill_update: schemas.SkillUpdate,
    db: Session = Depends(get_db)
):
    skill = crud.update_skill(db, skill_id, skill_update)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    if not crud.delete_skill(db, skill_id):
        raise HTTPException(status_code=404, detail="Skill not found")

# ==================== EXPERIENCE ENDPOINTS ====================

@app.post("/experiences", response_model=schemas.ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    return crud.create_experience(db, experience)

@app.get("/experiences", response_model=List[schemas.ExperienceResponse])
async def list_experiences(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return crud.get_experiences(db, skip=skip, limit=limit)

@app.get("/experiences/{experience_id}", response_model=schemas.ExperienceResponse)
async def get_experience(experience_id: int, db: Session = Depends(get_db)):
    experience = crud.get_experience(db, experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@app.put("/experiences/{experience_id}", response_model=schemas.ExperienceResponse)
async def update_experience(
    experience_id: int,
    experience_update: schemas.ExperienceUpdate,
    db: Session = Depends(get_db)
):
    experience = crud.update_experience(db, experience_id, experience_update)
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@app.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    if not crud.delete_experience(db, experience_id):
        raise HTTPException(status_code=404, detail="Experience not found")

# ==================== HEALTH ENDPOINT ====================

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Portfolio API is running"}

# ==================== STATS ENDPOINT ====================

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    return {
        "total_projects": db.query(models.Project).count(),
        "total_skills": db.query(models.Skill).count(),
        "total_experiences": db.query(models.Experience).count()
    }

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
