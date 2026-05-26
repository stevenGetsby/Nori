"""Redacted telemetry hook for project LLM gateway calls."""
from __future__ import annotations

import time
from typing import Any, Callable


TelemetrySink = Callable[[dict[str, Any]], None]
_telemetry_sink: TelemetrySink | None = None


def set_telemetry_sink(sink: TelemetrySink | None) -> None:
    """Register a process-local telemetry sink for redacted model call metadata."""

    global _telemetry_sink
    _telemetry_sink = sink


def emit_telemetry(
    operation: str,
    usage: str,
    model: Any,
    started: float,
    *,
    error: Exception | None = None,
) -> None:
    """Emit prompt-free model call metadata; sink failures never affect calls."""

    if _telemetry_sink is None:
        return
    record = {
        "operation": operation,
        "usage": usage,
        "model_key": getattr(model, "key", ""),
        "provider_id": getattr(model, "provider_id", ""),
        "model_id": getattr(model, "model_id", ""),
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "success": error is None,
    }
    if error is not None:
        record["error_type"] = type(error).__name__
    try:
        _telemetry_sink(record)
    except Exception:  # noqa: BLE001 - telemetry must never break model calls.
        return
