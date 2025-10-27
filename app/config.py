"""Configuration management using Pydantic Settings."""

from typing import Optional

from pydantic import Field, HttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Service Configuration
    service_name: str = Field(default="my-service", description="Name of the service")
    service_version: str = Field(default="1.0.0", description="Version of the service")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Authentication
    auth_token: str = Field(..., description="Bearer token for request authentication")
    webhook_auth_token: str = Field(..., description="Bearer token for webhook authentication")
    
    # Alerting System
    alert_webhook_url: Optional[HttpUrl] = Field(
        default=None, 
        description="Supabase Edge Function URL for alerts"
    )
    alert_api_key: Optional[str] = Field(
        default=None, 
        description="API key for alert webhook"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or console)")
    
    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()
    
    @validator("log_format")
    def validate_log_format(cls, v: str) -> str:
        """Validate log format."""
        valid_formats = ["json", "console"]
        if v.lower() not in valid_formats:
            raise ValueError(f"log_format must be one of {valid_formats}")
        return v.lower()
    
    @validator("auth_token")
    def validate_auth_token(cls, v: str) -> str:
        """Validate auth token is not empty."""
        if not v or len(v.strip()) == 0:
            raise ValueError("auth_token cannot be empty")
        return v.strip()
    
    @validator("webhook_auth_token")
    def validate_webhook_auth_token(cls, v: str) -> str:
        """Validate webhook auth token is not empty."""
        if not v or len(v.strip()) == 0:
            raise ValueError("webhook_auth_token cannot be empty")
        return v.strip()
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
