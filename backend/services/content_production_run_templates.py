"""Content-production run request template builder."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..assets import select_assets
from ..experiments import experiment_readiness
from .content_production_preflight_actions import _content_production_template_actions
from .content_production_preflight_checks import _content_production_template_checks
from .content_production_preflight_summaries import (
    _asset_preflight_summary,
    _market_evidence_preflight_summary,
    _reference_image_preflight_summary,
)
from .content_production_run_payloads import _execution_mode
from .session_assets import (
    attach_public_reference_urls as _attach_public_reference_urls,
    backend_public_base_url as _backend_public_base_url,
    latest_reference_image_generation_check as _latest_reference_image_generation_check,
    reference_image_generation_run_evidence as _reference_image_generation_run_evidence,
)
from .session_store import BackendSessionStore


class ContentProductionRunTemplateBuilder:
    """Builds UI-ready launch templates for content-production runs."""

    def __init__(
        self,
        *,
        experiment_runner: Any,
        session_store: BackendSessionStore,
        enforce_model_readiness: bool,
    ) -> None:
        self.experiment_runner = experiment_runner
        self.session_store = session_store
        self.enforce_model_readiness = bool(enforce_model_readiness)

    def build(
        self,
        *,
        session_id: str = "",
        task_id: str = "",
        case_id: str = "",
        case_title: str = "",
        platform: str = "xhs",
        goal: str = "",
        brief_text: str = "",
        asset_ids: list[str] | None = None,
        asset_paths: list[str] | None = None,
        backend_public_base_url: str = "",
        execution_mode: str = "sync",
        human_gate_mode: str = "skip",
        require_image_references: bool = False,
        require_reference_image_generation_check: bool = False,
        verify_reference_urls: bool = False,
        reference_url_probe_timeout: float = 3.0,
        market_evidence: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        request_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        session_id = str(session_id or "").strip()
        session = self.session_store.get_session(session_id) if session_id else None
        metadata = dict(getattr(session, "metadata", {}) or {}) if session is not None else {}
        task = None
        task_id = str(task_id or "").strip()
        if session is not None and task_id:
            task = self.session_store.find_task(session, task_id)
        elif session is not None:
            task = self.session_store.latest_task(session)
        if task is not None and not task_id:
            task_id = task.task_id

        resolved_goal = str(goal or getattr(task, "goal", "") or metadata.get("goal") or brief_text or "").strip()
        resolved_brief = str(brief_text or metadata.get("brief_text") or resolved_goal).strip()
        resolved_case_id = str(case_id or metadata.get("case_id") or metadata.get("project") or session_id or "").strip()
        resolved_case_title = str(case_title or metadata.get("case_title") or resolved_case_id).strip()
        resolved_base_url = str(
            backend_public_base_url
            or metadata.get("backend_public_base_url")
            or _backend_public_base_url()
        ).strip()
        resolved_market_evidence = (
            dict(market_evidence)
            if isinstance(market_evidence, dict) and market_evidence
            else dict(metadata.get("market_evidence") or {})
            if isinstance(metadata.get("market_evidence"), dict)
            else {}
        )
        resolved_config = (
            dict(config)
            if isinstance(config, dict) and config
            else dict(metadata.get("config") or {})
            if isinstance(metadata.get("config"), dict)
            else {}
        )
        selected_assets: list[dict[str, Any]] = []
        asset_error = ""
        if session is not None:
            try:
                selected_assets = select_assets(metadata.get("assets", []), asset_ids=list(asset_ids or []))
                for path in asset_paths or []:
                    selected_assets.append(
                        {"asset_id": "", "kind": "image", "path": str(path), "filename": Path(str(path)).name}
                    )
                selected_assets = _attach_public_reference_urls(
                    session_id,
                    selected_assets,
                    public_base_url=resolved_base_url,
                )
            except ValueError as exc:
                asset_error = str(exc)

        payload_metadata = dict(request_metadata or {})
        payload_metadata.setdefault("source", "backend.content_production_run_template")
        request_payload = {
            "session_id": session_id,
            "task_id": task_id,
            "goal": resolved_goal,
            "brief_text": resolved_brief,
            "case_id": resolved_case_id,
            "case_title": resolved_case_title,
            "platform": str(platform or metadata.get("platform") or "xhs"),
            "asset_ids": [str(row.get("asset_id") or "") for row in selected_assets if row.get("asset_id")],
            "asset_paths": [str(row.get("path") or "") for row in selected_assets if not row.get("asset_id")],
            "backend_public_base_url": resolved_base_url,
            "execution_mode": _execution_mode(execution_mode),
            "human_gate_mode": str(human_gate_mode or "skip"),
            "require_image_references": bool(require_image_references),
            "require_reference_image_generation_check": bool(require_reference_image_generation_check),
            "verify_reference_urls": bool(verify_reference_urls),
            "reference_url_probe_timeout": reference_url_probe_timeout,
            "market_evidence": resolved_market_evidence,
            "config": resolved_config,
            "metadata": payload_metadata,
        }
        latest_reference_check = _latest_reference_image_generation_check(session.events if session is not None else [])
        if latest_reference_check:
            request_payload["reference_image_generation_check"] = _reference_image_generation_run_evidence(
                latest_reference_check,
                selected_assets,
            )
        readiness = experiment_readiness(project_root=self.experiment_runner.project_root)
        checks = _content_production_template_checks(
            request_payload,
            session_exists=session is not None,
            task_exists=(not task_id or task is not None),
            asset_error=asset_error,
            selected_assets=selected_assets,
            readiness=readiness,
            has_custom_market_collector=getattr(self.experiment_runner, "top_notes_collector", None) is not None,
            enforce_model_readiness=self.enforce_model_readiness,
        )
        missing_fields = [check["name"] for check in checks if check["status"] == "failed"]
        asset_summary = _asset_preflight_summary(selected_assets)
        reference_summary = _reference_image_preflight_summary(
            request_payload,
            readiness=readiness,
            asset_rows=selected_assets,
        )
        reference_summary["latest_check"] = latest_reference_check
        reference_summary["latest_check_for_selected_references"] = dict(
            request_payload.get("reference_image_generation_check") or {}
        )
        return {
            "schema_version": 1,
            "ready_for_preflight": not missing_fields,
            "ready_for_run": not missing_fields,
            "missing_fields": missing_fields,
            "checks": checks,
            "request": request_payload,
            "session": {
                "session_id": session_id,
                "exists": session is not None,
                "task_id": task_id,
                "task_exists": bool(not task_id or task is not None),
                "will_create_task": bool(session is not None and not task_id),
            },
            "assets": asset_summary,
            "market_evidence": _market_evidence_preflight_summary(resolved_market_evidence),
            "reference_images": reference_summary,
            "actions": _content_production_template_actions(
                request_payload,
                checks=checks,
                session_id=session_id,
                asset_summary=asset_summary,
            ),
            "links": {
                "create_session": "/sessions",
                "upload_assets": f"/sessions/{session_id}/assets" if session_id else "/sessions/{session_id}/assets",
                "publish_references": (
                    f"/sessions/{session_id}/assets/publish-references"
                    if session_id
                    else "/sessions/{session_id}/assets/publish-references"
                ),
                "preflight": "/workflows/content-production/runs/preflight",
                "run": "/workflows/content-production/runs",
            },
        }
