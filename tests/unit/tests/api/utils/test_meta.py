from pablog_api.api.server import VERSION

from fastapi import status
from httpx import AsyncClient


PING_PATH = "/healthcheck"
INFO_PATH = "/api/v1/info"


async def test_status(client: AsyncClient):
    response = await client.get(PING_PATH)
    assert response.status_code == status.HTTP_200_OK


async def test_meta(client: AsyncClient):
    response = await client.get(INFO_PATH)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"version": VERSION}
