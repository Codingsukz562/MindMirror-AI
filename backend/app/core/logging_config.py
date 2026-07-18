"""Logging configuration for MindMirror AI."""

import logging
import sys
from typing import Optional


class RequestIDFilter(logging.Filter):
    """Add request ID to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add request_id to log record."""
        # Try to get request_id from extra or default to 'N/A'
        record.extra_request_id = getattr(record, 'request_id', 'N/A')
        return True


def setup_logging(log_level: str = "INFO") -> None:
    """Setup structured logging for the application."""
    
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter with request ID support
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s | request_id=%(extra_request_id)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    console_handler.addFilter(RequestIDFilter())
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
