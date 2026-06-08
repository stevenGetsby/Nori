"""Artifact indexing helpers for content production runs."""
from __future__ import annotations

from pathlib import Path

from nori.core import CaseWorkspace


CONTENT_PRODUCTION_ARTIFACTS = [
    ("xhs_top_notes_result.json", "xhs_top_notes", "DataCollector", []),
    ("market_session_skill_report.json", "market_skill_report", "XHSNoteAnalyzer", ["xhs_top_notes"]),
    ("note_skill_guides.json", "note_skill_guides", "XHSNoteAnalyzer", ["market_skill_report"]),
    ("intake_result.json", "intake_result", "IntakeAgent", ["original_brief"]),
    ("account_plan.json", "account_plan", "AccountPlannerAgent", ["intake_result"]),
    ("client_brief.json", "client_brief", "ContentProductionWorkflow", ["account_plan", "xhs_top_notes"]),
    ("operation_project.json", "operation_project", "OperationPlannerAgent", ["client_brief", "account_plan"]),
    ("kpi_plan.json", "kpi_plan", "KPIPlannerAgent", ["operation_project"]),
    ("content_calendar.json", "content_calendar", "CalendarPlannerAgent", ["operation_project", "kpi_plan"]),
    ("selected_task.json", "selected_task", "ContentProductionWorkflow", ["content_calendar"]),
    ("content_context_pack.json", "content_context_pack", "ContextPackBuilder", ["operation_project", "selected_task"]),
    ("content_design_spec.json", "content_design_spec", "ContentSpecAgent", ["content_context_pack"]),
    ("content_package.json", "content_package", "ArtifactGenerationAgent", ["content_design_spec"]),
    ("reviews.json", "reviews", "ReviewGateAgent", ["content_package"]),
    ("summary.md", "summary", "ContentProductionWorkflow", ["reviews", "content_package"]),
    ("session.json", "session", "RuntimeRunRecorder", []),
    ("context_bundle.json", "context_bundle", "RuntimeRunRecorder", ["session"]),
    ("workflow_run.json", "workflow_run", "RuntimeRunRecorder", ["session"]),
]


def record_content_production_artifacts(
    case: CaseWorkspace,
    run_dir: str | Path,
    *,
    status: str = "completed",
) -> None:
    run_path = Path(run_dir)
    run_id = run_path.name
    for filename, artifact_type, created_by, input_artifacts in CONTENT_PRODUCTION_ARTIFACTS:
        path = run_path / filename
        if path.is_file():
            case.record_artifact(
                run_id=run_id,
                artifact_type=artifact_type,
                path=path,
                created_by=created_by,
                input_artifacts=input_artifacts,
                status=status,
            )
    covers_dir = run_path / "covers"
    if covers_dir.is_dir():
        for path in sorted(covers_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                case.record_artifact(
                    run_id=run_id,
                    artifact_type=f"cover__{path.stem}",
                    path=path,
                    created_by="ArtifactGenerationAgent",
                    input_artifacts=["content_package"],
                    status=status,
                )


__all__ = ["CONTENT_PRODUCTION_ARTIFACTS", "record_content_production_artifacts"]
