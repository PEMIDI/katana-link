from .health import router as health_router  # re-export
from .users import router as users_router  # re-export

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"]) 
api_router.include_router(users_router, prefix="/users", tags=["users"]) 
