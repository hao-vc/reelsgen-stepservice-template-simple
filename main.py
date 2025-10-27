"""FastAPI microservice template for beginners."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import example, health, operations
from app.auth import auth_middleware
from app.config import settings
from app.logging_config import configure_logging, get_logger
from app.services.alert_service import AlertService

# Configure logging
configure_logging()
logger = get_logger(__name__)

# Initialize alert service
alert_service = AlertService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(
        "Starting FastAPI microservice",
        service_name=settings.service_name,
        version=settings.service_version,
        debug=settings.debug,
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI microservice")
    await alert_service.close()


# Create FastAPI application
app = FastAPI(
    title=settings.service_name,
    description="Simple FastAPI microservice template for beginners",
    version=settings.service_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.middleware("http")(auth_middleware)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    try:
        logger.info(
            "Incoming request",
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None,
        )
        
        response = await call_next(request)
        
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )
        
        return response
    except Exception as e:
        logger.error("Request logging error", error=str(e))
        return await call_next(request)


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with alerting."""
    try:
        operation_id = request.headers.get("X-Operation-ID", "unknown")
        
        logger.error(
            "Validation error",
            operation_id=operation_id,
            path=request.url.path,
            method=request.method,
            errors=exc.errors(),
        )
        
        # Send alert for validation errors
        await alert_service.send_error_alert(
            error=exc,
            operation_id=operation_id,
            endpoint=request.url.path,
        )
    except Exception as alert_error:
        logger.error("Alert sending failed", error=str(alert_error))
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )


# Global exception handler for general errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with alerting."""
    try:
        operation_id = request.headers.get("X-Operation-ID", "unknown")
        
        logger.error(
            "Unhandled exception",
            operation_id=operation_id,
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_info=True,
        )
        
        # Send alert for unhandled exceptions
        await alert_service.send_error_alert(
            error=exc,
            operation_id=operation_id,
            endpoint=request.url.path,
        )
    except Exception as alert_error:
        logger.error("Alert sending failed", error=str(alert_error))
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred",
        },
    )


# Include routers
app.include_router(health.router)
app.include_router(operations.router)
app.include_router(example.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI Microservice Template",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
