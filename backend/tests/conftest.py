"""Pytest config + fixtures for osquestador-auditor backend.
Uses httpx.AsyncClient with ASGITransport for in-process testing.
"""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from osquestador.db import app, db, init_seed

@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for all async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    """Async HTTP client for the FastAPI app."""
    init_seed()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_client():
    """Client with auth cookie pre-set (max/max123)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/auth/login", json={"username": "max", "password": "max123"})
        assert r.status_code == 200
        yield ac
