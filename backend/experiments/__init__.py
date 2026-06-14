"""Backend adapters for executable Nori experiments."""
from __future__ import annotations

from .common import (
    EVALUATION_STATUSES,
    EXPERIMENT_EVALUATIONS_NAME,
    EXPERIMENT_MANIFEST_NAME,
    EXPERIMENT_SELECTION_NAME,
    PROJECT_ROOT,
    SELECTION_DECISIONS,
    _file_sha256,
    _json_sha256,
    _read_json,
    llms,
)
from .acceptance import (
    content_production_run_acceptance_report,
    content_production_run_proof,
)
from .reference_acceptance import content_production_summary_reference_transfer
from .diagnostics import content_production_diagnostics, experiment_readiness
from .models import ContentCaseRef, ContentRunRef
from .repositories import ContentProductionExperimentRepository
from .reviews import (
    build_content_production_evaluation_draft,
    evaluation_summary,
    get_content_production_run_acceptance,
    list_content_production_run_evaluations,
    record_content_production_run_evaluation,
)
from .visual_reviews import visual_reference_review
from .artifacts import (
    artifact_catalog_for_run,
    artifact_urls_for_run,
    build_content_production_case_delivery_export,
    build_content_production_case_export,
    build_content_production_run_export,
    cover_urls_for_run,
    inspect_content_production_run_artifacts,
    resolve_content_production_artifact_path,
)
from .reference_images import image_reference_from_package, image_reference_summary
from .runs import (
    compare_content_production_runs,
    content_production_count_by,
    content_production_count_values,
    content_production_comparison_run,
    list_content_production_runs,
    summarize_content_production_run,
)
from .presenters import content_production_report_run, content_production_report_run_score
from .actions import content_production_case_next_actions
from .delivery import content_production_case_delivery
from .selections import (
    get_content_production_case_selection,
    promote_content_production_case_run,
    record_content_production_case_selection,
)
from .cases import (
    content_production_case_compare,
    content_production_experiment_overview,
    content_production_experiment_report,
    get_content_production_case_selected_run,
    list_content_production_cases,
)
from .workbench import content_production_experiment_workbench
from .timelines import content_production_case_timeline
from .runner import ContentProductionExperimentRunner, ContentProductionRunFailed


__all__ = [
    'ContentCaseRef',
    'ContentProductionExperimentRepository',
    'ContentProductionExperimentRunner',
    'ContentProductionRunFailed',
    'ContentRunRef',
    'artifact_catalog_for_run',
    'artifact_urls_for_run',
    'build_content_production_case_delivery_export',
    'build_content_production_case_export',
    'build_content_production_evaluation_draft',
    'build_content_production_run_export',
    'compare_content_production_runs',
    'content_production_case_compare',
    'content_production_case_delivery',
    'content_production_case_next_actions',
    'content_production_case_timeline',
    'content_production_comparison_run',
    'content_production_count_by',
    'content_production_count_values',
    'content_production_diagnostics',
    'content_production_experiment_overview',
    'content_production_experiment_report',
    'content_production_experiment_workbench',
    'content_production_report_run',
    'content_production_report_run_score',
    'content_production_run_acceptance_report',
    'content_production_run_proof',
    'content_production_summary_reference_transfer',
    'cover_urls_for_run',
    'evaluation_summary',
    'experiment_readiness',
    'get_content_production_case_selected_run',
    'get_content_production_case_selection',
    'get_content_production_run_acceptance',
    'image_reference_from_package',
    'image_reference_summary',
    'inspect_content_production_run_artifacts',
    'list_content_production_cases',
    'list_content_production_run_evaluations',
    'list_content_production_runs',
    'promote_content_production_case_run',
    'record_content_production_case_selection',
    'record_content_production_run_evaluation',
    'resolve_content_production_artifact_path',
    'summarize_content_production_run',
    'visual_reference_review',
]
