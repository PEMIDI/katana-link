import asyncio
from typing import Optional

from celery import Celery

from app.core.config import get_settings
from app.core.db.session import AsyncSessionLocal
from app.core.redis.session import redis_client
from app.repositories.link_repository import LinkRepository
from app.services.cache_service import CacheService


settings = get_settings()

_redis_host = settings.REDIS_HOST or "localhost"
_redis_port = settings.REDIS_PORT or 6379
BROKER_URL = f"redis://{_redis_host}:{_redis_port}/0"

app = Celery("katana_link_tasks", broker=BROKER_URL)


async def _write_back_visits_to_db_async():
    """Async implementation: scan Redis for visit counters, flush them to DB, and reset."""
    cache_service = CacheService()

    pattern = f"{cache_service.VISITS_PREFIX}*"

    updates: list[tuple[int, int]] = []

    async for key in redis_client.scan_iter(match=pattern):
        value: Optional[str] = await redis_client.getset(key, 0)
        if not value:
            continue
        try:
            count = int(value)
        except (TypeError, ValueError):
            continue
        if count <= 0:
            continue

        if key.startswith(cache_service.VISITS_PREFIX):
            link_id_str = key[len(cache_service.VISITS_PREFIX) :]
            try:
                link_id = int(link_id_str)
            except ValueError:
                continue
            updates.append((link_id, count))

    if not updates:
        return

    async with AsyncSessionLocal() as db:
        repo = LinkRepository(db)
        for link_id, count in updates:
            await repo.add_visits_to_link(link_id=link_id, visits=count)


@app.task(name="app.tasks.counter_tasks.write_back_visits_to_db")
def write_back_visits_to_db():
    """Scheduled Celery task wrapper that runs the async implementation."""
    asyncio.run(_write_back_visits_to_db_async())
