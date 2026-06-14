"""Run proof and input-integrity checks for content-production experiments."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    Path,
    _file_sha256,
    _json_sha256,
    _read_json,
    infer_project_root_from_cases_path,
)
from .reference_acceptance import (
    content_production_summary_reference_transfer,
    reference_generation_proof_check,
    reference_images_sent_proof_check,
    reference_transfer_proof_check,
    summary_reference_generation_check,
)


def content_production_run_proof(summary: dict[str, Any]) -> dict[str, Any]:
    """Build a product-facing proof summary for one recorded experiment run."""

    from .runs import content_production_comparison_run

    row = content_production_comparison_run(summary)
    artifact_paths = summary.get("artifact_paths") if isinstance(summary.get("artifact_paths"), dict) else {}
    artifact_urls = summary.get("artifact_urls") if isinstance(summary.get("artifact_urls"), dict) else {}
    input_manifest = summary.get("input_manifest") if isinstance(summary.get("input_manifest"), dict) else {}
    experiment_manifest = summary.get("experiment_manifest") if isinstance(summary.get("experiment_manifest"), dict) else {}
    inputs = experiment_manifest.get("inputs") if isinstance(experiment_manifest.get("inputs"), dict) else {}
    run_options = dict(inputs.get("run_options") or input_manifest.get("run_options") or {})
    market_evidence = dict(inputs.get("market_evidence") or input_manifest.get("market_evidence") or {})
    reference_transfer = content_production_summary_reference_transfer(summary)
    image_reference = summary.get("image_reference") if isinstance(summary.get("image_reference"), dict) else {}
    reference_generation_check = summary_reference_generation_check(summary)
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
        reference_transfer_proof_check(reference_transfer, require_refs=require_refs),
        reference_images_sent_proof_check(image_reference, require_refs=require_refs),
        *(
            [reference_generation_proof_check(reference_generation_check, required=require_reference_generation_check)]
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


def _evaluation_check(evaluation: dict[str, Any]) -> dict[str, Any]:
    status = str(evaluation.get("status") or "pending")
    if status == "passed":
        return _proof_check("evaluation", "passed", "latest evaluation passed")
    if status == "blocked":
        return _proof_check("evaluation", "failed", "latest evaluation is blocked")
    if status == "needs_revision":
        return _proof_check("evaluation", "warning", "latest evaluation needs revision")
    return _proof_check("evaluation", "warning", "no passing evaluation has been recorded")


__all__ = ["content_production_run_proof"]
