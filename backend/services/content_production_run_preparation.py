"""Session, task, asset, and gate preparation for content-production runs."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from ..assets import select_assets
from ..contracts import ApiError
from ..experiments import experiment_readiness
from .content_production_preflight_checks import _assert_content_production_run_gates
from .content_production_run_payloads import _execution_mode
from .session_assets import (
    assert_asset_paths_exist as _assert_asset_paths_exist,
    attach_public_reference_urls as _attach_public_reference_urls,
    latest_reference_image_generation_check as _latest_reference_image_generation_check,
    reference_image_generation_run_evidence as _reference_image_generation_run_evidence,
)
from .session_store import BackendSessionStore


class ContentProductionRunPreparer:
    """Prepares backend-owned session/task/assets state before run execution."""

    def __init__(
        self,
        *,
        experiment_runner: Any,
        session_store: BackendSessionStore,
        enforce_model_readiness: bool,
        readiness_provider: Callable[[], dict[str, Any]] | None = None,
    ) -> None:
        self.experiment_runner = experiment_runner
        self.session_store = session_store
        self.enforce_model_readiness = bool(enforce_model_readiness)
        self.readiness_provider = readiness_provider or (
            lambda: experiment_readiness(project_root=self.experiment_runner.project_root)
        )

    def prepare(
        self,
        payload: dict[str, Any],
        *,
        create_task: bool,
        enforce_strict_references: bool,
    ) -> dict[str, Any]:
        execution_mode = _execution_mode(payload.get("execution_mode"))
        session_id = str(payload.get("session_id") or "").strip()
        session = self.session_store.require_session(session_id)

        task_id = str(payload.get("task_id") or "").strip()
        task = None
        if task_id:
            task = self.session_store.find_task(session, task_id)
            if task is None:
                raise ApiError(f"task not found in session: {task_id}", status_code=404)
        else:
            goal = str(payload.get("goal") or payload.get("brief_text") or "").strip()
            if not goal:
                raise ApiError("goal or brief_text is required", status_code=400)

        try:
            selected_assets = select_assets(
                session.metadata.get("assets", []),
                asset_ids=list(payload.get("asset_ids") or []),
            )
            for path in payload.get("asset_paths") or []:
                selected_assets.append(
                    {"asset_id": "", "kind": "image", "path": str(path), "filename": Path(str(path)).name}
                )
            selected_assets = _attach_public_reference_urls(
                session_id,
                selected_assets,
                public_base_url=str(payload.get("backend_public_base_url") or ""),
            )
            _assert_asset_paths_exist(selected_assets)
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

        latest_reference_check = _latest_reference_image_generation_check(session.events)
        if latest_reference_check:
            payload["reference_image_generation_check"] = _reference_image_generation_run_evidence(
                latest_reference_check,
                selected_assets,
            )

        if enforce_strict_references and bool(payload.get("require_image_references")) and not selected_assets:
            raise ApiError("require_image_references=true requires at least one selected image asset", status_code=400)
        if enforce_strict_references:
            readiness = self.readiness_provider()
            _assert_content_production_run_gates(
                payload,
                readiness=readiness,
                asset_rows=selected_assets,
                has_custom_market_collector=getattr(self.experiment_runner, "top_notes_collector", None) is not None,
                enforce_model_readiness=self.enforce_model_readiness,
            )

        if create_task and not task_id:
            goal = str(payload.get("goal") or payload.get("brief_text") or "").strip()
            task = self.session_store.start_task(
                session_id,
                goal=goal,
                workflow_name="content-production",
                acceptance=["content_design_spec", "content_package", "cover image", "summary"],
                metadata={"source": "backend.run_content_production"},
            )
            task_id = task.task_id

        return {
            "payload": payload,
            "execution_mode": execution_mode,
            "session_id": session_id,
            "session": session,
            "task_id": task_id,
            "task": task,
            "asset_rows": selected_assets,
        }


__all__ = [
    "ContentProductionRunPreparer",
]
