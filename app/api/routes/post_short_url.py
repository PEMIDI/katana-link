from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from schemas.link_dto import LinkCreate
from services.link_service import LinkService

router = APIRouter()

post_short_url_summary = "Create a short link"


def get_link_service(db: AsyncSession = Depends(get_db)) -> LinkService:
    return LinkService(db)


@router.post(
    "/short_url",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary=post_short_url_summary,

)
async def post_short_url(link: LinkCreate, link_service: LinkService = Depends(get_link_service), ):
    # TODO if exists, just return the short url



    # TODO if not exists, create a new short url
    link = await link_service.create_link(data=link)
    return link
