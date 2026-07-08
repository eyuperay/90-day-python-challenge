import pytest


@pytest.mark.anyio
async def test_inventory_unauthorized(client):
    response = await client.get("/api/v1/inventory/")
    assert response.status_code == 401