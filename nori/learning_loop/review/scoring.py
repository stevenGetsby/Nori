"""Content review issue, scoring, and suggestion helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import dedupe_preserve_order


HIGH_PENALTY = 40
MEDIUM_PENALTY = 15
LOW_PENALTY = 5


def issue(
    code: str,
    severity: str,
    field: str,
    message: str,
    evidence: str = "",
) -> dict[str, Any]:
    row = {
        "code": code,
        "severity": severity,
        "field": field,
        "message": message,
    }
    if evidence:
        row["evidence"] = evidence[:180]
    return row


def score_issues(issues: list[dict[str, Any]]) -> int:
    score = 100
    for row in issues:
        severity = row.get("severity")
        if severity == "high":
            score -= HIGH_PENALTY
        elif severity == "medium":
            score -= MEDIUM_PENALTY
        elif severity == "low":
            score -= LOW_PENALTY
    return max(0, score)


def status_for_issues(issues: list[dict[str, Any]], score: int) -> str:
    if any(row.get("severity") == "high" for row in issues) or score < 60:
        return "blocked"
    if issues or score < 85:
        return "needs_revision"
    return "passed"


def severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for row in issues:
        severity = str(row.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def suggestions(issues: list[dict[str, Any]]) -> list[str]:
    output = []
    for row in issues:
        code = row.get("code")
        if code in {"missing_title", "missing_body"}:
            output.append("补齐标题和正文后再进入审核。")
        elif code == "client_taboo_term":
            output.append("删除或替换客户明确禁用的表达。")
        elif code == "unsupported_absolute_claim":
            output.append("把绝对化承诺改成可证据支持的描述。")
        elif code == "note_maker_needs_human_review":
            output.append("按 NoteMaker validation 的问题逐条修订。")
        elif code in {"topic_not_reflected", "objective_not_reflected"}:
            output.append("让标题/正文明确回应任务主题和目标。")
        elif code == "cover_prompt_not_aligned":
            output.append("让封面 prompt 包含生成标题或任务 cover_title 的核心词。")
        elif code == "required_asset_not_tracked":
            output.append("补充素材使用记录或调整任务 required_assets。")
        elif code == "brand_not_reflected":
            output.append("确认是否需要在内容或封面 prompt 中显式出现品牌。")
        else:
            output.append("按审核问题修订后重新提交。")
    return dedupe(output)


def dedupe(values: list[str]) -> list[str]:
    return dedupe_preserve_order(values)
