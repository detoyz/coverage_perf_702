import asyncio
from typing import Callable
import uvloop
import pytest as pytest

from httpx import AsyncClient

from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    uvloop.install()
    uvloop.EventLoopPolicy.get_event_loop = asyncio.get_running_loop
    loop = asyncio.new_event_loop()
    yield loop


@pytest.fixture(scope="session")
async def api_loader() -> Callable[..., AsyncClient]:
    # ... normally here we load all packages/modules with routers to resolve inverted fastapi decorated routes
    def _inner(headers: dict = None):
        return AsyncClient(app=app, base_url="http://app.test", headers=headers)

    return _inner


@pytest.fixture
async def api(api_loader) -> AsyncClient:
    async with api_loader() as ac:
        yield ac


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["john"] * 50)
async def test_return_name(api: AsyncClient, name):
    result = await api.get(f"/hello/{name}")
    assert result.json() == {"message": f"Hello {name}"}
