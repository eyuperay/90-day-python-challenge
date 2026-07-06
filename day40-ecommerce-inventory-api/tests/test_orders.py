import pytest
from fastapi.testclient import TestClient

def test_get_orders(client: TestClient):
    response = client.get("/api/v1/orders")
    assert response.status_code == 401  # Unauthorized

def test_create_order_unauthorized(client: TestClient):
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "shipping_address": "123 Test St",
            "items": []
        }
    )
    assert response.status_code == 401