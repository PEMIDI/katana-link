# db.py (Async Version)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..core.config import get_settings

settings = get_settings()

# 1. Use create_async_engine
engine = create_async_engine(
    # 2. Ensure settings.DATABASE_URL uses an async driver (e.g., postgresql+asyncpg)
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    pool_pre_ping=True,
)

# 3. SessionLocal should be bound to AsyncSession
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,  # <- IMPORTANT: Use AsyncSession
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)