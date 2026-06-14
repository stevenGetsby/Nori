"""Content-production run payload helpers."""
from __future__ import annotations

from typing import Any

from ..contracts import ApiError, ContentProductionRunRequest


def _model_data(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _execution_mode(value: Any) -> str:
    mode = str(value or "sync").strip().lower()
    if mode in {"sync", "synchronous"}:
        return "sync"
    if mode in {"background", "async"}:
        return "background"
    raise ApiError(f"unsupported execution_mode: {value}", status_code=400)


_REPLAY_OVERRIDE_FIELDS = {
    "session_id",
    "task_id",
    "goal",
    "brief_text",
    "case_id",
    "case_title",
    "platform",
    "asset_ids",
    "asset_paths",
    "backend_public_base_url",
    "execution_mode",
    "human_gate_mode",
    "require_image_references",
    "require_reference_image_generation_check",
    "verify_reference_urls",
    "reference_url_probe_timeout",
    "market_evidence",
    "config",
    "metadata",
}


def _content_run_request_fields() -> set[str]:
    fields = getattr(ContentProductionRunRequest, "model_fields", None) or getattr(ContentProductionRunRequest, "__fields__", {})
    return set(fields)


def _replay_payload_with_overrides(
    replay_payload: dict[str, Any],
    replay_data: dict[str, Any],
    *,
    source_case_id: str,
    source_run_id: str,
) -> dict[str, Any]:
    run_fields = _content_run_request_fields()
    payload = {key: value for key, value in replay_payload.items() if key in run_fields}
    overrides = dict(replay_data.get("overrides") or {})
    invalid = sorted(key for key in overrides if key not in _REPLAY_OVERRIDE_FIELDS)
    if invalid:
        raise ApiError(f"unsupported replay override fields: {invalid}", status_code=400)
    payload.update({key: value for key, value in overrides.items() if key in run_fields})

    for key in ("case_id", "case_title", "execution_mode", "human_gate_mode", "backend_public_base_url"):
        value = str(replay_data.get(key) or "").strip()
        if value:
            payload[key] = value
    if replay_data.get("require_image_references") is not None:
        payload["require_image_references"] = bool(replay_data["require_image_references"])
    if replay_data.get("require_reference_image_generation_check") is not None:
        payload["require_reference_image_generation_check"] = bool(
            replay_data["require_reference_image_generation_check"]
        )
    if replay_data.get("verify_reference_urls") is not None:
        payload["verify_reference_urls"] = bool(replay_data["verify_reference_urls"])
    if replay_data.get("reference_url_probe_timeout") is not None:
        payload["reference_url_probe_timeout"] = replay_data["reference_url_probe_timeout"]

    original_metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    metadata = dict(original_metadata)
    replay_metadata = replay_data.get("metadata") if isinstance(replay_data.get("metadata"), dict) else {}
    metadata.update(replay_metadata)
    metadata["replay_of"] = {"case_id": source_case_id, "run_id": source_run_id}
    metadata.setdefault("source", "backend.replay_content_production_run")
    payload["metadata"] = metadata

    payload["_explicit_session_id"] = str(replay_data.get("session_id") or overrides.get("session_id") or "").strip()
    payload["_explicit_task_id"] = str(replay_data.get("task_id") or overrides.get("task_id") or "").strip()
    payload.setdefault("execution_mode", "sync")
    payload.setdefault("human_gate_mode", "skip")
    payload.setdefault("asset_ids", [])
    payload.setdefault("asset_paths", [])
    return payload
