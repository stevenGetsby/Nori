"""Execution runner and manifest writing for content-production experiments."""
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
from .artifacts import artifact_urls_for_run, cover_urls_for_run, image_reference_summary, _enrich_image_reference_trace
from .diagnostics import _runtime_model_snapshot
from .reviews import _read_evaluations, evaluation_summary


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
