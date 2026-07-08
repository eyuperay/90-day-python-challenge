import pytest


@pytest.mark.anyio
async def test_comments_unauthorized(client):
    response = await client.get("/api/v1/comments/")
    assert response.status_code == 401