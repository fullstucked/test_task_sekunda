import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("request")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = uuid.uuid4().hex
        structlog.contextvars.bind_contextvars(request_id=request_id)

        logger.info("request_started", path=request.url.path, method=request.method)

        response = await call_next(request)

        logger.info("request_finished", status=response.status_code)

        structlog.contextvars.clear_contextvars()
        return response
