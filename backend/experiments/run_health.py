"""Rule-based run-health review for content-production experiments."""
from __future__ import annotations

from .common import Any, _dedupe_strings, _slug


def run_health_review(summary: dict[str, Any], *, case_id: str, run_id: str) -> dict[str, Any]:
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
    if check_status == "warning" or name in {
        "replay_snapshot",
        "replay_snapshot_available",
        "export_available",
        "artifact_catalog_available",
    }:
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


__all__ = ["run_health_review"]
