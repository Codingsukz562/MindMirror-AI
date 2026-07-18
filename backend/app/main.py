"""MindMirror AI Backend Application."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uuid

from app.core.config import get_settings
from app.api import habits, health, chat
from app.core.logging_config import setup_logging
from app.core.exception_handler import (
    mindmirror_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.exceptions import MindMirrorException
from app.core.rate_limiter import RateLimitMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting MindMirror AI Backend")
    yield
    logger.info("Shutting down MindMirror AI Backend")


app = FastAPI(
    title="MindMirror AI",
    description="AI Behavioral Coach for habit change",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mindmirror-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add request ID to each request for tracing."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Register exception handlers
app.add_exception_handler(MindMirrorException, mindmirror_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(habits.router, prefix="/api", tags=["Habits"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to MindMirror AI", "version": "1.0.0"}
