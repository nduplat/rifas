from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from app.core.config import settings


def get_user_identifier(request: Request) -> str:
    """Get user identifier for rate limiting."""
    # Try to get user ID from JWT token if available
    try:
        from app.core.security import verify_token
        from fastapi.security import OAuth2PasswordBearer
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")

        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            payload = verify_token(token, lambda: None)
            if payload and payload.user_id:
                return str(payload.user_id)
    except:
        pass

    # Fallback to IP address
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=["100 per minute", "1000 per hour"]
)

# Purchase-specific limiter (more restrictive)
purchase_limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=["10 per minute", "50 per hour"]
)