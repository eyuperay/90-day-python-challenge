import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient):
    resp = await client.post("/auth/register", json={
        "email": "newuser@test.com",
        "full_name": "New User",
        "password": "securepass",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "newuser@test.com"
    assert data["role"] == "customer"
    assert "hashed_password" not in data


async def test_register_duplicate_email(client: AsyncClient, customer_user):
    resp = await client.post("/auth/register", json={
        "email": "customer@test.com",
        "full_name": "Dup User",
        "password": "securepass",
    })
    assert resp.status_code == 409


async def test_register_short_password(client: AsyncClient):
    resp = await client.post("/auth/register", json={
        "email": "short@test.com",
        "full_name": "Short Pwd",
        "password": "123",
    })
    assert resp.status_code == 422


async def test_login_success(client: AsyncClient, customer_user):
    resp = await client.post("/auth/login", json={
        "email": "customer@test.com",
        "password": "password123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, customer_user):
    resp = await client.post("/auth/login", json={
        "email": "customer@test.com",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


async def test_login_unknown_email(client: AsyncClient):
    resp = await client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "password123",
    })
    assert resp.status_code == 401


async def test_refresh_token(client: AsyncClient, customer_user):
    login = await client.post("/auth/login", json={
        "email": "customer@test.com",
        "password": "password123",
    })
    refresh_token = login.json()["refresh_token"]
    resp = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_refresh_with_access_token_is_rejected(client: AsyncClient, customer_user):
    """Access tokens must not be accepted as refresh tokens."""
    login = await client.post("/auth/login", json={
        "email": "customer@test.com",
        "password": "password123",
    })
    access_token = login.json()["access_token"]
    resp = await client.post("/auth/refresh", json={"refresh_token": access_token})
    assert resp.status_code == 401


async def test_get_me(client: AsyncClient, customer_token: str):
    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {customer_token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "customer@test.com"


async def test_get_me_unauthenticated(client: AsyncClient):
    resp = await client.get("/auth/me")
    assert resp.status_code == 403


async def test_change_password(client: AsyncClient, customer_token: str):
    resp = await client.post(
        "/auth/change-password",
        json={"current_password": "password123", "new_password": "newpassword456"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 204


async def test_change_password_wrong_current(client: AsyncClient, customer_token: str):
    resp = await client.post(
        "/auth/change-password",
        json={"current_password": "wrongcurrent", "new_password": "newpassword456"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 400
