"""
Tests for booking lifecycle, state machine, conflict detection, and access control.
"""
import pytest
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


def _future_dt(days: int = 1, hour: int = 10) -> str:
    """Return an ISO-8601 UTC datetime string `days` weekdays from now."""
    dt = datetime.now(timezone.utc).replace(hour=hour, minute=0, second=0, microsecond=0)
    dt += timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    for _ in range(days - 1):
        dt += timedelta(days=1)
        while dt.weekday() >= 5:
            dt += timedelta(days=1)
    return dt.isoformat()


async def test_create_booking_success(
    client: AsyncClient,
    customer_token: str,
    provider_with_availability,
    test_service,
):
    provider = provider_with_availability
    resp = await client.post(
        "/bookings/",
        json={
            "provider_id": provider.id,
            "service_id": test_service.id,
            "start_datetime": _future_dt(2, 11),
            "notes": "Please use lavender oil.",
        },
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "pending"
    assert data["service_name_snapshot"] == "Deep Tissue Massage"
    assert data["duration_minutes"] == 60
    assert float(data["price"]) == 80.0


async def test_create_booking_past_datetime_rejected(
    client: AsyncClient,
    customer_token: str,
    provider_with_availability,
    test_service,
):
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    resp = await client.post(
        "/bookings/",
        json={
            "provider_id": provider_with_availability.id,
            "service_id": test_service.id,
            "start_datetime": past,
        },
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 422


async def test_create_booking_unauthenticated(
    client: AsyncClient,
    provider_with_availability,
    test_service,
):
    resp = await client.post(
        "/bookings/",
        json={
            "provider_id": provider_with_availability.id,
            "service_id": test_service.id,
            "start_datetime": _future_dt(3),
        },
    )
    assert resp.status_code == 403


async def test_get_my_bookings(client: AsyncClient, customer_token: str, pending_booking):
    resp = await client.get(
        "/bookings/my",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 200
    ids = [b["id"] for b in resp.json()]
    assert pending_booking.id in ids


async def test_confirm_booking_by_provider(
    client: AsyncClient,
    provider_token: str,
    pending_booking,
):
    resp = await client.patch(
        f"/bookings/{pending_booking.id}/confirm",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


async def test_confirm_booking_by_customer_forbidden(
    client: AsyncClient,
    customer_token: str,
    pending_booking,
):
    resp = await client.patch(
        f"/bookings/{pending_booking.id}/confirm",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 403


async def test_complete_booking(
    client: AsyncClient,
    provider_token: str,
    confirmed_booking,
):
    resp = await client.patch(
        f"/bookings/{confirmed_booking.id}/complete",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


async def test_complete_already_completed_rejected(
    client: AsyncClient,
    provider_token: str,
    confirmed_booking,
    db,
):
    # First complete it
    confirmed_booking.status = __import__("app.models.booking", fromlist=["BookingStatus"]).BookingStatus.completed
    await db.flush()
    resp = await client.patch(
        f"/bookings/{confirmed_booking.id}/complete",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 422
    assert "terminal" in resp.json()["detail"].lower() or "Cannot transition" in resp.json()["detail"]


async def test_cancel_pending_booking_by_customer(
    client: AsyncClient,
    customer_token: str,
    pending_booking,
):
    resp = await client.patch(
        f"/bookings/{pending_booking.id}/cancel",
        json={"reason": "Changed my mind about the appointment."},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "cancelled"
    assert data["cancelled_by"] == "customer"
    assert "Changed my mind" in data["cancellation_reason"]


async def test_cancel_cancelled_booking_rejected(
    client: AsyncClient,
    customer_token: str,
    pending_booking,
    db,
):
    from app.models.booking import BookingStatus
    pending_booking.status = BookingStatus.cancelled
    await db.flush()
    resp = await client.patch(
        f"/bookings/{pending_booking.id}/cancel",
        json={"reason": "Trying again."},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 422


async def test_no_show_by_provider(
    client: AsyncClient,
    provider_token: str,
    confirmed_booking,
):
    resp = await client.patch(
        f"/bookings/{confirmed_booking.id}/no-show",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "no_show"


async def test_no_show_from_pending_rejected(
    client: AsyncClient,
    provider_token: str,
    pending_booking,
):
    """pending → no_show is not a valid transition."""
    resp = await client.patch(
        f"/bookings/{pending_booking.id}/no-show",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert resp.status_code == 422


async def test_admin_can_list_all_bookings(
    client: AsyncClient,
    admin_token: str,
    pending_booking,
):
    resp = await client.get(
        "/bookings/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert any(b["id"] == pending_booking.id for b in resp.json())


async def test_customer_cannot_list_all_bookings(
    client: AsyncClient,
    customer_token: str,
):
    resp = await client.get(
        "/bookings/",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 403


async def test_other_customer_cannot_cancel_booking(
    client: AsyncClient,
    admin_token: str,
    provider_with_availability,
    test_service,
    db,
):
    """Customer B must NOT be able to cancel Customer A's booking."""
    from app.core.security import create_access_token, get_password_hash
    from app.models.user import User, UserRole

    # Create a second customer
    customer_b = User(
        email="customer_b@test.com",
        full_name="Customer B",
        hashed_password=get_password_hash("password123"),
        role=UserRole.customer,
    )
    db.add(customer_b)
    await db.flush()
    token_b = create_access_token({"sub": str(customer_b.id), "role": customer_b.role})

    # Customer A creates a booking (use admin for simplicity — they can also book)
    provider = provider_with_availability
    create = await client.post(
        "/bookings/",
        json={
            "provider_id": provider.id,
            "service_id": test_service.id,
            "start_datetime": _future_dt(5, 11),
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert create.status_code == 201
    booking_id = create.json()["id"]

    # Customer B tries to cancel Customer A's booking — must be 403
    resp = await client.patch(
        f"/bookings/{booking_id}/cancel",
        json={"reason": "I am sneakily cancelling someone else's booking."},
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert resp.status_code == 403


async def test_booking_outside_availability_window_rejected(
    client: AsyncClient,
    customer_token: str,
    provider_with_availability,
    test_service,
):
    """Booking at 03:00 UTC when provider only works 09:00–17:00 must be rejected."""
    dt = _future_dt(3, 3)  # 03:00 UTC — outside working hours
    resp = await client.post(
        "/bookings/",
        json={
            "provider_id": provider_with_availability.id,
            "service_id": test_service.id,
            "start_datetime": dt,
        },
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert resp.status_code == 422
    assert "availability" in resp.json()["detail"].lower() or "outside" in resp.json()["detail"].lower()


async def test_booking_state_machine_full_happy_path(
    client: AsyncClient,
    provider_token: str,
    customer_token: str,
    provider_with_availability,
    test_service,
):
    """pending → confirmed → completed full happy path."""
    # Create
    create = await client.post(
        "/bookings/",
        json={
            "provider_id": provider_with_availability.id,
            "service_id": test_service.id,
            "start_datetime": _future_dt(4, 14),
        },
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert create.status_code == 201
    booking_id = create.json()["id"]

    # Confirm
    confirm = await client.patch(
        f"/bookings/{booking_id}/confirm",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert confirm.json()["status"] == "confirmed"

    # Complete
    complete = await client.patch(
        f"/bookings/{booking_id}/complete",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert complete.json()["status"] == "completed"

    # Cannot cancel completed booking
    cancel = await client.patch(
        f"/bookings/{booking_id}/cancel",
        json={"reason": "Too late to cancel."},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert cancel.status_code == 422
