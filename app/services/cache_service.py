from app.core.redis.session import redis_client


class CacheService:
    def __init__(self):
        self.client = redis_client
        self.VISITS_PREFIX = "link:visits:"

    async def increment_visits(self, link_id: int):
        """Atomically increments the visit count for a link ID in Redis."""
        key = f"{self.VISITS_PREFIX}{link_id}"
        await self.client.incr(key)

    async def get_visits_key(self, link_id: int) -> str:
        """Returns the Redis key for the visits count."""
        return f"{self.VISITS_PREFIX}{link_id}"
