import pytest
from fastapi.testclient import TestClient

def test_get_tasks_unauthorized(client: TestClient):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401

def test_get_tasks_with_auth(client: TestClient, auth_token):
    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)