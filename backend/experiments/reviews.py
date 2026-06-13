"""Review gates, acceptance checks, evaluation drafts, and evaluation persistence."""
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
from .artifacts import _run_export_url, _run_replay_url
from .models import ContentRunRef
from .repositories import ContentProductionExperimentRepository


def list_content_production_run_evaluations(
    *,
    project_root: str | Path = PROJECT_ROOT,
    case_id: str,
    run_id: str,
) -> dict[str, Any]:
    repository = ContentProductionExperimentRepository(project_root)
    evaluations = repository.read_evaluations(ContentRunRef(case_id=case_id, run_id=run_id))
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
    from .runs import summarize_content_production_run

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
    from .runs import summarize_content_production_run

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
    repository = ContentProductionExperimentRepository(project_root)
    run_ref = ContentRunRef(case_id=case_id, run_id=run_id)
    run_dir = repository.run_dir(run_ref)
    existing = repository.read_evaluations(run_ref)
    normalized = _normalize_evaluation(evaluation, existing_count=len(existing) + 1)
    evaluations = [*existing, normalized]
    repository.write_evaluations(run_ref, evaluations)
    _refresh_experiment_manifest_evaluations(run_dir, evaluations)
    return {
        "case_id": case_id,
        "run_id": run_id,
        "evaluation": normalized,
        "evaluations": evaluations,
        "summary": evaluation_summary(evaluations),
    }


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

    from .runs import _comparison_run

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

    from .runs import _comparison_run

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
        project_root = infer_project_root_from_cases_path(run_dir)
        actual_asset_sha256s = _local_asset_sha256s(
            input_manifest.get("assets") or inputs.get("assets") or [],
            project_root=project_root,
        )
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


def _local_asset_sha256s(assets: Any, *, project_root: Path | None = None) -> list[str]:
    out: list[str] = []
    source = assets if isinstance(assets, list) else []
    for item in source:
        if not isinstance(item, dict):
            continue
        path = _stored_project_path(str(item.get("path") or ""), project_root=project_root)
        if path.is_file():
            out.append(_file_sha256(path))
    return out


def _stored_project_path(value: str, *, project_root: Path | None) -> Path:
    path = Path(str(value or ""))
    if path.is_absolute() or project_root is None:
        return path
    return project_root / path


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
