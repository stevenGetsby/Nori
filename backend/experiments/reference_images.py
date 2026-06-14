"""Reference-image summary and trace projections for experiment runs."""
from __future__ import annotations

from .common import Any, Path, _read_json, provider_fetchable_reference_url


def image_reference_summary(run_dir: str | Path, *, require_image_references: bool = False) -> dict[str, Any]:
    summary = image_reference_from_package(_read_json(Path(run_dir) / "content_package.json"))
    summary["required"] = bool(require_image_references)
    if require_image_references and summary.get("selected_count") and not summary.get("sent"):
        summary["status"] = "failed_required"
    return summary


def image_reference_from_package(package: dict[str, Any]) -> dict[str, Any]:
    cover_result = ((package.get("prompts") or {}).get("cover_result") or {})
    extra = cover_result.get("extra") or {}
    selected_paths = list(cover_result.get("reference_paths") or [])
    sent = bool(extra.get("reference_images_sent"))
    fallback = str(extra.get("reference_image_fallback") or "")
    status = "not_selected"
    if selected_paths and sent:
        status = "sent"
    elif selected_paths and fallback:
        status = "fallback"
    elif selected_paths:
        status = "selected_not_sent"
    return {
        "status": status,
        "required": False,
        "selected_count": len(selected_paths),
        "selected_paths": selected_paths,
        "sent": sent,
        "fallback": fallback,
        "uploaded": bool(extra.get("reference_images_uploaded")),
        "upload_count": int(extra.get("reference_upload_count") or 0),
        "object_keys": list(extra.get("reference_object_keys") or []),
        "public_urls": list(extra.get("reference_public_urls") or []),
        "trace": _image_reference_trace_from_cover_result(
            selected_paths=selected_paths,
            extra=extra,
            sent=sent,
        ),
    }


def _image_reference_trace_from_cover_result(
    *,
    selected_paths: list[Any],
    extra: dict[str, Any],
    sent: bool,
) -> list[dict[str, Any]]:
    """Build per-reference evidence from the cover package, compatible with old runs."""

    published_items = [item for item in extra.get("reference_items") or [] if isinstance(item, dict)]
    public_urls = [str(value) for value in extra.get("reference_public_urls") or [] if str(value or "").strip()]
    object_keys = [str(value) for value in extra.get("reference_object_keys") or [] if str(value or "").strip()]
    trace: list[dict[str, Any]] = []
    for index, raw_path in enumerate(selected_paths):
        selected_path = str(raw_path or "")
        item = _published_reference_for_path(selected_path, published_items, index=index)
        public_url = str(item.get("public_url") or item.get("url_public") or "")
        if not public_url and index < len(public_urls):
            public_url = public_urls[index]
        object_key = str(item.get("key") or "")
        if not object_key and index < len(object_keys):
            object_key = object_keys[index]
        model_input = str(item.get("url") or public_url or "")
        provider_fetchable_url = provider_fetchable_reference_url(public_url) or provider_fetchable_reference_url(selected_path)
        trace.append(
            {
                "index": index,
                "selected_path": selected_path,
                "public_url": public_url,
                "provider_fetchable_url": provider_fetchable_url,
                "provider_fetchable": bool(provider_fetchable_url),
                "object_key": object_key,
                "publish_reason": str(item.get("reason") or ""),
                "uploaded": bool(item.get("uploaded")) if item else False,
                "sent": bool(sent),
                "model_input_type": "url" if model_input.startswith(("http://", "https://")) else ("bytes" if sent else ""),
            }
        )
    return trace


def _published_reference_for_path(path: str, items: list[dict[str, Any]], *, index: int) -> dict[str, Any]:
    if index < len(items):
        return dict(items[index])
    for item in items:
        if str(item.get("original_path") or "") == path:
            return dict(item)
    return {}


def _image_reference_trace_with_transfer(
    image_reference: dict[str, Any],
    transfer: dict[str, Any],
) -> list[dict[str, Any]]:
    trace = [dict(item) for item in image_reference.get("trace") or [] if isinstance(item, dict)]
    transfer_items = [dict(item) for item in transfer.get("items") or [] if isinstance(item, dict)]
    if not trace:
        selected_count = int(image_reference.get("selected_count") or 0)
        required = bool(image_reference.get("required") or transfer.get("required"))
        if selected_count > 0 or required:
            trace = [
                _trace_from_transfer_item(item, index=index, sent=bool(image_reference.get("sent")))
                for index, item in enumerate(transfer_items)
            ]
    if not transfer_items:
        return trace
    return [_merge_trace_transfer_item(item, transfer_items) for item in trace]


def _trace_from_transfer_item(item: dict[str, Any], *, index: int, sent: bool) -> dict[str, Any]:
    provider_fetchable_url = str(item.get("provider_fetchable_url") or "")
    return {
        "index": index,
        "asset_id": str(item.get("asset_id") or ""),
        "filename": str(item.get("filename") or ""),
        "selected_path": str(item.get("path") or ""),
        "public_url": str(item.get("public_reference_url") or ""),
        "provider_fetchable_url": provider_fetchable_url,
        "provider_fetchable": bool(provider_fetchable_url or item.get("provider_fetchable")),
        "sent": sent,
    }


def _merge_trace_transfer_item(trace_item: dict[str, Any], transfer_items: list[dict[str, Any]]) -> dict[str, Any]:
    match = _match_transfer_item(trace_item, transfer_items)
    if not match:
        return trace_item
    merged = dict(trace_item)
    for key, value in {
        "asset_id": str(match.get("asset_id") or ""),
        "filename": str(match.get("filename") or ""),
        "input_path": str(match.get("path") or ""),
        "transfer_public_reference_url": str(match.get("public_reference_url") or ""),
        "transfer_provider_fetchable_url": str(match.get("provider_fetchable_url") or ""),
    }.items():
        if value:
            merged[key] = value
    if not merged.get("provider_fetchable_url") and match.get("provider_fetchable_url"):
        merged["provider_fetchable_url"] = str(match.get("provider_fetchable_url") or "")
    merged["provider_fetchable"] = bool(merged.get("provider_fetchable") or match.get("provider_fetchable"))
    return merged


def _match_transfer_item(trace_item: dict[str, Any], transfer_items: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = {
        str(trace_item.get("selected_path") or ""),
        str(trace_item.get("public_url") or ""),
        str(trace_item.get("provider_fetchable_url") or ""),
    }
    for item in transfer_items:
        values = {
            str(item.get("path") or ""),
            str(item.get("public_reference_url") or ""),
            str(item.get("provider_fetchable_url") or ""),
        }
        if candidates.intersection(value for value in values if value):
            return item
    return {}


def _enrich_image_reference_trace(image_reference: dict[str, Any], transfer: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(image_reference)
    trace = _image_reference_trace_with_transfer(enriched, transfer)
    if trace:
        enriched["trace"] = trace
        enriched["trace_count"] = len(trace)
        enriched["trace_provider_fetchable_count"] = sum(1 for item in trace if item.get("provider_fetchable"))
        enriched["trace_sent_count"] = sum(1 for item in trace if item.get("sent"))
    return enriched


__all__ = ["_enrich_image_reference_trace", "image_reference_from_package", "image_reference_summary"]
