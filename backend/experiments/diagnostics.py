"""Experiment readiness and model/reference diagnostics."""
from __future__ import annotations

from .common import (
    Any,
    Callable,
    CaseWorkspace,
    ClientBrief,
    ContentProductionConfig,
    ContentProductionWorkflow,
    ContentTask,
    EVALUATION_STATUSES,
    EXPERIMENT_EVALUATIONS_NAME,
    EXPERIMENT_MANIFEST_NAME,
    EXPERIMENT_SELECTION_NAME,
    IntentContract,
    LLMFactory,
    PROJECT_ROOT,
    Path,
    SELECTION_DECISIONS,
    TopNotesResult,
    _case_id_from_run_dir,
    _content_case_dir,
    _content_case_dir_or_none,
    _content_run_dir,
    _dedupe_strings,
    _dict_list,
    _exportable_input_files,
    _exportable_run_files,
    _file_sha256,
    _first_stage_time,
    _is_relative_to,
    _is_remote_url,
    _json_sha256,
    _read_json,
    _reference_transfer_snapshot,
    _safe_run_artifact_path,
    _slug,
    _string_list,
    _write_json,
    datetime,
    hashlib,
    importlib,
    infer_project_root_from_cases_path,
    io,
    json,
    llms,
    os,
    provider_fetchable_reference_url,
    record_content_production_artifacts,
    top_notes_result_from_dict,
    zipfile,
)


def experiment_readiness(*, project_root: str | Path = PROJECT_ROOT, environ: dict[str, str] | None = None) -> dict[str, Any]:
    """Return backend experiment readiness without exposing secrets."""

    env = os.environ if environ is None else environ
    llm_status, llm_model = _active_model_status("llm")
    vision_status, vision_model = _active_model_status("vision")
    image_status, image_model = _active_model_status("image")
    required_oss = [
        "NORI_OSS_ACCESS_KEY_ID",
        "NORI_OSS_SECRET_ACCESS_KEY",
        "NORI_OSS_BUCKET",
        "NORI_OSS_ENDPOINT",
        "NORI_OSS_REGION",
    ]
    alias_pairs = {
        "NORI_OSS_ACCESS_KEY_ID": "TOS_ACCESS_KEY_ID",
        "NORI_OSS_SECRET_ACCESS_KEY": "TOS_SECRET_ACCESS_KEY",
        "NORI_OSS_BUCKET": "TOS_BUCKET",
        "NORI_OSS_ENDPOINT": "TOS_ENDPOINT",
        "NORI_OSS_REGION": "TOS_REGION",
    }
    missing_oss = [
        name
        for name in required_oss
        if not str(env.get(name) or env.get(alias_pairs[name]) or "").strip()
    ]
    oss_configured = not missing_oss
    relay_needs_urls = bool(image_model) and getattr(image_model, "provider_id", "") == "relay"
    supports_reference = bool(image_model) and bool(getattr(image_model, "supports_reference_image", False))
    backend_public_base_url = str(env.get("NORI_BACKEND_PUBLIC_BASE_URL") or "").strip()
    backend_public_url_configured = bool(provider_fetchable_reference_url(backend_public_base_url))
    local_upload_reference_ready = supports_reference and (not relay_needs_urls or oss_configured or backend_public_url_configured)
    model_statuses = {
        "llm": llm_status,
        "vision": vision_status,
        "image": image_status,
    }
    return {
        "ready": all(bool(status.get("ready")) for status in model_statuses.values()),
        "project_root": str(Path(project_root)),
        "models": model_statuses,
        "reference_images": {
            "supports_reference_image": supports_reference,
            "provider_requires_public_urls": relay_needs_urls,
            "oss_configured": oss_configured,
            "backend_public_url_configured": backend_public_url_configured,
            "backend_public_base_url": backend_public_base_url if backend_public_url_configured else "",
            "missing_oss_env": missing_oss,
            "local_upload_reference_ready": local_upload_reference_ready,
            "strict_reference_mode_ready": local_upload_reference_ready,
        },
        "routes": {
            "upload_assets": "/sessions/{session_id}/assets",
            "asset_file": "/sessions/{session_id}/assets/{asset_id}/file",
            "publish_asset_references": "/sessions/{session_id}/assets/publish-references",
            "session_reference_image_generation_check": "/sessions/{session_id}/assets/reference-image-generation-check",
            "reference_publish_check": "/experiments/content-production/reference-publish-check",
            "reference_image_generation_check": "/experiments/content-production/reference-image-generation-check",
            "content_production_workbench": "/experiments/content-production/workbench",
            "content_production_run_template": "/experiments/content-production/run-template",
            "content_production_overview": "/experiments/content-production/overview",
            "content_production_report": "/experiments/content-production/report",
            "content_production_cases": "/experiments/content-production/cases",
            "content_production_case_selection": "/experiments/content-production/cases/{case_id}/selection",
            "content_production_case_selected_run": "/experiments/content-production/cases/{case_id}/selected-run",
            "content_production_case_compare": "/experiments/content-production/cases/{case_id}/compare",
            "content_production_case_next_actions": "/experiments/content-production/cases/{case_id}/next-actions",
            "content_production_case_promotion": "/experiments/content-production/cases/{case_id}/promotion",
            "content_production_case_replay": "/experiments/content-production/cases/{case_id}/replay",
            "content_production_case_evaluation_draft": "/experiments/content-production/cases/{case_id}/evaluations/draft",
            "content_production_case_evaluations": "/experiments/content-production/cases/{case_id}/evaluations",
            "content_production_case_delivery": "/experiments/content-production/cases/{case_id}/delivery",
            "content_production_case_delivery_export": "/experiments/content-production/cases/{case_id}/delivery/export",
            "content_production_case_timeline": "/experiments/content-production/cases/{case_id}/timeline",
            "content_production_case_export": "/experiments/content-production/cases/{case_id}/export",
            "run_content_production": "/workflows/content-production/runs",
            "preflight_content_production": "/workflows/content-production/runs/preflight",
            "list_runs": "/workflows/content-production/runs",
            "get_run": "/workflows/content-production/runs/{case_id}/{run_id}",
            "run_acceptance": "/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
            "run_evaluations": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations",
            "run_evaluation_draft": "/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft",
            "replay_run": "/workflows/content-production/runs/{case_id}/{run_id}/replay",
            "export_run": "/workflows/content-production/runs/{case_id}/{run_id}/export",
            "inspect_run_artifacts": "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
            "run_artifact_file": "/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name}",
            "list_jobs": "/experiments/jobs",
            "job_status": "/experiments/jobs/{job_id}",
            "cancel_job": "/experiments/jobs/{job_id}/cancel",
        },
    }


def content_production_diagnostics(
    *,
    project_root: str | Path = PROJECT_ROOT,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return product-facing diagnostics for backend content-production runs."""

    readiness = experiment_readiness(project_root=project_root, environ=environ)
    reference = readiness.get("reference_images") if isinstance(readiness.get("reference_images"), dict) else {}
    models = readiness.get("models") if isinstance(readiness.get("models"), dict) else {}
    checks = [
        _diagnostic_check(
            "models_ready",
            "passed" if bool(readiness.get("ready")) else "failed",
            "active LLM, vision, and image models are configured"
            if bool(readiness.get("ready"))
            else "one or more active model configurations are unavailable",
            details={
                "models": {
                    usage: {
                        "ready": bool((status or {}).get("ready")),
                        "provider_id": str((status or {}).get("provider_id") or ""),
                        "model_id": str((status or {}).get("model_id") or ""),
                        "error_type": str((status or {}).get("error_type") or ""),
                        "error": str((status or {}).get("error") or ""),
                    }
                    for usage, status in models.items()
                    if isinstance(status, dict)
                }
            },
        ),
        _diagnostic_check(
            "image_reference_capability",
            "passed" if bool(reference.get("supports_reference_image")) else "failed",
            "active image model supports reference_images"
            if bool(reference.get("supports_reference_image"))
            else "active image model does not support reference_images",
        ),
        _diagnostic_check(
            "oss_reference_storage",
            "passed" if bool(reference.get("oss_configured")) else "warning",
            "OSS reference storage is configured"
            if bool(reference.get("oss_configured"))
            else "OSS reference storage is not fully configured",
            details={"missing_env": list(reference.get("missing_oss_env") or [])},
        ),
        _diagnostic_check(
            "backend_public_url",
            "passed" if bool(reference.get("backend_public_url_configured")) else "warning",
            "backend public URL is configured"
            if bool(reference.get("backend_public_url_configured"))
            else "backend public URL is not configured",
            details={"backend_public_base_url": str(reference.get("backend_public_base_url") or "")},
        ),
        _diagnostic_check(
            "strict_reference_mode",
            "passed" if bool(reference.get("strict_reference_mode_ready")) else "failed",
            "strict reference mode can send local uploaded images to the image provider"
            if bool(reference.get("strict_reference_mode_ready"))
            else "strict reference mode cannot send local uploaded images yet",
            details={
                "provider_requires_public_urls": bool(reference.get("provider_requires_public_urls")),
                "local_upload_reference_ready": bool(reference.get("local_upload_reference_ready")),
            },
        ),
    ]
    blockers = [check for check in checks if check["status"] == "failed"]
    warnings = [check for check in checks if check["status"] == "warning"]
    return {
        "schema_version": 1,
        "ready": not blockers,
        "status": "blocked" if blockers else ("needs_configuration" if warnings else "ready"),
        "project_root": str(Path(project_root)),
        "checks": checks,
        "blocking_checks": [check["name"] for check in blockers],
        "warning_checks": [check["name"] for check in warnings],
        "recommended_actions": _diagnostic_actions(readiness, checks),
        "readiness": readiness,
        "routes": {
            "readiness": "/experiments/readiness",
            "preflight": "/workflows/content-production/runs/preflight",
            "upload_assets": "/sessions/{session_id}/assets",
            "publish_asset_references": "/sessions/{session_id}/assets/publish-references",
            "session_reference_image_generation_check": "/sessions/{session_id}/assets/reference-image-generation-check",
            "run_workflow": "/workflows/content-production/runs",
        },
    }


def _diagnostic_check(name: str, status: str, message: str, *, details: dict[str, Any] | None = None) -> dict[str, Any]:
    row: dict[str, Any] = {"name": name, "status": status, "message": message}
    if details:
        row["details"] = details
    return row


def _diagnostic_actions(readiness: dict[str, Any], checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks_by_name = {str(check.get("name") or ""): check for check in checks}
    reference = readiness.get("reference_images") if isinstance(readiness.get("reference_images"), dict) else {}
    actions: list[dict[str, Any]] = []
    if checks_by_name.get("models_ready", {}).get("status") == "failed":
        actions.append(
            {
                "action_id": "configure_active_models",
                "severity": "blocking",
                "message": "Fix active LLM, vision, and image model configuration before running live experiments.",
            }
        )
    if checks_by_name.get("image_reference_capability", {}).get("status") == "failed":
        actions.append(
            {
                "action_id": "switch_reference_image_model",
                "severity": "blocking",
                "message": "Switch active image model to one with supports_reference_image=true for strict uploaded-image experiments.",
            }
        )
    if checks_by_name.get("strict_reference_mode", {}).get("status") == "failed":
        actions.append(
            {
                "action_id": "configure_reference_transfer",
                "severity": "blocking",
                "message": "Configure OSS reference storage or NORI_BACKEND_PUBLIC_BASE_URL so local uploads become provider-fetchable HTTPS URLs.",
            }
        )
    missing = list(reference.get("missing_oss_env") or [])
    if missing:
        actions.append(
            {
                "action_id": "configure_oss_env",
                "severity": "recommended",
                "message": "Configure OSS/TOS env vars for durable reference-image publishing.",
                "env_vars": missing,
            }
        )
    if not bool(reference.get("backend_public_url_configured")):
        actions.append(
            {
                "action_id": "configure_backend_public_url",
                "severity": "recommended",
                "message": "Set NORI_BACKEND_PUBLIC_BASE_URL or pass backend_public_base_url in run/preflight requests for relay strict-reference tests.",
                "env_vars": ["NORI_BACKEND_PUBLIC_BASE_URL"],
            }
        )
    if not actions:
        actions.append(
            {
                "action_id": "run_holly_strict_smoke",
                "severity": "next_step",
                "message": "Run scripts/backend_holly_smoke.py --require-image-references to validate the full backend upload/preflight path.",
            }
        )
    return actions


def _runtime_model_snapshot() -> dict[str, Any]:
    return {
        usage: status
        for usage, (status, _model) in {
            "llm": _active_model_status("llm"),
            "vision": _active_model_status("vision"),
            "image": _active_model_status("image"),
        }.items()
    }


def _model_status(model: Any) -> dict[str, Any]:
    return {
        "ready": True,
        "key": str(getattr(model, "key", "")),
        "provider_id": str(getattr(model, "provider_id", "")),
        "model_id": str(getattr(model, "model_id", "")),
        "type": str(getattr(model, "type", "")),
        "supports_vision": bool(getattr(model, "supports_vision", False)),
        "supports_reference_image": bool(getattr(model, "supports_reference_image", False)),
    }


def _active_model_status(usage: str) -> tuple[dict[str, Any], Any | None]:
    try:
        model = llms.get_active(usage)
    except Exception as exc:  # noqa: BLE001
        return {
            "ready": False,
            "key": "",
            "provider_id": "",
            "model_id": "",
            "type": "",
            "supports_vision": False,
            "supports_reference_image": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }, None
    return _model_status(model), model
