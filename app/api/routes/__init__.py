from .health import router as health_router  # re-export

from fastapi import APIRouter

from .post_short_url import router as post_short_url

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(post_short_url,prefix='/create-link', tags=["post_short_url"])
