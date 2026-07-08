import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_list_services_public(client: AsyncClient, test_service):
    resp = await client.get("/services/")
    assert resp.status_code == 200
    assert any(s["name"] == "Deep Tissue Massage" for s in resp.json())


async def test_get_service_by_id(client: AsyncClient, test_service):
    resp = await client.get(f"/services/{test_service.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Deep Tissue Massage"
    assert resp.json()["duration_minutes"] == 60


async def test_get_service_not_found(client: AsyncClient):
    resp = await client.get("/services/99999")
    assert resp.status_code == 404


async def test_create_service_as_admin(client: AsyncClient, admin_token: str):
    resp = await client.post(
        "/services/",
        json={
            "name": "Swedish Massage",
            "category": "massage",
            "duration_minutes": 45,
            "base_price": 60.0,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Swedish Massage"


async def test_create_service_as_customer_forbidden(client: AsyncClient, customer_token: str):
    resp = await client.post(
        "/services/",
        json={"name": "Hair Cut", "category": "haircare", "duration_minutes": 30, "base_price": 25.0},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 403


async def test_create_service_duplicate_name(client: AsyncClient, admin_token: str, test_service):
    resp = await client.post(
        "/services/",
        json={
            "name": "Deep Tissue Massage",  # already exists
            "category": "massage",
            "duration_minutes": 60,
            "base_price": 80.0,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 409


async def test_update_service(client: AsyncClient, admin_token: str, test_service):
    resp = await client.patch(
        f"/services/{test_service.id}",
        json={"base_price": 95.0, "duration_minutes": 75},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["base_price"] == 95.0
    assert data["duration_minutes"] == 75


async def test_deactivate_service(client: AsyncClient, admin_token: str, test_service):
    resp = await client.patch(
        f"/services/{test_service.id}",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False

    # Should not appear in active-only list
    list_resp = await client.get("/services/?active_only=true")
    assert not any(s["id"] == test_service.id for s in list_resp.json())


async def test_delete_service(client: AsyncClient, admin_token: str):
    # Create then delete
    create = await client.post(
        "/services/",
        json={"name": "Temp Service", "category": "other", "duration_minutes": 30, "base_price": 10.0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    service_id = create.json()["id"]
    resp = await client.delete(
        f"/services/{service_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 204

    get_resp = await client.get(f"/services/{service_id}")
    assert get_resp.status_code == 404
