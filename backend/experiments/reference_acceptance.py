"""Reference-image proof and acceptance checks for content-production runs."""
from __future__ import annotations

from .common import Any, _reference_transfer_snapshot


def content_production_summary_reference_transfer(summary: dict[str, Any]) -> dict[str, Any]:
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    transfer = inputs.get("reference_transfer") if isinstance(inputs.get("reference_transfer"), dict) else {}
    if not transfer:
        transfer = input_manifest.get("reference_transfer") if isinstance(input_manifest.get("reference_transfer"), dict) else {}
    if transfer:
        return dict(transfer)

    assets = inputs.get("assets") if isinstance(inputs.get("assets"), list) else input_manifest.get("assets")
    asset_rows = [dict(row) for row in assets or [] if isinstance(row, dict)]
    run_options = dict(inputs.get("run_options") or input_manifest.get("run_options") or {})
    public_map = input_manifest.get("reference_public_urls_by_path")
    return _reference_transfer_snapshot(
        asset_rows,
        reference_public_urls_by_path=dict(public_map or {}) if isinstance(public_map, dict) else {},
        require_image_references=bool(run_options.get("require_image_references")),
    )


def summary_reference_generation_check(summary: dict[str, Any]) -> dict[str, Any]:
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    reference_images = (
        experiment_manifest.get("reference_images")
        if isinstance(experiment_manifest.get("reference_images"), dict)
        else {}
    )
    latest = reference_images.get("latest_generation_check") if isinstance(reference_images.get("latest_generation_check"), dict) else {}
    if latest:
        return dict(latest)
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    check = (
        inputs.get("reference_image_generation_check")
        if isinstance(inputs.get("reference_image_generation_check"), dict)
        else {}
    )
    if check:
        return dict(check)
    check = (
        input_manifest.get("reference_image_generation_check")
        if isinstance(input_manifest.get("reference_image_generation_check"), dict)
        else {}
    )
    return dict(check or {})


def reference_transfer_proof_check(transfer: dict[str, Any], *, require_refs: bool) -> dict[str, Any]:
    selected = int(transfer.get("selected_count") or 0)
    fetchable = int(transfer.get("provider_fetchable_count") or 0)
    if require_refs and selected <= 0:
        return _proof_check("reference_transfer", "failed", "strict reference mode has no selected image assets")
    if require_refs and fetchable < selected:
        return _proof_check(
            "reference_transfer",
            "failed",
            "strict reference mode has selected images that are not provider-fetchable",
        )
    if selected > 0 and fetchable < selected:
        return _proof_check("reference_transfer", "warning", "some selected references are not provider-fetchable")
    if selected > 0:
        return _proof_check("reference_transfer", "passed", "selected references are provider-fetchable")
    return _proof_check("reference_transfer", "warning", "no image references were selected")


def reference_generation_proof_check(generation_check: dict[str, Any], *, required: bool) -> dict[str, Any]:
    ready = bool(generation_check.get("ready"))
    covers_selected = bool(generation_check.get("covers_selected_reference_images"))
    reason = str(generation_check.get("reason") or "")
    if not generation_check and not required:
        return _proof_check("reference_image_generation_check", "passed", "provider reference-image check was not required")
    if not generation_check:
        return _proof_check(
            "reference_image_generation_check",
            "failed",
            "provider reference-image check was required but no check evidence was recorded",
        )
    if ready and covers_selected:
        return _proof_check(
            "reference_image_generation_check",
            "passed",
            "provider reference-image check covers selected references",
            provider_fetchable_count=int(generation_check.get("provider_fetchable_count") or 0),
            reason=reason,
        )
    status = "failed" if required else "warning"
    missing = list(generation_check.get("missing_selected_reference_images") or [])
    if not ready:
        message = f"provider reference-image check is not ready: {reason or 'unknown'}"
    elif missing:
        message = "provider reference-image check is missing selected references"
    else:
        message = "provider reference-image check did not prove selected-reference coverage"
    return _proof_check(
        "reference_image_generation_check",
        status,
        message,
        provider_fetchable_count=int(generation_check.get("provider_fetchable_count") or 0),
        missing_selected_reference_images=missing,
        reason=reason,
    )


def reference_images_sent_proof_check(image_reference: dict[str, Any], *, require_refs: bool) -> dict[str, Any]:
    selected = int(image_reference.get("selected_count") or 0)
    sent = bool(image_reference.get("sent"))
    status = str(image_reference.get("status") or "")
    trace_count = int(image_reference.get("trace_count") or len(image_reference.get("trace") or []))
    sent_count = int(image_reference.get("trace_sent_count") or 0)
    if require_refs and not sent:
        return _proof_check(
            "reference_images_sent",
            "failed",
            "strict reference mode did not send references to the image gateway",
            trace_count=trace_count,
            sent_count=sent_count,
        )
    if selected > 0 and sent:
        return _proof_check(
            "reference_images_sent",
            "passed",
            "selected references were sent to the image gateway",
            trace_count=trace_count,
            sent_count=sent_count,
        )
    if selected > 0:
        return _proof_check(
            "reference_images_sent",
            "warning",
            f"references were selected but not sent: {status}",
            trace_count=trace_count,
            sent_count=sent_count,
        )
    return _proof_check(
        "reference_images_sent",
        "warning",
        "no image references were selected by the cover stage",
        trace_count=trace_count,
        sent_count=sent_count,
    )


def acceptance_reference_check(
    *,
    reference_required: bool,
    transfer: dict[str, Any],
    image_reference: dict[str, Any],
) -> dict[str, Any]:
    selected = int(transfer.get("selected_count") or image_reference.get("selected_count") or 0)
    fetchable = int(transfer.get("provider_fetchable_count") or 0)
    sent = bool(image_reference.get("sent"))
    if not reference_required and selected <= 0:
        return _acceptance_check(
            "strict_reference_satisfied",
            "passed",
            "strict reference mode was not required",
            required=False,
        )
    if reference_required and selected <= 0:
        return _acceptance_check(
            "strict_reference_satisfied",
            "failed",
            "strict reference mode had no selected image references",
            required=True,
        )
    if reference_required and fetchable < selected:
        return _acceptance_check(
            "strict_reference_satisfied",
            "failed",
            "strict reference mode had selected references that were not provider-fetchable",
            required=True,
            selected_count=selected,
            provider_fetchable_count=fetchable,
        )
    if reference_required and not sent:
        return _acceptance_check(
            "strict_reference_satisfied",
            "failed",
            "strict reference mode did not send references to the image provider",
            required=True,
            selected_count=selected,
            provider_fetchable_count=fetchable,
        )
    if selected > 0 and not sent:
        return _acceptance_check(
            "strict_reference_satisfied",
            "warning",
            "references were selected but not sent to the image provider",
            required=False,
            selected_count=selected,
            provider_fetchable_count=fetchable,
        )
    return _acceptance_check(
        "strict_reference_satisfied",
        "passed",
        "reference-image requirement is satisfied",
        required=reference_required,
        selected_count=selected,
        provider_fetchable_count=fetchable,
    )


def acceptance_reference_generation_check(
    *,
    generation_check_required: bool,
    generation_check: dict[str, Any],
) -> dict[str, Any]:
    ready = bool(generation_check.get("ready"))
    covers_selected = bool(generation_check.get("covers_selected_reference_images"))
    reason = str(generation_check.get("reason") or "")
    if not generation_check and not generation_check_required:
        return _acceptance_check(
            "provider_reference_check_satisfied",
            "passed",
            "provider reference-image check was not required",
            required=False,
        )
    if not generation_check:
        return _acceptance_check(
            "provider_reference_check_satisfied",
            "failed",
            "provider reference-image check was required but no check evidence was recorded",
            required=True,
        )
    if ready and covers_selected:
        return _acceptance_check(
            "provider_reference_check_satisfied",
            "passed",
            "provider reference-image check is ready and covers selected references",
            required=generation_check_required,
            reason=reason,
            provider_fetchable_count=int(generation_check.get("provider_fetchable_count") or 0),
        )
    status = "failed" if generation_check_required else "warning"
    missing = list(generation_check.get("missing_selected_reference_images") or [])
    if not ready:
        message = f"provider reference-image check is not ready: {reason or 'unknown'}"
    elif missing:
        message = "provider reference-image check does not cover selected references"
    else:
        message = "provider reference-image check did not prove selected-reference coverage"
    return _acceptance_check(
        "provider_reference_check_satisfied",
        status,
        message,
        required=generation_check_required,
        reason=reason,
        missing_selected_reference_images=missing,
        provider_fetchable_count=int(generation_check.get("provider_fetchable_count") or 0),
    )


def _proof_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if value is not None and value != ""})
    return data


def _acceptance_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if not _empty_acceptance_extra(value)})
    return data


def _empty_acceptance_extra(value: Any) -> bool:
    return value is None or value == "" or value == []


__all__ = [
    "acceptance_reference_check",
    "acceptance_reference_generation_check",
    "content_production_summary_reference_transfer",
    "reference_generation_proof_check",
    "reference_images_sent_proof_check",
    "reference_transfer_proof_check",
    "summary_reference_generation_check",
]
