"""Content-production preflight summary helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..reference_urls import provider_fetchable_reference_url
from .session_assets import (
    backend_public_base_url as _backend_public_base_url,
    is_remote_url as _is_remote_url,
    reference_url_probe_summary as _reference_url_probe_summary,
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


def _reference_fetchable_url(row: dict[str, Any]) -> str:
    public_url = str(row.get("public_reference_url") or "").strip()
    path = str(row.get("path") or "").strip()
    fetchable = provider_fetchable_reference_url(public_url)
    if fetchable:
        return fetchable
    return provider_fetchable_reference_url(path)
