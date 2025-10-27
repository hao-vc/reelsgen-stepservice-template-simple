"""Authentication middleware and utilities."""

from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.logging_config import get_logger

logger = get_logger(__name__)

# Security scheme for OpenAPI documentation
security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials) -> bool:
    """Verify Bearer token."""
    if credentials.credentials != settings.auth_token:
        logger.warning(
            "Invalid token provided",
            provided_token=credentials.credentials[:8] + "...",
        )
        return False
    return True


async def get_current_user(credentials: HTTPAuthorizationCredentials) -> str:
    """Get current authenticated user (returns 'authenticated' for valid tokens)."""
    if not await verify_token(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "authenticated"


def is_health_endpoint(request: Request) -> bool:
    """Check if request is to health endpoint."""
    return request.url.path == "/health"


async def auth_middleware(request: Request, call_next):
    """Authentication middleware."""
    # Skip authentication for health endpoint
    if is_health_endpoint(request):
        return await call_next(request)
    
    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logger.warning(
            "Missing Authorization header",
            endpoint=request.url.path,
            method=request.method,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check Bearer token format
    if not auth_header.startswith("Bearer "):
        logger.warning(
            "Invalid Authorization header format",
            endpoint=request.url.path,
            method=request.method,
            auth_header=auth_header[:20] + "...",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract and verify token
    token = auth_header[7:]  # Remove "Bearer " prefix
    if token != settings.auth_token:
        logger.warning(
            "Invalid token",
            endpoint=request.url.path,
            method=request.method,
            token_prefix=token[:8] + "...",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token is valid, proceed with request
    logger.debug(
        "Authentication successful",
        endpoint=request.url.path,
        method=request.method,
    )
    
    return await call_next(request)
