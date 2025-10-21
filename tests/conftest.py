import os
import pytest
from httpx import AsyncClient, ASGITransport

# Configure test environment BEFORE importing the app
os.environ.setdefault("ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SHORT_DOMAIN", "http://testserver")
os.environ.setdefault("ENABLE_DOCS", "false")

from app.app import app  # noqa: E402
from app.core.db.session import engine  # noqa: E402
from app.models.coremodel import CoreModel  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    # Ensure database tables exist for tests (since ASGI lifespan isn't run by transport)
    async with engine.begin() as conn:
        await conn.run_sync(CoreModel.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
