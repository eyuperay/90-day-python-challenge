import pytest
from fastapi.testclient import TestClient

def test_get_inventory(client: TestClient):
    response = client.get("/api/v1/inventory")
    assert response.status_code == 401  # Unauthorized