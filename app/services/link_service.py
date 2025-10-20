import base62
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.link_repository import LinkRepository
from schemas.link_dto import LinkCreate


class LinkService:
    def __init__(self, db: AsyncSession):
        self.repo = LinkRepository(db)

    async def create_link(self, data: LinkCreate):
        return await self.repo.get_or_create_link(data)

    async def get_long_link(self, short_url: str) -> str | None:
        try:
            short_url_id = base62.decode(short_url)
        except Exception:
            return None

        link = await self.repo.get_link(short_url_id)
        if not link:
            return None

        await self.repo.increment_visits(link)
        return link.long_url

