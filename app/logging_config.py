"""Structured logging configuration using structlog."""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from app.config import settings


def configure_logging() -> None:
    """Configure structured logging."""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level),
    )
    
    # Configure structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Add JSON or console formatter based on configuration
    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def log_request(
    logger: structlog.BoundLogger,
    method: str,
    path: str,
    operation_id: str,
    **kwargs: Any,
) -> None:
    """Log incoming request."""
    logger.info(
        "Request received",
        service=settings.service_name,
        endpoint=path,
        method=method,
        operation_id=operation_id,
        **kwargs,
    )


def log_operation_start(
    logger: structlog.BoundLogger,
    operation_id: str,
    endpoint: str,
    **kwargs: Any,
) -> None:
    """Log operation start."""
    logger.info(
        "Operation started",
        service=settings.service_name,
        endpoint=endpoint,
        operation_id=operation_id,
        **kwargs,
    )


def log_operation_complete(
    logger: structlog.BoundLogger,
    operation_id: str,
    endpoint: str,
    **kwargs: Any,
) -> None:
    """Log operation completion."""
    logger.info(
        "Operation completed",
        service=settings.service_name,
        endpoint=endpoint,
        operation_id=operation_id,
        **kwargs,
    )


def log_error(
    logger: structlog.BoundLogger,
    operation_id: str,
    endpoint: str,
    error: Exception,
    **kwargs: Any,
) -> None:
    """Log error with context."""
    logger.error(
        "Operation failed",
        service=settings.service_name,
        endpoint=endpoint,
        operation_id=operation_id,
        error=str(error),
        error_type=type(error).__name__,
        exc_info=True,
        **kwargs,
    )


def log_webhook_sent(
    logger: structlog.BoundLogger,
    operation_id: str,
    webhook_url: str,
    status_code: int,
    **kwargs: Any,
) -> None:
    """Log webhook sent."""
    logger.info(
        "Webhook sent",
        service=settings.service_name,
        operation_id=operation_id,
        webhook_url=webhook_url,
        status_code=status_code,
        **kwargs,
    )


def log_alert_sent(
    logger: structlog.BoundLogger,
    operation_id: str,
    alert_text: str,
    priority: str,
    **kwargs: Any,
) -> None:
    """Log alert sent."""
    logger.warning(
        "Alert sent",
        service=settings.service_name,
        operation_id=operation_id,
        alert_text=alert_text,
        priority=priority,
        **kwargs,
    )
