import pendulum
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from src.core.config import settings
from src.core.logging_config import configure_logging

# Import endpoints
from src.api.v1.endpoints import (
    student
)

# Configure logging before anything else
configure_logging()
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application", env=settings.ENVIRONMENT)
    yield
    logger.info("Shutting down application")

# Docs only in dev
docs_url = "/docs" if settings.ENVIRONMENT != "production" else None
redoc_url = "/redoc" if settings.ENVIRONMENT != "production" else None
openapi_url = f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts = ["*"]
)
# Main route
@app.get("/")
async def root():
    data = {
        'now': pendulum.now(),
    }
    return {"message": "Welcome to "+settings.PROJECT_NAME, "data": data}

# Include your API routers
app.include_router(student.router, prefix=settings.API_V1_STR, tags=["student"])