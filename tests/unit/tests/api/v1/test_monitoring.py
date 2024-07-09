from fastapi import status
from httpx import AsyncClient


async def test_healthcheck(client: AsyncClient):
    response = await client.get("/api/v1/healthcheck")
    assert response.status_code == status.HTTP_200_OK


async def test_info(client: AsyncClient):
    response = await client.get("/api/v1/info")
    assert response.status_code == status.HTTP_200_OK
