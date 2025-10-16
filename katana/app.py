from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.logging import setup_logging
from .api.routes import api_router
from .db.session import engine
from .models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    setup_logging(level=settings.LOG_LEVEL)
    # Place for DB init, migrations, cache warm-up, etc.
    # Auto-create tables in development for convenience
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # Avoid failing startup if migrations expected in production
        pass
    yield
    # Shutdown
    # Close connections, flush metrics, etc.


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router)

    return app
