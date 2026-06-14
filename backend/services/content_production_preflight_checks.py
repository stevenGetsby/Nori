"""Content-production preflight checks and gate enforcement."""
from __future__ import annotations

from typing import Any

from ..contracts import ApiError
from .content_production_preflight_actions import (
    _content_production_preflight_actions,
    _content_production_preflight_links,
)
from .content_production_preflight_summaries import (
    _asset_preflight_summary,
    _market_evidence_preflight_summary,
    _preflight_check,
    _reference_image_preflight_summary,
)


def _content_production_template_checks(
    payload: dict[str, Any],
    *,
    session_exists: bool,
    task_exists: bool,
    asset_error: str,
    selected_assets: list[dict[str, Any]],
    readiness: dict[str, Any],
    has_custom_market_collector: bool,
    enforce_model_readiness: bool,
) -> list[dict[str, str]]:
    has_goal = bool(str(payload.get("goal") or payload.get("brief_text") or "").strip())
    checks = [
        _preflight_check(
            "session",
            "passed" if session_exists else "failed",
            "session exists" if session_exists else "create or select a backend session",
        ),
        _preflight_check(
            "task",
            "passed" if task_exists else "failed",
            "task exists or will be created" if task_exists else "selected task_id does not exist in session",
        ),
        _preflight_check(
            "goal_or_brief_text",
            "passed" if has_goal else "failed",
            "goal or brief_text is ready" if has_goal else "goal or brief_text is required",
        ),
        _preflight_check(
            "asset_selection",
            "failed" if asset_error else "passed",
            asset_error or "asset selection is valid",
        ),
    ]
    checks.extend(
        _content_production_preflight_checks(
            payload,
            readiness=readiness,
            asset_rows=selected_assets,
            has_custom_market_collector=has_custom_market_collector,
        )
    )
    if not enforce_model_readiness:
        checks = [
            {
                **check,
                "status": "warning",
                "message": "model readiness is not enforced for this runner",
            }
            if check["name"] == "models_ready" and check["status"] == "failed"
            else check
            for check in checks
        ]
    return checks


def _content_production_preflight_checks(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    has_custom_market_collector: bool,
    reference_summary: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    reference = reference_summary or _reference_image_preflight_summary(payload, readiness=readiness, asset_rows=asset_rows)
    market = _market_evidence_preflight_summary(payload.get("market_evidence"))
    strict_references = bool(payload.get("require_image_references"))
    checks = [
        _preflight_check(
            "models_ready",
            "passed" if bool(readiness.get("ready")) else "failed",
            "active LLM, vision, and image model configuration is ready"
            if bool(readiness.get("ready"))
            else "one or more active model configurations are not ready",
        ),
        _preflight_check(
            "market_evidence",
            "passed" if market["provided"] or has_custom_market_collector else "failed",
            "market evidence is provided or a custom collector is configured"
            if market["provided"] or has_custom_market_collector
            else "market_evidence is required when the backend runner has no custom collector",
        ),
        _preflight_check(
            "reference_assets_selected",
            "passed" if asset_rows else ("failed" if strict_references else "warning"),
            "selected image references are available"
            if asset_rows
            else "no image reference assets are selected for this run",
        ),
    ]
    if asset_rows:
        status = "passed" if reference["can_send_selected_references"] else ("failed" if strict_references else "warning")
        checks.append(
            _preflight_check(
                "reference_transfer",
                status,
                "selected references can be sent to the image provider"
                if reference["can_send_selected_references"]
                else "selected local references need OSS or provider-fetchable HTTPS URLs before they can be sent",
            )
        )
        probe = reference.get("url_probe") if isinstance(reference.get("url_probe"), dict) else {}
        if probe.get("enabled"):
            probe_passed = bool(probe.get("passed"))
            checks.append(
                _preflight_check(
                    "reference_url_reachability",
                    "passed" if probe_passed else ("failed" if strict_references else "warning"),
                    "selected reference URLs are reachable from the backend"
                    if probe_passed
                    else "selected reference URLs could not be reached from the backend before live generation",
                )
            )
    generation_check = _reference_image_generation_gate_check(payload)
    if generation_check is not None:
        checks.append(generation_check)
    return checks


def _reference_image_generation_gate_check(payload: dict[str, Any]) -> dict[str, str] | None:
    if not bool(payload.get("require_reference_image_generation_check")):
        return None
    evidence = payload.get("reference_image_generation_check") if isinstance(
        payload.get("reference_image_generation_check"),
        dict,
    ) else {}
    ready = bool(evidence.get("ready"))
    covers_selected = bool(evidence.get("covers_selected_reference_images"))
    if ready and covers_selected:
        return _preflight_check(
            "reference_image_generation_check",
            "passed",
            "latest image-provider reference check covers the selected references",
        )
    if not evidence:
        message = "run requires a successful image-provider reference check before generation"
    elif not ready:
        reason = str(evidence.get("reason") or "not_ready")
        message = f"latest image-provider reference check is not ready: {reason}"
    else:
        missing = list(evidence.get("missing_selected_reference_images") or [])
        message = (
            "latest image-provider reference check does not cover all selected references"
            if not missing
            else f"latest image-provider reference check is missing selected references: {missing}"
        )
    return _preflight_check("reference_image_generation_check", "failed", message)


def _assert_content_production_run_gates(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    has_custom_market_collector: bool,
    enforce_model_readiness: bool = False,
) -> None:
    """Reject deterministic run blockers before task creation or model calls."""

    checked_names = {
        "market_evidence",
        "reference_assets_selected",
        "reference_transfer",
        "reference_url_reachability",
        "reference_image_generation_check",
    }
    if enforce_model_readiness:
        checked_names.add("models_ready")
    failures = [
        check
        for check in _content_production_preflight_checks(
            payload,
            readiness=readiness,
            asset_rows=asset_rows,
            has_custom_market_collector=has_custom_market_collector,
        )
        if check["name"] in checked_names and check["status"] == "failed"
    ]
    if not failures:
        return
    message = "; ".join(f"{check['name']}: {check['message']}" for check in failures)
    raise ApiError(
        f"content-production run preflight failed: {message}",
        status_code=400,
        data={
            "checks": failures,
            "actions": _content_production_preflight_actions(
                payload,
                checks=failures,
                session_id=str(payload.get("session_id") or ""),
                asset_summary=_asset_preflight_summary(asset_rows),
            ),
            "links": _content_production_preflight_links(payload, session_id=str(payload.get("session_id") or "")),
        },
    )
