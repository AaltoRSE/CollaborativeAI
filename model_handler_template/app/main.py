"""
Sets up FastAPI app with user and conversation routers and custom middleware.
"""


import logging
import logging.config

# FastAPI and starlette imports
from fastapi import FastAPI

# Custom imports
from app.router import (
    model_router,
    session_router    
)
from app.utils.lifecycle import startup


# Logging configuration
logging.config.fileConfig("app/logging.conf", disable_existing_loggers=False)

# Configure logger settings based on environment variable

logger = logging.getLogger("app")

# Initialize auth service
# NOTE: do not use the auth_service here but rather get a reference through get_entrajwt_auth_service call


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """ 
    logger.info("Starting application ...")

    # Initialize the FastAPI application
    _app = FastAPI(
        lifespan=startup,
        # SECURITY: disable docs and openapi spec if not development environment
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        # SECURITY: enabling would cause http-redirect, we hardcode the URLs in UI anyway
        redirect_slashes=False,
    )

    logger.info("Application started ...")
    # Include routers
    _app.include_router(model_router.router)
    _app.include_router(session_router.router)
        

    return _app

app = create_app()
