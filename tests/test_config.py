import os
from unittest import mock
import pytest
from app.config import Settings, get_settings


def test_default_settings():
    settings = Settings()
    assert settings.PORT == 8000
    assert settings.HOST == "0.0.0.0"
    assert settings.OLLAMA_BASE_URL == "http://localhost:11434"
    assert settings.OLLAMA_MODEL == "gemma2:2b"
    assert settings.REPO_PATH == "."
    assert settings.SENTRY_DSN is None
    assert settings.ELEVENLABS_API_KEY is None


def test_settings_override_from_env():
    with mock.patch.dict(os.environ, {
        "PORT": "9090",
        "OLLAMA_MODEL": "gemma2:9b",
        "SENTRY_DSN": "https://test@sentry.io/123",
        "ELEVENLABS_API_KEY": "test-key"
    }):
        settings = Settings()
        assert settings.PORT == 9090
        assert settings.OLLAMA_MODEL == "gemma2:9b"
        assert settings.SENTRY_DSN == "https://test@sentry.io/123"
        assert settings.ELEVENLABS_API_KEY == "test-key"
