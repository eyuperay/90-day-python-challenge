import pytest


@pytest.mark.anyio
async def test_register(client):
    payload = {
        "email": "test@example.com",
        "password": "test1234",
        "full_name": "Test User",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code in [200, 400]


@pytest.mark.anyio
async def test_login_invalid(client):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401