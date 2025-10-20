from fastapi import APIRouter

from .health import router as health_router
from .post_short_url import router as post_short_url
from .get_long_url import router as get_short_url

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(post_short_url, prefix='/create-link', tags=["post_short_url"])
api_router.include_router(get_short_url, prefix='/redirect-link', tags=["get_long_url"])
