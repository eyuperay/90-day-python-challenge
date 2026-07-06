import pytest
from fastapi.testclient import TestClient

def test_get_leads_unauthorized(client: TestClient):
    response = client.get("/api/v1/leads/")
    assert response.status_code == 401

def test_get_leads_with_auth(client: TestClient, auth_token):
    response = client.get(
        "/api/v1/leads/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_lead(client: TestClient, auth_token):
    response = client.post(
        "/api/v1/leads/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "phone": "+9876543210",
            "company": "Lead Corp"
        }
    )
    assert response.status_code in [200, 201]