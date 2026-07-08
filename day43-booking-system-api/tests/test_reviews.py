"""
Tests for review creation, access control, and provider rating aggregation.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus

pytestmark = pytest.mark.asyncio


async def test_create_review_success(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    # Must be completed first
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    resp = await client.post(
        "/reviews/",
        json={
            "booking_id": confirmed_booking.id,
            "rating": 5,
            "comment": "Absolutely wonderful session!",
        },
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["rating"] == 5
    assert data["comment"] == "Absolutely wonderful session!"


async def test_review_only_for_completed_booking(
    client: AsyncClient,
    customer_token: str,
    pending_booking: Booking,
):
    """Cannot review a pending booking."""
    resp = await client.post(
        "/reviews/",
        json={"booking_id": pending_booking.id, "rating": 4},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 422
    assert "completed" in resp.json()["detail"].lower()


async def test_review_only_own_booking(
    client: AsyncClient,
    admin_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    """Admin cannot review a booking they didn't make."""
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    resp = await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 3},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 403


async def test_duplicate_review_rejected(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    resp1 = await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 5},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp1.status_code == 201

    resp2 = await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 3},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp2.status_code == 409


async def test_review_rating_out_of_range(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    for bad_rating in [0, 6, -1]:
        resp = await client.post(
            "/reviews/",
            json={"booking_id": confirmed_booking.id, "rating": bad_rating},
            headers={"Authorization": f"Bearer {customer_token}"},
        )
        assert resp.status_code == 422, f"Expected 422 for rating={bad_rating}"


async def test_get_provider_reviews(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    test_provider,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 4, "comment": "Great!"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )

    resp = await client.get(f"/reviews/provider/{test_provider.id}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert resp.json()[0]["rating"] == 4


async def test_provider_rating_updated_after_review(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    test_provider,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 4},
        headers={"Authorization": f"Bearer {customer_token}"},
    )

    provider_resp = await client.get(f"/providers/{test_provider.id}")
    assert provider_resp.status_code == 200
    data = provider_resp.json()
    assert data["total_reviews"] >= 1
    assert data["average_rating"] > 0


async def test_delete_own_review(
    client: AsyncClient,
    customer_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    create = await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 2},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    review_id = create.json()["id"]

    del_resp = await client.delete(
        f"/reviews/{review_id}",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert del_resp.status_code == 204


async def test_delete_other_user_review_forbidden(
    client: AsyncClient,
    customer_token: str,
    provider_token: str,
    confirmed_booking: Booking,
    db: AsyncSession,
):
    confirmed_booking.status = BookingStatus.completed
    await db.flush()

    create = await client.post(
        "/reviews/",
        json={"booking_id": confirmed_booking.id, "rating": 5},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    review_id = create.json()["id"]

    del_resp = await client.delete(
        f"/reviews/{review_id}",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert del_resp.status_code == 403
