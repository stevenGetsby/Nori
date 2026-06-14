"""Execution runner and manifest writing for content-production experiments."""
from __future__ import annotations

from .common import (
    Any,
    Callable,
    CaseWorkspace,
    ContentProductionConfig,
    ContentProductionWorkflow,
    LLMFactory,
    PROJECT_ROOT,
    Path,
    TopNotesResult,
    _dict_list,
    _slug,
    _string_list,
    _write_json,
    datetime,
    llms,
    record_content_production_artifacts,
    top_notes_result_from_dict,
)
from .runner_manifests import (
    _input_manifest,
    _reference_public_urls_by_path,
    _replay_request,
    _run_response,
    _write_experiment_manifest,
)


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
        top_notes_collector: Callable[[dict[str, Any], Path], TopNotesResult] | None = None,
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
        reference_urls_by_path = _reference_public_urls_by_path(asset_rows)
        replay_payload = _replay_request(request, session_id=session_id, task_id=task_id, asset_rows=asset_rows)
        _write_json(run_dir / "replay_request.json", replay_payload)
        manifest = _input_manifest(
            request=request,
            session_id=session_id,
            task_id=task_id,
            brief_text=brief_text,
            brief_path=brief_path,
            asset_rows=asset_rows,
            reference_public_urls_by_path=reference_urls_by_path,
            replay_request_path=run_dir / "replay_request.json",
        )
        _write_json(run_dir / "input_manifest.json", manifest)
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
            reference_public_urls_by_path=reference_urls_by_path,
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
                input_manifest=manifest,
                require_image_references=config.require_image_references,
                error={"type": type(exc).__name__, "message": str(exc)},
            )
            failure_result = _run_response(
                run_dir=run_dir,
                workflow_name=config.workflow_name,
                workflow_run=workflow_run_data,
                asset_rows=asset_rows,
                input_manifest=manifest,
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
            input_manifest=manifest,
            require_image_references=config.require_image_references,
        )
        return _run_response(
            run_dir=run_dir,
            workflow_name=config.workflow_name,
            workflow_run=workflow_run.to_dict(),
            asset_rows=asset_rows,
            input_manifest=manifest,
            require_image_references=config.require_image_references,
        )

    def _collector(self, request: dict[str, Any]) -> Callable[[Path], TopNotesResult]:
        def collect(market_dir: Path) -> TopNotesResult:
            if self.top_notes_collector is not None:
                return self.top_notes_collector(request, market_dir)
            evidence = request.get("market_evidence")
            if not isinstance(evidence, dict) or not evidence:
                raise ValueError("market_evidence is required for backend content-production runs")
            result = top_notes_result_from_dict(evidence)
            _write_json(market_dir / "xhs_top_notes_result.json", result.to_dict())
            return result

        return collect


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
        top_k_per_keyword=int(config.get("top_k_per_keyword") or 1),
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
