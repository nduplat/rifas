import os
from pydantic import BaseModel, validator


class Settings(BaseModel):
    app_name: str = "Rifa1122 API"
    debug: bool = False
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Stripe
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # Environment
    environment: str = "development"

    # Sentry
    sentry_dsn: str = ""

    # Celery
    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def celery_result_backend(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @validator('debug', pre=True, always=True)
    def set_debug_based_on_env(cls, v):
        # Force debug=False in production
        env = os.getenv('ENVIRONMENT', 'development')
        if env.lower() == 'production':
            return False
        return v or os.getenv('DEBUG', 'false').lower() == 'true'

    class Config:
        env_file = ".env"


# Validate required environment variables
required_env_vars = [
    'DATABASE_URL',
    'SECRET_KEY',
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY',
    'STRIPE_WEBHOOK_SECRET'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

settings = Settings()
