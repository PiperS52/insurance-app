import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, ANY


@pytest.mark.anyio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.json() == {"status": "healthy"}
