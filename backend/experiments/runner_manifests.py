"""Run response, input manifest, experiment manifest, and replay snapshots."""
from __future__ import annotations

from .common import (
    Any,
    EXPERIMENT_MANIFEST_NAME,
    Path,
    _case_id_from_run_dir,
    _file_sha256,
    _first_stage_time,
    _json_sha256,
    _read_json,
    _reference_transfer_snapshot,
    _string_list,
    _write_json,
    hashlib,
    provider_fetchable_reference_url,
)
from .artifacts import artifact_urls_for_run, cover_urls_for_run
from .diagnostics import _runtime_model_snapshot
from .reference_images import _enrich_image_reference_trace, image_reference_summary
from .reviews import _read_evaluations, evaluation_summary


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


__all__ = [
    "_experiment_manifest",
    "_input_manifest",
    "_manifest_asset",
    "_reference_public_urls_by_path",
    "_replay_request",
    "_run_response",
    "_write_experiment_manifest",
]
