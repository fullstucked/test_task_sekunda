from contextlib import asynccontextmanager
from structlog import get_logger

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from presentation.router import api_router as router
from setup.exceptions.not_found_404 import NotFoundError


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secunda test task",
        version="0.0.1",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_exceptions(app)
    # register routers
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

    # --- shutdown ---
    # await close_redis()
    # await close_db()


def add_exceptions(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(
        request: Request,
        exc: NotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc) or "Resource not found",
            },
        )
