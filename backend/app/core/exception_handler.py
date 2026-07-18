"""Global exception handler for FastAPI."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

from app.core.exceptions import MindMirrorException

logger = logging.getLogger(__name__)


async def mindmirror_exception_handler(
    request: Request, 
    exc: MindMirrorException
) -> JSONResponse:
    """Handle custom MindMirror exceptions."""
    logger.error(
        f"MindMirror exception: {exc.message}",
        extra={"request_id": getattr(request.state, "request_id", "N/A")}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "type": exc.__class__.__name__
        }
    )


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"request_id": getattr(request.state, "request_id", "N/A")}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation failed",
            "details": exc.errors()
        }
    )


async def pydantic_exception_handler(
    request: Request, 
    exc: ValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(
        f"Pydantic validation error: {exc.errors()}",
        extra={"request_id": getattr(request.state, "request_id", "N/A")}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Invalid data format",
            "details": exc.errors()
        }
    )


async def generic_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(
        f"Unexpected error: {str(exc)}",
        extra={"request_id": getattr(request.state, "request_id", "N/A")}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred",
        }
    )
