"""
Unit tests for services.
"""
import pytest
from unittest.mock import patch, Mock
import httpx
from app.services.operation_service import OperationService
from app.services.webhook_service import WebhookService
from app.services.alert_service import AlertService


class TestOperationService:
    """Test cases for OperationService."""
    
    def test_generate_operation_id(self):
        """Test operation ID generation."""
        service = OperationService()
        operation_id = service.generate_operation_id()
        
        assert operation_id is not None
        assert isinstance(operation_id, str)
        assert len(operation_id) == 36  # UUID length
    
    def test_generate_operation_id_unique(self):
        """Test that operation IDs are unique."""
        service = OperationService()
        ids = [service.generate_operation_id() for _ in range(100)]
        
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
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "success"}
            mock_post.return_value = mock_response
            
            result = await webhook_service.send_webhook(
                url="https://test.example.com/webhook",
                data={"test": "data"},
                auth_token="test-token"
            )
            
            assert result["status"] == "success"
            assert result["response_code"] == 200
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_webhook_failure(self, webhook_service):
        """Test webhook sending failure."""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")
            
            result = await webhook_service.send_webhook(
                url="https://test.example.com/webhook",
                data={"test": "data"},
                auth_token="test-token"
            )
            
            assert result["status"] == "error"
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_send_webhook_http_error(self, webhook_service):
        """Test webhook sending with HTTP error."""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_post.return_value = mock_response
            
            result = await webhook_service.send_webhook(
                url="https://test.example.com/webhook",
                data={"test": "data"},
                auth_token="test-token"
            )
            
            assert result["status"] == "error"
            assert result["response_code"] == 500


class TestAlertService:
    """Test cases for AlertService."""
    
    @pytest.fixture
    def alert_service(self):
        """Create AlertService instance."""
        return AlertService()
    
    @pytest.mark.asyncio
    async def test_send_alert_success(self, alert_service):
        """Test successful alert sending."""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "success"}
            mock_post.return_value = mock_response
            
            result = await alert_service.send_alert(
                text="Test alert",
                priority="high",
                tags=["test", "error"]
            )
            
            assert result["status"] == "success"
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_alert_failure(self, alert_service):
        """Test alert sending failure."""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")
            
            result = await alert_service.send_alert(
                text="Test alert",
                priority="high",
                tags=["test", "error"]
            )
            
            assert result["status"] == "error"
            assert "error" in result
    
    def test_format_alert_data(self, alert_service):
        """Test alert data formatting."""
        alert_data = alert_service._format_alert_data(
            text="Test error",
            priority="high",
            tags=["test", "error"],
            debug_logs="Debug information"
        )
        
        assert alert_data["text"] == "Test error"
        assert alert_data["priority"] == "high"
        assert alert_data["tags"] == ["test", "error"]
        assert alert_data["debug_logs"] == "Debug information"
        assert "timestamp" in alert_data
