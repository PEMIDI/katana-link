from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.link_dto import LinkCreate, LinkRead
from app.services.link_service import LinkService

router = APIRouter()

post_short_url_summary = "Create a short link"


def get_link_service(db: AsyncSession = Depends(get_db)) -> LinkService:
    return LinkService(db)


@router.post(
    "/short_url",
    response_model=LinkRead,
    summary=post_short_url_summary,
)
async def post_short_url(
    link: LinkCreate,
    response: Response,
    link_service: LinkService = Depends(get_link_service),
):
    created_link, is_created = await link_service.create_link(data=link)
    response.status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK

    full_short_link = link_service.build_public_short_link(created_link.short_url)

    return LinkRead(short_link=full_short_link, long_link=created_link.long_url)
