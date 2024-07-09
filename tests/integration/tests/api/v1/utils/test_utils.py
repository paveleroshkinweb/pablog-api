import aiohttp

from fastapi import status


async def test_info():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://nginx:8001/api/v1/info', timeout=5) as response:
            assert response.status == status.HTTP_200_OK
