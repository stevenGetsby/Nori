"""Reference-image result and action payload helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..reference_urls import provider_fetchable_reference_url


def _asset_publish_result(row: dict[str, Any], *, public_reference_url: str, reason: str) -> dict[str, Any]:
    path = str(row.get("path") or "")
    return {
        "asset_id": str(row.get("asset_id") or ""),
        "filename": str(row.get("filename") or Path(path).name),
        "path": path,
        "public_reference_url": public_reference_url,
        "reason": reason,
    }


def _reference_publish_check_result(
    *,
    ready: bool,
    path: Path,
    reason: str,
    public_reference_url: str = "",
    object_key: str = "",
    uploaded: bool = False,
    error_type: str = "",
    error: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ready": bool(ready),
        "reason": reason,
        "public_reference_url": public_reference_url,
        "provider_fetchable": bool(provider_fetchable_reference_url(public_reference_url)),
        "uploaded": bool(uploaded),
        "object_key": object_key,
        "test_image": {
            "filename": path.name,
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "content_type": "image/png",
        },
        "error_type": error_type,
        "error": error,
        "metadata": dict(metadata or {}),
        "next_actions": _reference_publish_check_actions(ready=ready, reason=reason, error=error),
    }


def _reference_publish_check_actions(*, ready: bool, reason: str, error: str) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_preflight",
                "severity": "next_step",
                "message": "Run content-production preflight with require_image_references=true.",
            }
        ]
    actions = [
        {
            "action_id": "configure_reference_publisher",
            "severity": "blocking",
            "message": "Configure OSS/TOS env vars or backend_public_base_url so reference images become HTTPS URLs.",
        }
    ]
    if reason == "object_store_error" or error:
        actions.append(
            {
                "action_id": "check_object_store_permissions",
                "severity": "blocking",
                "message": "Check object store credentials, bucket, endpoint, region, and write permissions.",
            }
        )
    return actions


def _reference_image_generation_check_result(
    *,
    ready: bool,
    reason: str,
    prompt: str,
    reference_images: list[str],
    provider_fetchable_refs: list[str],
    size: str,
    image_count: int = 0,
    first_image_preview: str = "",
    error_type: str = "",
    error: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ready": bool(ready),
        "reason": reason,
        "prompt": prompt,
        "size": size,
        "reference_count": len(reference_images),
        "provider_fetchable_count": len(provider_fetchable_refs),
        "reference_images": list(reference_images),
        "provider_fetchable_reference_images": list(provider_fetchable_refs),
        "image_count": int(image_count),
        "first_image_preview": first_image_preview,
        "error_type": error_type,
        "error": error,
        "metadata": dict(metadata or {}),
        "next_actions": _reference_image_generation_check_actions(ready=ready, reason=reason),
    }


def _reference_image_generation_check_actions(*, ready: bool, reason: str) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_content_production",
                "severity": "next_step",
                "message": "Run the full content-production workflow with require_image_references=true.",
            }
        ]
    if reason == "invalid_reference_images":
        return [
            {
                "action_id": "publish_reference_assets",
                "severity": "blocking",
                "message": "Publish uploaded assets to provider-fetchable HTTPS URLs before checking image generation.",
            }
        ]
    return [
        {
            "action_id": "inspect_image_model_config",
            "severity": "blocking",
            "message": "Inspect active image model configuration and provider reference-image support.",
        }
    ]


def _provider_fetchable_urls_from_publish_result(publish: dict[str, Any]) -> list[str]:
    assets = publish.get("assets") if isinstance(publish.get("assets"), list) else []
    urls: list[str] = []
    for item in assets:
        if not isinstance(item, dict):
            continue
        url = provider_fetchable_reference_url(str(item.get("public_reference_url") or ""))
        if url:
            urls.append(url)
    return list(dict.fromkeys(urls))


def _session_reference_image_generation_check_result(
    *,
    ready: bool,
    reason: str,
    publish: dict[str, Any],
    generation: dict[str, Any] | None,
    reference_images: list[str],
    url_probe: dict[str, Any] | None,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    failed_publish = int(publish.get("failed_count") or 0) if isinstance(publish, dict) else 0
    return {
        "ready": bool(ready),
        "reason": reason,
        "selected_count": int(publish.get("selected_count") or 0) if isinstance(publish, dict) else 0,
        "published_count": int(publish.get("published_count") or 0) if isinstance(publish, dict) else 0,
        "failed_count": failed_publish,
        "provider_fetchable_count": len(reference_images),
        "provider_fetchable_reference_images": list(reference_images),
        "publish": dict(publish or {}),
        "url_probe": dict(url_probe or {}),
        "generation": dict(generation or {}),
        "metadata": dict(metadata or {}),
        "next_actions": _session_reference_image_generation_check_actions(
            ready=bool(ready),
            reason=reason,
            failed_publish=failed_publish,
        ),
    }


def _session_reference_image_generation_event_payload(result: dict[str, Any]) -> dict[str, Any]:
    generation = result.get("generation") if isinstance(result.get("generation"), dict) else {}
    url_probe = result.get("url_probe") if isinstance(result.get("url_probe"), dict) else {}
    return {
        "ready": bool(result.get("ready")),
        "reason": str(result.get("reason") or ""),
        "selected_count": int(result.get("selected_count") or 0),
        "published_count": int(result.get("published_count") or 0),
        "failed_count": int(result.get("failed_count") or 0),
        "provider_fetchable_count": int(result.get("provider_fetchable_count") or 0),
        "provider_fetchable_reference_images": list(result.get("provider_fetchable_reference_images") or []),
        "url_probe": {
            "enabled": bool(url_probe.get("enabled")),
            "passed": bool(url_probe.get("passed")),
            "checked_count": int(url_probe.get("checked_count") or 0),
            "reachable_count": int(url_probe.get("reachable_count") or 0),
            "failed_count": int(url_probe.get("failed_count") or 0),
        },
        "generation": {
            "ready": bool(generation.get("ready")),
            "reason": str(generation.get("reason") or ""),
            "image_count": int(generation.get("image_count") or 0),
            "error_type": str(generation.get("error_type") or ""),
            "error": str(generation.get("error") or ""),
        },
        "metadata": dict(result.get("metadata") or {}),
    }


def _session_reference_image_generation_check_actions(
    *,
    ready: bool,
    reason: str,
    failed_publish: int,
) -> list[dict[str, str]]:
    if ready:
        return [
            {
                "action_id": "run_strict_preflight",
                "severity": "next_step",
                "message": "Run strict reference preflight or the full content-production experiment.",
            }
        ]
    if reason == "no_provider_fetchable_reference_images" or failed_publish:
        return [
            {
                "action_id": "set_backend_public_base_url_or_configure_oss",
                "severity": "blocking",
                "message": "Provide a real backend_public_base_url or configure OSS so session assets become public HTTPS references.",
            }
        ]
    if reason == "reference_url_probe_failed":
        return [
            {
                "action_id": "fix_reference_url_reachability",
                "severity": "blocking",
                "message": "Fix the backend public URL, HTTPS tunnel, CDN, or object-store public access before calling the image model.",
            }
        ]
    return [
        {
            "action_id": "inspect_image_model_config",
            "severity": "blocking",
            "message": "Inspect active image model configuration and provider reference-image support.",
        }
    ]
