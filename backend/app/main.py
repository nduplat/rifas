# app/main.py
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import configure_structlog
from app.core.rate_limiting import limiter
from app.db.session import init_db, close_db
from slowapi.middleware import SlowAPIMiddleware

# Configure structlog
configure_structlog()

# Initialize Sentry
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=1.0,
        integrations=[
            sentry_sdk.integrations.fastapi.FastAPIIntegration(),
            sentry_sdk.integrations.redis.RedisIntegration(),
            sentry_sdk.integrations.sqlalchemy.SqlalchemyIntegration(),
        ],
    )

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json" if settings.debug else None,
    docs_url=f"{settings.api_v1_prefix}/docs" if settings.debug else None,
    redoc_url=f"{settings.api_v1_prefix}/redoc" if settings.debug else None
)

# Add HTTPS redirect middleware (only in production behind reverse proxy)
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Add rate limiting middleware
app.add_middleware(SlowAPIMiddleware)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

app.include_router(api_router, prefix=settings.api_v1_prefix)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup():
    await init_db()       # conecta motor/async session pool
    global redis_client
    redis_client = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}")

@app.on_event("shutdown")
async def shutdown():
    await close_db()
    global redis_client
    if redis_client:
        await redis_client.close()
