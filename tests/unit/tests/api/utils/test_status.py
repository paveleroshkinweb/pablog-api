from fastapi import status
from httpx import AsyncClient


PING_PATH = "/status"


async def test_status(client_v1: AsyncClient):
    response = await client_v1.get(PING_PATH)
    assert response.status_code == status.HTTP_200_OK
