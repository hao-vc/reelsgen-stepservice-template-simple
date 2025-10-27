"""
Pytest configuration and fixtures for FastAPI testing.
"""
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import tempfile
from typing import Generator

# Set test environment variables before importing the app
os.environ.update({
    "SERVICE_NAME": "test-service",
    "SERVICE_VERSION": "1.0.0-test",
    "AUTH_TOKEN": "test-auth-token",
    "WEBHOOK_AUTH_TOKEN": "test-webhook-token",
    "ALERT_WEBHOOK_URL": "https://test.example.com/webhook",
    "ALERT_API_KEY": "test-api-key",
    "LOG_LEVEL": "DEBUG",
    "LOG_FORMAT": "json",
    "DEBUG": "true"
})

from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for FastAPI app."""
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Return authentication headers for testing."""
    return {"Authorization": "Bearer test-auth-token"}


@pytest.fixture
def webhook_auth_headers() -> dict[str, str]:
    """Return webhook authentication headers for testing."""
    return {"Authorization": "Bearer test-webhook-token"}


@pytest.fixture
def sample_webhook_url() -> str:
    """Return a sample webhook URL for testing."""
    return "https://test.example.com/webhook"


@pytest.fixture
def sample_operation_data() -> dict:
    """Return sample operation data for testing."""
    return {
        "webhook_url": "https://test.example.com/webhook",
        "data": {
            "input": "test data"
        }
    }


@pytest.fixture
def sample_step_call_data() -> dict:
    """Return sample step call data for testing."""
    return {
        "step": {
            "id": "550e8400-e29b-41d4-a716-446655440000"
        },
        "webhook": {
            "url": "https://test.example.com/webhook"
        },
        "initial": {
            "input": {
                "video_url": "https://example.com/video.mp4",
                "duration": 120
            }
        },
        "variables": {
            "quality": "1080p",
            "format": "mp4"
        }
    }


@pytest.fixture
def sample_example_data() -> dict:
    """Return sample example data for testing."""
    return {
        "step": {
            "id": "550e8400-e29b-41d4-a716-446655440000"
        },
        "webhook": {
            "url": "https://test.example.com/webhook"
        },
        "initial": {
            "input": {
                "text": "Hello World",
                "operation": "uppercase",
                "language": "en",
                "format": "plain"
            }
        },
        "variables": {
            "timeout": 30,
            "retry_count": 3
        }
    }


@pytest.fixture
def mock_webhook_response():
    """Mock webhook response for testing."""
    with patch('app.services.webhook_service.WebhookService.send_webhook') as mock:
        mock.return_value = None  # send_webhook is async and returns None
        yield mock


@pytest.fixture
def mock_alert_service():
    """Mock alert service for testing."""
    with patch('app.services.alert_service.send_alert') as mock:
        mock.return_value = {"status": "success"}
        yield mock


@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment variables after each test."""
    yield
    # Clean up any test-specific environment variables if needed
    pass
