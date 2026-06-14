"""Evaluation drafts and evaluation persistence for content-production runs."""
from __future__ import annotations

from .common import (
    Any,
    EVALUATION_STATUSES,
    EXPERIMENT_EVALUATIONS_NAME,
    EXPERIMENT_MANIFEST_NAME,
    PROJECT_ROOT,
    Path,
    _case_id_from_run_dir,
    _content_run_dir,
    _dict_list,
    _read_json,
    _write_json,
    datetime,
    hashlib,
)
from .auto_reviews import auto_evaluation_draft
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
    draft, reviews, context = auto_evaluation_draft(
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
