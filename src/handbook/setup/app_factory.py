from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from presentation.router import api_router as router
from setup.dependencies_g import require_api_key
from setup.exceptions.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secunda test task",
        version="0.0.1",
        lifespan=lifespan,
        dependencies=[Depends(require_api_key)],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(router, prefix="/v1/handbook")
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    # init_logging()
    logger = get_logger()
    logger.info("app startup")
    # --- startup ---

    yield
