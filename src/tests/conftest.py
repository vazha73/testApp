# Make requests in our tests
import warnings
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, request
import config
import pytest_asyncio
from main import get_application

    
@pytest_asyncio.fixture
def app() -> FastAPI:
    return  get_application()

@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://localhost",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client
