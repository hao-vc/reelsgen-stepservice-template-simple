"""
Unit tests for services.
"""
import pytest
from unittest.mock import patch, Mock, AsyncMock
import httpx
from uuid import UUID
from app.services.operation_service import OperationService
from app.services.webhook_service import WebhookService
from app.services.alert_service import AlertService


class TestOperationService:
    """Test cases for OperationService."""
    
    @pytest.fixture
    def mock_webhook_service(self):
        """Create mock webhook service."""
        return AsyncMock(spec=WebhookService)
    
    @pytest.fixture
    def operation_service(self, mock_webhook_service):
        """Create OperationService instance."""
        return OperationService(mock_webhook_service)
    
    def test_generate_operation_id(self, operation_service):
        """Test operation ID generation."""
        operation_id = operation_service.generate_operation_id()
        
        assert operation_id is not None
        assert isinstance(operation_id, UUID)
        assert len(str(operation_id)) == 36  # UUID length
    
    def test_generate_operation_id_unique(self, operation_service):
        """Test that operation IDs are unique."""
        ids = [operation_service.generate_operation_id() for _ in range(100)]
        
        assert len(set(ids)) == 100  # All IDs should be unique


class TestWebhookService:
    """Test cases for WebhookService."""
    
    @pytest.fixture
    def webhook_service(self):
        """Create WebhookService instance."""
        return WebhookService()
    
    @pytest.mark.asyncio
    async def test_send_webhook_success(self, webhook_service):
        """Test successful webhook sending."""
        from app.schemas.operations import WebhookPayload
        from uuid import uuid4
        
        with patch.object(webhook_service.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            operation_id = uuid4()
            payload = WebhookPayload(
                operation_id=operation_id,
                status="completed",
                result={"test": "data"},
                timestamp="2024-01-15T10:30:00Z"
            )
            
            await webhook_service.send_webhook(
                webhook_url="https://test.example.com/webhook",
                payload=payload
            )
            
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_webhook_failure(self, webhook_service):
        """Test webhook sending failure."""
        from app.schemas.operations import WebhookPayload
        from uuid import uuid4
        
        with patch.object(webhook_service.client, 'post') as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")
            
            operation_id = uuid4()
            payload = WebhookPayload(
                operation_id=operation_id,
                status="completed",
                result={"test": "data"},
                timestamp="2024-01-15T10:30:00Z"
            )
            
            with pytest.raises(httpx.RequestError):
                await webhook_service.send_webhook(
                    webhook_url="https://test.example.com/webhook",
                    payload=payload
                )
    
    @pytest.mark.asyncio
    async def test_send_webhook_http_error(self, webhook_service):
        """Test webhook sending with HTTP error."""
        from app.schemas.operations import WebhookPayload
        from uuid import uuid4
        
        with patch.object(webhook_service.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Server Error", request=Mock(), response=mock_response
            )
            mock_post.return_value = mock_response
            
            operation_id = uuid4()
            payload = WebhookPayload(
                operation_id=operation_id,
                status="completed",
                result={"test": "data"},
                timestamp="2024-01-15T10:30:00Z"
            )
            
            with pytest.raises(httpx.HTTPStatusError):
                await webhook_service.send_webhook(
                    webhook_url="https://test.example.com/webhook",
                    payload=payload
                )


class TestAlertService:
    """Test cases for AlertService."""
    
    @pytest.fixture
    def alert_service(self):
        """Create AlertService instance."""
        return AlertService()
    
    @pytest.mark.asyncio
    async def test_send_alert_success(self, alert_service):
        """Test successful alert sending."""
        with patch.object(alert_service.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            await alert_service.send_alert(
                text="Test alert",
                priority="high",
                tags=["test", "error"]
            )
            
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_alert_failure(self, alert_service):
        """Test alert sending failure."""
        with patch.object(alert_service.client, 'post') as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")
            
            # Alert service should not raise exceptions
            await alert_service.send_alert(
                text="Test alert",
                priority="high",
                tags=["test", "error"]
            )
            
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_alert_skipped_when_not_configured(self, alert_service):
        """Test that alerts are skipped when not configured."""
        with patch('app.config.settings') as mock_settings:
            mock_settings.alert_webhook_url = None
            mock_settings.alert_api_key = None
            
            # Mock the actual settings used in the service
            original_settings = alert_service.__class__.__module__ + '.settings'
            with patch(original_settings) as mock_service_settings:
                mock_service_settings.alert_webhook_url = None
                mock_service_settings.alert_api_key = None
                
                with patch.object(alert_service.client, 'post') as mock_post:
                    await alert_service.send_alert(
                        text="Test alert",
                        priority="high",
                        tags=["test", "error"]
                    )
                    
                    # Should not call post when not configured
                    mock_post.assert_not_called()
