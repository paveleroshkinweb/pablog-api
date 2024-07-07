from fastapi import status
from httpx import AsyncClient


PING_PATH = "/healthcheck"


async def test_status(client: AsyncClient):
    response = await client.get(PING_PATH)
    assert response.status_code == status.HTTP_200_OK
