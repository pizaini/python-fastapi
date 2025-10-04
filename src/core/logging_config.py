import logging
import os

import structlog
import sys
from src.core.config import settings

def configure_logging():
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    pre_chain = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        timestamper,
    ]

    # Choose renderer based on environment
    if settings.ENVIRONMENT == "development":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    # Configure structlog
    structlog.configure(
        processors=[
            *pre_chain,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Formatter for logging.Handler
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=pre_chain,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Reset root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

    # Prevent Uvicorn log duplication
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(logger_name).handlers.clear()
        logging.getLogger(logger_name).propagate = True
