"""Proof and acceptance gates for content-production runs."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    Path,
    _file_sha256,
    _json_sha256,
    _read_json,
    _reference_transfer_snapshot,
    infer_project_root_from_cases_path,
)
from .artifacts import _run_export_url, _run_replay_url


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
