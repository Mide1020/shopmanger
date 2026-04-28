from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.config import settings
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.rate_limit import limiter
from app.routes.api_v1 import api_router
from app.exceptions import (
    validation_exception_handler,
    integrity_error_handler,
    global_exception_handler
)

import os
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("TESTING") == "1":
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    else:
        try:
            # Attempt to connect to Redis
            redis = aioredis.from_url(
                settings.REDIS_URL, 
                encoding="utf8", 
                decode_responses=False,
                socket_connect_timeout=3,
                socket_timeout=3
            )
            await redis.ping()
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
            logger.info("Connected to Redis successfully for caching.")
        except Exception as e:
            # Fallback to in-memory if Redis is not reachable
            logger.warning(f"Redis is unreachable: {str(e)}. Falling back to InMemoryBackend.")
            FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="ShopManager API",
    description="A self-managed e-commerce platform",
    version="1.0.0",
    lifespan=lifespan
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS — configure ALLOWED_ORIGINS in your .env for production
# e.g. ALLOWED_ORIGINS=https://myapp.com,https://admin.myapp.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Versioned API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

from datetime import datetime

@app.get("/health")
def health_check():
    """System health check for monitoring and Docker/K8s"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version
    }

@app.get("/")
def root():
    return {"message": "Welcome to ShopManager API", "docs": "/docs", "api_v1": settings.API_V1_STR}