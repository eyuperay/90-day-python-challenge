"""
Tests for provider availability and unavailability management.
"""
import pytest
from datetime import date, timedelta
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_availability(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    resp = await client.post(
        f"/providers/{test_provider.id}/availability",
        json={"day_of_week": 0, "start_time": "09:00:00", "end_time": "17:00:00"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["day_of_week"] == 0
    assert data["is_active"] is True


async def test_create_availability_end_before_start_rejected(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    resp = await client.post(
        f"/providers/{test_provider.id}/availability",
        json={"day_of_week": 1, "start_time": "17:00:00", "end_time": "09:00:00"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 422


async def test_create_duplicate_day_availability_rejected(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    payload = {"day_of_week": 2, "start_time": "08:00:00", "end_time": "16:00:00"}
    r1 = await client.post(
        f"/providers/{test_provider.id}/availability",
        json=payload,
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert r1.status_code == 201

    r2 = await client.post(
        f"/providers/{test_provider.id}/availability",
        json=payload,
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert r2.status_code == 409


async def test_get_provider_availability(
    client: AsyncClient,
    provider_with_availability,
):
    provider = provider_with_availability
    resp = await client.get(f"/providers/{provider.id}/availability")
    assert resp.status_code == 200
    days = [a["day_of_week"] for a in resp.json()]
    assert sorted(days) == [0, 1, 2, 3, 4]  # Mon–Fri


async def test_update_availability(
    client: AsyncClient,
    provider_token: str,
    provider_with_availability,
    db,
):
    provider = provider_with_availability
    avail_resp = await client.get(f"/providers/{provider.id}/availability")
    avail_id = avail_resp.json()[0]["id"]

    resp = await client.patch(
        f"/providers/{provider.id}/availability/{avail_id}",
        json={"start_time": "10:00:00", "end_time": "18:00:00"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["start_time"] == "10:00:00"


async def test_delete_availability(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    # Create then delete
    create = await client.post(
        f"/providers/{test_provider.id}/availability",
        json={"day_of_week": 6, "start_time": "10:00:00", "end_time": "14:00:00"},
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    avail_id = create.json()["id"]

    del_resp = await client.delete(
        f"/providers/{test_provider.id}/availability/{avail_id}",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert del_resp.status_code == 204


async def test_create_unavailability(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    today = date.today()
    start = today + timedelta(days=10)
    end = today + timedelta(days=14)
    resp = await client.post(
        f"/providers/{test_provider.id}/unavailability",
        json={
            "start_date": str(start),
            "end_date": str(end),
            "reason": "Annual leave",
        },
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["reason"] == "Annual leave"


async def test_unavailability_end_before_start_rejected(
    client: AsyncClient,
    provider_token: str,
    test_provider,
):
    today = date.today()
    resp = await client.post(
        f"/providers/{test_provider.id}/unavailability",
        json={
            "start_date": str(today + timedelta(days=5)),
            "end_date": str(today + timedelta(days=2)),
        },
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 422


async def test_slots_blocked_during_unavailability(
    client: AsyncClient,
    provider_with_availability,
    test_service,
    provider_token: str,
):
    """No slots returned on a day the provider has blocked."""
    provider = provider_with_availability
    # Find next Monday
    today = date.today()
    days_ahead = (0 - today.weekday()) % 7 or 7
    next_monday = today + timedelta(days=days_ahead)

    # Block the entire next week
    await client.post(
        f"/providers/{provider.id}/unavailability",
        json={
            "start_date": str(next_monday),
            "end_date": str(next_monday + timedelta(days=6)),
            "reason": "Holiday",
        },
        headers={"Authorization": f"Bearer {provider_token}"},
    )

    resp = await client.get(
        f"/providers/{provider.id}/slots",
        params={"service_id": test_service.id, "target_date": str(next_monday)},
    )
    assert resp.status_code == 200
    assert resp.json() == []
