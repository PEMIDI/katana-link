from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.api.deps import get_db
from app.services.link_service import LinkService

router = APIRouter()

get_short_url_summary = "Redirect to the original link"


def get_link_service(db: AsyncSession = Depends(get_db)) -> LinkService:
    return LinkService(db)


@router.get(
    "/{short_url}",
    response_model=None,
    summary=get_short_url_summary,
)
async def get_long_url(short_url: str, link_service: LinkService = Depends(get_link_service)):
    long_url = await link_service.get_long_link(short_url)
    if not long_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    return RedirectResponse(url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
