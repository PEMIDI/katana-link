# Async database session and engine setup for PostgreSQL
from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()


def _ensure_asyncpg_driver(url: str) -> str:
    """Ensure the database URL uses asyncpg driver for PostgreSQL.

    Converts postgresql:// to postgresql+asyncpg://
    """
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


# Create async engine (PostgreSQL by default; supports SQLite for tests)
_database_url = _ensure_asyncpg_driver(settings.DATABASE_URL)
_is_sqlite = _database_url.startswith("sqlite+")

_engine_kwargs = {
    "echo": settings.SQL_ECHO,
    "pool_pre_ping": True,
}
# SQLite (especially in-memory) doesn't support pool_size/max_overflow in the same way
if not _is_sqlite:
    _engine_kwargs.update({
        "pool_size": settings.SQL_POOL_SIZE,
        "max_overflow": settings.SQL_MAX_OVERFLOW,
    })

engine = create_async_engine(
    _database_url,
    **_engine_kwargs,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
