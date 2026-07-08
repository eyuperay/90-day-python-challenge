import pytest


@pytest.mark.anyio
async def test_tasks_unauthorized(client):
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 401