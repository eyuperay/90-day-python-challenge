import pytest


@pytest.mark.anyio
async def test_projects_unauthorized(client):
    response = await client.get("/api/v1/projects/")
    assert response.status_code == 401