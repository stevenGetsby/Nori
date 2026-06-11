"""Backend adapters for executable Nori experiments."""
from __future__ import annotations

import json
import os
import hashlib
import inspect
import importlib
import io
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from data_collect.adapter import TopNotesResult
import nori.core.llms as llms
from nori.core import CaseWorkspace, ClientBrief, ContentTask, IntentContract, LLMFactory
from nori.workflows.content_production import (
    ContentProductionConfig,
    ContentProductionWorkflow,
    record_content_production_artifacts,
    top_notes_result_from_dict,
)

from .reference_urls import provider_fetchable_reference_url


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_MANIFEST_NAME = "experiment_manifest.json"
EXPERIMENT_EVALUATIONS_NAME = "experiment_evaluations.json"
EXPERIMENT_SELECTION_NAME = "experiment_selection.json"
EVALUATION_STATUSES = {"passed", "needs_revision", "blocked", "pending"}
SELECTION_DECISIONS = {"selected", "promoted", "needs_revision", "rejected", "archived"}


class ContentProductionRunFailed(RuntimeError):
    """Workflow failed after a run workspace and failure manifest were written."""

    def __init__(self, original: Exception, *, failure_result: dict[str, Any]) -> None:
        self.original = original
        self.failure_result = dict(failure_result)
        self.original_error_type = type(original).__name__
        self.original_message = str(original)
        super().__init__(f"{self.original_error_type}: {self.original_message}")


class ContentProductionExperimentRunner:
    """Run content-production from backend-owned session/task inputs."""

    def __init__(
        self,
        *,
        project_root: str | Path = PROJECT_ROOT,
        llm_factory: LLMFactory | None = None,
        workflow_factory: Callable[[ContentProductionConfig], Any] | None = None,
        top_notes_collector: Callable[..., TopNotesResult] | None = None,
    ) -> None:
        self.project_root = Path(project_root)
        self.llm_factory = llm_factory
        self.workflow_factory = workflow_factory or (lambda config: ContentProductionWorkflow(config=config))
        self.top_notes_collector = top_notes_collector

    def run(
        self,
        request: dict[str, Any],
        *,
        session_id: str,
        task_id: str,
        asset_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        brief_text = str(request.get("brief_text") or request.get("goal") or "").strip()
        if not brief_text:
            raise ValueError("brief_text or goal is required")

        config = _config_from_request(request, brief_text=brief_text)
        case = CaseWorkspace(
            self.project_root,
            case_id=str(request.get("case_id") or session_id),
            title=str(request.get("case_title") or request.get("case_id") or session_id),
        ).ensure()
        run_dir = case.create_run_dir(
            config.workflow_name,
            at=datetime.now(),
            metadata={
                "source": "backend",
                "session_id": session_id,
                "task_id": task_id,
                **dict(request.get("metadata") or {}),
            },
        )
        market_dir = run_dir / "market"
        covers_dir = run_dir / "covers"
        market_dir.mkdir(parents=True, exist_ok=True)
        covers_dir.mkdir(parents=True, exist_ok=True)

        brief_path = run_dir / "original_brief.md"
        brief_path.write_text(brief_text, encoding="utf-8")
        reference_public_urls_by_path = _reference_public_urls_by_path(asset_rows)
        replay_request = _replay_request(request, session_id=session_id, task_id=task_id, asset_rows=asset_rows)
        _write_json(run_dir / "replay_request.json", replay_request)
        input_manifest = _input_manifest(
            request=request,
            session_id=session_id,
            task_id=task_id,
            brief_text=brief_text,
            brief_path=brief_path,
            asset_rows=asset_rows,
            reference_public_urls_by_path=reference_public_urls_by_path,
            replay_request_path=run_dir / "replay_request.json",
        )
        _write_json(run_dir / "input_manifest.json", input_manifest)
        case.record_artifact(
            run_id=run_dir.name,
            artifact_type="original_brief",
            path=brief_path,
            created_by="user",
            status="source",
        )
        for index, row in enumerate(asset_rows, start=1):
            path = Path(str(row.get("path") or ""))
            if path.is_file():
                case.record_artifact(
                    run_id=run_dir.name,
                    artifact_type=f"input_asset_{index}",
                    path=path,
                    created_by="user",
                    status="source",
                    metadata={"asset_id": row.get("asset_id"), "filename": row.get("filename")},
                )

        workflow = self.workflow_factory(config)
        state = workflow.initial_state(
            run_dir=run_dir,
            market_dir=market_dir,
            covers_dir=covers_dir,
            llm_factory=self.llm_factory or _default_llm_factory(),
            brief_text=brief_text,
            asset_paths=[Path(str(row["path"])) for row in asset_rows],
            reference_public_urls_by_path=reference_public_urls_by_path,
            top_notes_collector=self._collector(request),
        )

        try:
            _final_state, workflow_run = workflow.run(
                state,
                session_id=session_id,
                task_id=task_id,
                human_gate_mode=str(request.get("human_gate_mode") or "skip"),
            )
        except Exception as exc:
            failed_run = getattr(exc, "workflow_run", None)
            workflow_run_data = failed_run.to_dict() if failed_run is not None else {
                "workflow_name": config.workflow_name,
                "session_id": session_id,
                "task_id": task_id,
                "status": "failed",
            }
            _write_json(run_dir / "workflow_run.json", workflow_run_data)
            case.record_run(
                run_dir,
                workflow=config.workflow_name,
                status="failed",
                metadata={"error_type": type(exc).__name__, "error": str(exc)},
            )
            record_content_production_artifacts(case, run_dir, status="failed")
            _write_experiment_manifest(
                run_dir=run_dir,
                workflow_name=config.workflow_name,
                workflow_run=workflow_run_data,
                asset_rows=asset_rows,
                input_manifest=input_manifest,
                require_image_references=config.require_image_references,
                error={"type": type(exc).__name__, "message": str(exc)},
            )
            failure_result = _run_response(
                run_dir=run_dir,
                workflow_name=config.workflow_name,
                workflow_run=workflow_run_data,
                asset_rows=asset_rows,
                input_manifest=input_manifest,
                require_image_references=config.require_image_references,
            )
            raise ContentProductionRunFailed(exc, failure_result=failure_result) from exc

        _write_json(run_dir / "workflow_run.json", workflow_run.to_dict())
        case.record_run(run_dir, workflow=config.workflow_name, status=workflow_run.status)
        record_content_production_artifacts(case, run_dir, status=workflow_run.status)
        _write_experiment_manifest(
            run_dir=run_dir,
            workflow_name=config.workflow_name,
            workflow_run=workflow_run.to_dict(),
            asset_rows=asset_rows,
            input_manifest=input_manifest,
            require_image_references=config.require_image_references,
        )
        return _run_response(
            run_dir=run_dir,
            workflow_name=config.workflow_name,
            workflow_run=workflow_run.to_dict(),
            asset_rows=asset_rows,
            input_manifest=input_manifest,
            require_image_references=config.require_image_references,
        )

    def _collector(self, request: dict[str, Any]) -> Callable[..., TopNotesResult]:
        def collect(market_dir: Path, search_context: dict[str, Any] | None = None) -> TopNotesResult:
            if self.top_notes_collector is not None:
                return _call_backend_top_notes_collector(self.top_notes_collector, request, market_dir, search_context or {})
            evidence = request.get("market_evidence")
            if not isinstance(evidence, dict) or not evidence:
                raise ValueError("market_evidence is required for backend content-production runs")
            result = top_notes_result_from_dict(evidence)
            (market_dir / "xhs_top_notes_result.json").write_text(
                json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return result

        return collect


def _call_backend_top_notes_collector(
    collector: Callable[..., TopNotesResult],
    request: dict[str, Any],
    market_dir: Path,
    search_context: dict[str, Any],
) -> TopNotesResult:
    try:
        signature = inspect.signature(collector)
    except (TypeError, ValueError):
        return collector(request, market_dir, search_context)
    params = list(signature.parameters.values())
    accepts_varargs = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params)
    positional = [
        param for param in params
        if param.kind in {inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    ]
    if accepts_varargs or len(positional) >= 3:
        return collector(request, market_dir, search_context)
    return collector(request, market_dir)


def _config_from_request(request: dict[str, Any], *, brief_text: str) -> ContentProductionConfig:
    config = dict(request.get("config") or {})
    goal = str(request.get("goal") or brief_text[:120]).strip()
    client_name = str(config.get("client_name") or request.get("case_title") or request.get("case_id") or "Nori User")
    brand_name = str(config.get("brand_name") or client_name)
    platform = str(config.get("platform") or request.get("platform") or "xhs")
    topic = str(config.get("topic") or goal or brief_text[:80])
    return ContentProductionConfig(
        workflow_name=str(config.get("workflow_name") or "content_production"),
        client_name=client_name,
        brand_name=brand_name,
        platform=platform,
        project_id_prefix=str(config.get("project_id_prefix") or _slug(str(request.get("case_id") or client_name))),
        project_name=str(config.get("project_name") or f"{brand_name} Content Production"),
        topic=topic,
        account_position=str(config.get("account_position") or f"{brand_name} content account."),
        target_audience=str(config.get("target_audience") or "Target users interested in the brand and topic."),
        goals=_string_list(config.get("goals")) or [goal or topic],
        positioning_notes=_string_list(config.get("positioning_notes")),
        constraints=_string_list(config.get("constraints")),
        taboos=_string_list(config.get("taboos")),
        platform_rules=_dict_list(config.get("platform_rules")) or [{"rule": "Keep platform copy concrete and inspectable."}],
        top_k_per_keyword=int(config.get("top_k_per_keyword") or config.get("search_top_k_per_keyword") or 3),
        search_keywords_per_layer=int(config.get("search_keywords_per_layer") or 2),
        search_top_k_per_keyword=int(config.get("search_top_k_per_keyword") or config.get("top_k_per_keyword") or 3),
        download_media=bool(config.get("download_media") or False),
        horizon_days=int(config.get("horizon_days") or 7),
        market_case_brief_chars=int(config.get("market_case_brief_chars") or 1200),
        llm_label=str(config.get("llm_label") or ""),
        image_label=str(config.get("image_label") or ""),
        require_image_references=bool(request.get("require_image_references") or config.get("require_image_references") or False),
        stage_timeout_seconds=float(config.get("stage_timeout_seconds") or 180),
        content_package_timeout_seconds=float(config.get("content_package_timeout_seconds") or 240),
        human_gate_name=str(config.get("human_gate_name") or "approve_content_design_spec"),
        human_gate_prompt=str(
            config.get("human_gate_prompt") or "Review content_design_spec.json before generating final copy and cover."
        ),
        human_gate_metadata=dict(config.get("human_gate_metadata") or {"artifact": "content_design_spec.json"}),
    )


def _default_llm_factory() -> LLMFactory:
    def chat(messages: list[dict[str, Any]], **kwargs: Any) -> str:
        kwargs.setdefault("timeout", 180)
        return llms.chat(messages, **kwargs)

    def chat_json(messages: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("timeout", 180)
        return llms.chat_json(messages, **kwargs)

    def image(prompt: str, **kwargs: Any) -> list[str]:
        kwargs.setdefault("timeout", 300)
        return llms.image(prompt, **kwargs)

    return LLMFactory(chat_func=chat, chat_json_func=chat_json, image_func=image)


def _run_response(
    *,
    run_dir: Path,
    workflow_name: str,
    workflow_run: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    input_manifest: dict[str, Any] | None = None,
    require_image_references: bool = False,
) -> dict[str, Any]:
    artifact_paths = {
        path.name: str(path)
        for path in sorted(run_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".json", ".md"}
    }
    covers_dir = run_dir / "covers"
    cover_paths = [
        str(path)
        for path in sorted(covers_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() else []
    reference_transfer = dict(input_manifest.get("reference_transfer") or {})
    reference_images = image_reference_summary(
        run_dir,
        require_image_references=require_image_references,
    )
    reference_images = _enrich_image_reference_trace(reference_images, reference_transfer)
    latest_reference_check = dict(input_manifest.get("reference_image_generation_check") or {})
    if latest_reference_check:
        reference_images["latest_generation_check"] = latest_reference_check
    return {
        "workflow_name": workflow_name,
        "run_id": run_dir.name,
        "run_dir": str(run_dir),
        "status": workflow_run.get("status"),
        "session_id": workflow_run.get("session_id", ""),
        "task_id": workflow_run.get("task_id", ""),
        "asset_paths": [str(row.get("path") or "") for row in asset_rows],
        "asset_ids": [str(row.get("asset_id") or "") for row in asset_rows],
        "artifact_paths": artifact_paths,
        "cover_paths": cover_paths,
        "artifact_urls": artifact_urls_for_run(run_dir),
        "cover_urls": cover_urls_for_run(run_dir),
        "input_manifest": dict(input_manifest or {}),
        "experiment_manifest": _read_json(run_dir / EXPERIMENT_MANIFEST_NAME),
        "image_reference": image_reference_summary(run_dir, require_image_references=require_image_references),
        "workflow_run": workflow_run,
    }


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


def list_content_production_runs(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    status: str = "",
    proof_status: str = "",
    reference_status: str = "",
    evaluation_status: str = "",
    search: str = "",
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    root = Path(project_root)
    case_dirs = [root / "cases" / case_id] if case_id else sorted((root / "cases").glob("*"))
    all_runs: list[dict[str, Any]] = []
    for case_dir in case_dirs:
        runs_dir = case_dir / "runs"
        if not runs_dir.is_dir():
            continue
        for run_dir in sorted((path for path in runs_dir.iterdir() if path.is_dir()), reverse=True):
            summary = summarize_content_production_run(project_root=root, case_id=case_dir.name, run_id=run_dir.name)
            if summary:
                all_runs.append(summary)
    filters = {
        "case_id": str(case_id or ""),
        "status": str(status or ""),
        "proof_status": str(proof_status or ""),
        "reference_status": str(reference_status or ""),
        "evaluation_status": str(evaluation_status or ""),
        "search": str(search or ""),
    }
    filtered = [
        summary
        for summary in all_runs
        if _run_matches_filters(
            summary,
            status=filters["status"],
            proof_status=filters["proof_status"],
            reference_status=filters["reference_status"],
            evaluation_status=filters["evaluation_status"],
            search=filters["search"],
        )
    ]
    normalized_offset = max(0, int(offset or 0))
    normalized_limit = max(1, min(int(limit or 100), 500))
    paged = filtered[normalized_offset : normalized_offset + normalized_limit]
    rows = [_comparison_run(summary) for summary in filtered]
    return {
        "runs": paged,
        "total_count": len(all_runs),
        "filtered_count": len(filtered),
        "returned_count": len(paged),
        "offset": normalized_offset,
        "limit": normalized_limit,
        "has_more": normalized_offset + normalized_limit < len(filtered),
        "filters": filters,
        "summary": {
            "status_counts": _count_by(rows, "status"),
            "proof_status_counts": _count_values([str((summary.get("proof") or {}).get("status") or "") for summary in filtered]),
            "acceptance_status_counts": _count_values(
                [str((summary.get("acceptance") or {}).get("status") or "") for summary in filtered]
            ),
            "reference_status_counts": _count_by(rows, "reference_status"),
            "evaluation_status_counts": _count_by(rows, "evaluation_status"),
            "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
            "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
        },
    }


def content_production_experiment_overview(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 20,
) -> dict[str, Any]:
    """Aggregate recorded content-production experiments for product dashboards."""

    normalized_limit = max(1, min(int(limit or 20), 100))
    summaries = list_content_production_runs(project_root=project_root, case_id=case_id).get("runs", [])
    rows = [_overview_run(summary) for summary in summaries]
    cases: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        cases.setdefault(row["case_id"], []).append(row)

    blocked_reasons: dict[str, int] = {}
    for row in rows:
        for reason in row["candidate"]["blocking_reasons"]:
            blocked_reasons[reason] = blocked_reasons.get(reason, 0) + 1

    return {
        "case_id": str(case_id or ""),
        "run_count": len(rows),
        "case_count": len(cases),
        "latest_runs": rows[:normalized_limit],
        "summary": {
            "status_counts": _count_by(rows, "status"),
            "acceptance_status_counts": _count_by(rows, "acceptance_status"),
            "reference_status_counts": _count_by(rows, "reference_status"),
            "evaluation_status_counts": _count_by(rows, "evaluation_status"),
            "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
            "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
            "blocking_reason_counts": blocked_reasons,
        },
        "cases": [
            _overview_case(case_rows, project_root=project_root)
            for _case_id, case_rows in sorted(
                cases.items(),
                key=lambda item: str(item[1][0].get("created_at") or ""),
                reverse=True,
            )
        ],
    }


def content_production_experiment_workbench(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 20,
    include_diagnostics: bool = True,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build one product-console snapshot for backend content-production experiments."""

    normalized_case_id = str(case_id or "").strip()
    normalized_limit = max(1, min(int(limit or 20), 100))
    diagnostics = (
        content_production_diagnostics(project_root=project_root, environ=environ)
        if include_diagnostics
        else {}
    )
    overview = content_production_experiment_overview(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    cases = [
        _workbench_case(row, project_root=project_root)
        for row in (overview.get("cases") or [])[:normalized_limit]
        if isinstance(row, dict)
    ]
    if normalized_case_id and not cases:
        cases = [_empty_workbench_case(normalized_case_id)]
    primary_actions = [
        {"case_id": row["case_id"], **dict(row.get("primary_action") or {})}
        for row in cases
        if isinstance(row.get("primary_action"), dict) and row.get("primary_action")
    ]
    case_compare = (
        content_production_case_compare(
            project_root=project_root,
            case_id=normalized_case_id,
            limit=normalized_limit,
        )
        if normalized_case_id
        else {}
    )
    active_run_id = _workbench_active_run_id(case_compare)
    active_run_artifacts = (
        inspect_content_production_run_artifacts(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=active_run_id,
        )
        if normalized_case_id and active_run_id
        else {}
    )
    case_delivery = (
        content_production_case_delivery(
            project_root=project_root,
            case_id=normalized_case_id,
        )
        if normalized_case_id
        else {}
    )
    return {
        "schema_version": 1,
        "scope": "case" if normalized_case_id else "all_cases",
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "ready": bool(diagnostics.get("ready", True)) if include_diagnostics else True,
        "status": _workbench_status(diagnostics=diagnostics, cases=cases, overview=overview),
        "diagnostics": diagnostics,
        "overview": overview,
        "cases": cases,
        "primary_actions": primary_actions,
        "case_compare": case_compare,
        "case_delivery": case_delivery,
        "active_run_id": active_run_id,
        "active_run_artifacts": active_run_artifacts,
        "links": {
            "diagnostics": "/experiments/content-production/diagnostics",
            "overview": (
                f"/experiments/content-production/overview?case_id={normalized_case_id}"
                if normalized_case_id
                else "/experiments/content-production/overview"
            ),
            "cases": "/experiments/content-production/cases",
            "runs": (
                f"/workflows/content-production/runs?case_id={normalized_case_id}"
                if normalized_case_id
                else "/workflows/content-production/runs"
            ),
            "run_template": (
                f"/experiments/content-production/run-template?case_id={normalized_case_id}"
                if normalized_case_id
                else "/experiments/content-production/run-template"
            ),
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare" if normalized_case_id else "",
            "case_delivery": f"/experiments/content-production/cases/{normalized_case_id}/delivery" if normalized_case_id else "",
            "case_delivery_export": (
                f"/experiments/content-production/cases/{normalized_case_id}/delivery/export"
                if normalized_case_id
                else ""
            ),
            "case_replay": f"/experiments/content-production/cases/{normalized_case_id}/replay" if normalized_case_id else "",
            "case_evaluation_draft": (
                f"/experiments/content-production/cases/{normalized_case_id}/evaluations/draft"
                if normalized_case_id
                else ""
            ),
            "case_evaluations": (
                f"/experiments/content-production/cases/{normalized_case_id}/evaluations"
                if normalized_case_id
                else ""
            ),
            "active_run_artifacts": (
                f"/workflows/content-production/runs/{normalized_case_id}/{active_run_id}/artifacts/inspect"
                if normalized_case_id and active_run_id
                else ""
            ),
        },
    }


def content_production_experiment_report(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str = "",
    limit: int = 50,
) -> dict[str, Any]:
    """Build a case-level experiment report for product/operator review."""

    normalized_limit = max(1, min(int(limit or 50), 500))
    listed = list_content_production_runs(project_root=project_root, case_id=case_id, limit=normalized_limit)
    summaries = [dict(row) for row in listed.get("runs") or [] if isinstance(row, dict)]
    rows = [_report_run(summary) for summary in summaries]
    best_summary = max(summaries, key=_report_run_score) if summaries else {}
    best_run = _report_run(best_summary) if best_summary else {}
    if best_run:
        best_run["selection_reason"] = _best_run_reason(best_run)
    latest_run = rows[0] if rows else {}
    accepted = [row["run_id"] for row in rows if row["acceptance_status"] == "accepted"]
    needs_review = [row["run_id"] for row in rows if row["acceptance_status"] == "needs_review"]
    rejected = [row["run_id"] for row in rows if row["acceptance_status"] == "rejected"]
    summary = _report_summary(rows)
    selection = _case_selection_payload(_content_case_dir_or_none(project_root=project_root, case_id=case_id), include_history=False)
    return {
        "schema_version": 1,
        "case_id": str(case_id or ""),
        "scope": "case" if case_id else "all_cases",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(rows),
        "total_count": int(listed.get("total_count") or len(rows)),
        "filtered_count": int(listed.get("filtered_count") or len(rows)),
        "limit": normalized_limit,
        "has_more": bool(listed.get("has_more")),
        "best_run": best_run,
        "latest_run": latest_run,
        "accepted_run_ids": accepted,
        "needs_review_run_ids": needs_review,
        "rejected_run_ids": rejected,
        "summary": summary,
        "selection": selection.get("current") or {},
        "recommendations": _report_recommendations(rows, best_run=best_run, summary=summary),
        "runs": rows,
        "links": {
            "overview": f"/experiments/content-production/overview?case_id={case_id}" if case_id else "/experiments/content-production/overview",
            "runs": f"/workflows/content-production/runs?case_id={case_id}" if case_id else "/workflows/content-production/runs",
            "cases": "/experiments/content-production/cases",
        },
    }


def get_content_production_case_selection(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
) -> dict[str, Any]:
    case_dir = _content_case_dir(project_root=project_root, case_id=case_id)
    payload = _case_selection_payload(case_dir, include_history=True)
    payload["report"] = content_production_experiment_report(project_root=project_root, case_id=case_id)
    return payload


def record_content_production_case_selection(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    selection: dict[str, Any],
) -> dict[str, Any]:
    case_dir = _content_case_dir(project_root=project_root, case_id=case_id)
    run_id = str(selection.get("run_id") or "").strip()
    if not run_id:
        raise ValueError("run_id is required")
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")

    existing = _case_selection_payload(case_dir, include_history=True)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id)
    normalized = _normalize_case_selection(
        selection,
        case_id=case_id,
        run_summary=summary,
        report=report,
        existing_count=len(existing.get("history") or []) + 1,
    )
    history = [*list(existing.get("history") or []), normalized]
    payload = {
        "schema_version": 1,
        "case_id": case_id,
        "current": normalized,
        "history": history,
    }
    _write_json(case_dir / EXPERIMENT_SELECTION_NAME, payload)
    return {
        "case_id": case_id,
        "selection": normalized,
        "current": normalized,
        "history": history,
        "report": content_production_experiment_report(project_root=project_root, case_id=case_id),
        "selection_path": str(case_dir / EXPERIMENT_SELECTION_NAME),
    }


def promote_content_production_case_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    promotion: dict[str, Any],
) -> dict[str, Any]:
    """Promote an accepted run into the current case decision."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    case_dir = _content_case_dir(project_root=project_root, case_id=normalized_case_id)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(project_root=project_root, case_id=normalized_case_id, limit=500)
    best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
    run_id = (
        str(promotion.get("run_id") or "").strip()
        or str(selection.get("run_id") or "").strip()
        or str(best_run.get("run_id") or "").strip()
    )
    if not run_id:
        raise ValueError("run_id is required")
    summary = summarize_content_production_run(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {normalized_case_id}/{run_id}")
    acceptance = content_production_run_acceptance_report(summary)
    allow_unaccepted = bool(promotion.get("allow_unaccepted"))
    if not bool(acceptance.get("accepted")) and not allow_unaccepted:
        raise ValueError(
            "run is not accepted; pass allow_unaccepted=true to promote with override"
        )
    reason = str(promotion.get("reason") or "").strip()
    if not reason:
        reason = "accepted run promoted" if bool(acceptance.get("accepted")) else "unaccepted run promoted with override"
    metadata = {
        "source": "backend.promote_content_production_case_run",
        "allow_unaccepted": allow_unaccepted,
        "acceptance_status": str(acceptance.get("status") or ""),
        **dict(promotion.get("metadata") or {}),
    }
    selection_result = record_content_production_case_selection(
        project_root=project_root,
        case_id=normalized_case_id,
        selection={
            "run_id": run_id,
            "decision": "promoted",
            "reviewer": str(promotion.get("reviewer") or "operator"),
            "reason": reason,
            "notes": str(promotion.get("notes") or ""),
            "metadata": metadata,
        },
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "run_id": run_id,
        "promoted": True,
        "override": allow_unaccepted and not bool(acceptance.get("accepted")),
        "selection": dict(selection_result.get("selection") or {}),
        "selection_history_count": len(selection_result.get("history") or []),
        "acceptance": acceptance,
        "proof": dict(summary.get("proof") or {}),
        "run": _report_run(summary),
        "links": {
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{normalized_case_id}/selected-run",
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "run": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}",
            "artifact_inspection": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}/artifacts/inspect",
            "export": _run_export_url(normalized_case_id, run_id),
            "replay": _run_replay_url(normalized_case_id, run_id),
        },
    }


def content_production_case_delivery(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    allow_unpromoted: bool = False,
) -> dict[str, Any]:
    """Return a case-level delivery readiness snapshot."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")

    case_dir = _content_case_dir_or_none(project_root=project_root, case_id=normalized_case_id)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    best_run = dict(report.get("best_run") or {})
    run_id = str(selection.get("run_id") or "").strip() or str(best_run.get("run_id") or "").strip()
    promoted = str(selection.get("decision") or "") == "promoted" and bool(selection.get("run_id"))
    blockers: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {}
    acceptance: dict[str, Any] = {}
    inspection: dict[str, Any] = {}

    if not run_id:
        blockers.append("no_run")
    else:
        summary = summarize_content_production_run(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=run_id,
        )
        if not summary:
            blockers.append("run_not_found")
        else:
            acceptance = content_production_run_acceptance_report(summary)
            inspection = inspect_content_production_run_artifacts(
                project_root=project_root,
                case_id=normalized_case_id,
                run_id=run_id,
            )
            if not promoted and not allow_unpromoted:
                blockers.append("not_promoted")
            elif not promoted:
                warnings.append("unpromoted_preview")
            if str(acceptance.get("status") or "") != "accepted":
                blockers.append("not_accepted")
            missing_core = [str(item) for item in inspection.get("missing_core_artifacts") or [] if item]
            if missing_core:
                blockers.append("missing_core_artifacts")
            if not _run_export_url(normalized_case_id, run_id):
                blockers.append("missing_export")

    status = _case_delivery_status(blockers, warnings)
    case_compare = content_production_case_compare(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    next_actions = content_production_case_next_actions(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=500,
    )
    delivery = _case_delivery_payload(
        case_id=normalized_case_id,
        run_id=run_id if summary else "",
        inspection=inspection,
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "ready": not blockers,
        "status": status,
        "allow_unpromoted": bool(allow_unpromoted),
        "run_id": run_id if summary else "",
        "promoted": promoted,
        "selection": selection,
        "selection_history": list(selection_payload.get("history") or []),
        "blocking_reasons": blockers,
        "warning_reasons": warnings,
        "acceptance": acceptance,
        "proof": dict(summary.get("proof") or {}) if summary else {},
        "run": _report_run(summary) if summary else {},
        "artifact_inspection": inspection,
        "case_compare": case_compare,
        "next_actions": next_actions,
        "delivery": delivery,
        "links": {
            "workbench": f"/experiments/content-production/workbench?case_id={normalized_case_id}",
            "case_compare": f"/experiments/content-production/cases/{normalized_case_id}/compare",
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "promotion": f"/experiments/content-production/cases/{normalized_case_id}/promotion",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "delivery_export": f"/experiments/content-production/cases/{normalized_case_id}/delivery/export",
            "run": f"/workflows/content-production/runs/{normalized_case_id}/{run_id}" if summary else "",
            "artifact_inspection": (
                f"/workflows/content-production/runs/{normalized_case_id}/{run_id}/artifacts/inspect"
                if summary
                else ""
            ),
            "export": _run_export_url(normalized_case_id, run_id) if summary else "",
            "replay": _run_replay_url(normalized_case_id, run_id) if summary else "",
        },
    }


def content_production_case_timeline(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 200,
) -> dict[str, Any]:
    """Return a chronological audit timeline for one content-production case."""

    _content_case_dir(project_root=project_root, case_id=case_id)
    normalized_limit = max(1, min(int(limit or 200), 1000))
    runs = list_content_production_runs(project_root=project_root, case_id=case_id, limit=1000).get("runs", [])
    selection = get_content_production_case_selection(project_root=project_root, case_id=case_id)
    events: list[dict[str, Any]] = []
    for summary in runs:
        events.extend(_timeline_events_for_run(summary))
    for item in selection.get("history") or []:
        if isinstance(item, dict):
            events.append(_timeline_selection_event(item))
    events = sorted(events, key=_timeline_sort_key, reverse=True)
    visible = events[:normalized_limit]
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "event_count": len(events),
        "returned_count": len(visible),
        "limit": normalized_limit,
        "has_more": len(events) > normalized_limit,
        "events": visible,
        "summary": {
            "event_type_counts": _count_by(events, "event_type"),
            "run_count": len(runs),
            "evaluation_count": sum(1 for event in events if event["event_type"] == "evaluation_recorded"),
            "selection_count": sum(1 for event in events if event["event_type"] == "selection_recorded"),
        },
        "links": {
            "report": f"/experiments/content-production/report?case_id={case_id}",
            "cases": "/experiments/content-production/cases",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
        },
    }


def get_content_production_case_selected_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    fallback_to_best: bool = True,
) -> dict[str, Any]:
    """Resolve the current selected run for a case, optionally falling back to best_run."""

    case_dir = _content_case_dir(project_root=project_root, case_id=case_id)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=500)
    source = "selection" if selection.get("run_id") else ""
    run_id = str(selection.get("run_id") or "")
    if not run_id and fallback_to_best:
        best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
        run_id = str(best_run.get("run_id") or "")
        source = "best_run" if run_id else ""
    run = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id) if run_id else {}
    reason = ""
    if not run_id:
        reason = "no_selection_or_best_run"
    elif not run:
        reason = "selected_run_not_found" if source == "selection" else "best_run_not_found"
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "resolved": bool(run),
        "source": source,
        "fallback_to_best": bool(fallback_to_best),
        "reason": reason,
        "run_id": run_id if run else "",
        "selection": selection,
        "run": run,
        "report": report,
        "links": {
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "timeline": f"/experiments/content-production/cases/{case_id}/timeline",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "run": f"/workflows/content-production/runs/{case_id}/{run_id}" if run else "",
            "run_export": _run_export_url(case_id, run_id) if run else "",
        },
    }


def content_production_case_next_actions(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """Return a backend-derived action plan for one content-production case."""

    case_dir = _content_case_dir_or_none(project_root=project_root, case_id=case_id)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=limit)
    selection_payload = _case_selection_payload(case_dir, include_history=True)
    selection = dict(selection_payload.get("current") or {})
    rows = [row for row in report.get("runs") or [] if isinstance(row, dict)]
    selected_run_id = str(selection.get("run_id") or "")
    selected_run = next((row for row in rows if str(row.get("run_id") or "") == selected_run_id), {})
    best_run = dict(report.get("best_run") or {})
    target_run = dict(selected_run or best_run)
    selected_missing = bool(selected_run_id and not selected_run)
    status = _case_next_action_status(
        run_count=len(rows),
        selection=selection,
        selected_missing=selected_missing,
        target_run=target_run,
    )
    actions = _case_next_actions(
        case_id=case_id,
        status=status,
        selection=selection,
        selected_missing=selected_missing,
        selected_run=selected_run,
        best_run=best_run,
        target_run=target_run,
        report=report,
    )
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "status": status,
        "run_count": len(rows),
        "selected_run_id": selected_run_id,
        "best_run_id": str(best_run.get("run_id") or ""),
        "target_run_id": str(target_run.get("run_id") or ""),
        "selection": selection,
        "selected_run": selected_run,
        "best_run": best_run,
        "target_run": target_run,
        "selected_missing": selected_missing,
        "primary_action": actions[0] if actions else {},
        "actions": actions,
        "recommendations": list(report.get("recommendations") or []),
        "summary": dict(report.get("summary") or {}),
        "links": {
            "report": f"/experiments/content-production/report?case_id={case_id}",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{case_id}/selected-run",
            "timeline": f"/experiments/content-production/cases/{case_id}/timeline",
            "export": f"/experiments/content-production/cases/{case_id}/export",
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
            "run": f"/workflows/content-production/runs/{case_id}/{target_run.get('run_id')}" if target_run else "",
            "run_export": _run_export_url(case_id, str(target_run.get("run_id") or "")) if target_run else "",
        },
    }


def content_production_case_compare(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    limit: int = 500,
) -> dict[str, Any]:
    """Build a case-centered comparison snapshot for experiment decision UIs."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    normalized_limit = max(1, min(int(limit or 500), 1000))
    report = content_production_experiment_report(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    summaries = [
        dict(row)
        for row in list_content_production_runs(
            project_root=project_root,
            case_id=normalized_case_id,
            limit=normalized_limit,
        ).get("runs", [])
        if isinstance(row, dict)
    ]
    selection_payload = _case_selection_payload(
        _content_case_dir_or_none(project_root=project_root, case_id=normalized_case_id),
        include_history=True,
    )
    selection = dict(selection_payload.get("current") or {})
    next_actions = content_production_case_next_actions(
        project_root=project_root,
        case_id=normalized_case_id,
        limit=normalized_limit,
    )
    best_run = dict(report.get("best_run") or {})
    selected_run_id = str(selection.get("run_id") or "")
    best_run_id = str(best_run.get("run_id") or "")
    recommended_run_id = selected_run_id or best_run_id
    report_rows_by_id = {
        str(row.get("run_id") or ""): row
        for row in report.get("runs") or []
        if isinstance(row, dict)
    }
    candidates = [
        _case_compare_candidate(
            summary,
            report_row=report_rows_by_id.get(str(summary.get("run_id") or ""), {}),
            selected_run_id=selected_run_id,
            best_run_id=best_run_id,
            recommended_run_id=recommended_run_id,
        )
        for summary in summaries
    ]
    comparison = (
        compare_content_production_runs(
            project_root=project_root,
            case_id=normalized_case_id,
            run_ids=[str(summary.get("run_id") or "") for summary in summaries],
        )
        if len(summaries) >= 2
        else {}
    )
    return {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(candidates),
        "selected_run_id": selected_run_id,
        "best_run_id": best_run_id,
        "recommended_run_id": recommended_run_id,
        "selection": selection,
        "selection_history": list(selection_payload.get("history") or []),
        "best_run": best_run,
        "selected_run": next((row for row in candidates if row["run_id"] == selected_run_id), {}),
        "recommended_run": next((row for row in candidates if row["run_id"] == recommended_run_id), {}),
        "candidates": candidates,
        "summary": dict(report.get("summary") or {}),
        "comparison_summary": dict((comparison.get("summary") or {}) if isinstance(comparison, dict) else {}),
        "differences": dict((comparison.get("differences") or {}) if isinstance(comparison, dict) else {}),
        "next_actions": next_actions,
        "primary_action": dict(next_actions.get("primary_action") or {}),
        "recommendations": list(report.get("recommendations") or []),
        "links": {
            "report": f"/experiments/content-production/report?case_id={normalized_case_id}",
            "runs": f"/workflows/content-production/runs?case_id={normalized_case_id}",
            "run_template": f"/experiments/content-production/run-template?case_id={normalized_case_id}",
            "compare_runs": (
                "/workflows/content-production/runs/compare?"
                f"case_id={normalized_case_id}&run_ids="
                f"{','.join(row['run_id'] for row in candidates)}"
            ) if len(candidates) >= 2 else "",
            "selection": f"/experiments/content-production/cases/{normalized_case_id}/selection",
            "selected_run": f"/experiments/content-production/cases/{normalized_case_id}/selected-run",
            "next_actions": f"/experiments/content-production/cases/{normalized_case_id}/next-actions",
            "case_evaluation_draft": f"/experiments/content-production/cases/{normalized_case_id}/evaluations/draft",
            "case_evaluations": f"/experiments/content-production/cases/{normalized_case_id}/evaluations",
            "timeline": f"/experiments/content-production/cases/{normalized_case_id}/timeline",
            "export": f"/experiments/content-production/cases/{normalized_case_id}/export",
        },
    }


def list_content_production_cases(*, project_root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    """Return case-level summaries for recorded content-production experiments."""

    overview = content_production_experiment_overview(project_root=project_root, limit=1)
    return {
        "case_count": overview["case_count"],
        "run_count": overview["run_count"],
        "cases": overview["cases"],
        "summary": dict(overview.get("summary") or {}),
    }


def compare_content_production_runs(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_ids: list[str],
) -> dict[str, Any]:
    """Compare recorded content-production runs within one case workspace."""

    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    normalized_run_ids = _dedupe_strings(run_ids)
    if len(normalized_run_ids) < 2:
        raise ValueError("at least two run_ids are required")

    summaries: list[dict[str, Any]] = []
    missing: list[str] = []
    for run_id in normalized_run_ids:
        summary = summarize_content_production_run(
            project_root=project_root,
            case_id=normalized_case_id,
            run_id=run_id,
        )
        if summary:
            summaries.append(summary)
        else:
            missing.append(run_id)
    if missing:
        raise FileNotFoundError(f"content-production runs not found: {normalized_case_id}/{missing}")

    rows = [_comparison_run(summary) for summary in summaries]
    return {
        "case_id": normalized_case_id,
        "run_ids": normalized_run_ids,
        "run_count": len(rows),
        "runs": rows,
        "summary": {
            "status_counts": _count_by(rows, "status"),
            "acceptance_status_counts": _count_by(rows, "acceptance_status"),
            "reference_status_counts": _count_by(rows, "reference_status"),
            "ready_run_ids": [row["run_id"] for row in rows if row["candidate"]["ready_for_review"]],
            "blocked_run_ids": [row["run_id"] for row in rows if not row["candidate"]["ready_for_review"]],
            "artifact_names": sorted({name for row in rows for name in row["artifact_names"]}),
            "evaluation_status_counts": _count_by(rows, "evaluation_status"),
        },
        "differences": {
            "brief_sha256": _value_diff(rows, "brief_sha256"),
            "asset_fingerprints": _value_diff(rows, "asset_fingerprints"),
            "input_fingerprints": _value_diff(rows, "input_fingerprints"),
            "market_queries": _value_diff(rows, "market_queries"),
            "run_options": _value_diff(rows, "run_options"),
            "image_model": _value_diff(rows, "image_model"),
            "artifact_names": _value_diff(rows, "artifact_names"),
            "evaluation_status": _value_diff(rows, "evaluation_status"),
        },
    }


def list_content_production_run_evaluations(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    evaluations = _read_evaluations(run_dir)
    return {
        "case_id": case_id,
        "run_id": run_id,
        "evaluations": evaluations,
        "summary": evaluation_summary(evaluations),
    }


def get_content_production_run_acceptance(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    summary = summarize_content_production_run(
        project_root=project_root,
        case_id=case_id,
        run_id=run_id,
    )
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")
    return {
        "case_id": case_id,
        "run_id": run_id,
        "acceptance": dict(summary.get("acceptance") or {}),
    }


def inspect_content_production_run_artifacts(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    """Return a product-ready artifact inspection payload for one run."""

    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    if not summary:
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")
    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    catalog = [dict(row) for row in summary.get("artifact_catalog") or [] if isinstance(row, dict)]
    catalog_by_name = {str(row.get("artifact_name") or ""): row for row in catalog}
    markdown = [
        _artifact_inspection_entry(run_dir, row)
        for row in catalog
        if str(row.get("artifact_name") or "").endswith(".md")
    ]
    covers = [
        _artifact_inspection_entry(run_dir, row)
        for row in catalog
        if str(row.get("artifact_type") or "") == "cover"
    ]
    manifest_names = [
        "input_manifest.json",
        EXPERIMENT_MANIFEST_NAME,
        "replay_request.json",
        "workflow_run.json",
        "run.json",
    ]
    manifests = {
        _artifact_panel_key(name): _artifact_inspection_entry(
            run_dir,
            catalog_by_name.get(name, {"artifact_name": name}),
        )
        for name in manifest_names
    }
    core = {
        "content_package": _artifact_inspection_entry(
            run_dir,
            catalog_by_name.get("content_package.json", {"artifact_name": "content_package.json"}),
        ),
        "input_manifest": manifests["input_manifest"],
        "experiment_manifest": manifests["experiment_manifest"],
        "replay_request": manifests["replay_request"],
        "cover_output": {
            "available": bool(covers),
            "count": len(covers),
            "items": covers,
        },
    }
    missing_core = [
        name
        for name, entry in core.items()
        if name != "cover_output" and not bool(entry.get("available"))
    ]
    if not covers:
        missing_core.append("cover_output")
    return {
        "schema_version": 1,
        "case_id": str(case_id),
        "run_id": str(run_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": str(summary.get("status") or ""),
        "workflow_name": str(summary.get("workflow_name") or ""),
        "created_at": str(summary.get("created_at") or ""),
        "finished_at": str(summary.get("finished_at") or ""),
        "ready_for_review": bool((summary.get("proof") or {}).get("ready_for_review")),
        "proof": dict(summary.get("proof") or {}),
        "acceptance": dict(summary.get("acceptance") or {}),
        "evaluations": dict(summary.get("evaluations") or {}),
        "image_reference": dict(summary.get("image_reference") or {}),
        "visual_reference_review": dict(summary.get("visual_reference_review") or {}),
        "core_artifacts": core,
        "content_package": core["content_package"],
        "manifests": manifests,
        "markdown": markdown,
        "covers": covers,
        "artifact_catalog": catalog,
        "artifact_counts": {
            "total": len(catalog),
            "json": sum(1 for row in catalog if str(row.get("artifact_name") or "").endswith(".json")),
            "markdown": len(markdown),
            "covers": len(covers),
        },
        "missing_core_artifacts": missing_core,
        "links": {
            "run": f"/workflows/content-production/runs/{case_id}/{run_id}",
            "export": _run_export_url(str(case_id), str(run_id)),
            "replay": _run_replay_url(str(case_id), str(run_id)),
            "acceptance": f"/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
            "evaluations": f"/workflows/content-production/runs/{case_id}/{run_id}/evaluations",
            "evaluation_draft": f"/workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft",
        },
    }


def build_content_production_evaluation_draft(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    reviewer: str = "auto_review_gate",
    persist: bool = False,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    draft, reviews, context = _auto_evaluation_draft(
        run_dir,
        summary=summary,
        case_id=case_id,
        run_id=run_id,
        reviewer=reviewer,
        metadata=dict(metadata or {}),
    )
    result = {
        "case_id": case_id,
        "run_id": run_id,
        "persisted": False,
        "draft": draft,
        "reviews": reviews,
        "context": context,
    }
    if persist:
        recorded = record_content_production_run_evaluation(
            project_root=project_root,
            case_id=case_id,
            run_id=run_id,
            evaluation=draft,
        )
        result["persisted"] = True
        result["recorded"] = recorded
    return result


def record_content_production_run_evaluation(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    evaluation: dict[str, Any],
) -> dict[str, Any]:
    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    existing = _read_evaluations(run_dir)
    normalized = _normalize_evaluation(evaluation, existing_count=len(existing) + 1)
    evaluations = [*existing, normalized]
    _write_json(run_dir / EXPERIMENT_EVALUATIONS_NAME, {"evaluations": evaluations})
    _refresh_experiment_manifest_evaluations(run_dir, evaluations)
    return {
        "case_id": case_id,
        "run_id": run_id,
        "evaluation": normalized,
        "evaluations": evaluations,
        "summary": evaluation_summary(evaluations),
    }


def summarize_content_production_run(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    root = Path(project_root)
    run_dir = root / "cases" / case_id / "runs" / run_id
    if not run_dir.is_dir():
        return {}
    run_manifest = _read_json(run_dir / "run.json")
    workflow_run = _read_json(run_dir / "workflow_run.json")
    input_manifest = _read_json(run_dir / "input_manifest.json")
    experiment_manifest = _read_json(run_dir / EXPERIMENT_MANIFEST_NAME)
    evaluations = _read_evaluations(run_dir)
    manifest_evaluations = experiment_manifest.get("evaluations") if isinstance(experiment_manifest.get("evaluations"), dict) else {}
    if not evaluations and isinstance(manifest_evaluations.get("items"), list):
        evaluations = [dict(item) for item in manifest_evaluations["items"] if isinstance(item, dict)]
    evaluation_summary_data = (
        dict(manifest_evaluations.get("summary") or {})
        if not evaluations and isinstance(manifest_evaluations.get("summary"), dict)
        else evaluation_summary(evaluations)
    )
    package = _read_json(run_dir / "content_package.json")
    covers_dir = run_dir / "covers"
    cover_paths = [
        str(path)
        for path in sorted(covers_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() else []
    summary = {
        "case_id": case_id,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "workflow_name": run_manifest.get("workflow") or workflow_run.get("workflow_name") or "",
        "status": run_manifest.get("status") or workflow_run.get("status") or "",
        "created_at": _first_stage_time(workflow_run),
        "finished_at": workflow_run.get("finished_at", ""),
        "artifact_paths": {
            path.name: str(path)
            for path in sorted(run_dir.iterdir())
            if path.is_file() and path.suffix.lower() in {".json", ".md"}
        },
        "cover_paths": cover_paths,
        "artifact_urls": artifact_urls_for_run(run_dir, case_id=case_id, run_id=run_id),
        "cover_urls": cover_urls_for_run(run_dir, case_id=case_id, run_id=run_id),
        "artifact_catalog": artifact_catalog_for_run(run_dir, case_id=case_id, run_id=run_id),
        "input_manifest": input_manifest,
        "experiment_manifest": experiment_manifest,
        "evaluations": {
            "items": evaluations,
            "summary": evaluation_summary_data,
        },
        "image_reference": (
            dict(experiment_manifest.get("reference_images") or {})
            if experiment_manifest
            else image_reference_from_package(package)
        ),
        "workflow_run": workflow_run,
    }
    summary["image_reference"] = _enrich_image_reference_trace(
        summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {},
        _summary_reference_transfer(summary),
    )
    summary["proof"] = content_production_run_proof(summary)
    summary["proof_status"] = str(summary["proof"].get("status") or "")
    summary["proof_failed_checks"] = list(summary["proof"].get("failed_checks") or [])
    summary["proof_warning_checks"] = list(summary["proof"].get("warning_checks") or [])
    summary["acceptance"] = content_production_run_acceptance_report(summary)
    summary["acceptance_status"] = str(summary["acceptance"].get("status") or "")
    summary["acceptance_blocking_checks"] = list(summary["acceptance"].get("blocking_checks") or [])
    summary["acceptance_warning_checks"] = list(summary["acceptance"].get("warning_checks") or [])
    summary["visual_reference_review"] = visual_reference_review(summary)
    return summary


def visual_reference_review(summary: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic review panel for human visual-reference checks."""

    image_reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    run_options = input_manifest.get("run_options") if isinstance(input_manifest.get("run_options"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    trace = [dict(item) for item in image_reference.get("trace") or [] if isinstance(item, dict)]
    cover_urls = list(summary.get("cover_urls") or [])
    required = bool(image_reference.get("required") or run_options.get("require_image_references"))
    selected_count = int(image_reference.get("selected_count") or len(trace) or 0)
    sent = bool(image_reference.get("sent"))
    evaluation_status = str(evaluation.get("status") or "pending")
    applicable = required or selected_count > 0
    checks = [
        _visual_reference_check(
            "references_selected",
            "passed" if selected_count > 0 else ("failed" if required else "not_applicable"),
            "reference images were selected" if selected_count > 0 else "no reference images were selected",
            selected_count=selected_count,
        ),
        _visual_reference_check(
            "reference_trace_available",
            "passed" if trace else ("failed" if required else "not_applicable"),
            "per-reference trace is available" if trace else "per-reference trace is missing",
            trace_count=len(trace),
        ),
        _visual_reference_check(
            "references_sent_to_gateway",
            "passed" if sent else ("failed" if required else "not_applicable"),
            "selected references were sent to the image gateway" if sent else "selected references were not sent",
            sent=sent,
            reference_status=str(image_reference.get("status") or ""),
        ),
        _visual_reference_check(
            "cover_output_available",
            "passed" if cover_urls else ("failed" if applicable else "not_applicable"),
            "cover output is available" if cover_urls else "cover output is missing",
            cover_count=len(cover_urls),
        ),
        _visual_reference_check(
            "human_visual_match_review",
            "passed" if evaluation_status == "passed" else ("pending" if applicable else "not_applicable"),
            "latest evaluation passed" if evaluation_status == "passed" else "human visual match review is still required",
            evaluation_status=evaluation_status,
            latest_evaluation_id=str(evaluation.get("latest_evaluation_id") or ""),
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    pending = [check for check in checks if check["status"] == "pending"]
    status = "not_applicable"
    if failed:
        status = "blocked"
    elif applicable and pending:
        status = "needs_human_review"
    elif applicable:
        status = "passed"
    return {
        "schema_version": 1,
        "status": status,
        "required": required,
        "human_review_required": status in {"blocked", "needs_human_review"},
        "selected_count": selected_count,
        "sent": sent,
        "trace_count": len(trace),
        "provider_fetchable_count": int(
            image_reference.get("trace_provider_fetchable_count")
            or sum(1 for item in trace if item.get("provider_fetchable"))
        ),
        "cover_count": len(cover_urls),
        "cover_urls": cover_urls,
        "reference_trace": trace,
        "checks": checks,
        "evaluation_status": evaluation_status,
        "review_questions": [
            "Does the generated cover preserve the visible brand/product/IP cues from the uploaded references?",
            "Does the cover use the references as visual source material instead of only following the text prompt?",
            "Are important user-provided assets missing, distorted, or replaced by unrelated imagery?",
        ],
    }


def _visual_reference_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if value is not None and value != "" and value != []})
    return data


def content_production_run_proof(summary: dict[str, Any]) -> dict[str, Any]:
    """Build a product-facing proof summary for one recorded experiment run."""

    row = _comparison_run(summary)
    artifact_paths = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    artifact_urls = summary.get("artifact_urls") if isinstance(summary.get("artifact_urls"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    run_options = dict(inputs.get("run_options") or input_manifest.get("run_options") or {})
    market_evidence = dict(inputs.get("market_evidence") or input_manifest.get("market_evidence") or {})
    reference_transfer = _summary_reference_transfer(summary)
    image_reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    reference_generation_check = _summary_reference_generation_check(summary)
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    require_refs = bool(run_options.get("require_image_references") or reference_transfer.get("required") or image_reference.get("required"))
    require_reference_generation_check = bool(run_options.get("require_reference_image_generation_check"))
    checks = [
        _proof_check(
            "workflow_succeeded",
            "passed" if row["status"] == "succeeded" else "failed",
            "workflow completed successfully" if row["status"] == "succeeded" else "workflow did not complete successfully",
        ),
        _proof_check(
            "market_evidence",
            "passed" if _market_evidence_available(market_evidence) else "failed",
            "market evidence was recorded" if _market_evidence_available(market_evidence) else "market evidence is missing from the run record",
        ),
        _proof_check(
            "content_package",
            "passed" if "content_package.json" in artifact_paths else "failed",
            "content_package.json is available" if "content_package.json" in artifact_paths else "content_package.json is missing",
            artifact_url=str(artifact_urls.get("content_package.json") or ""),
        ),
        _proof_check(
            "cover_output",
            "passed" if row["cover_count"] > 0 else "failed",
            "cover image output is available" if row["cover_count"] > 0 else "cover image output is missing",
        ),
        _input_integrity_check(summary),
        _reference_transfer_check(reference_transfer, require_refs=require_refs),
        _image_reference_check(image_reference, require_refs=require_refs),
        *(
            [_reference_generation_check_proof_check(reference_generation_check, required=require_reference_generation_check)]
            if require_reference_generation_check or reference_generation_check
            else []
        ),
        _evaluation_check(evaluation),
        _proof_check(
            "replay_snapshot",
            "passed" if "replay_request.json" in artifact_paths else "warning",
            "replay_request.json is available" if "replay_request.json" in artifact_paths else "replay_request.json is missing",
            artifact_url=str(artifact_urls.get("replay_request.json") or ""),
        ),
        _proof_check(
            "export_available",
            "passed" if row["run_id"] and summary.get("case_id") else "warning",
            "export endpoint can be used" if row["run_id"] and summary.get("case_id") else "export endpoint cannot be derived",
            url=(
                f"/workflows/content-production/runs/{summary.get('case_id')}/{row['run_id']}/export"
                if row["run_id"] and summary.get("case_id")
                else ""
            ),
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    warnings = [check for check in checks if check["status"] == "warning"]
    return {
        "schema_version": 1,
        "status": "blocked" if failed else ("needs_review" if warnings else "ready"),
        "ready_for_review": not failed and row["candidate"]["ready_for_review"],
        "blocking_reasons": list(row["candidate"]["blocking_reasons"]),
        "failed_checks": [check["name"] for check in failed],
        "warning_checks": [check["name"] for check in warnings],
        "checks": checks,
        "reference": {
            "required": require_refs,
            "transfer": reference_transfer,
            "image_reference": dict(image_reference),
            "generation_check_required": require_reference_generation_check,
            "generation_check": dict(reference_generation_check),
        },
        "inputs": {
            "fingerprints": dict(row.get("input_fingerprints") or {}),
        },
        "artifacts": {
            "content_package_url": str(artifact_urls.get("content_package.json") or ""),
            "input_manifest_url": str(artifact_urls.get("input_manifest.json") or ""),
            "experiment_manifest_url": str(artifact_urls.get(EXPERIMENT_MANIFEST_NAME) or ""),
            "replay_request_url": str(artifact_urls.get("replay_request.json") or ""),
            "cover_count": row["cover_count"],
            "cover_urls": list(summary.get("cover_urls") or []),
            "catalog_count": len(summary.get("artifact_catalog") or []),
            "export_url": (
                f"/workflows/content-production/runs/{summary.get('case_id')}/{row['run_id']}/export"
                if row["run_id"] and summary.get("case_id")
                else ""
            ),
        },
        "evaluation": dict(evaluation),
    }


def content_production_run_acceptance_report(summary: dict[str, Any]) -> dict[str, Any]:
    """Build the operator/product acceptance report for one experiment run."""

    row = _comparison_run(summary)
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    artifact_paths = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    artifact_catalog = [item for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    case_id = str(summary.get("case_id") or "")
    run_id = str(summary.get("run_id") or row.get("run_id") or "")
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    reference = proof.get("reference") if isinstance(proof.get("reference"), dict) else {}
    transfer = reference.get("transfer") if isinstance(reference.get("transfer"), dict) else {}
    image_reference = reference.get("image_reference") if isinstance(reference.get("image_reference"), dict) else {}
    generation_check = reference.get("generation_check") if isinstance(reference.get("generation_check"), dict) else {}
    reference_required = bool(reference.get("required") or row.get("reference_required"))
    generation_check_required = bool(reference.get("generation_check_required"))
    export_url = _run_export_url(case_id, run_id)
    replay_url = _run_replay_url(case_id, run_id)
    proof_failed = list(proof.get("failed_checks") or [])
    proof_warnings = list(proof.get("warning_checks") or [])
    evaluation_status = str(evaluation.get("status") or "pending")
    evaluation_check_status = "passed"
    evaluation_message = "latest evaluation passed"
    if evaluation_status in {"blocked", "needs_revision"}:
        evaluation_check_status = "failed"
        evaluation_message = f"latest evaluation status is {evaluation_status}"
    elif evaluation_status != "passed":
        evaluation_check_status = "warning"
        evaluation_message = "no passing evaluation has been recorded"

    checks = [
        _acceptance_check(
            "workflow_succeeded",
            "passed" if row["status"] == "succeeded" else "failed",
            "workflow completed successfully" if row["status"] == "succeeded" else "workflow did not complete successfully",
            workflow_status=row["status"],
        ),
        _acceptance_check(
            "proof_ready",
            "failed" if proof_failed else ("warning" if proof_warnings else "passed"),
            "proof checks are ready" if not proof_failed and not proof_warnings else "proof has blocking or warning checks",
            proof_status=str(proof.get("status") or ""),
            failed_checks=proof_failed,
            warning_checks=proof_warnings,
        ),
        _acceptance_check(
            "content_package_available",
            "passed" if "content_package.json" in artifact_paths else "failed",
            "content_package.json is available" if "content_package.json" in artifact_paths else "content_package.json is missing",
            artifact_url=str((summary.get("artifact_urls") or {}).get("content_package.json") or ""),
        ),
        _acceptance_check(
            "cover_output_available",
            "passed" if row["cover_count"] > 0 else "failed",
            "cover output is available" if row["cover_count"] > 0 else "cover output is missing",
            cover_count=row["cover_count"],
        ),
        _acceptance_check(
            "artifact_catalog_available",
            "passed" if artifact_catalog else "warning",
            "artifact catalog is available" if artifact_catalog else "artifact catalog is empty",
            catalog_count=len(artifact_catalog),
        ),
        _acceptance_check(
            "export_available",
            "passed" if export_url and artifact_catalog else "warning",
            "export endpoint can be used" if export_url and artifact_catalog else "export endpoint or exportable artifacts are missing",
            url=export_url,
        ),
        _acceptance_check(
            "replay_snapshot_available",
            "passed" if "replay_request.json" in artifact_paths and replay_url else "warning",
            "replay snapshot is available" if "replay_request.json" in artifact_paths and replay_url else "replay snapshot is missing",
            artifact_url=str((summary.get("artifact_urls") or {}).get("replay_request.json") or ""),
            url=replay_url,
        ),
        _acceptance_reference_check(
            reference_required=reference_required,
            transfer=transfer,
            image_reference=image_reference,
        ),
        *(
            [
                _acceptance_reference_generation_check(
                    generation_check_required=generation_check_required,
                    generation_check=generation_check,
                )
            ]
            if generation_check_required or generation_check
            else []
        ),
        _acceptance_check(
            "evaluation_passed",
            evaluation_check_status,
            evaluation_message,
            evaluation_status=evaluation_status,
            score=evaluation.get("score"),
            latest_evaluation_id=str(evaluation.get("latest_evaluation_id") or ""),
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    warnings = [check for check in checks if check["status"] == "warning"]
    status = "rejected" if failed else ("needs_review" if warnings else "accepted")
    return {
        "schema_version": 1,
        "accepted": status == "accepted",
        "status": status,
        "blocking_checks": [check["name"] for check in failed],
        "warning_checks": [check["name"] for check in warnings],
        "checks": checks,
        "evidence": {
            "case_id": case_id,
            "run_id": run_id,
            "proof_status": str(proof.get("status") or ""),
            "workflow_status": row["status"],
            "evaluation": dict(evaluation),
            "reference_required": reference_required,
            "reference_sent": bool(image_reference.get("sent") or row.get("reference_sent")),
            "reference_generation_check_required": generation_check_required,
            "reference_generation_check_ready": bool(generation_check.get("ready")),
            "reference_generation_check_covers_selected": bool(
                generation_check.get("covers_selected_reference_images")
            ),
            "reference_generation_check_reason": str(generation_check.get("reason") or ""),
            "reference_status": str(image_reference.get("status") or row.get("reference_status") or ""),
            "provider_fetchable_count": int(transfer.get("provider_fetchable_count") or 0),
            "selected_reference_count": int(transfer.get("selected_count") or image_reference.get("selected_count") or 0),
            "reference_trace_count": int(image_reference.get("trace_count") or len(image_reference.get("trace") or [])),
            "reference_trace_provider_fetchable_count": int(image_reference.get("trace_provider_fetchable_count") or 0),
            "reference_trace_sent_count": int(image_reference.get("trace_sent_count") or 0),
            "reference_trace": list(image_reference.get("trace") or []),
            "artifact_catalog_count": len(artifact_catalog),
            "cover_count": row["cover_count"],
            "cover_urls": list(summary.get("cover_urls") or []),
            "export_url": export_url,
            "replay_url": replay_url,
        },
    }


def _acceptance_check(name: str, status: str, message: str, **extra: Any) -> dict[str, Any]:
    data = {"name": name, "status": status, "message": message}
    data.update({key: value for key, value in extra.items() if not _empty_acceptance_extra(value)})
    return data


def _empty_acceptance_extra(value: Any) -> bool:
    return value is None or value == "" or value == []


def _acceptance_reference_check(
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


def _acceptance_reference_generation_check(
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


def _market_evidence_available(market_evidence: dict[str, Any]) -> bool:
    if bool(market_evidence.get("provided")):
        return True
    return bool(market_evidence.get("queries") or market_evidence.get("hot_note_count") or market_evidence.get("hot_notes"))


def _input_integrity_check(summary: dict[str, Any]) -> dict[str, Any]:
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    fingerprints = inputs.get("fingerprints") if isinstance(inputs.get("fingerprints"), dict) else input_manifest.get("fingerprints")
    if not isinstance(fingerprints, dict) or not fingerprints:
        return _proof_check(
            "input_integrity",
            "warning",
            "input fingerprints are not recorded for this run",
            reason="missing_fingerprints",
        )

    run_dir_text = str(summary.get("run_dir") or "")
    run_dir = Path(run_dir_text) if run_dir_text else Path()
    replay_path = run_dir / str(input_manifest.get("replay_request_path") or "replay_request.json")
    replay_request = _read_json(replay_path) if replay_path.is_file() else {}
    issues: list[dict[str, Any]] = []
    verified: list[str] = []

    input_fingerprints = input_manifest.get("fingerprints") if isinstance(input_manifest.get("fingerprints"), dict) else {}
    manifest_fingerprints = inputs.get("fingerprints") if isinstance(inputs.get("fingerprints"), dict) else {}
    if input_fingerprints and manifest_fingerprints and input_fingerprints != manifest_fingerprints:
        issues.append({"field": "fingerprints", "reason": "input_manifest_and_experiment_manifest_differ"})

    def check_value(field: str, actual: str, *, missing_reason: str = "") -> None:
        expected = str(fingerprints.get(field) or "").strip()
        if not expected:
            return
        if not actual:
            issues.append({"field": field, "reason": missing_reason or "missing_actual"})
            return
        if actual != expected:
            issues.append({"field": field, "reason": "sha256_mismatch", "expected": expected, "actual": actual})
            return
        verified.append(field)

    check_value(
        "replay_request_sha256",
        _file_sha256(replay_path) if replay_path.is_file() else "",
        missing_reason="replay_request_missing",
    )

    brief = input_manifest.get("brief") if isinstance(input_manifest.get("brief"), dict) else {}
    brief_path_text = str(brief.get("text_path") or "")
    brief_path = run_dir / brief_path_text if brief_path_text else Path()
    check_value(
        "brief_sha256",
        _file_sha256(brief_path) if brief_path_text and brief_path.is_file() else "",
        missing_reason="brief_file_missing",
    )

    if replay_request:
        config = replay_request.get("config") if isinstance(replay_request.get("config"), dict) else {}
        market_evidence = (
            replay_request.get("market_evidence") if isinstance(replay_request.get("market_evidence"), dict) else {}
        )
        metadata = replay_request.get("metadata") if isinstance(replay_request.get("metadata"), dict) else {}
        check_value("config_sha256", _json_sha256(config))
        check_value("market_evidence_sha256", _json_sha256(market_evidence))
        check_value("metadata_sha256", _json_sha256(metadata))
    else:
        for field in ("config_sha256", "market_evidence_sha256", "metadata_sha256"):
            if str(fingerprints.get(field) or "").strip():
                issues.append({"field": field, "reason": "replay_request_missing"})

    expected_asset_sha256s = [str(item).strip() for item in fingerprints.get("asset_sha256s") or [] if str(item).strip()]
    if expected_asset_sha256s:
        actual_asset_sha256s = _local_asset_sha256s(input_manifest.get("assets") or inputs.get("assets") or [])
        if actual_asset_sha256s != expected_asset_sha256s:
            issues.append(
                {
                    "field": "asset_sha256s",
                    "reason": "asset_sha256s_mismatch",
                    "expected": expected_asset_sha256s,
                    "actual": actual_asset_sha256s,
                }
            )
        else:
            verified.append("asset_sha256s")

    if issues:
        return _proof_check(
            "input_integrity",
            "failed",
            "input fingerprints do not match current run artifacts",
            verified=verified,
            issues=issues,
        )
    return _proof_check(
        "input_integrity",
        "passed",
        "input fingerprints match current run artifacts",
        verified=verified,
    )


def _local_asset_sha256s(assets: Any) -> list[str]:
    out: list[str] = []
    source = assets if isinstance(assets, list) else []
    for item in source:
        if not isinstance(item, dict):
            continue
        path = Path(str(item.get("path") or ""))
        if path.is_file():
            out.append(_file_sha256(path))
    return out


def _summary_reference_transfer(summary: dict[str, Any]) -> dict[str, Any]:
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


def _summary_reference_generation_check(summary: dict[str, Any]) -> dict[str, Any]:
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


def _reference_transfer_check(transfer: dict[str, Any], *, require_refs: bool) -> dict[str, Any]:
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


def _reference_generation_check_proof_check(generation_check: dict[str, Any], *, required: bool) -> dict[str, Any]:
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


def _image_reference_check(image_reference: dict[str, Any], *, require_refs: bool) -> dict[str, Any]:
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


def _evaluation_check(evaluation: dict[str, Any]) -> dict[str, Any]:
    status = str(evaluation.get("status") or "pending")
    if status == "passed":
        return _proof_check("evaluation", "passed", "latest evaluation passed")
    if status == "blocked":
        return _proof_check("evaluation", "failed", "latest evaluation is blocked")
    if status == "needs_revision":
        return _proof_check("evaluation", "warning", "latest evaluation needs revision")
    return _proof_check("evaluation", "warning", "no passing evaluation has been recorded")


def artifact_urls_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> dict[str, str]:
    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    return {
        item.name: f"/workflows/content-production/runs/{actual_case_id}/{actual_run_id}/artifacts/{item.name}"
        for item in sorted(path.iterdir())
        if item.is_file() and item.suffix.lower() in {".json", ".md"}
    } if path.is_dir() and actual_case_id and actual_run_id else {}


def cover_urls_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> list[str]:
    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    covers_dir = path / "covers"
    return [
        f"/workflows/content-production/runs/{actual_case_id}/{actual_run_id}/artifacts/covers/{item.name}"
        for item in sorted(covers_dir.iterdir())
        if item.is_file() and item.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() and actual_case_id and actual_run_id else []


def _run_export_url(case_id: str, run_id: str) -> str:
    return f"/workflows/content-production/runs/{case_id}/{run_id}/export" if case_id and run_id else ""


def _run_replay_url(case_id: str, run_id: str) -> str:
    return f"/workflows/content-production/runs/{case_id}/{run_id}/replay" if case_id and run_id else ""


def artifact_catalog_for_run(run_dir: str | Path, *, case_id: str = "", run_id: str = "") -> list[dict[str, Any]]:
    """Return whitelisted run artifact metadata for product detail UIs."""

    path = Path(run_dir)
    actual_case_id = case_id or _case_id_from_run_dir(path)
    actual_run_id = run_id or path.name
    if not path.is_dir() or not actual_case_id or not actual_run_id:
        return []

    rows: list[dict[str, Any]] = []
    for item in sorted(path.iterdir()):
        if item.is_file() and item.suffix.lower() in {".json", ".md"}:
            artifact_name = item.name
            rows.append(_artifact_catalog_entry(item, artifact_name=artifact_name, case_id=actual_case_id, run_id=actual_run_id))

    covers_dir = path / "covers"
    if covers_dir.is_dir():
        for item in sorted(covers_dir.iterdir()):
            if item.is_file() and item.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
                artifact_name = f"covers/{item.name}"
                rows.append(
                    _artifact_catalog_entry(item, artifact_name=artifact_name, case_id=actual_case_id, run_id=actual_run_id)
                )
    return rows


def _artifact_catalog_entry(path: Path, *, artifact_name: str, case_id: str, run_id: str) -> dict[str, Any]:
    suffix = path.suffix.lower()
    artifact_type = "cover" if artifact_name.startswith("covers/") else "run_artifact"
    row = {
        "name": path.name,
        "artifact_name": artifact_name,
        "artifact_type": artifact_type,
        "media_type": _artifact_media_type(path),
        "size_bytes": path.stat().st_size,
        "sha256": _file_sha256(path),
        "url": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name}",
    }
    if suffix in {".json", ".md"}:
        row["preview"] = _artifact_text_preview(path)
    else:
        row["preview"] = {"kind": "image", "available": False}
    return row


def _artifact_inspection_entry(run_dir: Path, row: dict[str, Any]) -> dict[str, Any]:
    artifact_name = str(row.get("artifact_name") or "")
    if not artifact_name:
        return {"available": False, "artifact_name": ""}
    path = _artifact_path_from_catalog_name(run_dir, artifact_name)
    if not path.is_file():
        return {
            "available": False,
            "artifact_name": artifact_name,
            "reason": "missing_artifact",
        }
    entry = {
        "available": True,
        **dict(row),
    }
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = _read_json(path)
        entry["data"] = data
        entry["json_summary"] = {
            "keys": sorted(str(key) for key in data.keys()),
            "field_count": len(data),
        }
    elif suffix == ".md":
        entry["text"] = str((row.get("preview") or {}).get("text") or "")
    elif suffix in {".jpeg", ".jpg", ".png", ".webp"}:
        entry["preview"] = {"kind": "image", "available": True, "url": str(row.get("url") or "")}
    return entry


def _artifact_path_from_catalog_name(run_dir: Path, artifact_name: str) -> Path:
    name = str(artifact_name or "")
    if name.startswith("covers/"):
        return run_dir / "covers" / Path(name).name
    return run_dir / Path(name).name


def _artifact_panel_key(artifact_name: str) -> str:
    stem = Path(str(artifact_name or "")).stem
    return "experiment_manifest" if artifact_name == EXPERIMENT_MANIFEST_NAME else stem


def _artifact_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".json": "application/json",
        ".md": "text/markdown",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")


def _artifact_text_preview(path: Path, *, max_chars: int = 4096) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "kind": "text",
        "text": text[:max_chars],
        "char_count": len(text),
        "truncated": len(text) > max_chars,
    }


def resolve_content_production_artifact_path(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    artifact_name: str,
) -> Path:
    root = Path(project_root).resolve()
    run_dir = (root / "cases" / case_id / "runs" / run_id).resolve()
    if not _is_relative_to(run_dir, root / "cases") or not run_dir.is_dir():
        raise ValueError(f"content-production run not found: {case_id}/{run_id}")
    artifact = _safe_run_artifact_path(run_dir, artifact_name)
    if not artifact.is_file():
        raise FileNotFoundError(f"run artifact not found: {artifact_name}")
    return artifact


def build_content_production_run_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
    include_inputs: bool = False,
) -> dict[str, Any]:
    """Build a zip bundle for one recorded content-production run."""

    run_dir = _content_run_dir(project_root=project_root, case_id=case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=case_id, run_id=run_id)
    artifact_inspection = inspect_content_production_run_artifacts(
        project_root=project_root,
        case_id=case_id,
        run_id=run_id,
    )
    review_evidence = _run_review_evidence(summary=summary, inspection=artifact_inspection)
    json_entries: dict[str, Any] = {
        "artifact_inspection.json": artifact_inspection,
        "review_evidence.json": review_evidence,
        "run_summary.json": summary,
    }
    entries = _exportable_run_files(run_dir)
    skipped_inputs: list[dict[str, str]] = []
    if include_inputs:
        input_entries, skipped_inputs = _exportable_input_files(run_dir)
        entries.extend(input_entries)
    manifest = {
        "schema_version": 1,
        "case_id": str(case_id),
        "run_id": str(run_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "include_inputs": bool(include_inputs),
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in json_entries.items()
        ] + [
            {
                "path": arcname,
                "media_type": _artifact_media_type(path),
                "size_bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
            for arcname, path in entries
        ],
        "skipped_inputs": skipped_inputs,
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        for path, data in json_entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
        for arcname, path in entries:
            archive.write(path, arcname=arcname)
    return {
        "filename": f"nori_content_production_{_slug(str(case_id))}_{_slug(str(run_id))}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


def build_content_production_case_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
) -> dict[str, Any]:
    """Build a zip bundle for one recorded content-production case."""

    _content_case_dir(project_root=project_root, case_id=case_id)
    report = content_production_experiment_report(project_root=project_root, case_id=case_id, limit=500)
    selection = get_content_production_case_selection(project_root=project_root, case_id=case_id)
    cases = list_content_production_cases(project_root=project_root)
    case_summary = next((row for row in cases.get("cases") or [] if row.get("case_id") == case_id), {})
    runs = list_content_production_runs(project_root=project_root, case_id=case_id, limit=500).get("runs", [])
    selected_run_id = str((selection.get("current") or {}).get("run_id") or "")
    entries: dict[str, Any] = {
        "case_report.json": report,
        "case_selection.json": {
            key: value
            for key, value in selection.items()
            if key != "report"
        },
        "case_summary.json": case_summary,
    }
    for summary in runs:
        run_id = str(summary.get("run_id") or "")
        if run_id:
            entries[f"runs/{_slug(run_id)}/summary.json"] = summary
    manifest = {
        "schema_version": 1,
        "case_id": str(case_id),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "run_count": len(runs),
        "selected_run_id": selected_run_id,
        "selected_run_export_url": _run_export_url(case_id, selected_run_id) if selected_run_id else "",
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in entries.items()
        ],
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("case_export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, default=str))
        for path, data in entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
    return {
        "filename": f"nori_content_production_case_{_slug(str(case_id))}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


def build_content_production_case_delivery_export(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    allow_unready: bool = False,
) -> dict[str, Any]:
    """Build a delivery bundle for the run selected by the case delivery gate."""

    delivery = content_production_case_delivery(
        project_root=project_root,
        case_id=case_id,
        allow_unpromoted=allow_unready,
    )
    run_id = str(delivery.get("run_id") or "")
    if not run_id:
        raise ValueError("case has no delivery run to export")
    if not bool(delivery.get("ready")) and not allow_unready:
        blockers = ", ".join(str(item) for item in delivery.get("blocking_reasons") or []) or "not_ready"
        raise ValueError(f"case delivery is not ready: {blockers}")

    normalized_case_id = str(delivery.get("case_id") or case_id)
    run_dir = _content_run_dir(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    summary = summarize_content_production_run(project_root=project_root, case_id=normalized_case_id, run_id=run_id)
    artifact_inspection = dict(delivery.get("artifact_inspection") or {})
    review_evidence = _delivery_review_evidence(delivery=delivery, summary=summary)
    json_entries: dict[str, Any] = {
        "delivery.json": delivery,
        "artifact_inspection.json": artifact_inspection,
        "review_evidence.json": review_evidence,
        "case_compare.json": delivery.get("case_compare") or {},
        "next_actions.json": delivery.get("next_actions") or {},
        "run_summary.json": summary,
    }
    run_entries = [(f"run/{arcname}", path) for arcname, path in _exportable_run_files(run_dir)]
    generated_at = datetime.now().isoformat(timespec="seconds")
    manifest = {
        "schema_version": 1,
        "case_id": normalized_case_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "ready": bool(delivery.get("ready")),
        "status": str(delivery.get("status") or ""),
        "allow_unready": bool(allow_unready),
        "blocking_reasons": list(delivery.get("blocking_reasons") or []),
        "warning_reasons": list(delivery.get("warning_reasons") or []),
        "files": [
            {
                "path": path,
                "media_type": "application/json",
                "size_bytes": len(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")),
            }
            for path, data in json_entries.items()
        ] + [
            {
                "path": arcname,
                "media_type": _artifact_media_type(path),
                "size_bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
            for arcname, path in run_entries
        ],
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("delivery_export_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, default=str))
        for path, data in json_entries.items():
            archive.writestr(path, json.dumps(data, ensure_ascii=False, indent=2, default=str))
        for arcname, path in run_entries:
            archive.write(path, arcname=arcname)
    return {
        "filename": f"nori_content_production_delivery_{_slug(normalized_case_id)}_{_slug(run_id)}.zip",
        "media_type": "application/zip",
        "content": buffer.getvalue(),
        "manifest": manifest,
    }


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


def _comparison_run(summary: dict[str, Any]) -> dict[str, Any]:
    manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = manifest.get("inputs") if isinstance(manifest.get("inputs"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    artifacts = sorted((summary.get("artifact_paths") or {}).keys())
    run_options = dict(inputs.get("run_options") or input_manifest.get("run_options") or {})
    assets = inputs.get("assets") if isinstance(inputs.get("assets"), list) else input_manifest.get("assets") or []
    asset_ids = [str(item.get("asset_id") or "") for item in assets if isinstance(item, dict) and item.get("asset_id")]
    session = manifest.get("session") if isinstance(manifest.get("session"), dict) else {}
    fingerprints = inputs.get("fingerprints") if isinstance(inputs.get("fingerprints"), dict) else input_manifest.get("fingerprints")
    if not isinstance(fingerprints, dict):
        fingerprints = {}
    models = manifest.get("models") if isinstance(manifest.get("models"), dict) else {}
    image_model = models.get("image") if isinstance(models.get("image"), dict) else {}
    row = {
        "run_id": str(summary.get("run_id") or ""),
        "session_id": str(session.get("session_id") or input_manifest.get("session_id") or ""),
        "task_id": str(session.get("task_id") or input_manifest.get("task_id") or ""),
        "status": str(summary.get("status") or ""),
        "created_at": str(summary.get("created_at") or ""),
        "finished_at": str(summary.get("finished_at") or ""),
        "brief_sha256": str((inputs.get("brief") or input_manifest.get("brief") or {}).get("sha256") or ""),
        "asset_fingerprints": _asset_fingerprints(assets),
        "asset_ids": asset_ids,
        "input_fingerprints": dict(fingerprints),
        "market_queries": _string_list((inputs.get("market_evidence") or input_manifest.get("market_evidence") or {}).get("queries")),
        "run_options": run_options,
        "backend_public_base_url": str(run_options.get("backend_public_base_url") or ""),
        "image_model": {
            "key": str(image_model.get("key") or ""),
            "provider_id": str(image_model.get("provider_id") or ""),
            "model_id": str(image_model.get("model_id") or ""),
        },
        "reference_status": str(reference.get("status") or ""),
        "reference_required": bool(reference.get("required")),
        "reference_sent": bool(reference.get("sent")),
        "cover_count": len(summary.get("cover_paths") or []),
        "artifact_names": artifacts,
        "evaluation_status": str(evaluation.get("status") or "pending"),
        "evaluation_score": evaluation.get("score"),
        "evaluation_count": int(evaluation.get("count") or 0),
        "acceptance_status": str(acceptance.get("status") or ""),
        "accepted": bool(acceptance.get("accepted")),
        "acceptance_blocking_checks": list(acceptance.get("blocking_checks") or []),
        "acceptance_warning_checks": list(acceptance.get("warning_checks") or []),
    }
    row["candidate"] = _candidate_status(row)
    return row


def _case_compare_candidate(
    summary: dict[str, Any],
    *,
    report_row: dict[str, Any],
    selected_run_id: str,
    best_run_id: str,
    recommended_run_id: str,
) -> dict[str, Any]:
    row = _comparison_run(summary)
    run_id = row["run_id"]
    case_id = str(summary.get("case_id") or "")
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    report_data = dict(report_row or {})
    base = f"/workflows/content-production/runs/{case_id}/{run_id}" if case_id and run_id else ""
    return {
        **row,
        "case_id": case_id,
        "is_selected": bool(run_id and run_id == selected_run_id),
        "is_best": bool(run_id and run_id == best_run_id),
        "is_recommended": bool(run_id and run_id == recommended_run_id),
        "proof_status": str(proof.get("status") or ""),
        "proof_failed_checks": list(proof.get("failed_checks") or []),
        "proof_warning_checks": list(proof.get("warning_checks") or []),
        "provider_fetchable_count": int(report_data.get("provider_fetchable_count") or 0),
        "selected_reference_count": int(report_data.get("selected_reference_count") or 0),
        "artifact_count": int(report_data.get("artifact_count") or len(row.get("artifact_names") or [])),
        "artifact_catalog_count": int(report_data.get("artifact_catalog_count") or 0),
        "selection_reason": str(report_data.get("selection_reason") or ""),
        "links": {
            "self": base,
            "acceptance": f"{base}/acceptance" if base else "",
            "evaluations": f"{base}/evaluations" if base else "",
            "evaluation_draft": f"{base}/evaluations/draft" if base else "",
            "replay": f"{base}/replay" if base else "",
            "export": f"{base}/export" if base else "",
        },
    }


def _overview_run(summary: dict[str, Any]) -> dict[str, Any]:
    row = _comparison_run(summary)
    evaluation = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation_summary_data = evaluation.get("summary") if isinstance(evaluation.get("summary"), dict) else {}
    reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    artifacts = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    case_id = str(summary.get("case_id") or "")
    return {
        "case_id": case_id,
        "run_id": row["run_id"],
        "workflow_name": str(summary.get("workflow_name") or ""),
        "status": row["status"],
        "created_at": row["created_at"],
        "finished_at": row["finished_at"],
        "reference_status": row["reference_status"],
        "reference_required": row["reference_required"],
        "reference_sent": row["reference_sent"],
        "cover_count": row["cover_count"],
        "artifact_count": len(artifacts),
        "evaluation_status": row["evaluation_status"],
        "evaluation_score": row["evaluation_score"],
        "evaluation_count": row["evaluation_count"],
        "candidate": row["candidate"],
        "proof_status": str((summary.get("proof") or {}).get("status") or ""),
        "proof_failed_checks": list((summary.get("proof") or {}).get("failed_checks") or []),
        "proof_warning_checks": list((summary.get("proof") or {}).get("warning_checks") or []),
        "acceptance_status": row["acceptance_status"],
        "accepted": row["accepted"],
        "acceptance_blocking_checks": row["acceptance_blocking_checks"],
        "acceptance_warning_checks": row["acceptance_warning_checks"],
        "links": {
            "self": f"/workflows/content-production/runs/{case_id}/{row['run_id']}",
            "evaluations": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/evaluations",
            "replay": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/replay",
            "export": f"/workflows/content-production/runs/{case_id}/{row['run_id']}/export",
        },
        "image_reference": {
            "status": str(reference.get("status") or ""),
            "selected_count": int(reference.get("selected_count") or 0),
            "sent": bool(reference.get("sent")),
            "fallback": str(reference.get("fallback") or ""),
        },
        "evaluations": evaluation_summary_data,
    }


def _overview_case(rows: list[dict[str, Any]], *, project_root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    latest = rows[0] if rows else {}
    case_id = str(latest.get("case_id") or "")
    latest_run_id = str(latest.get("run_id") or "")
    latest_base = f"/workflows/content-production/runs/{case_id}/{latest_run_id}" if case_id and latest_run_id else ""
    selection = _case_selection_payload(
        _content_case_dir_or_none(project_root=project_root, case_id=case_id),
        include_history=False,
    ).get("current") or {}
    return {
        "case_id": case_id,
        "run_count": len(rows),
        "latest_run_id": latest_run_id,
        "latest_status": str(latest.get("status") or ""),
        "latest_created_at": str(latest.get("created_at") or ""),
        "latest_finished_at": str(latest.get("finished_at") or ""),
        "status_counts": _count_by(rows, "status"),
        "acceptance_status_counts": _count_by(rows, "acceptance_status"),
        "reference_status_counts": _count_by(rows, "reference_status"),
        "evaluation_status_counts": _count_by(rows, "evaluation_status"),
        "ready_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
        "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
        "selection": selection,
        "selected_run_id": str(selection.get("run_id") or ""),
        "selection_decision": str(selection.get("decision") or ""),
        "links": {
            "runs": f"/workflows/content-production/runs?case_id={case_id}" if case_id else "",
            "run_template": f"/experiments/content-production/run-template?case_id={case_id}" if case_id else "",
            "selection": f"/experiments/content-production/cases/{case_id}/selection" if case_id else "",
            "selected_run": f"/experiments/content-production/cases/{case_id}/selected-run" if case_id else "",
            "next_actions": f"/experiments/content-production/cases/{case_id}/next-actions" if case_id else "",
            "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft" if case_id else "",
            "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations" if case_id else "",
            "case_delivery": f"/experiments/content-production/cases/{case_id}/delivery" if case_id else "",
            "case_delivery_export": f"/experiments/content-production/cases/{case_id}/delivery/export" if case_id else "",
            "case_replay": f"/experiments/content-production/cases/{case_id}/replay" if case_id else "",
            "case_timeline": f"/experiments/content-production/cases/{case_id}/timeline" if case_id else "",
            "case_export": f"/experiments/content-production/cases/{case_id}/export" if case_id else "",
            "latest_run": latest_base,
            "latest_export": f"{latest_base}/export" if latest_base else "",
            "latest_replay": f"{latest_base}/replay" if latest_base else "",
        },
    }


def _report_run(summary: dict[str, Any]) -> dict[str, Any]:
    row = _comparison_run(summary)
    case_id = str(summary.get("case_id") or "")
    run_id = row["run_id"]
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    evidence = acceptance.get("evidence") if isinstance(acceptance.get("evidence"), dict) else {}
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    evaluation = evaluations.get("summary") if isinstance(evaluations.get("summary"), dict) else {}
    transfer = _summary_reference_transfer(summary)
    artifact_catalog = [item for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    base = f"/workflows/content-production/runs/{case_id}/{run_id}" if case_id and run_id else ""
    return {
        "case_id": case_id,
        "run_id": run_id,
        "session_id": row["session_id"],
        "task_id": row["task_id"],
        "workflow_name": str(summary.get("workflow_name") or ""),
        "status": row["status"],
        "created_at": row["created_at"],
        "finished_at": row["finished_at"],
        "acceptance_status": row["acceptance_status"],
        "accepted": row["accepted"],
        "proof_status": str(proof.get("status") or ""),
        "evaluation_status": row["evaluation_status"],
        "evaluation_score": row["evaluation_score"],
        "evaluation_count": row["evaluation_count"],
        "reference_status": row["reference_status"],
        "reference_required": row["reference_required"],
        "reference_sent": row["reference_sent"],
        "asset_ids": list(row.get("asset_ids") or []),
        "run_options": dict(row.get("run_options") or {}),
        "backend_public_base_url": str(row.get("backend_public_base_url") or ""),
        "provider_fetchable_count": int(transfer.get("provider_fetchable_count") or evidence.get("provider_fetchable_count") or 0),
        "selected_reference_count": int(transfer.get("selected_count") or evidence.get("selected_reference_count") or 0),
        "cover_count": row["cover_count"],
        "artifact_count": len(summary.get("artifact_paths") or {}),
        "artifact_catalog_count": len(artifact_catalog),
        "blocking_checks": row["acceptance_blocking_checks"],
        "warning_checks": row["acceptance_warning_checks"],
        "proof_failed_checks": list(proof.get("failed_checks") or []),
        "proof_warning_checks": list(proof.get("warning_checks") or []),
        "candidate": row["candidate"],
        "evaluation": dict(evaluation),
        "links": {
            "self": base,
            "acceptance": f"{base}/acceptance" if base else "",
            "evaluations": f"{base}/evaluations" if base else "",
            "evaluation_draft": f"{base}/evaluations/draft" if base else "",
            "replay": f"{base}/replay" if base else "",
            "export": f"{base}/export" if base else "",
        },
    }


def _report_run_score(summary: dict[str, Any]) -> tuple[int, int, int, int, int, int, float, str]:
    row = _comparison_run(summary)
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance_rank = {"accepted": 3, "needs_review": 2, "rejected": 1}.get(row["acceptance_status"], 0)
    proof_rank = {"ready": 3, "needs_review": 2, "blocked": 1}.get(str(proof.get("status") or ""), 0)
    evaluation_rank = {"passed": 3, "pending": 2, "needs_revision": 1, "blocked": 0}.get(row["evaluation_status"], 0)
    reference_rank = 2 if (not row["reference_required"] or row["reference_sent"]) else 0
    cover_rank = min(int(row["cover_count"] or 0), 3)
    artifact_rank = min(len(row["artifact_names"]), 10)
    score = row.get("evaluation_score")
    numeric_score = float(score) if isinstance(score, (int, float)) else -1.0
    return (
        acceptance_rank,
        proof_rank,
        evaluation_rank,
        reference_rank,
        cover_rank,
        artifact_rank,
        numeric_score,
        str(row.get("created_at") or ""),
    )


def _best_run_reason(row: dict[str, Any]) -> str:
    if row.get("acceptance_status") == "accepted":
        return "accepted run with the strongest proof, evaluation, reference, and artifact signal"
    if row.get("acceptance_status") == "needs_review":
        return "highest-scoring run that still needs operator review"
    if row.get("acceptance_status") == "rejected":
        return "least-blocked rejected run; use its blocking checks as the next repair target"
    return "highest-scoring available run"


def _report_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status_counts": _count_by(rows, "status"),
        "acceptance_status_counts": _count_by(rows, "acceptance_status"),
        "proof_status_counts": _count_by(rows, "proof_status"),
        "reference_status_counts": _count_by(rows, "reference_status"),
        "evaluation_status_counts": _count_by(rows, "evaluation_status"),
        "blocking_check_counts": _count_values([name for row in rows for name in row["blocking_checks"]]),
        "warning_check_counts": _count_values([name for row in rows for name in row["warning_checks"]]),
        "proof_failed_check_counts": _count_values([name for row in rows for name in row["proof_failed_checks"]]),
        "proof_warning_check_counts": _count_values([name for row in rows for name in row["proof_warning_checks"]]),
        "candidate_blocking_reason_counts": _count_values(
            [name for row in rows for name in row["candidate"]["blocking_reasons"]]
        ),
        "evaluation_issue_counts": _evaluation_issue_counts(rows),
        "accepted_count": sum(1 for row in rows if row["acceptance_status"] == "accepted"),
        "needs_review_count": sum(1 for row in rows if row["acceptance_status"] == "needs_review"),
        "rejected_count": sum(1 for row in rows if row["acceptance_status"] == "rejected"),
        "ready_for_review_count": sum(1 for row in rows if row["candidate"]["ready_for_review"]),
        "blocked_count": sum(1 for row in rows if not row["candidate"]["ready_for_review"]),
    }


def _evaluation_issue_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    issue_codes: list[str] = []
    for row in rows:
        for issue in row.get("evaluation", {}).get("issues") or []:
            if isinstance(issue, dict):
                issue_codes.append(str(issue.get("code") or issue.get("category") or "issue"))
    return _count_values(issue_codes)


def _report_recommendations(
    rows: list[dict[str, Any]],
    *,
    best_run: dict[str, Any],
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    if not rows:
        return [
            {
                "action_id": "run_first_experiment",
                "severity": "next_step",
                "message": "Run the first content-production experiment for this case.",
            }
        ]

    recommendations: list[dict[str, Any]] = []
    accepted_ids = [row["run_id"] for row in rows if row["acceptance_status"] == "accepted"]
    needs_review_ids = [row["run_id"] for row in rows if row["acceptance_status"] == "needs_review"]
    blocked_counts = dict(summary.get("blocking_check_counts") or {})
    candidate_counts = dict(summary.get("candidate_blocking_reason_counts") or {})
    proof_failed = dict(summary.get("proof_failed_check_counts") or {})
    evaluation_counts = dict(summary.get("evaluation_status_counts") or {})

    if accepted_ids:
        recommendations.append(
            {
                "action_id": "promote_accepted_run",
                "severity": "next_step",
                "message": "Promote the best accepted run into product review, export, or publishing preparation.",
                "run_id": str(best_run.get("run_id") or accepted_ids[0]),
            }
        )
    elif needs_review_ids:
        recommendations.append(
            {
                "action_id": "review_pending_runs",
                "severity": "review",
                "message": "Review the strongest needs_review runs and persist an evaluation decision.",
                "run_ids": needs_review_ids[:5],
            }
        )
    else:
        recommendations.append(
            {
                "action_id": "fix_blockers",
                "severity": "blocking",
                "message": "All visible runs are rejected; fix the most common blocking checks before rerunning.",
                "blocking_check_counts": blocked_counts,
            }
        )

    if blocked_counts.get("strict_reference_satisfied") or candidate_counts.get("strict_reference_not_sent"):
        recommendations.append(
            {
                "action_id": "fix_reference_transfer",
                "severity": "blocking",
                "message": "Fix reference-image transfer so selected uploads are provider-fetchable and sent to the image model.",
            }
        )
    if blocked_counts.get("cover_output_available") or candidate_counts.get("missing_cover") or proof_failed.get("cover_output"):
        recommendations.append(
            {
                "action_id": "rerun_cover_generation",
                "severity": "blocking",
                "message": "Rerun or debug cover generation; at least one run is missing image output.",
            }
        )
    if blocked_counts.get("content_package_available") or candidate_counts.get("missing_content_package"):
        recommendations.append(
            {
                "action_id": "debug_content_package",
                "severity": "blocking",
                "message": "Debug content package generation before comparing creative quality.",
            }
        )
    if evaluation_counts.get("passed", 0) < 1:
        recommendations.append(
            {
                "action_id": "record_or_draft_evaluation",
                "severity": "review",
                "message": "Generate or record at least one passing evaluation so the case has a reviewable winner.",
            }
            )
    return recommendations


def _workbench_active_run_id(case_compare: dict[str, Any]) -> str:
    for key in ("recommended_run_id", "target_run_id", "selected_run_id", "best_run_id"):
        value = str(case_compare.get(key) or "").strip()
        if value:
            return value
    return ""


def _case_delivery_status(blockers: list[str], warnings: list[str]) -> str:
    if not blockers:
        return "preview_ready" if "unpromoted_preview" in warnings else "ready"
    if "no_run" in blockers:
        return "needs_run"
    if "run_not_found" in blockers:
        return "missing_run"
    if "not_promoted" in blockers:
        return "needs_promotion"
    if "not_accepted" in blockers:
        return "needs_acceptance"
    if "missing_core_artifacts" in blockers:
        return "needs_artifacts"
    return "blocked"


def _case_delivery_payload(*, case_id: str, run_id: str, inspection: dict[str, Any]) -> dict[str, Any]:
    if not run_id or not inspection:
        return {
            "content_package": {},
            "covers": [],
            "export_url": "",
            "artifact_inspection_url": "",
        }
    return {
        "content_package": dict(inspection.get("content_package") or {}),
        "covers": list(inspection.get("covers") or []),
        "visual_reference_review": dict(inspection.get("visual_reference_review") or {}),
        "export_url": _run_export_url(case_id, run_id),
        "artifact_inspection_url": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
    }


def _delivery_review_evidence(*, delivery: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    inspection = delivery.get("artifact_inspection") if isinstance(delivery.get("artifact_inspection"), dict) else {}
    return {
        "schema_version": 1,
        "case_id": str(delivery.get("case_id") or summary.get("case_id") or ""),
        "run_id": str(delivery.get("run_id") or summary.get("run_id") or ""),
        "ready": bool(delivery.get("ready")),
        "status": str(delivery.get("status") or ""),
        "blocking_reasons": list(delivery.get("blocking_reasons") or []),
        "warning_reasons": list(delivery.get("warning_reasons") or []),
        "proof": dict(delivery.get("proof") or summary.get("proof") or {}),
        "acceptance": dict(delivery.get("acceptance") or summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }


def _run_review_evidence(*, summary: dict[str, Any], inspection: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": str(summary.get("case_id") or ""),
        "run_id": str(summary.get("run_id") or ""),
        "status": str(summary.get("status") or ""),
        "proof": dict(summary.get("proof") or {}),
        "acceptance": dict(summary.get("acceptance") or {}),
        "evaluations": dict(inspection.get("evaluations") or summary.get("evaluations") or {}),
        "image_reference": dict(inspection.get("image_reference") or summary.get("image_reference") or {}),
        "visual_reference_review": dict(
            inspection.get("visual_reference_review")
            or summary.get("visual_reference_review")
            or {}
        ),
        "artifact_counts": dict(inspection.get("artifact_counts") or {}),
        "missing_core_artifacts": list(inspection.get("missing_core_artifacts") or []),
    }


def _workbench_case(row: dict[str, Any], *, project_root: str | Path) -> dict[str, Any]:
    case_id = str(row.get("case_id") or "")
    next_actions = content_production_case_next_actions(project_root=project_root, case_id=case_id)
    case_base = f"/experiments/content-production/cases/{case_id}" if case_id else ""
    return {
        **dict(row),
        "action_status": str(next_actions.get("status") or ""),
        "target_run_id": str(next_actions.get("target_run_id") or ""),
        "primary_action": dict(next_actions.get("primary_action") or {}),
        "actions": list(next_actions.get("actions") or []),
        "action_count": len(next_actions.get("actions") or []),
        "links": {
            **dict(row.get("links") or {}),
            "next_actions": f"{case_base}/next-actions" if case_base else "",
            "case_evaluation_draft": f"{case_base}/evaluations/draft" if case_base else "",
            "case_evaluations": f"{case_base}/evaluations" if case_base else "",
        },
    }


def _empty_workbench_case(case_id: str) -> dict[str, Any]:
    actions = _case_next_actions(
        case_id=case_id,
        status="needs_first_run",
        selection={},
        selected_missing=False,
        selected_run={},
        best_run={},
        target_run={},
        report={},
    )
    return {
        "case_id": case_id,
        "run_count": 0,
        "latest_run_id": "",
        "latest_status": "",
        "ready_count": 0,
        "blocked_count": 0,
        "selection": {},
        "selected_run_id": "",
        "selection_decision": "",
        "action_status": "needs_first_run",
        "target_run_id": "",
        "primary_action": actions[0] if actions else {},
        "actions": actions,
        "action_count": len(actions),
        "links": {
            "runs": f"/workflows/content-production/runs?case_id={case_id}",
            "run_template": f"/experiments/content-production/run-template?case_id={case_id}",
            "selection": f"/experiments/content-production/cases/{case_id}/selection",
            "next_actions": f"/experiments/content-production/cases/{case_id}/next-actions",
            "case_evaluation_draft": f"/experiments/content-production/cases/{case_id}/evaluations/draft",
            "case_evaluations": f"/experiments/content-production/cases/{case_id}/evaluations",
        },
    }


def _workbench_status(*, diagnostics: dict[str, Any], cases: list[dict[str, Any]], overview: dict[str, Any]) -> str:
    if diagnostics and str(diagnostics.get("status") or "") == "blocked":
        return "setup_blocked"
    if not cases and int(overview.get("run_count") or 0) == 0:
        return "empty"
    severities = [
        str((row.get("primary_action") or {}).get("severity") or "")
        for row in cases
        if isinstance(row.get("primary_action"), dict)
    ]
    if "blocking" in severities:
        return "needs_attention"
    if severities:
        return "actionable"
    return "ready"


def _case_next_action_status(
    *,
    run_count: int,
    selection: dict[str, Any],
    selected_missing: bool,
    target_run: dict[str, Any],
) -> str:
    if run_count == 0:
        return "needs_first_run"
    if selected_missing:
        return "selection_stale"
    if not selection:
        return "needs_selection"
    decision = str(selection.get("decision") or "")
    if decision in {"rejected", "archived"}:
        return "selection_rejected"
    acceptance = str(target_run.get("acceptance_status") or "")
    evaluation = str(target_run.get("evaluation_status") or "")
    if decision == "promoted" and acceptance == "accepted" and evaluation == "passed":
        return "promoted"
    if acceptance == "accepted" and evaluation == "passed":
        return "ready_to_promote"
    if acceptance == "needs_review" or evaluation == "pending":
        return "needs_review"
    return "blocked"


def _case_next_actions(
    *,
    case_id: str,
    status: str,
    selection: dict[str, Any],
    selected_missing: bool,
    selected_run: dict[str, Any],
    best_run: dict[str, Any],
    target_run: dict[str, Any],
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    if status == "needs_first_run":
        template_href = f"/experiments/content-production/run-template?case_id={case_id}&human_gate_mode=skip"
        return [
            {
                "action_id": "run_first_experiment",
                "severity": "next_step",
                "label": "Run experiment",
                "message": "Build a backend launch template, resolve missing fields, then run the first content-production experiment for this case.",
                "method": "GET",
                "href": template_href,
                "payload": {"case_id": case_id, "human_gate_mode": "skip"},
                "links": {
                    "run_template": template_href,
                    "preflight": "/workflows/content-production/runs/preflight",
                    "run": "/workflows/content-production/runs",
                },
            }
        ]

    if selected_missing:
        return [
            {
                "action_id": "repair_stale_selection",
                "severity": "blocking",
                "label": "Repair selection",
                "message": "The current case selection points to a run that no longer exists; select the best visible run.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/selection",
                "payload": _selection_payload(best_run, decision="selected", reason="replace stale selection"),
            }
        ]

    actions: list[dict[str, Any]] = []
    if status == "promoted" and target_run:
        run_id = str(target_run.get("run_id") or "")
        return [
            {
                "action_id": "export_promoted_run",
                "severity": "next_step",
                "label": "Export run",
                "message": "The selected run has already been promoted; export it for product review or publishing.",
                "run_id": run_id,
                "method": "GET",
                "href": _run_export_url(case_id, run_id),
            },
            {
                "action_id": "inspect_promoted_run",
                "severity": "review",
                "label": "Inspect run",
                "message": "Inspect the promoted run artifacts, proof, and evaluation evidence.",
                "run_id": run_id,
                "method": "GET",
                "href": f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect",
            },
        ]

    if not selection and best_run:
        actions.append(
            {
                "action_id": "select_best_run",
                "severity": "next_step",
                "label": "Select best run",
                "message": "Persist the backend-selected best run as the current operator selection.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/selection",
                "payload": _selection_payload(best_run, decision="selected", reason="backend best run"),
            }
        )

    target_acceptance = str(target_run.get("acceptance_status") or "")
    target_evaluation = str(target_run.get("evaluation_status") or "")
    if status == "ready_to_promote" and target_run:
        actions.append(
            {
                "action_id": "promote_selected_run",
                "severity": "next_step",
                "label": "Promote run",
                "message": "The selected run is accepted and has a passing evaluation; export it for product review or publishing.",
                "run_id": str(target_run.get("run_id") or ""),
                "method": "POST",
                "href": f"/experiments/content-production/cases/{case_id}/promotion",
                "payload": {
                    "run_id": str(target_run.get("run_id") or ""),
                    "reason": "promote accepted run",
                },
            }
        )
    elif target_run and (target_acceptance == "rejected" or target_evaluation in {"blocked", "needs_revision"}):
        actions.extend(_repair_actions(case_id=case_id, target_run=target_run, report=report))
    elif status in {"needs_review", "needs_selection"} and target_run:
        actions.extend(_review_actions(case_id=case_id, target_run=target_run))
    elif status in {"blocked", "selection_rejected"} and target_run:
        actions.extend(_repair_actions(case_id=case_id, target_run=target_run, report=report))

    if not actions and best_run:
        actions.append(
            {
                "action_id": "inspect_best_run",
                "severity": "review",
                "label": "Inspect run",
                "message": "Inspect the strongest visible run and decide whether to evaluate, select, or rerun.",
                "run_id": str(best_run.get("run_id") or ""),
                "method": "GET",
                "href": f"/workflows/content-production/runs/{case_id}/{best_run.get('run_id')}",
            }
        )
    return actions


def _selection_payload(run: dict[str, Any], *, decision: str, reason: str) -> dict[str, Any]:
    run_id = str(run.get("run_id") or "")
    return {
        "run_id": run_id,
        "decision": decision,
        "reviewer": "operator",
        "reason": reason,
    }


def _review_actions(*, case_id: str, target_run: dict[str, Any]) -> list[dict[str, Any]]:
    run_id = str(target_run.get("run_id") or "")
    base = f"/experiments/content-production/cases/{case_id}"
    actions = [
        {
            "action_id": "draft_evaluation",
            "severity": "review",
            "label": "Draft evaluation",
            "message": "Generate a deterministic backend evaluation draft for the target run.",
            "run_id": run_id,
            "method": "POST",
            "href": f"{base}/evaluations/draft",
            "payload": {"run_id": run_id, "reviewer": "operator", "persist": False},
        }
    ]
    if str(target_run.get("evaluation_status") or "") == "pending":
        actions.append(
            {
                "action_id": "record_evaluation",
                "severity": "review",
                "label": "Record evaluation",
                "message": "Persist a manual or automated evaluation decision for the target run.",
                "run_id": run_id,
                "method": "POST",
                "href": f"{base}/evaluations",
                "payload": {"run_id": run_id},
            }
        )
    return actions


def _repair_actions(*, case_id: str, target_run: dict[str, Any], report: dict[str, Any]) -> list[dict[str, Any]]:
    run_id = str(target_run.get("run_id") or "")
    blockers = [
        *[str(item) for item in target_run.get("blocking_checks") or []],
        *[str(item) for item in target_run.get("proof_failed_checks") or []],
    ]
    if (
        "strict_reference_satisfied" in blockers
        or "provider_reference_check_satisfied" in blockers
        or "reference_image_generation_check" in blockers
        or str(target_run.get("reference_status") or "") in {"fallback", "failed_required"}
    ):
        action_id = "check_reference_image_generation" if (
            "provider_reference_check_satisfied" in blockers or "reference_image_generation_check" in blockers
        ) else "fix_reference_transfer"
        href = _reference_repair_href(action_id=action_id, target_run=target_run)
        payload = _reference_repair_payload(action_id=action_id, case_id=case_id, target_run=target_run)
        return [
            {
                "action_id": action_id,
                "severity": "blocking",
                "label": "Check references" if action_id == "check_reference_image_generation" else "Fix references",
                "message": (
                    "Run the session reference-image generation check, then rerun the experiment with strict provider-check evidence."
                    if action_id == "check_reference_image_generation"
                    else "Publish selected images as provider-fetchable references, then rerun the experiment."
                ),
                "run_id": run_id,
                "method": "POST",
                "href": href,
                "payload": payload,
                "blockers": blockers,
            },
            _rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
        ]
    recommendations = [item for item in report.get("recommendations") or [] if isinstance(item, dict)]
    return [
        {
            "action_id": "fix_blockers",
            "severity": "blocking",
            "label": "Fix blockers",
            "message": "Fix the target run blockers before promoting this case.",
            "run_id": run_id,
            "method": "GET",
            "href": f"/workflows/content-production/runs/{case_id}/{run_id}/acceptance",
            "blockers": blockers,
            "recommendation_ids": [str(item.get("action_id") or "") for item in recommendations if item.get("action_id")],
        },
        _rerun_action(case_id=case_id, run_id=run_id, blockers=blockers, target_run=target_run),
    ]


def _reference_repair_href(*, action_id: str, target_run: dict[str, Any]) -> str:
    session_id = str(target_run.get("session_id") or "").strip()
    route = (
        "reference-image-generation-check"
        if action_id == "check_reference_image_generation"
        else "publish-references"
    )
    if session_id:
        return f"/sessions/{session_id}/assets/{route}"
    return f"/sessions/{{session_id}}/assets/{route}"


def _reference_repair_payload(*, action_id: str, case_id: str, target_run: dict[str, Any]) -> dict[str, Any]:
    asset_ids = [str(item) for item in target_run.get("asset_ids") or [] if str(item)]
    run_options = target_run.get("run_options") if isinstance(target_run.get("run_options"), dict) else {}
    backend_public_base_url = str(
        target_run.get("backend_public_base_url") or run_options.get("backend_public_base_url") or ""
    ).strip()
    payload: dict[str, Any] = {"asset_ids": asset_ids}
    if backend_public_base_url:
        payload["backend_public_base_url"] = backend_public_base_url
    if action_id == "check_reference_image_generation":
        try:
            timeout = float(run_options.get("reference_url_probe_timeout") or 3.0)
        except (TypeError, ValueError):
            timeout = 3.0
        payload.update(
            {
                "verify_reference_urls": bool(run_options.get("verify_reference_urls")),
                "reference_url_probe_timeout": timeout,
                "prompt": "Generate a simple product image using the selected session reference image.",
                "size": "1024x1024",
                "metadata": {
                    "source": "content_production_case_next_actions",
                    "case_id": case_id,
                    "run_id": str(target_run.get("run_id") or ""),
                },
            }
        )
    else:
        payload["metadata"] = {
            "source": "content_production_case_next_actions",
            "case_id": case_id,
            "run_id": str(target_run.get("run_id") or ""),
        }
    return payload


def _rerun_action(
    *,
    case_id: str,
    run_id: str,
    blockers: list[str],
    target_run: dict[str, Any] | None = None,
) -> dict[str, Any]:
    target_run = target_run if isinstance(target_run, dict) else {}
    session_id = str(target_run.get("session_id") or "").strip()
    payload: dict[str, Any] = {"run_id": run_id, "human_gate_mode": "skip", "metadata": {"blockers": blockers}}
    if session_id:
        payload["session_id"] = session_id
    return {
        "action_id": "replay_or_rerun",
        "severity": "next_step",
        "label": "Replay run",
        "message": "Replay the target run after fixing blockers, or start a new run with corrected inputs.",
        "run_id": run_id,
        "method": "POST",
        "href": f"/experiments/content-production/cases/{case_id}/replay",
        "payload": payload,
        "blockers": blockers,
    }


def _case_selection_payload(case_dir: Path | None, *, include_history: bool) -> dict[str, Any]:
    if case_dir is None:
        return {"schema_version": 1, "case_id": "", "current": {}, "history": [] if include_history else []}
    data = _read_json(case_dir / EXPERIMENT_SELECTION_NAME)
    current = data.get("current") if isinstance(data.get("current"), dict) else {}
    history = data.get("history") if isinstance(data.get("history"), list) else []
    payload = {
        "schema_version": int(data.get("schema_version") or 1),
        "case_id": str(data.get("case_id") or case_dir.name),
        "current": dict(current),
    }
    if include_history:
        payload["history"] = [dict(item) for item in history if isinstance(item, dict)]
    return payload


def _normalize_case_selection(
    data: dict[str, Any],
    *,
    case_id: str,
    run_summary: dict[str, Any],
    report: dict[str, Any],
    existing_count: int,
) -> dict[str, Any]:
    decision = str(data.get("decision") or "selected").strip().lower()
    if decision not in SELECTION_DECISIONS:
        raise ValueError(f"unsupported selection decision: {decision}")
    run = _report_run(run_summary)
    reviewer = str(data.get("reviewer") or "operator").strip() or "operator"
    created_at = datetime.now().isoformat(timespec="seconds")
    run_id = str(run.get("run_id") or "")
    seed = f"{case_id}:{run_id}:{decision}:{reviewer}:{created_at}:{existing_count}"
    best_run = report.get("best_run") if isinstance(report.get("best_run"), dict) else {}
    best_run_id = str(best_run.get("run_id") or "")
    return {
        "selection_id": f"sel_{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}",
        "selected_at": created_at,
        "case_id": case_id,
        "run_id": run_id,
        "decision": decision,
        "reviewer": reviewer,
        "reason": str(data.get("reason") or ""),
        "notes": str(data.get("notes") or ""),
        "metadata": dict(data.get("metadata") or {}),
        "report_best_run_id": best_run_id,
        "matches_report_best": bool(best_run_id and run_id == best_run_id),
        "run": {
            "status": run.get("status"),
            "acceptance_status": run.get("acceptance_status"),
            "proof_status": run.get("proof_status"),
            "evaluation_status": run.get("evaluation_status"),
            "evaluation_score": run.get("evaluation_score"),
            "reference_status": run.get("reference_status"),
            "reference_sent": run.get("reference_sent"),
            "cover_count": run.get("cover_count"),
            "links": dict(run.get("links") or {}),
        },
    }


def _timeline_events_for_run(summary: dict[str, Any]) -> list[dict[str, Any]]:
    case_id = str(summary.get("case_id") or "")
    run_id = str(summary.get("run_id") or "")
    row = _report_run(summary)
    base = {
        "case_id": case_id,
        "run_id": run_id,
        "workflow_name": str(summary.get("workflow_name") or ""),
        "run_status": str(row.get("status") or ""),
        "acceptance_status": str(row.get("acceptance_status") or ""),
        "proof_status": str(row.get("proof_status") or ""),
        "evaluation_status": str(row.get("evaluation_status") or ""),
        "reference_status": str(row.get("reference_status") or ""),
        "links": dict(row.get("links") or {}),
    }
    events: list[dict[str, Any]] = []
    created_at = str(summary.get("created_at") or "")
    if created_at:
        events.append(
            {
                **base,
                "event_id": f"run_started:{case_id}:{run_id}",
                "event_type": "run_started",
                "timestamp": created_at,
                "title": f"Run started: {run_id}",
            }
        )
    finished_at = str(summary.get("finished_at") or "")
    if finished_at:
        events.append(
            {
                **base,
                "event_id": f"run_finished:{case_id}:{run_id}",
                "event_type": "run_finished",
                "timestamp": finished_at,
                "title": f"Run finished: {run_id}",
            }
        )
    evaluations = summary.get("evaluations") if isinstance(summary.get("evaluations"), dict) else {}
    for evaluation in evaluations.get("items") or []:
        if isinstance(evaluation, dict):
            events.append(_timeline_evaluation_event(evaluation, base=base))
    return events


def _timeline_evaluation_event(evaluation: dict[str, Any], *, base: dict[str, Any]) -> dict[str, Any]:
    evaluation_id = str(evaluation.get("evaluation_id") or "")
    run_id = str(base.get("run_id") or "")
    timestamp = str(evaluation.get("created_at") or "")
    return {
        **base,
        "event_id": evaluation_id or f"evaluation:{base.get('case_id')}:{run_id}:{timestamp}",
        "event_type": "evaluation_recorded",
        "timestamp": timestamp,
        "title": f"Evaluation recorded: {run_id}",
        "evaluation_id": evaluation_id,
        "reviewer": str(evaluation.get("reviewer") or ""),
        "source": str(evaluation.get("source") or ""),
        "status": str(evaluation.get("status") or ""),
        "score": evaluation.get("score"),
        "issue_count": len(evaluation.get("issues") or []),
    }


def _timeline_selection_event(selection: dict[str, Any]) -> dict[str, Any]:
    case_id = str(selection.get("case_id") or "")
    run_id = str(selection.get("run_id") or "")
    return {
        "event_id": str(selection.get("selection_id") or f"selection:{case_id}:{run_id}:{selection.get('selected_at') or ''}"),
        "event_type": "selection_recorded",
        "timestamp": str(selection.get("selected_at") or ""),
        "title": f"Selection recorded: {run_id}",
        "case_id": case_id,
        "run_id": run_id,
        "decision": str(selection.get("decision") or ""),
        "reviewer": str(selection.get("reviewer") or ""),
        "reason": str(selection.get("reason") or ""),
        "matches_report_best": bool(selection.get("matches_report_best")),
        "run_status": str((selection.get("run") or {}).get("status") or ""),
        "acceptance_status": str((selection.get("run") or {}).get("acceptance_status") or ""),
        "links": dict((selection.get("run") or {}).get("links") or {}),
    }


def _timeline_sort_key(event: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(event.get("timestamp") or ""),
        str(event.get("event_type") or ""),
        str(event.get("event_id") or ""),
    )


def _candidate_status(row: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if row["status"] != "succeeded":
        blockers.append("run_not_succeeded")
    if "content_package.json" not in row["artifact_names"]:
        blockers.append("missing_content_package")
    if row["cover_count"] < 1:
        blockers.append("missing_cover")
    if row["reference_required"] and not row["reference_sent"]:
        blockers.append("strict_reference_not_sent")
    if row.get("evaluation_status") == "blocked":
        blockers.append("evaluation_blocked")
    elif row.get("evaluation_status") == "needs_revision":
        blockers.append("evaluation_needs_revision")
    return {
        "ready_for_review": not blockers,
        "blocking_reasons": blockers,
    }


def _run_matches_filters(
    summary: dict[str, Any],
    *,
    status: str,
    proof_status: str,
    reference_status: str,
    evaluation_status: str,
    search: str,
) -> bool:
    row = _comparison_run(summary)
    if status and row["status"] != status:
        return False
    actual_proof_status = str((summary.get("proof") or {}).get("status") or "")
    if proof_status and actual_proof_status != proof_status:
        return False
    if reference_status and row["reference_status"] != reference_status:
        return False
    if evaluation_status and row["evaluation_status"] != evaluation_status:
        return False
    needle = str(search or "").strip().lower()
    if not needle:
        return True
    return needle in _run_search_text(summary, row)


def _run_search_text(summary: dict[str, Any], row: dict[str, Any]) -> str:
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    market = inputs.get("market_evidence") if isinstance(inputs.get("market_evidence"), dict) else input_manifest.get("market_evidence")
    artifacts = [str(item.get("artifact_name") or "") for item in summary.get("artifact_catalog") or [] if isinstance(item, dict)]
    values = [
        str(summary.get("case_id") or ""),
        str(summary.get("run_id") or ""),
        str(summary.get("workflow_name") or ""),
        row["status"],
        str((summary.get("proof") or {}).get("status") or ""),
        str((summary.get("acceptance") or {}).get("status") or ""),
        row["reference_status"],
        row["evaluation_status"],
        *row["market_queries"],
        *_string_list((market or {}).get("queries") if isinstance(market, dict) else []),
        *artifacts,
    ]
    return " ".join(value.lower() for value in values if value)


def _asset_fingerprints(assets: Any) -> list[str]:
    out: list[str] = []
    source = assets if isinstance(assets, list) else []
    for item in source:
        if not isinstance(item, dict):
            continue
        value = (
            str(item.get("sha256") or "").strip()
            or str(item.get("public_reference_url") or "").strip()
            or str(item.get("path") or "").strip()
            or str(item.get("asset_id") or "").strip()
        )
        if value:
            out.append(value)
    return out


def _count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "")
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_values(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        text = str(value or "")
        counts[text] = counts.get(text, 0) + 1
    return counts


def _value_diff(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = {row["run_id"]: row.get(key) for row in rows}
    comparable = [json.dumps(value, ensure_ascii=False, sort_keys=True, default=str) for value in values.values()]
    return {
        "changed": len(set(comparable)) > 1,
        "by_run": values,
    }


def _dedupe_strings(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _write_experiment_manifest(
    *,
    run_dir: Path,
    workflow_name: str,
    workflow_run: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    input_manifest: dict[str, Any],
    require_image_references: bool,
    error: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = _experiment_manifest(
        run_dir=run_dir,
        workflow_name=workflow_name,
        workflow_run=workflow_run,
        asset_rows=asset_rows,
        input_manifest=input_manifest,
        require_image_references=require_image_references,
        error=error,
    )
    _write_json(run_dir / EXPERIMENT_MANIFEST_NAME, manifest)
    return manifest


def _experiment_manifest(
    *,
    run_dir: Path,
    workflow_name: str,
    workflow_run: dict[str, Any],
    asset_rows: list[dict[str, Any]],
    input_manifest: dict[str, Any],
    require_image_references: bool,
    error: dict[str, Any] | None = None,
) -> dict[str, Any]:
    case_id = str(input_manifest.get("case_id") or _case_id_from_run_dir(run_dir))
    run_id = run_dir.name
    status = str(workflow_run.get("status") or ("failed" if error else "unknown"))
    artifact_paths = {
        path.name: str(path)
        for path in sorted(run_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".json", ".md"}
    }
    artifact_paths[EXPERIMENT_MANIFEST_NAME] = str(run_dir / EXPERIMENT_MANIFEST_NAME)
    artifact_urls = artifact_urls_for_run(run_dir, case_id=case_id, run_id=run_id)
    artifact_urls[EXPERIMENT_MANIFEST_NAME] = (
        f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{EXPERIMENT_MANIFEST_NAME}"
        if case_id and run_id
        else ""
    )
    covers_dir = run_dir / "covers"
    cover_paths = [
        str(path)
        for path in sorted(covers_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}
    ] if covers_dir.is_dir() else []
    reference_transfer = dict(input_manifest.get("reference_transfer") or {})
    reference_images = image_reference_summary(
        run_dir,
        require_image_references=require_image_references,
    )
    reference_images = _enrich_image_reference_trace(reference_images, reference_transfer)
    latest_reference_check = dict(input_manifest.get("reference_image_generation_check") or {})
    if latest_reference_check:
        reference_images["latest_generation_check"] = latest_reference_check
    return {
        "schema_version": 1,
        "experiment": {
            "case_id": case_id,
            "run_id": run_id,
            "workflow_name": workflow_name,
            "status": status,
            "run_dir": str(run_dir),
            "created_at": _first_stage_time(workflow_run),
            "finished_at": str(workflow_run.get("finished_at") or ""),
        },
        "session": {
            "session_id": str(input_manifest.get("session_id") or workflow_run.get("session_id") or ""),
            "task_id": str(input_manifest.get("task_id") or workflow_run.get("task_id") or ""),
        },
        "inputs": {
            "brief": dict(input_manifest.get("brief") or {}),
            "assets": [_manifest_asset(row) for row in asset_rows],
            "reference_transfer": reference_transfer,
            "reference_image_generation_check": latest_reference_check,
            "market_evidence": dict(input_manifest.get("market_evidence") or {}),
            "config": dict(input_manifest.get("config") or {}),
            "run_options": dict(input_manifest.get("run_options") or {}),
            "metadata": dict(input_manifest.get("metadata") or {}),
            "fingerprints": dict(input_manifest.get("fingerprints") or {}),
        },
        "reference_images": reference_images,
        "models": _runtime_model_snapshot(),
        "artifacts": {
            "paths": artifact_paths,
            "urls": artifact_urls,
            "cover_paths": cover_paths,
            "cover_urls": cover_urls_for_run(run_dir, case_id=case_id, run_id=run_id),
        },
        "evaluations": {
            "items": _read_evaluations(run_dir),
            "summary": evaluation_summary(_read_evaluations(run_dir)),
        },
        "replay": {
            "request_path": str(input_manifest.get("replay_request_path") or "replay_request.json"),
            "request_url": (
                f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/replay_request.json"
                if case_id and run_id
                else ""
            ),
            "endpoint": f"/workflows/content-production/runs/{case_id}/{run_id}/replay" if case_id and run_id else "",
        },
        "error": dict(error or {}),
    }


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


def evaluation_summary(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    if not evaluations:
        return {
            "count": 0,
            "status": "pending",
            "score": None,
            "latest_evaluation_id": "",
            "latest_reviewer": "",
            "issue_count": 0,
            "high_issue_count": 0,
        }
    latest = evaluations[-1]
    issues = [
        issue
        for evaluation in evaluations
        for issue in evaluation.get("issues", [])
        if isinstance(issue, dict)
    ]
    scores = [int(item["score"]) for item in evaluations if isinstance(item.get("score"), int)]
    return {
        "count": len(evaluations),
        "status": str(latest.get("status") or "pending"),
        "score": scores[-1] if scores else None,
        "latest_evaluation_id": str(latest.get("evaluation_id") or ""),
        "latest_reviewer": str(latest.get("reviewer") or ""),
        "issue_count": len(issues),
        "high_issue_count": sum(1 for item in issues if str(item.get("severity") or "") == "high"),
    }


def _auto_evaluation_draft(
    run_dir: Path,
    *,
    summary: dict[str, Any],
    case_id: str,
    run_id: str,
    reviewer: str,
    metadata: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    package_data = _read_json(run_dir / "content_package.json")
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    replay_request = _read_json(run_dir / "replay_request.json")
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    task = _auto_review_task(
        package_data=package_data,
        input_manifest=input_manifest,
        replay_request=replay_request,
        experiment_manifest=experiment_manifest,
        case_id=case_id,
        run_id=run_id,
    )
    brief = _auto_review_brief(
        replay_request=replay_request,
        experiment_manifest=experiment_manifest,
        input_manifest=input_manifest,
    )
    contract = IntentContract.from_brief_and_task(
        brief,
        task,
        contract_id=f"intent_{_slug(case_id)}_{_slug(run_id)}",
    )
    if not package_data:
        package_data = {"package_id": "", "task_id": task.task_id, "platform": task.platform}
    reviews = [
        review.to_dict()
        for review in _review_content_package(
            package_data,
            task=task,
            client_brief=brief,
            intent_contract=contract,
        )
    ]
    run_health_review = _run_health_review(summary, case_id=case_id, run_id=run_id)
    if run_health_review["issues"] or run_health_review["status"] != "passed":
        reviews.append(run_health_review)
    visual_review = _visual_reference_review_for_evaluation(summary, case_id=case_id, run_id=run_id)
    if visual_review:
        reviews.append(visual_review)
    draft = _evaluation_draft_from_reviews(
        reviews,
        reviewer=reviewer,
        metadata={
            "source": "backend.auto_review_gate",
            "case_id": case_id,
            "run_id": run_id,
            "review_count": len(reviews),
            "reviewers": [str(row.get("reviewer") or "") for row in reviews],
            "content_package_available": bool(_read_json(run_dir / "content_package.json")),
            "intent_contract": contract.to_dict(),
            **metadata,
        },
    )
    context = {
        "content_package_available": bool(_read_json(run_dir / "content_package.json")),
        "task": task.to_dict(),
        "client_brief": brief.to_dict(),
        "intent_contract": contract.to_dict(),
        "visual_reference_review": dict(summary.get("visual_reference_review") or {}),
    }
    return draft, reviews, context


def _visual_reference_review_for_evaluation(summary: dict[str, Any], *, case_id: str, run_id: str) -> dict[str, Any]:
    visual = summary.get("visual_reference_review") if isinstance(summary.get("visual_reference_review"), dict) else {}
    status = str(visual.get("status") or "")
    if status == "not_applicable" or not status:
        return {}
    issue = _visual_reference_issue(visual) if status != "passed" else {}
    issues = [issue] if issue else []
    return {
        "review_id": f"review_visual_reference_{_slug(case_id)}_{_slug(run_id)}",
        "package_id": "",
        "task_id": str((summary.get("input_manifest") or {}).get("task_id") or ""),
        "status": "passed" if status == "passed" else ("blocked" if status == "blocked" else "pending"),
        "score": 100 if status == "passed" else (45 if status == "blocked" else 75),
        "issues": issues,
        "fix_suggestions": _visual_reference_suggestions(visual),
        "reviewer": "visual_reference",
        "metadata": {
            "review_type": "rule_based_visual_reference",
            "visual_reference_status": status,
            "selected_count": int(visual.get("selected_count") or 0),
            "sent": bool(visual.get("sent")),
            "trace_count": int(visual.get("trace_count") or 0),
            "provider_fetchable_count": int(visual.get("provider_fetchable_count") or 0),
            "cover_count": int(visual.get("cover_count") or 0),
            "review_questions": list(visual.get("review_questions") or []),
        },
    }


def _visual_reference_issue(visual: dict[str, Any]) -> dict[str, Any]:
    status = str(visual.get("status") or "")
    if status == "blocked":
        severity = "high"
        message = "Visual reference evidence is blocked; selected references or cover output are missing."
    else:
        severity = "medium"
        message = "Human visual match review is required before accepting reference-driven cover quality."
    return {
        "code": f"visual_reference_{status or 'review_required'}",
        "severity": severity,
        "field": "visual_reference_review",
        "message": message,
        "evidence": (
            f"selected={int(visual.get('selected_count') or 0)}; "
            f"sent={bool(visual.get('sent'))}; "
            f"trace={int(visual.get('trace_count') or 0)}; "
            f"covers={int(visual.get('cover_count') or 0)}"
        ),
    }


def _visual_reference_suggestions(visual: dict[str, Any]) -> list[str]:
    status = str(visual.get("status") or "")
    if status == "passed":
        return []
    if status == "blocked":
        return ["先修复参考图传输、trace 或 cover 输出，再进入视觉参考验收。"]
    return ["人工对照 reference trace 和封面图，确认品牌/IP/产品视觉元素是否被实际吸收。"]


def _review_content_package(package: dict[str, Any], **kwargs: Any) -> list[Any]:
    review_module = importlib.import_module("nori.agents.learning_loop.review")
    return review_module.review_content_package(package, **kwargs)


def _run_health_review(summary: dict[str, Any], *, case_id: str, run_id: str) -> dict[str, Any]:
    proof = summary.get("proof") if isinstance(summary.get("proof"), dict) else {}
    acceptance = summary.get("acceptance") if isinstance(summary.get("acceptance"), dict) else {}
    checks = [check for check in proof.get("checks", []) if isinstance(check, dict)]
    checks_by_name = {str(check.get("name") or ""): check for check in checks}
    issue_names = _dedupe_strings([
        *[str(name) for name in proof.get("failed_checks", [])],
        *[str(name) for name in proof.get("warning_checks", [])],
        *[str(name) for name in acceptance.get("blocking_checks", [])],
        *[str(name) for name in acceptance.get("warning_checks", [])],
    ])
    issues = [
        _run_health_issue(name, checks_by_name.get(name, {}))
        for name in issue_names
        if name != "evaluation" and name != "evaluation_passed"
    ]
    score = _run_health_score(issues)
    return {
        "review_id": f"review_run_health_{_slug(case_id)}_{_slug(run_id)}",
        "package_id": "",
        "task_id": str((summary.get("input_manifest") or {}).get("task_id") or ""),
        "status": _run_health_status(issues, score),
        "score": score,
        "issues": issues,
        "fix_suggestions": _run_health_suggestions(issues),
        "reviewer": "run_health",
        "metadata": {
            "review_type": "rule_based_run_health",
            "proof_status": str(proof.get("status") or ""),
            "acceptance_status": str(acceptance.get("status") or ""),
            "issue_count": len(issues),
            "severity_counts": _issue_severity_counts(issues),
        },
    }


def _run_health_issue(name: str, check: dict[str, Any]) -> dict[str, Any]:
    severity = _run_health_severity(name, str(check.get("status") or ""))
    message = str(check.get("message") or _run_health_message(name))
    issue = {
        "code": f"run_{name}",
        "severity": severity,
        "field": f"proof.{name}",
        "message": message,
    }
    evidence = _run_health_evidence(check)
    if evidence:
        issue["evidence"] = evidence
    return issue


def _run_health_message(name: str) -> str:
    return {
        "workflow_succeeded": "workflow did not complete successfully",
        "market_evidence": "market evidence is missing",
        "content_package": "content package is missing",
        "content_package_available": "content package is missing",
        "cover_output": "cover output is missing",
        "cover_output_available": "cover output is missing",
        "reference_transfer": "reference transfer is not ready",
        "reference_images_sent": "selected reference images were not sent",
        "reference_image_generation_check": "provider reference-image generation check is not ready",
        "strict_reference_satisfied": "strict reference-image requirement is not satisfied",
        "provider_reference_check_satisfied": "provider reference-image generation check is not satisfied",
        "replay_snapshot": "replay snapshot is missing",
        "replay_snapshot_available": "replay snapshot is missing",
        "export_available": "export endpoint or artifacts are missing",
        "proof_ready": "proof has blocking or warning checks",
        "artifact_catalog_available": "artifact catalog is empty",
    }.get(name, f"run health check needs attention: {name}")


def _run_health_severity(name: str, check_status: str) -> str:
    if check_status == "warning" or name in {"replay_snapshot", "replay_snapshot_available", "export_available", "artifact_catalog_available"}:
        return "medium"
    if name in {
        "workflow_succeeded",
        "market_evidence",
        "content_package",
        "content_package_available",
        "cover_output",
        "cover_output_available",
        "reference_transfer",
        "reference_images_sent",
        "reference_image_generation_check",
        "strict_reference_satisfied",
        "provider_reference_check_satisfied",
        "proof_ready",
    }:
        return "high"
    return "medium"


def _run_health_evidence(check: dict[str, Any]) -> str:
    values = []
    for key in ("artifact_url", "url", "proof_status", "failed_checks", "warning_checks"):
        value = check.get(key)
        if value:
            values.append(f"{key}={value}")
    return "; ".join(values)[:180]


def _run_health_score(issues: list[dict[str, Any]]) -> int:
    score = 100
    for issue in issues:
        severity = str(issue.get("severity") or "")
        if severity == "high":
            score -= 40
        elif severity == "medium":
            score -= 15
        elif severity == "low":
            score -= 5
    return max(0, score)


def _run_health_status(issues: list[dict[str, Any]], score: int) -> str:
    if any(str(issue.get("severity") or "") == "high" for issue in issues) or score < 60:
        return "blocked"
    if issues or score < 85:
        return "needs_revision"
    return "passed"


def _run_health_suggestions(issues: list[dict[str, Any]]) -> list[str]:
    suggestions = []
    for issue in issues:
        code = str(issue.get("code") or "")
        if code in {"run_market_evidence"}:
            suggestions.append("补齐真实 market_evidence 后重新运行实验。")
        elif code in {"run_reference_transfer", "run_reference_images_sent", "run_strict_reference_satisfied"}:
            suggestions.append("修复 OSS/backend public URL/reference 传输后重新运行严格参考图实验。")
        elif code in {"run_content_package", "run_content_package_available"}:
            suggestions.append("重新运行内容生成，确保 content_package.json 写入成功。")
        elif code in {"run_cover_output", "run_cover_output_available"}:
            suggestions.append("重新运行封面生成，确保 cover 输出可下载。")
        elif code in {"run_replay_snapshot", "run_replay_snapshot_available"}:
            suggestions.append("补齐 replay_request.json，保证实验可复现。")
        elif code == "run_export_available":
            suggestions.append("检查 artifact catalog 和 export endpoint，保证评审包可交付。")
        elif code == "run_workflow_succeeded":
            suggestions.append("先修复 workflow 失败原因，再进入内容质量评估。")
        else:
            suggestions.append("按 run health issue 修复实验证据后重新评估。")
    return _dedupe_strings(suggestions)


def _issue_severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for issue in issues:
        severity = str(issue.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def _auto_review_task(
    *,
    package_data: dict[str, Any],
    input_manifest: dict[str, Any],
    replay_request: dict[str, Any],
    experiment_manifest: dict[str, Any],
    case_id: str,
    run_id: str,
) -> ContentTask:
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    config = replay_request.get("config") if isinstance(replay_request.get("config"), dict) else {}
    brief = input_manifest.get("brief") if isinstance(input_manifest.get("brief"), dict) else {}
    task_id = (
        str(package_data.get("task_id") or "")
        or str(input_manifest.get("task_id") or "")
        or str((experiment_manifest.get("session") or {}).get("task_id") or "")
        or f"{case_id}:{run_id}"
    )
    topic = str(config.get("topic") or replay_request.get("goal") or package_data.get("title") or case_id)
    objective = str(replay_request.get("goal") or config.get("goals") or "")
    if isinstance(config.get("goals"), list):
        objective = "；".join(str(item) for item in config["goals"] if str(item).strip())
    assets = inputs.get("assets") if isinstance(inputs.get("assets"), list) else input_manifest.get("assets")
    required_assets = [
        str(row.get("filename") or row.get("asset_id") or row.get("path") or "")
        for row in (assets or [])
        if isinstance(row, dict) and str(row.get("filename") or row.get("asset_id") or row.get("path") or "").strip()
    ]
    return ContentTask(
        task_id=task_id,
        title=str(package_data.get("title") or topic or case_id),
        platform=str(package_data.get("platform") or config.get("platform") or replay_request.get("platform") or "xhs"),
        content_type=str(config.get("content_type") or "note"),
        topic=topic,
        objective=objective,
        brief={
            "brief_sha256": str(brief.get("sha256") or ""),
            "cover_title": str((package_data.get("prompts") or {}).get("cover_title") or ""),
            "must_include": _auto_review_must_include(config=config, case_id=case_id),
        },
        required_assets=required_assets,
        package_id=str(package_data.get("package_id") or ""),
        metadata={"case_id": case_id, "run_id": run_id},
    )


def _auto_review_brief(
    *,
    replay_request: dict[str, Any],
    experiment_manifest: dict[str, Any],
    input_manifest: dict[str, Any],
) -> ClientBrief:
    config = replay_request.get("config") if isinstance(replay_request.get("config"), dict) else {}
    metadata = input_manifest.get("metadata") if isinstance(input_manifest.get("metadata"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    return ClientBrief(
        client_name=str(config.get("client_name") or metadata.get("client_name") or ""),
        brand_name=str(config.get("brand_name") or metadata.get("brand_name") or ""),
        platform=str(config.get("platform") or replay_request.get("platform") or "xhs"),
        goals=_string_list(config.get("goals")) or _string_list(replay_request.get("goal")),
        audience=_string_list(config.get("target_audience")),
        positioning_notes=_string_list(config.get("positioning_notes")),
        constraints=_string_list(config.get("constraints")),
        taboos=_string_list(config.get("taboos")),
        source_materials=_dict_list(inputs.get("assets")),
        context={
            "brief_text_present": bool(str(replay_request.get("brief_text") or "").strip()),
            "market_evidence": dict(inputs.get("market_evidence") or input_manifest.get("market_evidence") or {}),
        },
    )


def _auto_review_must_include(*, config: dict[str, Any], case_id: str) -> list[str]:
    values = [
        str(config.get("brand_name") or ""),
        str(config.get("topic") or ""),
        str(case_id or ""),
    ]
    return _dedupe_strings([value for value in values if value])


def _evaluation_draft_from_reviews(
    reviews: list[dict[str, Any]],
    *,
    reviewer: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    status = _aggregate_review_status(reviews)
    scores = [int(row.get("score")) for row in reviews if isinstance(row.get("score"), int)]
    issues = [
        {
            **issue,
            "reviewer": str(review.get("reviewer") or ""),
            "review_status": str(review.get("status") or ""),
        }
        for review in reviews
        for issue in review.get("issues", [])
        if isinstance(issue, dict)
    ]
    metrics = {
        "review_count": len(reviews),
        "scores_by_reviewer": {
            str(review.get("reviewer") or f"review_{index}"): review.get("score")
            for index, review in enumerate(reviews, start=1)
        },
        "status_by_reviewer": {
            str(review.get("reviewer") or f"review_{index}"): str(review.get("status") or "")
            for index, review in enumerate(reviews, start=1)
        },
        "issue_count": len(issues),
        "severity_counts": _aggregate_review_severity_counts(reviews),
    }
    suggestions = _dedupe_strings([
        str(item)
        for review in reviews
        for item in review.get("fix_suggestions", [])
        if str(item).strip()
    ])
    return {
        "reviewer": reviewer or "auto_review_gate",
        "source": "auto",
        "status": status,
        "score": min(scores) if scores else 0,
        "notes": _auto_evaluation_notes(status=status, issue_count=len(issues), suggestions=suggestions),
        "issues": issues,
        "metrics": metrics,
        "metadata": metadata,
    }


def _aggregate_review_status(reviews: list[dict[str, Any]]) -> str:
    statuses = [str(row.get("status") or "pending") for row in reviews]
    if any(status == "blocked" for status in statuses):
        return "blocked"
    if any(status == "needs_revision" for status in statuses):
        return "needs_revision"
    if statuses and all(status == "passed" for status in statuses):
        return "passed"
    return "pending"


def _aggregate_review_severity_counts(reviews: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for review in reviews:
        metadata = review.get("metadata") if isinstance(review.get("metadata"), dict) else {}
        severity_counts = metadata.get("severity_counts") if isinstance(metadata.get("severity_counts"), dict) else {}
        for key in counts:
            counts[key] += int(severity_counts.get(key) or 0)
    return counts


def _auto_evaluation_notes(*, status: str, issue_count: int, suggestions: list[str]) -> str:
    if status == "passed":
        return "Auto review gate passed with no blocking issues."
    prefix = f"Auto review gate found {issue_count} issue(s); status={status}."
    if suggestions:
        return f"{prefix} Top suggestion: {suggestions[0]}"
    return prefix


def _read_evaluations(run_dir: Path) -> list[dict[str, Any]]:
    data = _read_json(run_dir / EXPERIMENT_EVALUATIONS_NAME)
    values = data.get("evaluations") if isinstance(data.get("evaluations"), list) else []
    return [dict(item) for item in values if isinstance(item, dict)]


def _normalize_evaluation(data: dict[str, Any], *, existing_count: int) -> dict[str, Any]:
    status = str(data.get("status") or "pending").strip().lower()
    if status not in EVALUATION_STATUSES:
        raise ValueError(f"unsupported evaluation status: {status}")
    score = data.get("score")
    normalized_score = None
    if score is not None:
        normalized_score = int(score)
        if normalized_score < 0 or normalized_score > 100:
            raise ValueError("evaluation score must be between 0 and 100")
    created_at = datetime.now().isoformat(timespec="seconds")
    reviewer = str(data.get("reviewer") or "operator").strip() or "operator"
    source = str(data.get("source") or "manual").strip() or "manual"
    seed = f"{created_at}:{reviewer}:{source}:{existing_count}:{status}"
    return {
        "evaluation_id": f"eval_{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}",
        "created_at": created_at,
        "reviewer": reviewer,
        "source": source,
        "status": status,
        "score": normalized_score,
        "notes": str(data.get("notes") or ""),
        "issues": _dict_list(data.get("issues")),
        "metrics": dict(data.get("metrics") or {}),
        "metadata": dict(data.get("metadata") or {}),
    }


def _refresh_experiment_manifest_evaluations(run_dir: Path, evaluations: list[dict[str, Any]]) -> None:
    manifest_path = run_dir / EXPERIMENT_MANIFEST_NAME
    manifest = _read_json(manifest_path)
    if not manifest:
        return
    manifest["evaluations"] = {
        "items": evaluations,
        "summary": evaluation_summary(evaluations),
    }
    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
    paths = artifacts.get("paths") if isinstance(artifacts.get("paths"), dict) else {}
    urls = artifacts.get("urls") if isinstance(artifacts.get("urls"), dict) else {}
    case_id = str((manifest.get("experiment") or {}).get("case_id") or _case_id_from_run_dir(run_dir))
    run_id = str((manifest.get("experiment") or {}).get("run_id") or run_dir.name)
    paths[EXPERIMENT_EVALUATIONS_NAME] = str(run_dir / EXPERIMENT_EVALUATIONS_NAME)
    if case_id and run_id:
        urls[EXPERIMENT_EVALUATIONS_NAME] = (
            f"/workflows/content-production/runs/{case_id}/{run_id}/artifacts/{EXPERIMENT_EVALUATIONS_NAME}"
        )
    artifacts["paths"] = paths
    artifacts["urls"] = urls
    manifest["artifacts"] = artifacts
    _write_json(manifest_path, manifest)


def _first_stage_time(workflow_run: dict[str, Any]) -> str:
    stages = workflow_run.get("stages") if isinstance(workflow_run.get("stages"), list) else []
    for stage in stages:
        if isinstance(stage, dict) and stage.get("started_at"):
            return str(stage["started_at"])
    return str(workflow_run.get("started_at") or "")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _content_run_dir(*, project_root: str | Path, case_id: str, run_id: str) -> Path:
    root = Path(project_root).resolve()
    run_dir = (root / "cases" / str(case_id or "") / "runs" / str(run_id or "")).resolve()
    if not _is_relative_to(run_dir, root / "cases") or not run_dir.is_dir():
        raise FileNotFoundError(f"content-production run not found: {case_id}/{run_id}")
    return run_dir


def _content_case_dir(*, project_root: str | Path, case_id: str) -> Path:
    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        raise ValueError("case_id is required")
    root = Path(project_root).resolve()
    case_dir = (root / "cases" / normalized_case_id).resolve()
    if not _is_relative_to(case_dir, root / "cases") or not case_dir.is_dir():
        raise FileNotFoundError(f"content-production case not found: {normalized_case_id}")
    return case_dir


def _content_case_dir_or_none(*, project_root: str | Path, case_id: str) -> Path | None:
    normalized_case_id = str(case_id or "").strip()
    if not normalized_case_id:
        return None
    try:
        return _content_case_dir(project_root=project_root, case_id=normalized_case_id)
    except (FileNotFoundError, ValueError):
        return None


def _safe_run_artifact_path(run_dir: Path, artifact_name: str) -> Path:
    name = str(artifact_name or "").strip()
    if not name or name.startswith("/") or ".." in Path(name).parts:
        raise ValueError("invalid artifact name")
    parts = Path(name).parts
    if len(parts) == 1 and Path(name).suffix.lower() in {".json", ".md"}:
        return (run_dir / name).resolve()
    if len(parts) == 2 and parts[0] == "covers" and Path(parts[1]).suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
        return (run_dir / "covers" / parts[1]).resolve()
    raise ValueError("unsupported artifact name")


def _exportable_run_files(run_dir: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    for path in sorted(run_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in {".json", ".md"}:
            entries.append((path.name, path))
    covers_dir = run_dir / "covers"
    if covers_dir.is_dir():
        for path in sorted(covers_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in {".jpeg", ".jpg", ".png", ".webp"}:
                entries.append((f"covers/{path.name}", path))
    return entries


def _exportable_input_files(run_dir: Path) -> tuple[list[tuple[str, Path]], list[dict[str, str]]]:
    manifest = _read_json(run_dir / "input_manifest.json")
    assets = manifest.get("assets") if isinstance(manifest.get("assets"), list) else []
    entries: list[tuple[str, Path]] = []
    skipped: list[dict[str, str]] = []
    seen: set[Path] = set()
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            continue
        source = Path(str(asset.get("path") or ""))
        reason = ""
        if not str(asset.get("path") or "").strip():
            reason = "missing_path"
        elif _is_remote_url(str(asset.get("path") or "")):
            reason = "remote_url"
        elif not source.is_file():
            reason = "missing_file"
        elif source.suffix.lower() not in {".jpeg", ".jpg", ".png", ".webp", ".gif"}:
            reason = "unsupported_input_type"
        elif source.resolve() in seen:
            reason = "duplicate"
        if reason:
            skipped.append({"asset_id": str(asset.get("asset_id") or ""), "path": str(asset.get("path") or ""), "reason": reason})
            continue
        seen.add(source.resolve())
        asset_id = _slug(str(asset.get("asset_id") or f"asset_{index}"))
        filename = _safe_export_filename(str(asset.get("filename") or source.name))
        entries.append((f"inputs/{asset_id}_{filename}", source))
    return entries, skipped


def _safe_export_filename(value: str) -> str:
    name = Path(str(value or "")).name
    clean = "".join(ch if ch.isalnum() or ch in {"-", "_", ".", "@"} else "_" for ch in name)
    return clean.strip("._") or "input_asset"


def _is_remote_url(value: str) -> bool:
    return str(value or "").startswith(("http://", "https://"))


def _case_id_from_run_dir(run_dir: Path) -> str:
    parts = run_dir.parts
    if len(parts) >= 3 and parts[-2] == "runs":
        return parts[-3]
    return ""


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _string_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _slug(value: str) -> str:
    text = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    return text[:48].strip("_") or "nori"


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _input_manifest(
    *,
    request: dict[str, Any],
    session_id: str,
    task_id: str,
    brief_text: str,
    brief_path: Path,
    asset_rows: list[dict[str, Any]],
    reference_public_urls_by_path: dict[str, str],
    replay_request_path: Path,
) -> dict[str, Any]:
    market_evidence = request.get("market_evidence")
    market_evidence_payload = dict(market_evidence) if isinstance(market_evidence, dict) else {}
    config_payload = dict(request.get("config") or {}) if isinstance(request.get("config"), dict) else {}
    metadata_payload = dict(request.get("metadata") or {}) if isinstance(request.get("metadata"), dict) else {}
    reference_check_payload = (
        dict(request.get("reference_image_generation_check") or {})
        if isinstance(request.get("reference_image_generation_check"), dict)
        else {}
    )
    require_image_references = bool(request.get("require_image_references"))
    manifest_assets = [_manifest_asset(row) for row in asset_rows]
    brief_sha256 = hashlib.sha256(brief_text.encode("utf-8")).hexdigest()
    replay_request_sha256 = _file_sha256(replay_request_path) if replay_request_path.is_file() else ""
    return {
        "schema_version": 1,
        "session_id": session_id,
        "task_id": task_id,
        "case_id": str(request.get("case_id") or session_id),
        "case_title": str(request.get("case_title") or request.get("case_id") or session_id),
        "replay_request_path": replay_request_path.name,
        "brief": {
            "text_path": brief_path.name,
            "sha256": brief_sha256,
            "char_count": len(brief_text),
        },
        "assets": manifest_assets,
        "reference_public_urls_by_path": dict(reference_public_urls_by_path),
        "reference_transfer": _reference_transfer_snapshot(
            asset_rows,
            reference_public_urls_by_path=reference_public_urls_by_path,
            require_image_references=require_image_references,
        ),
        "reference_image_generation_check": reference_check_payload,
        "run_options": {
            "platform": str(request.get("platform") or "xhs"),
            "execution_mode": str(request.get("execution_mode") or "sync"),
            "human_gate_mode": str(request.get("human_gate_mode") or "skip"),
            "require_image_references": require_image_references,
            "require_reference_image_generation_check": bool(request.get("require_reference_image_generation_check")),
            "verify_reference_urls": bool(request.get("verify_reference_urls")),
            "reference_url_probe_timeout": request.get("reference_url_probe_timeout") or 3.0,
            "backend_public_base_url": str(request.get("backend_public_base_url") or ""),
            "backend_public_base_url_configured": bool(
                provider_fetchable_reference_url(str(request.get("backend_public_base_url") or ""))
            ),
        },
        "market_evidence": {
            "provided": isinstance(market_evidence, dict) and bool(market_evidence),
            "queries": _string_list((market_evidence or {}).get("queries") if isinstance(market_evidence, dict) else []),
            "hot_note_count": len((market_evidence or {}).get("hot_notes") or []) if isinstance(market_evidence, dict) else 0,
            "insufficient_count": len((market_evidence or {}).get("insufficient") or []) if isinstance(market_evidence, dict) else 0,
            "sha256": _json_sha256(market_evidence_payload),
        },
        "config": config_payload,
        "metadata": metadata_payload,
        "fingerprints": {
            "brief_sha256": brief_sha256,
            "replay_request_sha256": replay_request_sha256,
            "config_sha256": _json_sha256(config_payload),
            "market_evidence_sha256": _json_sha256(market_evidence_payload),
            "metadata_sha256": _json_sha256(metadata_payload),
            "reference_image_generation_check_sha256": _json_sha256(reference_check_payload),
            "asset_sha256s": [str(item.get("sha256") or "") for item in manifest_assets if item.get("sha256")],
        },
    }


def _replay_request(
    request: dict[str, Any],
    *,
    session_id: str,
    task_id: str,
    asset_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a request-shaped snapshot for rerunning the same experiment inputs."""
    return {
        "session_id": session_id,
        "task_id": task_id,
        "goal": str(request.get("goal") or ""),
        "brief_text": str(request.get("brief_text") or request.get("goal") or ""),
        "case_id": str(request.get("case_id") or session_id),
        "case_title": str(request.get("case_title") or request.get("case_id") or session_id),
        "platform": str(request.get("platform") or "xhs"),
        "asset_ids": [str(row.get("asset_id") or "") for row in asset_rows],
        "asset_paths": [str(row.get("path") or "") for row in asset_rows],
        "backend_public_base_url": str(request.get("backend_public_base_url") or ""),
        "execution_mode": str(request.get("execution_mode") or "sync"),
        "human_gate_mode": str(request.get("human_gate_mode") or "skip"),
        "require_image_references": bool(request.get("require_image_references")),
        "require_reference_image_generation_check": bool(request.get("require_reference_image_generation_check")),
        "verify_reference_urls": bool(request.get("verify_reference_urls")),
        "reference_url_probe_timeout": request.get("reference_url_probe_timeout") or 3.0,
        "reference_image_generation_check": dict(request.get("reference_image_generation_check") or {}),
        "market_evidence": dict(request.get("market_evidence") or {}),
        "config": dict(request.get("config") or {}),
        "metadata": dict(request.get("metadata") or {}),
    }


def _manifest_asset(row: dict[str, Any]) -> dict[str, Any]:
    path = str(row.get("path") or "")
    data = {
        "asset_id": str(row.get("asset_id") or ""),
        "kind": str(row.get("kind") or ""),
        "usage": str(row.get("usage") or ""),
        "filename": str(row.get("filename") or Path(path).name),
        "path": path,
        "public_reference_url": str(row.get("public_reference_url") or ""),
        "metadata": dict(row.get("metadata") or {}),
    }
    local_path = Path(path)
    if path and local_path.is_file():
        data["sha256"] = _file_sha256(local_path)
        data["size_bytes"] = local_path.stat().st_size
    return data


def _reference_transfer_snapshot(
    asset_rows: list[dict[str, Any]],
    *,
    reference_public_urls_by_path: dict[str, str],
    require_image_references: bool,
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for row in asset_rows:
        path = str(row.get("path") or "")
        public_url = str(row.get("public_reference_url") or "").strip()
        provider_fetchable_url = provider_fetchable_reference_url(public_url)
        if not provider_fetchable_url:
            provider_fetchable_url = provider_fetchable_reference_url(path)
        if not provider_fetchable_url:
            provider_fetchable_url = provider_fetchable_reference_url(str(reference_public_urls_by_path.get(path) or ""))
        items.append(
            {
                "asset_id": str(row.get("asset_id") or ""),
                "filename": str(row.get("filename") or Path(path).name),
                "path": path,
                "public_reference_url": public_url,
                "provider_fetchable_url": provider_fetchable_url,
                "provider_fetchable": bool(provider_fetchable_url),
            }
        )
    provider_fetchable_count = sum(1 for item in items if item["provider_fetchable"])
    selected_count = len(items)
    return {
        "required": bool(require_image_references),
        "selected_count": selected_count,
        "local_count": sum(1 for row in asset_rows if not _is_remote_url(str(row.get("path") or ""))),
        "remote_count": sum(1 for row in asset_rows if _is_remote_url(str(row.get("path") or ""))),
        "provider_fetchable_count": provider_fetchable_count,
        "all_selected_fetchable": bool(selected_count) and provider_fetchable_count == selected_count,
        "strict_public_url_ready": (
            provider_fetchable_count == selected_count and selected_count > 0
        ) if require_image_references else True,
        "items": items,
    }


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _reference_public_urls_by_path(asset_rows: list[dict[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in asset_rows:
        path = str(row.get("path") or "").strip()
        public_url = str(row.get("public_reference_url") or "").strip()
        fetchable = provider_fetchable_reference_url(public_url)
        if path and fetchable:
            out[path] = fetchable
            try:
                out[str(Path(path).resolve())] = fetchable
            except Exception:  # noqa: BLE001
                pass
    return out


__all__ = [
    "ContentProductionExperimentRunner",
    "ContentProductionRunFailed",
    "artifact_catalog_for_run",
    "build_content_production_case_export",
    "build_content_production_case_delivery_export",
    "build_content_production_evaluation_draft",
    "build_content_production_run_export",
    "compare_content_production_runs",
    "content_production_case_delivery",
    "content_production_case_next_actions",
    "content_production_case_timeline",
    "content_production_experiment_overview",
    "content_production_experiment_report",
    "content_production_experiment_workbench",
    "content_production_run_acceptance_report",
    "content_production_run_proof",
    "content_production_diagnostics",
    "experiment_readiness",
    "evaluation_summary",
    "get_content_production_case_selection",
    "get_content_production_case_selected_run",
    "image_reference_from_package",
    "image_reference_summary",
    "get_content_production_run_acceptance",
    "inspect_content_production_run_artifacts",
    "list_content_production_cases",
    "list_content_production_runs",
    "list_content_production_run_evaluations",
    "promote_content_production_case_run",
    "record_content_production_case_selection",
    "record_content_production_run_evaluation",
    "resolve_content_production_artifact_path",
    "summarize_content_production_run",
    "visual_reference_review",
]
