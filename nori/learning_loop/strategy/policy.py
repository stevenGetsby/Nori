"""Rule policy helpers for manual metrics and strategy iteration."""
from __future__ import annotations

from datetime import date
from typing import Any

from nori.content_generation.models import ContentPackage
from nori.core import ContentTask

from ..models import ComplianceReview, MetricsSnapshot


def ref_identity(ref: ContentPackage | ContentTask | str | dict[str, Any]) -> tuple[str, str]:
    if isinstance(ref, ContentPackage):
        return ref.package_id or ref.task_id or "package", "content_package"
    if isinstance(ref, ContentTask):
        return ref.package_id or ref.task_id or "task", "content_task"
    if isinstance(ref, str):
        return ref or "manual_ref", "manual_ref"
    if isinstance(ref, dict):
        if ref.get("package_id"):
            return str(ref["package_id"]), "content_package"
        if ref.get("task_id"):
            return str(ref["task_id"]), "content_task"
        if ref.get("ref_id"):
            return str(ref["ref_id"]), "manual_ref"
    return "manual_ref", "manual_ref"


def date_text(value: str | date | None) -> str:
    if isinstance(value, date):
        return value.isoformat()
    if value:
        return str(value)
    return date.today().isoformat()


def metric_summary(metrics: dict[str, Any]) -> dict[str, Any]:
    views = number(metrics.get("views") or metrics.get("impressions") or metrics.get("reads"))
    likes = number(metrics.get("likes"))
    collections = number(metrics.get("collections") or metrics.get("collected") or metrics.get("saves"))
    comments = number(metrics.get("comments"))
    shares = number(metrics.get("shares"))
    inquiries = number(metrics.get("inquiries"))
    engagement = likes + collections + comments + shares
    engagement_rate = round(engagement / views, 4) if views > 0 else None
    return {
        "views": views,
        "engagement": engagement,
        "engagement_rate": engagement_rate,
        "inquiries": inquiries,
    }


def review_summary(reviews: list[ComplianceReview]) -> dict[str, Any]:
    by_status = {"passed": 0, "needs_revision": 0, "blocked": 0, "pending": 0}
    high_issues: list[dict[str, Any]] = []
    medium_issues: list[dict[str, Any]] = []
    for review in reviews:
        by_status[review.status] = by_status.get(review.status, 0) + 1
        for issue in review.issues:
            if issue.get("severity") == "high":
                high_issues.append(issue)
            elif issue.get("severity") == "medium":
                medium_issues.append(issue)
    return {
        "total": len(reviews),
        "by_status": by_status,
        "high_issue_count": len(high_issues),
        "medium_issue_count": len(medium_issues),
        "top_issue_codes": top_issue_codes(reviews),
    }


def metrics_summary(snapshots: list[MetricsSnapshot]) -> dict[str, Any]:
    if not snapshots:
        return {"total": 0, "views": 0, "engagement": 0, "engagement_rate": None, "inquiries": 0}
    views = 0.0
    engagement = 0.0
    inquiries = 0.0
    for snapshot in snapshots:
        summary = metric_summary(snapshot.metrics)
        views += summary["views"]
        engagement += summary["engagement"]
        inquiries += summary["inquiries"]
    engagement_rate = round(engagement / views, 4) if views > 0 else None
    return {
        "total": len(snapshots),
        "views": int(views) if views.is_integer() else views,
        "engagement": int(engagement) if engagement.is_integer() else engagement,
        "engagement_rate": engagement_rate,
        "inquiries": int(inquiries) if inquiries.is_integer() else inquiries,
    }


def diagnosis(review_summary: dict[str, Any], metric_summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    if review_summary["by_status"].get("blocked", 0):
        rows.append("存在 blocked 审核结果，当前内容不能进入发布或复用。")
    if review_summary["by_status"].get("needs_revision", 0):
        rows.append("存在 needs_revision 审核结果，需要修订后重新跑 review gate。")
    if review_summary["total"] and review_summary["by_status"].get("passed", 0) == review_summary["total"]:
        rows.append("所有审核均通过，内容具备进入人工发布或实验的基础。")
    if metric_summary["total"] == 0:
        rows.append("缺少人工指标快照，暂不能判断内容表现。")
    elif metric_summary["engagement_rate"] is not None and metric_summary["engagement_rate"] < 0.03:
        rows.append("互动率低于 3%，当前选题或开头钩子表现偏弱。")
    elif metric_summary["engagement_rate"] is not None and metric_summary["engagement_rate"] >= 0.08:
        rows.append("互动率达到 8% 以上，当前角度具备复用价值。")
    if metric_summary.get("inquiries", 0) > 0:
        rows.append("已产生咨询或线索，转化角度值得保留并复盘来源。")
    return rows or ["当前证据不足，仅保留观察。"]


def decisions(review_summary: dict[str, Any], metric_summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    if review_summary["by_status"].get("blocked", 0):
        rows.append("先处理阻断级审核问题，再考虑发布或迭代。")
    elif review_summary["by_status"].get("needs_revision", 0):
        rows.append("先做小幅修订并复跑审核，不直接进入下一轮投放。")
    elif review_summary["total"]:
        rows.append("审核通过内容可作为后续指标观察样本。")
    if metric_summary["total"] == 0:
        rows.append("本轮决策以审核质量为主，等待人工指标补齐。")
    elif metric_summary.get("engagement_rate") is not None and metric_summary["engagement_rate"] >= 0.08:
        rows.append("保留当前内容角度，并在下一轮增加同类选题。")
    elif metric_summary.get("engagement_rate") is not None and metric_summary["engagement_rate"] < 0.03:
        rows.append("下一轮优先测试更强标题钩子和更明确受众场景。")
    if metric_summary.get("inquiries", 0) > 0:
        rows.append("保留带来咨询的 CTA 和素材来源。")
    return rows or ["暂不做策略调整。"]


def next_actions(review_summary: dict[str, Any], metric_summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    if review_summary["high_issue_count"]:
        rows.append("修复 high severity 审核问题，并重新运行 ReviewGateAgent。")
    if review_summary["medium_issue_count"]:
        rows.append("修订 medium severity 审核问题，优先处理标题、正文和封面 prompt 对齐。")
    if metric_summary["total"] == 0:
        rows.append("为已发布或实验内容记录一次 manual MetricsSnapshot。")
    elif metric_summary.get("engagement_rate") is not None and metric_summary["engagement_rate"] < 0.03:
        rows.append("下一条内容测试更具体的痛点标题和首段钩子。")
    elif metric_summary.get("engagement_rate") is not None and metric_summary["engagement_rate"] >= 0.08:
        rows.append("把高互动内容的主题、标题结构和素材来源加入下一轮 ContentTask brief。")
    if metric_summary.get("inquiries", 0) > 0:
        rows.append("复盘产生咨询的正文 CTA，并保留到下一轮任务 brief。")
    return rows or ["继续收集审核和指标证据。"]


def top_issue_codes(reviews: list[ComplianceReview]) -> list[str]:
    counts: dict[str, int] = {}
    for review in reviews:
        for issue in review.issues:
            code = str(issue.get("code") or "")
            if code:
                counts[code] = counts.get(code, 0) + 1
    return [
        code
        for code, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]
    ]


def number(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def slug(value: str) -> str:
    text = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in str(value))
    return text.strip("_")[:80] or "ref"
