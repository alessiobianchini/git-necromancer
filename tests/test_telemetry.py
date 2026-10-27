from unittest import mock
import pytest
from app.telemetry import init_telemetry, trace_seance, record_ai_metrics


def test_init_telemetry_disabled():
    # If SENTRY_DSN is None or empty, should return False and not raise
    assert init_telemetry(None) is False
    assert init_telemetry("") is False


def test_trace_seance_context_manager_without_sentry():
    # When sentry is disabled, context manager yields safely
    with trace_seance("branch-test-1", "gemma2:2b") as span:
        record_ai_metrics(prompt_tokens=50, completion_tokens=100)
    assert True


@mock.patch("sentry_sdk.start_span")
def test_trace_seance_with_sentry_active(mock_start_span):
    mock_span = mock.MagicMock()
    mock_start_span.return_value.__enter__.return_value = mock_span

    with trace_seance("branch-test-2", "gemma2:2b") as span:
        record_ai_metrics(prompt_tokens=42, completion_tokens=84)

    mock_start_span.assert_called_once()
    assert mock_span.set_data.called
