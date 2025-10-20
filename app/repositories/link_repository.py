from typing import Any

import base62
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Link
from schemas.link_dto import LinkCreate


class LinkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: LinkCreate) -> Link:
        link = Link(long_url=str(data.long_link))
        self.db.add(link)

        await self.db.flush()
        link.short_url = base62.encode(link.id)

        await self.db.commit()
        await self.db.refresh(link)

        return link

    async def get_link(self, id: int) -> Link | None:
        return await self.db.get(Link, id)

    async def increment_visits(self, link: Link) -> Link:
        link.visits += 1
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def get_or_create_link(self, data: LinkCreate) -> Link | Any:
        stmt = select(Link).where(Link.long_url == LinkCreate.long_link)
        result = await self.db.execute(stmt)
        link_exist = result.scalar_one_or_none()

        if link_exist:
            return link_exist.short_url

        return await self.create(LinkCreate(long_link=data.long_link))

    async def add_visits_to_link(self, link_id: int, visits: int):
        stmt = (
            update(Link).where(Link.id == link_id).values(visits=Link.visits + visits)
        )
        await self.db.execute(stmt)
        await self.db.commit()
