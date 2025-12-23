"""Pytest configuration and shared fixtures."""

import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_secrets():
    """Sample secrets for testing."""
    return {
        "API_KEY": "sk_test_1234567890abcdef",
        "DB_PASSWORD": "super_secret_password_123",
        "JWT_SECRET": "my-jwt-secret-key"
    }


@pytest.fixture
def mock_vault_response():
    """Mock successful Vault API response."""
    return {
        "data": {
            "data": {
                "API_KEY": "sk_test_1234567890abcdef",
                "DB_PASSWORD": "super_secret_password_123"
            }
        }
    }


@pytest.fixture
def mock_token():
    """Mock Vault token."""
    return "hvs.CAESIL1234567890abcdefghijklmnopqrstuvwxyz"


@pytest.fixture
def mock_session_info():
    """Mock session information."""
    return {
        "user": "test-user",
        "policies": ["default", "homelab-services"],
        "expiry": (datetime.now() + timedelta(minutes=60)).isoformat()
    }
