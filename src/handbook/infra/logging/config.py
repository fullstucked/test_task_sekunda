import os
import logging
import sys

import structlog


def init_logging():
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)

    handler = logging.StreamHandler(sys.stdout)

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            timestamper,
        ],
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("LOG_LEVEL")
    root_logger.handlers = [handler]

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.dev.set_exc_info,
            timestamper,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(settings.general.LOG_LEVEL),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
