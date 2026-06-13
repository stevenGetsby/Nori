"""Content-production preflight policy and action helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..contracts import ApiError
from ..reference_urls import provider_fetchable_reference_url
from .session_assets import (
    backend_public_base_url as _backend_public_base_url,
    is_remote_url as _is_remote_url,
    reference_url_probe_summary as _reference_url_probe_summary,
    reference_url_probe_timeout as _reference_url_probe_timeout,
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


def _content_production_template_actions(
    payload: dict[str, Any],
    *,
    checks: list[dict[str, str]],
    session_id: str,
    asset_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    failed = {check["name"] for check in checks if check["status"] == "failed"}
    actions: list[dict[str, Any]] = []
    if "session" in failed:
        actions.append(
            {
                "action_id": "create_session",
                "severity": "blocking",
                "method": "POST",
                "href": "/sessions",
                "payload": {"metadata": _template_session_metadata(payload)},
                "message": "Create a backend session before uploading assets or running the experiment.",
            }
        )
    if "goal_or_brief_text" in failed:
        actions.append(
            {
                "action_id": "add_brief",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["goal", "brief_text"],
                "message": "Add goal or brief_text to the run request template.",
            }
        )
    if "asset_selection" in failed:
        actions.append(
            {
                "action_id": "fix_asset_selection",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "payload": {"usage": "reference"},
                "input_fields": ["asset_ids", "asset_paths", "files"],
                "message": "Remove missing asset_ids or upload the referenced assets into this session.",
            }
        )
    if "models_ready" in failed:
        actions.append(
            {
                "action_id": "configure_active_models",
                "severity": "blocking",
                "method": "GET",
                "href": "/experiments/readiness",
                "message": "Fix active LLM, vision, or image model configuration before running.",
            }
        )
    if "market_evidence" in failed:
        actions.append(
            {
                "action_id": "attach_market_evidence",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["market_evidence"],
                "message": "Attach market_evidence or configure a backend collector before running.",
            }
        )
    if "reference_assets_selected" in failed:
        actions.append(
            {
                "action_id": "upload_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "message": "Upload or select image assets for strict reference mode.",
            }
        )
    if "reference_transfer" in failed:
        actions.append(
            {
                "action_id": "publish_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": (
                    f"/sessions/{session_id}/assets/publish-references"
                    if session_id
                    else "/sessions/{session_id}/assets/publish-references"
                ),
                "payload": _publish_reference_action_payload(payload),
                "message": "Publish selected assets or configure backend_public_base_url so the image provider can fetch references.",
            }
        )
    if "reference_image_generation_check" in failed:
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
            required=True,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    if not failed:
        actions.extend(
            [
                {
                    "action_id": "run_preflight",
                    "severity": "next_step",
                    "method": "POST",
                    "href": "/workflows/content-production/runs/preflight",
                    "payload": payload,
                    "message": "Run preflight with this request before live generation.",
                },
                {
                    "action_id": "run_experiment",
                    "severity": "next_step",
                    "method": "POST",
                    "href": "/workflows/content-production/runs",
                    "payload": payload,
                    "message": "Run the backend content-production experiment.",
                },
            ]
        )
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    return actions


def _template_session_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for key in ("case_id", "case_title", "goal", "brief_text", "platform", "backend_public_base_url"):
        value = payload.get(key)
        if value:
            metadata[key] = value
    for key in ("market_evidence", "config"):
        value = payload.get(key)
        if isinstance(value, dict) and value:
            metadata[key] = dict(value)
    return metadata


def _publish_reference_action_payload(payload: dict[str, Any]) -> dict[str, Any]:
    action_payload: dict[str, Any] = {"asset_ids": list(payload.get("asset_ids") or [])}
    backend_public_base_url = str(payload.get("backend_public_base_url") or "").strip()
    if backend_public_base_url:
        action_payload["backend_public_base_url"] = backend_public_base_url
    return action_payload


def _reference_image_generation_action(
    payload: dict[str, Any],
    *,
    session_id: str,
    asset_summary: dict[str, Any] | None,
    required: bool = False,
) -> dict[str, Any] | None:
    if not bool(payload.get("require_image_references")):
        return None
    urls = _provider_fetchable_urls_from_asset_summary(asset_summary)
    if not urls:
        return None
    asset_ids = [str(value) for value in payload.get("asset_ids") or [] if str(value)]
    if session_id and asset_ids:
        return {
            "action_id": "check_reference_image_generation",
            "severity": "blocking" if required else "optional",
            "method": "POST",
            "href": f"/sessions/{session_id}/assets/reference-image-generation-check",
            "payload": {
                "asset_ids": asset_ids,
                "backend_public_base_url": str(payload.get("backend_public_base_url") or ""),
                "verify_reference_urls": bool(payload.get("verify_reference_urls")),
                "reference_url_probe_timeout": _reference_url_probe_timeout(payload),
                "prompt": "Generate a simple product image using the selected session reference image.",
                "size": "1024x1024",
                "metadata": {
                    "source": "content_production_preflight",
                    "case_id": str(payload.get("case_id") or ""),
                },
            },
            "message": (
                "Publish selected session assets and verify that the active image provider accepts them as "
                "reference_images before this strict run."
                if required
                else "Optionally publish selected session assets and verify that the active image provider accepts them as reference_images before the full run."
            ),
        }
    return {
        "action_id": "check_reference_image_generation",
        "severity": "blocking" if required else "optional",
        "method": "POST",
        "href": "/experiments/content-production/reference-image-generation-check",
        "payload": {
            "prompt": "Generate a simple product image using the selected reference image.",
            "reference_images": urls,
            "size": "1024x1024",
            "metadata": {
                "source": "content_production_preflight",
                "case_id": str(payload.get("case_id") or ""),
            },
        },
        "message": (
            "Verify that the active image provider accepts these reference_images before this strict run."
            if required
            else "Optionally verify that the active image provider accepts these reference_images before the full run."
        ),
    }


def _provider_fetchable_urls_from_asset_summary(asset_summary: dict[str, Any] | None) -> list[str]:
    summary = asset_summary if isinstance(asset_summary, dict) else {}
    items = summary.get("items") if isinstance(summary.get("items"), list) else []
    urls: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = provider_fetchable_reference_url(str(item.get("provider_fetchable_url") or ""))
        if url:
            urls.append(url)
    return list(dict.fromkeys(urls))


def _content_production_preflight_actions(
    payload: dict[str, Any],
    *,
    checks: list[dict[str, str]],
    session_id: str,
    asset_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    failed = {check["name"] for check in checks if check["status"] == "failed"}
    if not failed:
        actions = [
            {
                "action_id": "run_experiment",
                "severity": "next_step",
                "method": "POST",
                "href": "/workflows/content-production/runs",
                "payload": payload,
                "message": "Run the backend content-production experiment with the preflight-validated request.",
            }
        ]
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
        )
        if reference_check_action:
            actions.append(reference_check_action)
        return actions

    actions: list[dict[str, Any]] = []
    if "models_ready" in failed:
        actions.append(
            {
                "action_id": "configure_active_models",
                "severity": "blocking",
                "method": "GET",
                "href": "/experiments/readiness",
                "message": "Fix active LLM, vision, or image model configuration before running.",
            }
        )
    if "market_evidence" in failed:
        actions.append(
            {
                "action_id": "attach_market_evidence",
                "severity": "blocking",
                "method": "POST",
                "href": "/experiments/content-production/run-template",
                "payload": payload,
                "input_fields": ["market_evidence"],
                "message": "Attach market_evidence or configure a backend collector before running.",
            }
        )
    if "reference_assets_selected" in failed:
        actions.append(
            {
                "action_id": "upload_reference_assets",
                "severity": "blocking",
                "method": "POST",
                "href": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "payload": {"usage": "reference"},
                "input_fields": ["asset_ids", "asset_paths", "files"],
                "message": "Upload or select image assets for strict reference mode.",
            }
        )
    if "reference_transfer" in failed:
        actions.extend(
            [
                {
                    "action_id": "publish_reference_assets",
                    "severity": "blocking",
                    "method": "POST",
                    "href": (
                        f"/sessions/{session_id}/assets/publish-references"
                        if session_id
                        else "/sessions/{session_id}/assets/publish-references"
                    ),
                    "payload": _publish_reference_action_payload(payload),
                    "message": "Publish selected assets so the image provider can fetch reference images.",
                },
                {
                    "action_id": "set_backend_public_base_url",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/experiments/content-production/run-template",
                    "payload": payload,
                    "input_fields": ["backend_public_base_url"],
                    "message": "Provide a backend_public_base_url when local uploads should be served through the backend.",
                },
            ]
        )
    if "reference_url_reachability" in failed:
        actions.extend(
            [
                {
                    "action_id": "verify_reference_urls",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/workflows/content-production/runs/preflight",
                    "payload": {**payload, "verify_reference_urls": True},
                    "input_fields": ["backend_public_base_url", "verify_reference_urls"],
                    "message": "Verify that selected reference URLs can be reached before live strict-reference generation.",
                },
                {
                    "action_id": "set_backend_public_base_url",
                    "severity": "blocking",
                    "method": "POST",
                    "href": "/experiments/content-production/run-template",
                    "payload": payload,
                    "input_fields": ["backend_public_base_url"],
                    "message": "Provide a reachable public backend URL, HTTPS tunnel, or OSS reference URL.",
                },
            ]
        )
    if "reference_image_generation_check" in failed:
        reference_check_action = _reference_image_generation_action(
            payload,
            session_id=session_id,
            asset_summary=asset_summary,
            required=True,
        )
        if reference_check_action:
            actions.append(reference_check_action)
    return actions


def _content_production_preflight_links(payload: dict[str, Any], *, session_id: str) -> dict[str, str]:
    case_id = str(payload.get("case_id") or "")
    template = "/experiments/content-production/run-template"
    if case_id:
        template = f"{template}?case_id={case_id}"
    return {
        "run_template": template,
        "run": "/workflows/content-production/runs",
        "preflight": "/workflows/content-production/runs/preflight",
        "upload_assets": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
        "publish_references": (
            f"/sessions/{session_id}/assets/publish-references"
            if session_id
            else "/sessions/{session_id}/assets/publish-references"
        ),
    }


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


def _preflight_check(name: str, status: str, message: str) -> dict[str, str]:
    return {"name": name, "status": status, "message": message}


def _asset_preflight_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fetchable = [_reference_fetchable_url(row) for row in rows]
    return {
        "selected_count": len(rows),
        "local_count": sum(1 for row in rows if not _is_remote_url(str(row.get("path") or ""))),
        "remote_count": sum(1 for row in rows if _is_remote_url(str(row.get("path") or ""))),
        "provider_fetchable_count": sum(1 for value in fetchable if value),
        "items": [
            {
                "asset_id": str(row.get("asset_id") or ""),
                "kind": str(row.get("kind") or ""),
                "filename": str(row.get("filename") or Path(str(row.get("path") or "")).name),
                "path": str(row.get("path") or ""),
                "public_reference_url": str(row.get("public_reference_url") or ""),
                "provider_fetchable_url": fetchable_url,
            }
            for row, fetchable_url in zip(rows, fetchable)
        ],
    }


def _market_evidence_preflight_summary(value: Any) -> dict[str, Any]:
    evidence = value if isinstance(value, dict) else {}
    return {
        "provided": bool(evidence),
        "queries": [str(item) for item in evidence.get("queries") or []],
        "hot_note_count": len(evidence.get("hot_notes") or []),
        "insufficient_count": len(evidence.get("insufficient") or []),
    }


def _reference_image_preflight_summary(
    payload: dict[str, Any],
    *,
    readiness: dict[str, Any],
    asset_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    reference_readiness = readiness.get("reference_images") if isinstance(readiness.get("reference_images"), dict) else {}
    fetchable = [_reference_fetchable_url(row) for row in asset_rows]
    probe = _reference_url_probe_summary(payload, fetchable)
    supports_reference = bool(reference_readiness.get("supports_reference_image"))
    provider_requires_public_urls = bool(reference_readiness.get("provider_requires_public_urls"))
    oss_configured = bool(reference_readiness.get("oss_configured"))
    can_send = supports_reference and bool(asset_rows)
    if can_send and provider_requires_public_urls:
        can_send = oss_configured or all(bool(value) for value in fetchable)
    if can_send and probe["enabled"]:
        can_send = bool(probe["passed"])
    return {
        "required": bool(payload.get("require_image_references")),
        "generation_check_required": bool(payload.get("require_reference_image_generation_check")),
        "supports_reference_image": supports_reference,
        "provider_requires_public_urls": provider_requires_public_urls,
        "oss_configured": oss_configured,
        "backend_public_base_url": _backend_public_base_url(str(payload.get("backend_public_base_url") or "")),
        "selected_count": len(asset_rows),
        "provider_fetchable_count": sum(1 for value in fetchable if value),
        "can_send_selected_references": can_send,
        "strict_reference_mode_ready": can_send if bool(payload.get("require_image_references")) else bool(
            reference_readiness.get("strict_reference_mode_ready")
        ),
        "url_probe": probe,
        "missing_oss_env": list(reference_readiness.get("missing_oss_env") or []),
    }


def _reference_fetchable_url(row: dict[str, Any]) -> str:
    public_url = str(row.get("public_reference_url") or "").strip()
    path = str(row.get("path") or "").strip()
    fetchable = provider_fetchable_reference_url(public_url)
    if fetchable:
        return fetchable
    return provider_fetchable_reference_url(path)
