"""Content-production preflight repair action helpers."""
from __future__ import annotations

from typing import Any

from .content_production_preflight_summaries import _provider_fetchable_urls_from_asset_summary
from .session_assets import reference_url_probe_timeout as _reference_url_probe_timeout


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
