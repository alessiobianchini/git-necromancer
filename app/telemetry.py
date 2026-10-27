"""Telemetry and Sentry Agent Tracing integration for AI séances."""

import logging
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger("git-necromancer.telemetry")

_sentry_initialized = False
_current_span = None


def init_telemetry(dsn: Optional[str] = None, environment: str = "development") -> bool:
    """Initialize Sentry SDK with OpenTelemetry and GenAI agent tracing if DSN is provided."""
    global _sentry_initialized
    if not dsn or not dsn.strip():
        _sentry_initialized = False
        return False

    try:
        import sentry_sdk
        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            send_default_pii=False,
        )
        _sentry_initialized = True
        logger.info("Sentry Agent Tracing successfully initialized")
        return True
    except Exception as exc:
        logger.warning(f"Failed to initialize Sentry: {exc}")
        _sentry_initialized = False
        return False


@contextmanager
def trace_seance(artifact_id: str, model_name: str = "gemma2:2b", operation: str = "gen_ai.chat"):
    """Context manager to trace an AI séance with Sentry OpenTelemetry spans."""
    global _current_span
    span_obj = None

    try:
        import sentry_sdk
        span_ctx = sentry_sdk.start_span(op=operation, name=f"seance:{artifact_id}")
        span_obj = span_ctx.__enter__()
        if span_obj:
            span_obj.set_data("gen_ai.system", "ollama")
            span_obj.set_data("gen_ai.request.model", model_name)
            span_obj.set_data("seance.artifact_id", artifact_id)
    except Exception:
        span_obj = None

    _current_span = span_obj
    try:
        yield span_obj
    except Exception as exc:
        if span_obj:
            span_obj.set_data("error", True)
            span_obj.set_data("error.message", str(exc))
        raise
    finally:
        if span_obj:
            try:
                span_ctx.__exit__(None, None, None)
            except Exception:
                pass
        _current_span = None


def record_ai_metrics(prompt_tokens: int = 0, completion_tokens: int = 0) -> None:
    """Record token counts onto the active séance span."""
    global _current_span
    if _current_span:
        try:
            total = prompt_tokens + completion_tokens
            _current_span.set_data("gen_ai.usage.prompt_tokens", prompt_tokens)
            _current_span.set_data("gen_ai.usage.completion_tokens", completion_tokens)
            _current_span.set_data("gen_ai.usage.total_tokens", total)
        except Exception:
            pass
