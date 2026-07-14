"""
API tests for Portfolio Project
"""

import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to Portfolio API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_projects" in response.json()

def test_projects_list():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_skills_list():
    response = client.get("/skills")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_experiences_list():
    response = client.get("/experiences")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
