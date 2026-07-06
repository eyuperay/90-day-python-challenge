import pytest
from fastapi.testclient import TestClient

def test_get_customers_unauthorized(client: TestClient):
    response = client.get("/api/v1/customers/")
    assert response.status_code == 401

def test_get_customers_with_auth(client: TestClient, auth_token):
    response = client.get(
        "/api/v1/customers/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_customer(client: TestClient, auth_token):
    response = client.post(
        "/api/v1/customers/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "company": "Test Corp",
            "position": "Developer"
        }
    )
    assert response.status_code in [200, 201]