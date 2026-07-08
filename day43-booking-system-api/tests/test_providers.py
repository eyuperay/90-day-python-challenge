import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_list_providers_public(client: AsyncClient, test_provider):
    resp = await client.get("/providers/")
    assert resp.status_code == 200
    assert any(p["id"] == test_provider.id for p in resp.json())


async def test_get_provider(client: AsyncClient, test_provider):
    resp = await client.get(f"/providers/{test_provider.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["bio"] == "Certified massage therapist with 5 years experience."
    assert data["user"]["role"] == "provider"


async def test_get_provider_not_found(client: AsyncClient):
    resp = await client.get("/providers/99999")
    assert resp.status_code == 404


async def test_create_provider_as_admin(client: AsyncClient, admin_token: str, admin_user):
    # Admin user can have a provider profile
    resp = await client.post(
        "/providers/",
        json={"user_id": admin_user.id, "bio": "Admin who also provides"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["user_id"] == admin_user.id


async def test_create_provider_duplicate_raises_conflict(
    client: AsyncClient, admin_token: str, test_provider, provider_user
):
    resp = await client.post(
        "/providers/",
        json={"user_id": provider_user.id},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 409


async def test_add_service_to_provider(
    client: AsyncClient, provider_token: str, test_provider, test_service
):
    resp = await client.post(
        f"/providers/{test_provider.id}/services",
        json={"service_id": test_service.id, "price_override": 90.0},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 201
    assert float(resp.json()["price_override"]) == 90.0


async def test_add_duplicate_service_to_provider(
    client: AsyncClient, provider_token: str, provider_with_service
):
    provider, ps = provider_with_service
    resp = await client.post(
        f"/providers/{provider.id}/services",
        json={"service_id": ps.service_id},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 409


async def test_list_provider_services(client: AsyncClient, provider_with_service):
    provider, ps = provider_with_service
    resp = await client.get(f"/providers/{provider.id}/services")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    # Check effective values are present
    item = resp.json()[0]
    assert "effective_price" in item
    assert "effective_duration_minutes" in item


async def test_update_provider_profile(
    client: AsyncClient, provider_token: str, test_provider
):
    resp = await client.patch(
        f"/providers/{test_provider.id}",
        json={"bio": "Updated bio", "years_of_experience": 8},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["bio"] == "Updated bio"
    assert resp.json()["years_of_experience"] == 8


async def test_get_available_slots(client: AsyncClient, provider_with_availability, test_service):
    from datetime import date, timedelta
    provider = provider_with_availability
    # Find next Monday
    today = date.today()
    days_ahead = (0 - today.weekday()) % 7 or 7
    next_monday = today + timedelta(days=days_ahead)

    resp = await client.get(
        f"/providers/{provider.id}/slots",
        params={"service_id": test_service.id, "target_date": str(next_monday)},
    )
    assert resp.status_code == 200
    slots = resp.json()
    # Should have 8 slots: 09:00–17:00, 60-min duration
    assert len(slots) == 8
    for slot in slots:
        assert slot["provider_id"] == provider.id
        assert slot["service_id"] == test_service.id
        assert slot["duration_minutes"] == 60


async def test_no_slots_on_weekend(client: AsyncClient, provider_with_availability, test_service):
    from datetime import date, timedelta
    today = date.today()
    days_ahead = (5 - today.weekday()) % 7 or 7
    next_saturday = today + timedelta(days=days_ahead)

    resp = await client.get(
        f"/providers/{provider_with_availability.id}/slots",
        params={"service_id": test_service.id, "target_date": str(next_saturday)},
    )
    assert resp.status_code == 200
    assert resp.json() == []


async def test_slots_past_date_rejected(client: AsyncClient, provider_with_availability, test_service):
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    resp = await client.get(
        f"/providers/{provider_with_availability.id}/slots",
        params={"service_id": test_service.id, "target_date": str(yesterday)},
    )
    assert resp.status_code == 422


async def test_provider_cannot_modify_another_providers_data(
    client: AsyncClient,
    provider_token: str,
    db,
):
    """Provider A must NOT be able to update Provider B's profile or add services to B."""
    from app.core.security import create_access_token, get_password_hash
    from app.models.user import User, UserRole
    from app.models.provider import Provider

    # Create a second provider user + profile
    user_b = User(
        email="provider_b@test.com",
        full_name="Provider B",
        hashed_password=get_password_hash("password123"),
        role=UserRole.provider,
    )
    db.add(user_b)
    await db.flush()

    provider_b = Provider(user_id=user_b.id, bio="Second provider")
    db.add(provider_b)
    await db.flush()

    # Provider A tries to update Provider B's profile — must be 403
    resp = await client.patch(
        f"/providers/{provider_b.id}",
        json={"bio": "Hijacked bio by provider A"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 403


async def test_provider_cannot_set_another_providers_availability(
    client: AsyncClient,
    provider_token: str,
    db,
):
    """Provider A must NOT be able to set availability for Provider B."""
    from app.core.security import get_password_hash
    from app.models.user import User, UserRole
    from app.models.provider import Provider

    user_b = User(
        email="provider_b_avail@test.com",
        full_name="Provider B Avail",
        hashed_password=get_password_hash("password123"),
        role=UserRole.provider,
    )
    db.add(user_b)
    await db.flush()
    provider_b = Provider(user_id=user_b.id, bio="Another provider")
    db.add(provider_b)
    await db.flush()

    resp = await client.post(
        f"/providers/{provider_b.id}/availability",
        json={"day_of_week": 0, "start_time": "09:00:00", "end_time": "17:00:00"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 403
