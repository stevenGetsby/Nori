from __future__ import annotations

import hashlib
import io
import importlib
import json
import zipfile
from pathlib import Path

import backend.experiments as experiments_module
from backend.experiments import ContentProductionExperimentRunner
from backend.experiments import (
    compare_content_production_runs,
    build_content_production_case_delivery_export,
    content_production_case_next_actions,
    content_production_experiment_overview,
    content_production_experiment_report,
    content_production_experiment_workbench,
    ContentProductionRunFailed,
    build_content_production_case_export,
    build_content_production_evaluation_draft,
    content_production_case_timeline,
    get_content_production_case_selection,
    get_content_production_case_selected_run,
    get_content_production_run_acceptance,
    list_content_production_cases,
    list_content_production_runs,
    list_content_production_run_evaluations,
    image_reference_from_package,
    record_content_production_case_selection,
    record_content_production_run_evaluation,
    resolve_content_production_artifact_path,
    summarize_content_production_run,
)
from backend.fixtures import holly_content_production_fixture
from nori.core import LLMFactory
from nori.workflows.schemas import WorkflowRun


ROOT = Path(__file__).resolve().parents[1]


def test_backend_experiments_is_split_into_capability_modules():
    experiments_package = importlib.import_module("backend.experiments")

    assert hasattr(experiments_package, "__path__")
    assert not (ROOT / "backend" / "experiments.py").exists()
    expected_modules = {
        "runner": ["ContentProductionExperimentRunner", "ContentProductionRunFailed"],
        "diagnostics": ["experiment_readiness", "content_production_diagnostics"],
        "runs": ["list_content_production_runs", "summarize_content_production_run"],
        "artifacts": [
            "artifact_catalog_for_run",
            "resolve_content_production_artifact_path",
            "build_content_production_run_export",
        ],
        "cases": [
            "content_production_case_compare",
        ],
        "actions": [
            "content_production_case_next_actions",
        ],
        "delivery": [
            "content_production_case_delivery",
        ],
        "timelines": ["content_production_case_timeline"],
        "reviews": [
            "build_content_production_evaluation_draft",
            "evaluation_summary",
        ],
        "acceptance": [
            "content_production_run_acceptance_report",
            "content_production_run_proof",
        ],
        "visual_reviews": ["visual_reference_review"],
        "models": ["ContentRunRef", "ContentCaseRef"],
        "repositories": ["ContentProductionExperimentRepository"],
    }
    for module_name, public_names in expected_modules.items():
        module = importlib.import_module(f"backend.experiments.{module_name}")
        assert len(Path(module.__file__).read_text(encoding="utf-8").splitlines()) < 2000
        for public_name in public_names:
            assert getattr(experiments_package, public_name) is getattr(module, public_name)
    for path in (ROOT / "backend" / "experiments").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "_wire_split_module_namespace" not in text
        assert "import *" not in text


def test_content_production_experiment_repository_owns_evaluations_and_selection_io(tmp_path):
    from backend.experiments import ContentCaseRef, ContentProductionExperimentRepository, ContentRunRef

    case_dir = tmp_path / "cases" / "case1"
    run_dir = case_dir / "runs" / "run1"
    run_dir.mkdir(parents=True)
    repo = ContentProductionExperimentRepository(tmp_path)
    run_ref = ContentRunRef(case_id="case1", run_id="run1")
    case_ref = ContentCaseRef(case_id="case1")

    repo.write_evaluations(run_ref, [{"evaluation_id": "eval_1", "status": "passed"}])
    repo.write_case_selection(case_ref, {"schema_version": 1, "case_id": "case1", "current": {"run_id": "run1"}})

    assert repo.run_dir(run_ref) == run_dir.resolve()
    assert repo.case_dir(case_ref) == case_dir.resolve()
    assert repo.read_evaluations(run_ref)[0]["evaluation_id"] == "eval_1"
    assert repo.read_case_selection(case_ref)["current"]["run_id"] == "run1"


def test_holly_content_production_fixture_builds_backend_request_from_case_files(tmp_path):
    case_dir = tmp_path / "cases" / "Holly"
    assets_dir = case_dir / "assets" / "raw" / "brand_materials"
    run_dir = case_dir / "runs" / "20260601_holly_live" / "market"
    assets_dir.mkdir(parents=True)
    run_dir.mkdir(parents=True)
    (case_dir / "brief").mkdir()
    (case_dir / "brief" / "original.md").write_text("Holly brief", encoding="utf-8")
    for name in ["微信图片_20250617195920.jpg", "资源 49@2x.png"]:
        (assets_dir / name).write_bytes(b"image")
    (run_dir / "xhs_top_notes_result.json").write_text(
        '{"platform":"xhs","queries":["怪趣文创"],"hot_notes":[{"title":"note"}],"insufficient":[]}',
        encoding="utf-8",
    )

    fixture = holly_content_production_fixture(project_root=tmp_path, max_assets=2)

    assert fixture["case_id"] == "Holly"
    assert fixture["brief_text"] == "Holly brief"
    assert fixture["asset_paths"] == [
        str(assets_dir / "微信图片_20250617195920.jpg"),
        str(assets_dir / "资源 49@2x.png"),
    ]
    assert fixture["market_evidence"]["queries"] == ["怪趣文创"]
    assert fixture["config"]["brand_name"] == "Holly Shit开心拉屎"
    assert fixture["metadata"]["source"] == "backend.fixture.holly_content_production"
    assert fixture["metadata"]["brief_path"] == "cases/Holly/brief/original.md"
    assert fixture["metadata"]["market_evidence_source"] == (
        "cases/Holly/runs/20260601_holly_live/market/xhs_top_notes_result.json"
    )


def test_content_production_experiment_runner_passes_assets_into_workflow_initial_state(tmp_path):
    asset_path = tmp_path / "asset.png"
    asset_path.write_bytes(b"fake-png")
    captured = {}

    class FakeWorkflow:
        def __init__(self, config):
            self.config = config

        def initial_state(self, **kwargs):
            captured["require_image_references"] = self.config.require_image_references
            captured["reference_public_urls_by_path"] = kwargs.get("reference_public_urls_by_path")
            captured["initial_state"] = kwargs
            return dict(kwargs)

        def run(self, state, *, session_id="", task_id="", human_gate_mode="skip"):
            top_result = state["top_notes_collector"](state["market_dir"])
            captured["top_notes"] = top_result.to_dict()
            captured["human_gate_mode"] = human_gate_mode
            workflow_run = WorkflowRun(
                workflow_name=self.config.workflow_name,
                session_id=session_id,
                task_id=task_id,
            )
            workflow_run.start()
            workflow_run.finish()
            return state, workflow_run

    runner = ContentProductionExperimentRunner(
        project_root=tmp_path,
        llm_factory=LLMFactory(
            chat_func=lambda *_args, **_kwargs: "",
            chat_json_func=lambda *_args, **_kwargs: {},
            image_func=lambda *_args, **_kwargs: [],
        ),
        workflow_factory=lambda config: FakeWorkflow(config),
    )

    result = runner.run(
        {
            "goal": "生成小红书图文",
            "brief_text": "参考图片做内容",
            "case_id": "case1",
            "execution_mode": "background",
            "human_gate_mode": "skip",
            "require_image_references": True,
            "market_evidence": {"platform": "xhs", "queries": ["怪趣文创"], "hot_notes": [], "insufficient": []},
            "config": {"brand_name": "Holly Shit开心拉屎", "goals": ["涨粉", "卖产品"]},
            "metadata": {"source": "test", "operator": "backend"},
            "reference_image_generation_check": {
                "ready": True,
                "reason": "image_generation_succeeded",
                "provider_fetchable_reference_images": ["https://backend.nori.ai/ref.png"],
                "covers_selected_reference_images": True,
            },
        },
        session_id="session_1",
        task_id="task_1",
        asset_rows=[
            {
                "asset_id": "asset_1",
                "kind": "image",
                "path": str(asset_path),
                "filename": "asset.png",
                "public_reference_url": "https://backend.nori.ai/ref.png",
            }
        ],
    )

    assert result["status"] == "succeeded"
    assert result["asset_paths"] == [str(asset_path)]
    assert captured["initial_state"]["asset_paths"] == [asset_path]
    assert captured["initial_state"]["brief_text"] == "参考图片做内容"
    assert captured["top_notes"]["queries"] == ["怪趣文创"]
    assert captured["human_gate_mode"] == "skip"
    assert captured["require_image_references"] is True
    assert captured["reference_public_urls_by_path"][str(asset_path)] == "https://backend.nori.ai/ref.png"
    assert Path(result["run_dir"]).is_dir()
    assert (Path(result["run_dir"]) / "workflow_run.json").is_file()
    assert result["input_manifest"]["session_id"] == "session_1"
    assert result["input_manifest"]["task_id"] == "task_1"
    assert result["input_manifest"]["brief"]["text_path"] == "original_brief.md"
    assert result["input_manifest"]["replay_request_path"] == "replay_request.json"
    assert result["input_manifest"]["run_options"]["require_image_references"] is True
    assert result["input_manifest"]["run_options"]["execution_mode"] == "background"
    assert result["input_manifest"]["run_options"]["human_gate_mode"] == "skip"
    assert result["input_manifest"]["market_evidence"]["provided"] is True
    assert result["input_manifest"]["market_evidence"]["sha256"] == experiments_module._json_sha256(
        {"platform": "xhs", "queries": ["怪趣文创"], "hot_notes": [], "insufficient": []}
    )
    assert result["input_manifest"]["config"]["brand_name"] == "Holly Shit开心拉屎"
    assert result["input_manifest"]["metadata"]["source"] == "test"
    assert result["input_manifest"]["assets"][0]["asset_id"] == "asset_1"
    assert result["input_manifest"]["assets"][0]["public_reference_url"] == "https://backend.nori.ai/ref.png"
    assert result["input_manifest"]["reference_public_urls_by_path"][str(asset_path)] == "https://backend.nori.ai/ref.png"
    assert result["input_manifest"]["reference_transfer"]["required"] is True
    assert result["input_manifest"]["reference_transfer"]["selected_count"] == 1
    assert result["input_manifest"]["reference_transfer"]["provider_fetchable_count"] == 1
    assert result["input_manifest"]["reference_transfer"]["strict_public_url_ready"] is True
    assert result["input_manifest"]["reference_transfer"]["items"][0]["provider_fetchable_url"] == "https://backend.nori.ai/ref.png"
    assert result["input_manifest"]["reference_image_generation_check"]["ready"] is True
    assert result["input_manifest"]["reference_image_generation_check"]["covers_selected_reference_images"] is True
    assert (Path(result["run_dir"]) / "input_manifest.json").is_file()
    assert (Path(result["run_dir"]) / "experiment_manifest.json").is_file()
    assert result["artifact_paths"]["experiment_manifest.json"] == str(Path(result["run_dir"]) / "experiment_manifest.json")
    assert result["experiment_manifest"]["schema_version"] == 1
    assert result["experiment_manifest"]["experiment"]["case_id"] == "case1"
    assert result["experiment_manifest"]["experiment"]["run_id"] == result["run_id"]
    assert result["experiment_manifest"]["experiment"]["status"] == "succeeded"
    assert result["experiment_manifest"]["session"]["session_id"] == "session_1"
    assert result["experiment_manifest"]["session"]["task_id"] == "task_1"
    assert result["experiment_manifest"]["inputs"]["assets"][0]["sha256"]
    assert result["experiment_manifest"]["inputs"]["config"]["brand_name"] == "Holly Shit开心拉屎"
    assert result["experiment_manifest"]["inputs"]["fingerprints"] == result["input_manifest"]["fingerprints"]
    assert result["experiment_manifest"]["inputs"]["reference_transfer"]["provider_fetchable_count"] == 1
    assert result["experiment_manifest"]["inputs"]["reference_transfer"]["items"][0]["provider_fetchable"] is True
    assert result["experiment_manifest"]["inputs"]["reference_image_generation_check"]["reason"] == "image_generation_succeeded"
    assert result["experiment_manifest"]["reference_images"]["required"] is True
    assert result["experiment_manifest"]["reference_images"]["latest_generation_check"]["ready"] is True
    assert result["experiment_manifest"]["artifacts"]["urls"]["experiment_manifest.json"].endswith(
        f"/workflows/content-production/runs/case1/{result['run_id']}/artifacts/experiment_manifest.json"
    )
    assert result["experiment_manifest"]["replay"]["endpoint"].endswith(
        f"/workflows/content-production/runs/case1/{result['run_id']}/replay"
    )
    replay_request_path = Path(result["run_dir"]) / "replay_request.json"
    assert replay_request_path.is_file()
    replay_request = experiments_module._read_json(replay_request_path)
    assert replay_request["session_id"] == "session_1"
    assert replay_request["task_id"] == "task_1"
    assert replay_request["brief_text"] == "参考图片做内容"
    assert replay_request["asset_paths"] == ["asset.png"]
    assert replay_request["asset_ids"] == ["asset_1"]
    assert replay_request["market_evidence"]["queries"] == ["怪趣文创"]
    assert replay_request["execution_mode"] == "background"
    assert replay_request["require_image_references"] is True
    assert replay_request["human_gate_mode"] == "skip"
    expected_replay_sha = hashlib.sha256(
        replay_request_path.read_bytes()
    ).hexdigest()
    assert result["input_manifest"]["fingerprints"]["replay_request_sha256"] == expected_replay_sha
    assert result["input_manifest"]["fingerprints"]["brief_sha256"] == result["input_manifest"]["brief"]["sha256"]
    assert result["input_manifest"]["fingerprints"]["config_sha256"] == experiments_module._json_sha256(
        {"brand_name": "Holly Shit开心拉屎", "goals": ["涨粉", "卖产品"]}
    )
    assert result["input_manifest"]["fingerprints"]["market_evidence_sha256"] == result["input_manifest"]["market_evidence"]["sha256"]
    assert result["input_manifest"]["fingerprints"]["metadata_sha256"] == experiments_module._json_sha256(
        {"source": "test", "operator": "backend"}
    )
    assert result["input_manifest"]["fingerprints"]["asset_sha256s"] == [_sha256_bytes(b"fake-png")]
    persisted_input_manifest = experiments_module._read_json(Path(result["run_dir"]) / "input_manifest.json")
    persisted_experiment_manifest = experiments_module._read_json(Path(result["run_dir"]) / "experiment_manifest.json")
    assert persisted_input_manifest["fingerprints"] == result["input_manifest"]["fingerprints"]
    assert persisted_experiment_manifest["inputs"]["fingerprints"] == result["input_manifest"]["fingerprints"]
    assert result["image_reference"]["status"] == "not_selected"

    summarized = summarize_content_production_run(project_root=tmp_path, case_id="case1", run_id=result["run_id"])
    summarized_checks = {check["name"]: check for check in summarized["proof"]["checks"]}
    assert summarized_checks["input_integrity"]["status"] == "passed"

    replay_request["brief_text"] = "tampered"
    replay_request_path.write_text(json.dumps(replay_request, ensure_ascii=False), encoding="utf-8")
    tampered = summarize_content_production_run(project_root=tmp_path, case_id="case1", run_id=result["run_id"])
    tampered_checks = {check["name"]: check for check in tampered["proof"]["checks"]}
    assert tampered_checks["input_integrity"]["status"] == "failed"
    assert "input_integrity" in tampered["proof"]["failed_checks"]
    assert tampered_checks["input_integrity"]["issues"][0]["field"] == "replay_request_sha256"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def test_content_production_experiment_runner_writes_failure_manifest(tmp_path):
    class FailingWorkflow:
        def __init__(self, config):
            self.config = config

        def initial_state(self, **kwargs):
            return dict(kwargs)

        def run(self, state, *, session_id="", task_id="", human_gate_mode="skip"):
            workflow_run = WorkflowRun(
                workflow_name=self.config.workflow_name,
                session_id=session_id,
                task_id=task_id,
            )
            workflow_run.start()
            exc = RuntimeError("image failed")
            workflow_run.fail(exc)
            exc.workflow_run = workflow_run
            raise exc

    runner = ContentProductionExperimentRunner(
        project_root=tmp_path,
        llm_factory=LLMFactory(),
        workflow_factory=lambda config: FailingWorkflow(config),
    )

    try:
        runner.run(
            {
                "goal": "生成小红书图文",
                "brief_text": "参考图片做内容",
                "case_id": "case_failed",
                "market_evidence": {"platform": "xhs", "queries": ["怪趣文创"], "hot_notes": [], "insufficient": []},
            },
            session_id="session_1",
            task_id="task_1",
            asset_rows=[],
        )
    except ContentProductionRunFailed as exc:
        assert exc.original_error_type == "RuntimeError"
        assert exc.original_message == "image failed"
        assert exc.failure_result["status"] == "failed"
        assert exc.failure_result["experiment_manifest"]["error"] == {"type": "RuntimeError", "message": "image failed"}
    else:
        raise AssertionError("expected workflow failure")

    runs_dir = tmp_path / "cases" / "case_failed" / "runs"
    run_dir = next(runs_dir.iterdir())
    manifest = experiments_module._read_json(run_dir / "experiment_manifest.json")
    workflow_run = experiments_module._read_json(run_dir / "workflow_run.json")

    assert manifest["experiment"]["status"] == "failed"
    assert manifest["session"]["session_id"] == "session_1"
    assert manifest["error"] == {"type": "RuntimeError", "message": "image failed"}
    assert manifest["replay"]["endpoint"].endswith(f"/workflows/content-production/runs/case_failed/{run_dir.name}/replay")
    assert workflow_run["status"] == "failed"


def test_content_production_experiment_runner_requires_market_evidence_without_collector(tmp_path):
    asset_path = tmp_path / "asset.png"
    asset_path.write_bytes(b"fake-png")

    class FakeWorkflow:
        def initial_state(self, **kwargs):
            return dict(kwargs)

        def run(self, state, **_kwargs):
            state["top_notes_collector"](state["market_dir"])

    runner = ContentProductionExperimentRunner(
        project_root=tmp_path,
        llm_factory=LLMFactory(),
        workflow_factory=lambda _config: FakeWorkflow(),
    )

    try:
        runner.run(
            {"goal": "生成内容", "brief_text": "brief", "case_id": "case2"},
            session_id="session_1",
            task_id="task_1",
            asset_rows=[{"asset_id": "asset_1", "kind": "image", "path": str(asset_path), "filename": "asset.png"}],
        )
    except ContentProductionRunFailed as exc:
        assert exc.original_error_type == "ValueError"
        assert "market_evidence is required" in exc.original_message
        assert exc.failure_result["status"] == "failed"
        assert exc.failure_result["experiment_manifest"]["error"]["type"] == "ValueError"
    else:
        raise AssertionError("expected market evidence validation")


def test_image_reference_summary_reports_fallback_and_upload_state():
    package = {
        "prompts": {
            "cover_result": {
                "reference_paths": ["/tmp/ref.png"],
                "extra": {
                    "reference_images_sent": False,
                    "reference_image_fallback": "local_refs_not_supported",
                    "reference_images_uploaded": False,
                    "reference_upload_count": 0,
                },
            }
        }
    }

    summary = image_reference_from_package(package)

    assert summary["status"] == "fallback"
    assert summary["selected_count"] == 1
    assert summary["sent"] is False
    assert summary["fallback"] == "local_refs_not_supported"


def test_summarize_content_production_run_reads_run_artifacts(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    brief_text = "brief"
    market_evidence = {"queries": ["q"]}
    (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"status":"succeeded","stages":[{"stage_name":"content_package","status":"succeeded","started_at":"t1"}],"finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "input_manifest.json").write_text(
        """
        {
          "session_id": "session_1",
          "task_id": "task_1",
          "replay_request_path": "replay_request.json",
          "assets": [{"asset_id": "asset_1", "path": "/tmp/ref.png"}],
          "run_options": {"require_image_references": true}
        }
        """,
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        '{"session_id":"session_1","brief_text":"brief","asset_paths":["/tmp/ref.png"],"market_evidence":{"queries":["q"]}}',
        encoding="utf-8",
    )
    (run_dir / "summary.md").write_text("# Run Summary\n\nOperator notes.", encoding="utf-8")
    (run_dir / "content_package.json").write_text(
        """
        {
          "prompts": {
            "cover_result": {
              "reference_paths": ["https://assets.nori.ai/ref.png"],
              "extra": {
                "reference_images_sent": true,
                "reference_images_uploaded": true,
                "reference_upload_count": 1,
                "reference_public_urls": ["https://assets.nori.ai/ref.png"]
              }
            }
          }
        }
        """,
        encoding="utf-8",
    )

    summary = summarize_content_production_run(project_root=tmp_path, case_id="case1", run_id="run1")

    assert summary["status"] == "succeeded"
    assert summary["cover_paths"] == [str(covers_dir / "cover.png")]
    assert summary["artifact_urls"]["content_package.json"] == "/workflows/content-production/runs/case1/run1/artifacts/content_package.json"
    assert summary["artifact_urls"]["input_manifest.json"] == "/workflows/content-production/runs/case1/run1/artifacts/input_manifest.json"
    assert summary["artifact_urls"]["replay_request.json"] == "/workflows/content-production/runs/case1/run1/artifacts/replay_request.json"
    catalog = {row["artifact_name"]: row for row in summary["artifact_catalog"]}
    assert catalog["content_package.json"]["media_type"] == "application/json"
    assert catalog["content_package.json"]["url"] == "/workflows/content-production/runs/case1/run1/artifacts/content_package.json"
    assert catalog["content_package.json"]["preview"]["kind"] == "text"
    assert catalog["summary.md"]["media_type"] == "text/markdown"
    assert catalog["summary.md"]["preview"]["text"].startswith("# Run Summary")
    assert catalog["covers/cover.png"]["artifact_type"] == "cover"
    assert catalog["covers/cover.png"]["media_type"] == "image/png"
    assert catalog["covers/cover.png"]["preview"] == {"kind": "image", "available": False}
    assert summary["input_manifest"]["session_id"] == "session_1"
    assert summary["input_manifest"]["replay_request_path"] == "replay_request.json"
    assert summary["input_manifest"]["run_options"]["require_image_references"] is True
    assert summary["experiment_manifest"] == {}
    assert summary["cover_urls"] == ["/workflows/content-production/runs/case1/run1/artifacts/covers/cover.png"]
    assert summary["image_reference"]["status"] == "sent"
    assert summary["image_reference"]["public_urls"] == ["https://assets.nori.ai/ref.png"]
    assert summary["image_reference"]["trace_count"] == 1
    assert summary["image_reference"]["trace"][0]["selected_path"] == "https://assets.nori.ai/ref.png"
    assert summary["image_reference"]["trace"][0]["provider_fetchable"] is True
    assert summary["image_reference"]["trace"][0]["sent"] is True
    assert summary["visual_reference_review"]["status"] == "needs_human_review"
    assert summary["visual_reference_review"]["human_review_required"] is True
    assert summary["visual_reference_review"]["reference_trace"][0]["selected_path"] == "https://assets.nori.ai/ref.png"
    assert summary["proof"]["status"] == "blocked"
    assert "market_evidence" in summary["proof"]["failed_checks"]
    assert "reference_transfer" in summary["proof"]["failed_checks"]
    assert summary["proof"]["reference"]["image_reference"]["sent"] is True
    assert summary["proof"]["artifacts"]["catalog_count"] == len(summary["artifact_catalog"])
    assert summary["proof"]["artifacts"]["export_url"] == "/workflows/content-production/runs/case1/run1/export"
    assert summary["acceptance"]["status"] == "rejected"
    assert summary["acceptance"]["accepted"] is False
    assert "proof_ready" in summary["acceptance"]["blocking_checks"]
    assert "strict_reference_satisfied" in summary["acceptance"]["blocking_checks"]
    assert summary["acceptance"]["evidence"]["export_url"] == "/workflows/content-production/runs/case1/run1/export"
    assert resolve_content_production_artifact_path(
        project_root=tmp_path,
        case_id="case1",
        run_id="run1",
        artifact_name="covers/cover.png",
    ) == covers_dir / "cover.png"


def test_content_production_run_acceptance_report_accepts_complete_run(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run_accepted"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "original_brief.md").write_text("brief", encoding="utf-8")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        """
        {
          "prompts": {
            "cover_result": {
              "reference_paths": ["https://assets.nori.ai/ref.png"],
              "extra": {"reference_images_sent": true, "reference_public_urls": ["https://assets.nori.ai/ref.png"]}
            }
          }
        }
        """,
        encoding="utf-8",
    )
    replay_request = {
        "session_id": "session_1",
        "brief_text": "brief",
        "asset_paths": ["/tmp/ref.png"],
        "market_evidence": {"queries": ["怪趣文创"]},
        "config": {},
        "metadata": {},
    }
    (run_dir / "replay_request.json").write_text(json.dumps(replay_request, ensure_ascii=False), encoding="utf-8")
    fingerprints = {
        "brief_sha256": _sha256_bytes(b"brief"),
        "replay_request_sha256": experiments_module._file_sha256(run_dir / "replay_request.json"),
        "config_sha256": experiments_module._json_sha256({}),
        "market_evidence_sha256": experiments_module._json_sha256({"queries": ["怪趣文创"]}),
        "metadata_sha256": experiments_module._json_sha256({}),
        "asset_sha256s": [],
    }
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "session_id": "session_1",
                "task_id": "task_1",
                "replay_request_path": "replay_request.json",
                "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                "assets": [
                    {
                        "asset_id": "asset_1",
                        "path": "/tmp/ref.png",
                        "public_reference_url": "https://assets.nori.ai/ref.png",
                    }
                ],
                "reference_transfer": {
                    "required": True,
                    "selected_count": 1,
                    "provider_fetchable_count": 1,
                    "items": [
                        {
                            "asset_id": "asset_1",
                            "filename": "ref.png",
                            "path": "/tmp/ref.png",
                            "public_reference_url": "https://assets.nori.ai/ref.png",
                            "provider_fetchable_url": "https://assets.nori.ai/ref.png",
                            "provider_fetchable": True,
                        }
                    ],
                },
                "market_evidence": {"queries": ["怪趣文创"], "hot_note_count": 2},
                "config": {},
                "metadata": {},
                "reference_image_generation_check": {
                    "ready": True,
                    "reason": "image_generation_succeeded",
                    "provider_fetchable_count": 1,
                    "provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                    "selected_provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                    "covered_selected_reference_images": ["https://assets.nori.ai/ref.png"],
                    "missing_selected_reference_images": [],
                    "covers_selected_reference_images": True,
                },
                "run_options": {
                    "require_image_references": True,
                    "require_reference_image_generation_check": True,
                    "human_gate_mode": "skip",
                },
                "fingerprints": fingerprints,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment": {"case_id": "case1", "run_id": "run_accepted", "status": "succeeded"},
                "inputs": {
                    "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                    "assets": [{"asset_id": "asset_1", "path": "/tmp/ref.png"}],
                    "reference_transfer": {
                        "required": True,
                        "selected_count": 1,
                        "provider_fetchable_count": 1,
                        "items": [
                            {
                                "asset_id": "asset_1",
                                "filename": "ref.png",
                                "path": "/tmp/ref.png",
                                "public_reference_url": "https://assets.nori.ai/ref.png",
                                "provider_fetchable_url": "https://assets.nori.ai/ref.png",
                                "provider_fetchable": True,
                            }
                        ],
                    },
                    "market_evidence": {"queries": ["怪趣文创"], "hot_note_count": 2},
                    "config": {},
                    "metadata": {},
                    "reference_image_generation_check": {
                        "ready": True,
                        "reason": "image_generation_succeeded",
                        "provider_fetchable_count": 1,
                        "provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                        "selected_provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                        "covered_selected_reference_images": ["https://assets.nori.ai/ref.png"],
                        "missing_selected_reference_images": [],
                        "covers_selected_reference_images": True,
                    },
                    "run_options": {
                        "require_image_references": True,
                        "require_reference_image_generation_check": True,
                        "human_gate_mode": "skip",
                    },
                    "fingerprints": fingerprints,
                },
                "reference_images": {
                    "status": "sent",
                    "required": True,
                    "sent": True,
                    "selected_count": 1,
                    "latest_generation_check": {
                        "ready": True,
                        "reason": "image_generation_succeeded",
                        "provider_fetchable_count": 1,
                        "provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                        "selected_provider_fetchable_reference_images": ["https://assets.nori.ai/ref.png"],
                        "covered_selected_reference_images": ["https://assets.nori.ai/ref.png"],
                        "missing_selected_reference_images": [],
                        "covers_selected_reference_images": True,
                    },
                },
                "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 94}},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    summary = summarize_content_production_run(project_root=tmp_path, case_id="case1", run_id="run_accepted")
    acceptance = get_content_production_run_acceptance(project_root=tmp_path, case_id="case1", run_id="run_accepted")

    assert summary["proof"]["status"] == "ready"
    proof_checks = {check["name"]: check for check in summary["proof"]["checks"]}
    assert proof_checks["input_integrity"]["status"] == "passed"
    assert proof_checks["reference_image_generation_check"]["status"] == "passed"
    assert summary["acceptance"]["status"] == "accepted"
    assert summary["acceptance"]["accepted"] is True
    assert summary["acceptance"]["blocking_checks"] == []
    assert summary["acceptance"]["warning_checks"] == []
    assert summary["acceptance"]["evidence"]["reference_sent"] is True
    assert summary["acceptance"]["evidence"]["provider_fetchable_count"] == 1
    assert summary["acceptance"]["evidence"]["reference_trace_count"] == 1
    assert summary["acceptance"]["evidence"]["reference_trace"][0]["asset_id"] == "asset_1"
    assert summary["acceptance"]["evidence"]["reference_trace"][0]["provider_fetchable"] is True
    assert summary["acceptance"]["evidence"]["reference_generation_check_required"] is True
    assert summary["acceptance"]["evidence"]["reference_generation_check_ready"] is True
    assert summary["acceptance"]["evidence"]["reference_generation_check_covers_selected"] is True
    assert summary["visual_reference_review"]["status"] == "passed"
    assert summary["visual_reference_review"]["human_review_required"] is False
    assert acceptance["acceptance"]["status"] == "accepted"


def test_content_production_acceptance_rejects_required_provider_reference_check_without_evidence(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run_missing_provider_check"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        '{"prompts":{"cover_result":{"reference_paths":["https://assets.nori.ai/ref.png"],"extra":{"reference_images_sent":true,"reference_public_urls":["https://assets.nori.ai/ref.png"]}}}}',
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text('{"brief_text":"brief"}', encoding="utf-8")
    run_options = {"require_image_references": True, "require_reference_image_generation_check": True}
    reference_transfer = {
        "required": True,
        "selected_count": 1,
        "provider_fetchable_count": 1,
        "items": [
            {
                "asset_id": "asset_1",
                "path": "/tmp/ref.png",
                "public_reference_url": "https://assets.nori.ai/ref.png",
                "provider_fetchable_url": "https://assets.nori.ai/ref.png",
                "provider_fetchable": True,
            }
        ],
    }
    input_manifest = {
        "brief": {"sha256": "brief"},
        "assets": [{"asset_id": "asset_1", "path": "/tmp/ref.png", "public_reference_url": "https://assets.nori.ai/ref.png"}],
        "market_evidence": {"queries": ["q"]},
        "reference_transfer": reference_transfer,
        "run_options": run_options,
    }
    experiment_manifest = {
        "schema_version": 1,
        "experiment": {"case_id": "case1", "run_id": "run_missing_provider_check", "status": "succeeded"},
        "inputs": {
            "assets": input_manifest["assets"],
            "market_evidence": input_manifest["market_evidence"],
            "reference_transfer": reference_transfer,
            "run_options": run_options,
        },
        "reference_images": {"status": "sent", "required": True, "sent": True, "selected_count": 1},
        "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 90}},
    }
    (run_dir / "input_manifest.json").write_text(json.dumps(input_manifest), encoding="utf-8")
    (run_dir / "experiment_manifest.json").write_text(json.dumps(experiment_manifest), encoding="utf-8")

    summary = summarize_content_production_run(
        project_root=tmp_path,
        case_id="case1",
        run_id="run_missing_provider_check",
    )

    proof_checks = {check["name"]: check for check in summary["proof"]["checks"]}
    acceptance_checks = {check["name"]: check for check in summary["acceptance"]["checks"]}
    assert summary["proof"]["status"] == "blocked"
    assert proof_checks["reference_image_generation_check"]["status"] == "failed"
    assert summary["acceptance"]["status"] == "rejected"
    assert "provider_reference_check_satisfied" in summary["acceptance"]["blocking_checks"]
    assert acceptance_checks["provider_reference_check_satisfied"]["status"] == "failed"
    assert summary["acceptance"]["evidence"]["reference_generation_check_required"] is True
    assert summary["acceptance"]["evidence"]["reference_generation_check_ready"] is False


def test_compare_content_production_runs_reports_input_and_candidate_differences(tmp_path):
    def write_run(run_id: str, *, brief_sha: str, reference_status: str, reference_sent: bool, with_cover: bool) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        run_dir.mkdir(parents=True)
        brief_text = f"brief-{run_id}"
        market_evidence = {"queries": ["q"]}
        (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
        if with_cover:
            covers_dir = run_dir / "covers"
            covers_dir.mkdir()
            (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            f"""
            {{
              "session_id": "session_1",
              "task_id": "task_{run_id}",
              "brief": {{"sha256": "{brief_sha}"}},
              "assets": [{{"asset_id": "asset_{run_id}", "sha256": "asset-{run_id}"}}],
              "market_evidence": {{"queries": ["q-{run_id}"]}},
              "run_options": {{"require_image_references": true, "human_gate_mode": "skip"}},
              "fingerprints": {{"brief_sha256": "{brief_sha}", "config_sha256": "config-{run_id}"}}
            }}
            """,
            encoding="utf-8",
        )
        (run_dir / "experiment_manifest.json").write_text(
            f"""
            {{
              "schema_version": 1,
              "experiment": {{"case_id": "case1", "run_id": "{run_id}", "status": "succeeded"}},
              "session": {{"session_id": "session_1", "task_id": "task_{run_id}"}},
              "inputs": {{
                "brief": {{"sha256": "{brief_sha}"}},
                "assets": [{{"asset_id": "asset_{run_id}", "sha256": "asset-{run_id}"}}],
                "market_evidence": {{"queries": ["q-{run_id}"]}},
                "run_options": {{"require_image_references": true, "human_gate_mode": "skip"}},
                "fingerprints": {{"brief_sha256": "{brief_sha}", "config_sha256": "config-{run_id}"}}
              }},
              "reference_images": {{"status": "{reference_status}", "required": true, "sent": {str(reference_sent).lower()}}},
              "models": {{"image": {{"key": "image-{run_id}", "provider_id": "relay", "model_id": "gpt-image"}}}},
              "artifacts": {{"urls": {{"content_package.json": "/artifact"}}}},
              "replay": {{"endpoint": "/workflows/content-production/runs/case1/{run_id}/replay"}}
            }}
            """,
            encoding="utf-8",
        )

    write_run("run1", brief_sha="brief-a", reference_status="sent", reference_sent=True, with_cover=True)
    write_run("run2", brief_sha="brief-b", reference_status="fallback", reference_sent=False, with_cover=False)

    comparison = compare_content_production_runs(project_root=tmp_path, case_id="case1", run_ids=["run1", "run2", "run1"])

    assert comparison["run_ids"] == ["run1", "run2"]
    assert comparison["summary"]["status_counts"] == {"succeeded": 2}
    assert comparison["summary"]["reference_status_counts"] == {"sent": 1, "fallback": 1}
    assert comparison["summary"]["ready_run_ids"] == ["run1"]
    assert comparison["summary"]["blocked_run_ids"] == ["run2"]
    assert comparison["differences"]["brief_sha256"]["changed"] is True
    assert comparison["differences"]["brief_sha256"]["by_run"] == {"run1": "brief-a", "run2": "brief-b"}
    assert comparison["differences"]["input_fingerprints"]["changed"] is True
    assert comparison["differences"]["input_fingerprints"]["by_run"]["run2"]["config_sha256"] == "config-run2"
    assert comparison["differences"]["image_model"]["changed"] is True
    run2 = next(row for row in comparison["runs"] if row["run_id"] == "run2")
    assert run2["candidate"]["ready_for_review"] is False
    assert run2["candidate"]["blocking_reasons"] == ["missing_cover", "strict_reference_not_sent"]


def test_content_production_experiment_overview_aggregates_run_health(tmp_path):
    def write_run(run_id: str, *, case_id: str, status: str, reference_sent: bool, with_cover: bool, evaluation_status: str) -> None:
        run_dir = tmp_path / "cases" / case_id / "runs" / run_id
        run_dir.mkdir(parents=True)
        if with_cover:
            covers_dir = run_dir / "covers"
            covers_dir.mkdir()
            (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text(f'{{"workflow":"content_production","status":"{status}"}}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            f'{{"workflow_name":"content_production","status":"{status}","started_at":"{run_id}","finished_at":"{run_id}-done"}}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            '{"brief":{"sha256":"brief"},"assets":[],"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":true}}',
            encoding="utf-8",
        )
        (run_dir / "experiment_manifest.json").write_text(
            f"""
            {{
              "schema_version": 1,
              "experiment": {{"case_id": "{case_id}", "run_id": "{run_id}", "status": "{status}"}},
              "inputs": {{"brief": {{"sha256": "brief"}}, "assets": [], "market_evidence": {{"queries": ["q"]}}, "run_options": {{"require_image_references": true}}}},
              "reference_images": {{"status": "{'sent' if reference_sent else 'fallback'}", "required": true, "sent": {str(reference_sent).lower()}, "selected_count": 1}},
              "artifacts": {{"paths": {{}}, "urls": {{}}}},
              "evaluations": {{"items": [], "summary": {{"count": 1, "status": "{evaluation_status}", "score": 88}}}}
            }}
            """,
            encoding="utf-8",
        )

    write_run("run_b", case_id="case1", status="succeeded", reference_sent=True, with_cover=True, evaluation_status="passed")
    write_run("run_a", case_id="case1", status="succeeded", reference_sent=False, with_cover=False, evaluation_status="needs_revision")
    write_run("run_c", case_id="case2", status="failed", reference_sent=False, with_cover=False, evaluation_status="pending")
    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_b", "decision": "promoted", "reviewer": "operator"},
    )

    overview = content_production_experiment_overview(project_root=tmp_path, limit=2)

    assert overview["run_count"] == 3
    assert overview["case_count"] == 2
    assert [row["run_id"] for row in overview["latest_runs"]] == ["run_b", "run_a"]
    assert overview["summary"]["status_counts"] == {"succeeded": 2, "failed": 1}
    assert overview["summary"]["reference_status_counts"] == {"sent": 1, "fallback": 2}
    assert overview["summary"]["evaluation_status_counts"] == {"passed": 1, "needs_revision": 1, "pending": 1}
    assert overview["summary"]["ready_count"] == 1
    assert overview["summary"]["blocked_count"] == 2
    assert overview["summary"]["blocking_reason_counts"]["strict_reference_not_sent"] == 2
    assert overview["summary"]["blocking_reason_counts"]["evaluation_needs_revision"] == 1
    case1 = next(row for row in overview["cases"] if row["case_id"] == "case1")
    assert case1["run_count"] == 2
    assert case1["ready_count"] == 1
    assert case1["blocked_count"] == 1
    assert case1["selected_run_id"] == "run_b"
    assert case1["selection_decision"] == "promoted"
    assert case1["selection"]["run_id"] == "run_b"
    assert case1["links"]["selection"] == "/experiments/content-production/cases/case1/selection"
    assert case1["links"]["case_evaluation_draft"] == "/experiments/content-production/cases/case1/evaluations/draft"
    assert case1["links"]["case_evaluations"] == "/experiments/content-production/cases/case1/evaluations"
    assert case1["links"]["case_delivery"] == "/experiments/content-production/cases/case1/delivery"
    assert case1["links"]["case_replay"] == "/experiments/content-production/cases/case1/replay"
    assert overview["latest_runs"][0]["links"]["self"] == "/workflows/content-production/runs/case1/run_b"
    assert overview["latest_runs"][0]["links"]["export"] == "/workflows/content-production/runs/case1/run_b/export"

    cases = list_content_production_cases(project_root=tmp_path)

    assert cases["run_count"] == 3
    assert cases["case_count"] == 2
    assert cases["summary"]["blocked_count"] == 2
    case1_from_cases = next(row for row in cases["cases"] if row["case_id"] == "case1")
    assert case1_from_cases["latest_run_id"] == "run_b"
    assert case1_from_cases["latest_created_at"] == "run_b"
    assert case1_from_cases["selected_run_id"] == "run_b"
    assert case1_from_cases["selection_decision"] == "promoted"
    assert case1_from_cases["links"]["runs"] == "/workflows/content-production/runs?case_id=case1"
    assert case1_from_cases["links"]["run_template"] == "/experiments/content-production/run-template?case_id=case1"
    assert case1_from_cases["links"]["next_actions"] == "/experiments/content-production/cases/case1/next-actions"
    assert case1_from_cases["links"]["case_evaluation_draft"] == (
        "/experiments/content-production/cases/case1/evaluations/draft"
    )
    assert case1_from_cases["links"]["case_evaluations"] == "/experiments/content-production/cases/case1/evaluations"
    assert case1_from_cases["links"]["latest_export"] == "/workflows/content-production/runs/case1/run_b/export"

    filtered = list_content_production_runs(
        project_root=tmp_path,
        reference_status="fallback",
        evaluation_status="needs_revision",
        limit=1,
        offset=0,
    )
    assert filtered["total_count"] == 3
    assert filtered["filtered_count"] == 1
    assert filtered["returned_count"] == 1
    assert filtered["runs"][0]["run_id"] == "run_a"
    assert filtered["summary"]["reference_status_counts"] == {"fallback": 1}
    assert filtered["has_more"] is False

    searched = list_content_production_runs(project_root=tmp_path, search="case2", status="failed")
    assert searched["filtered_count"] == 1
    assert searched["runs"][0]["case_id"] == "case2"

    workbench = content_production_experiment_workbench(
        project_root=tmp_path,
        limit=2,
        include_diagnostics=False,
    )

    assert workbench["status"] == "needs_attention"
    assert workbench["overview"]["run_count"] == 3
    workbench_case1 = next(row for row in workbench["cases"] if row["case_id"] == "case1")
    assert workbench_case1["selected_run_id"] == "run_b"
    assert workbench_case1["action_status"] == "blocked"
    assert workbench_case1["primary_action"]["action_id"] in {"fix_reference_transfer", "fix_blockers", "replay_or_rerun"}
    assert workbench_case1["links"]["next_actions"] == "/experiments/content-production/cases/case1/next-actions"
    assert workbench_case1["links"]["run_template"] == "/experiments/content-production/run-template?case_id=case1"
    assert {row["case_id"] for row in workbench["primary_actions"]} == {"case1", "case2"}

    empty_case_workbench = content_production_experiment_workbench(
        project_root=tmp_path,
        case_id="case_new",
        include_diagnostics=False,
    )

    assert empty_case_workbench["scope"] == "case"
    assert empty_case_workbench["status"] == "actionable"
    assert empty_case_workbench["links"]["run_template"] == "/experiments/content-production/run-template?case_id=case_new"
    assert empty_case_workbench["cases"][0]["action_status"] == "needs_first_run"
    assert empty_case_workbench["cases"][0]["links"]["run_template"] == (
        "/experiments/content-production/run-template?case_id=case_new"
    )
    assert empty_case_workbench["primary_actions"][0]["action_id"] == "run_first_experiment"
    assert empty_case_workbench["primary_actions"][0]["method"] == "GET"
    assert empty_case_workbench["primary_actions"][0]["href"] == (
        "/experiments/content-production/run-template?case_id=case_new&human_gate_mode=skip"
    )
    assert empty_case_workbench["primary_actions"][0]["links"]["preflight"] == (
        "/workflows/content-production/runs/preflight"
    )
    assert empty_case_workbench["case_compare"]["run_count"] == 0
    assert empty_case_workbench["case_delivery"]["status"] == "needs_run"
    assert empty_case_workbench["case_delivery"]["blocking_reasons"] == ["no_run"]
    assert empty_case_workbench["active_run_id"] == ""
    assert empty_case_workbench["active_run_artifacts"] == {}


def test_content_production_experiment_report_selects_best_run_and_recommends_next_actions(tmp_path):
    def write_run(
        run_id: str,
        *,
        status: str = "succeeded",
        reference_sent: bool = True,
        with_cover: bool = True,
        with_package: bool = True,
        evaluation_status: str = "passed",
        evaluation_score: int = 90,
    ) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        run_dir.mkdir(parents=True)
        brief_text = f"brief-{run_id}"
        market_evidence = {"queries": ["q"]}
        (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
        if with_cover:
            covers_dir = run_dir / "covers"
            covers_dir.mkdir()
            (covers_dir / "cover.png").write_bytes(b"png")
        if with_package:
            (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "run.json").write_text(f'{{"workflow":"content_production","status":"{status}"}}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            f'{{"workflow_name":"content_production","status":"{status}","started_at":"{run_id}","finished_at":"{run_id}-done"}}',
            encoding="utf-8",
        )
        (run_dir / "replay_request.json").write_text(
            json.dumps(
                {
                    "brief_text": brief_text,
                    "market_evidence": market_evidence,
                    "config": {},
                    "metadata": {},
                }
            ),
            encoding="utf-8",
        )
        fingerprints = {
            "brief_sha256": _sha256_bytes(brief_text.encode("utf-8")),
            "replay_request_sha256": experiments_module._file_sha256(run_dir / "replay_request.json"),
            "config_sha256": experiments_module._json_sha256({}),
            "market_evidence_sha256": experiments_module._json_sha256(market_evidence),
            "metadata_sha256": experiments_module._json_sha256({}),
            "asset_sha256s": [],
        }
        (run_dir / "input_manifest.json").write_text(
            json.dumps(
                {
                    "replay_request_path": "replay_request.json",
                    "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                    "assets": [
                        {
                            "asset_id": "asset_1",
                            "path": "/tmp/ref.png",
                            "public_reference_url": "https://assets.nori.ai/ref.png",
                        }
                    ],
                    "reference_transfer": {
                        "required": True,
                        "selected_count": 1,
                        "provider_fetchable_count": 1,
                    },
                    "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                    "config": {},
                    "metadata": {},
                    "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                    "fingerprints": fingerprints,
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": status},
                    "inputs": {
                        "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                        "assets": [{"asset_id": "asset_1", "sha256": "asset"}],
                        "reference_transfer": {
                            "required": True,
                            "selected_count": 1,
                            "provider_fetchable_count": 1,
                        },
                        "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                        "config": {},
                        "metadata": {},
                        "run_options": {"require_image_references": True, "human_gate_mode": "skip"},
                        "fingerprints": fingerprints,
                    },
                    "reference_images": {
                        "status": "sent" if reference_sent else "fallback",
                        "required": True,
                        "sent": reference_sent,
                        "selected_count": 1,
                    },
                    "evaluations": {
                        "items": [],
                        "summary": {
                            "count": 1,
                            "status": evaluation_status,
                            "score": evaluation_score,
                            "issues": [{"code": "reference_fit"}] if evaluation_status != "passed" else [],
                        },
                    },
                }
            ),
            encoding="utf-8",
        )

    write_run(
        "run_1_rejected",
        status="failed",
        reference_sent=False,
        with_cover=False,
        evaluation_status="blocked",
        evaluation_score=35,
    )
    write_run("run_2_review", evaluation_status="pending", evaluation_score=72)
    write_run("run_3_accepted", evaluation_status="passed", evaluation_score=94)

    report = content_production_experiment_report(project_root=tmp_path, case_id="case1")

    assert report["schema_version"] == 1
    assert report["case_id"] == "case1"
    assert report["run_count"] == 3
    assert report["best_run"]["run_id"] == "run_3_accepted"
    assert report["best_run"]["acceptance_status"] == "accepted"
    assert report["latest_run"]["run_id"] == "run_3_accepted"
    assert report["accepted_run_ids"] == ["run_3_accepted"]
    assert report["needs_review_run_ids"] == ["run_2_review"]
    assert report["rejected_run_ids"] == ["run_1_rejected"]
    assert report["summary"]["acceptance_status_counts"] == {"accepted": 1, "needs_review": 1, "rejected": 1}
    assert report["summary"]["blocking_check_counts"]["workflow_succeeded"] == 1
    assert report["summary"]["candidate_blocking_reason_counts"]["strict_reference_not_sent"] == 1
    assert report["summary"]["evaluation_issue_counts"]["reference_fit"] == 2
    assert report["recommendations"][0]["action_id"] == "promote_accepted_run"
    assert report["recommendations"][0]["run_id"] == "run_3_accepted"
    assert any(action["action_id"] == "fix_reference_transfer" for action in report["recommendations"])
    assert report["links"]["runs"] == "/workflows/content-production/runs?case_id=case1"


def test_content_production_case_next_actions_drives_selection_promotion_and_repair(tmp_path):
    def write_run(
        run_id: str,
        *,
        case_id: str,
        status: str = "succeeded",
        reference_sent: bool = True,
        with_cover: bool = True,
        evaluation_status: str = "passed",
        evaluation_score: int = 90,
        require_provider_check: bool = False,
        session_id: str = "session_1",
        backend_public_base_url: str = "",
    ) -> None:
        run_dir = tmp_path / "cases" / case_id / "runs" / run_id
        run_dir.mkdir(parents=True)
        brief_text = f"brief-{run_id}"
        market_evidence = {"queries": ["q"]}
        (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
        if with_cover:
            covers_dir = run_dir / "covers"
            covers_dir.mkdir()
            (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text(f'{{"workflow":"content_production","status":"{status}"}}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            f'{{"workflow_name":"content_production","status":"{status}","started_at":"{run_id}","finished_at":"{run_id}-done"}}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "replay_request.json").write_text(
            json.dumps(
                {
                    "brief_text": brief_text,
                    "market_evidence": market_evidence,
                    "config": {},
                    "metadata": {},
                }
            ),
            encoding="utf-8",
        )
        fingerprints = {
            "brief_sha256": _sha256_bytes(brief_text.encode("utf-8")),
            "replay_request_sha256": experiments_module._file_sha256(run_dir / "replay_request.json"),
            "config_sha256": experiments_module._json_sha256({}),
            "market_evidence_sha256": experiments_module._json_sha256(market_evidence),
            "metadata_sha256": experiments_module._json_sha256({}),
            "asset_sha256s": [],
        }
        (run_dir / "input_manifest.json").write_text(
            json.dumps(
                {
                    "session_id": session_id,
                    "replay_request_path": "replay_request.json",
                    "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                    "assets": [{"asset_id": "asset_1"}],
                    "reference_transfer": {"required": True, "selected_count": 1, "provider_fetchable_count": 1},
                    "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                    "config": {},
                    "metadata": {},
                    "run_options": {
                        "require_image_references": True,
                        "require_reference_image_generation_check": require_provider_check,
                        "human_gate_mode": "skip",
                        "backend_public_base_url": backend_public_base_url,
                    },
                    "fingerprints": fingerprints,
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": case_id, "run_id": run_id, "status": status},
                    "session": {"session_id": session_id, "task_id": "task_1"},
                    "inputs": {
                        "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                        "assets": [{"asset_id": "asset_1", "sha256": "asset"}],
                        "reference_transfer": {"required": True, "selected_count": 1, "provider_fetchable_count": 1},
                        "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                        "config": {},
                        "metadata": {},
                        "run_options": {
                            "require_image_references": True,
                            "require_reference_image_generation_check": require_provider_check,
                            "human_gate_mode": "skip",
                            "backend_public_base_url": backend_public_base_url,
                        },
                        "fingerprints": fingerprints,
                    },
                    "reference_images": {
                        "status": "sent" if reference_sent else "fallback",
                        "required": True,
                        "sent": reference_sent,
                        "selected_count": 1,
                    },
                    "evaluations": {
                        "items": [],
                        "summary": {
                            "count": 1,
                            "status": evaluation_status,
                            "score": evaluation_score,
                            "issues": [] if evaluation_status == "passed" else [{"code": "reference_fit"}],
                        },
                    },
                }
            ),
            encoding="utf-8",
        )

    write_run("run_good", case_id="case1", evaluation_status="passed", evaluation_score=96)

    before_selection = content_production_case_next_actions(project_root=tmp_path, case_id="case1")

    assert before_selection["status"] == "needs_selection"
    assert before_selection["best_run_id"] == "run_good"
    assert before_selection["target_run_id"] == "run_good"
    assert before_selection["primary_action"]["action_id"] == "select_best_run"
    assert before_selection["primary_action"]["href"] == "/experiments/content-production/cases/case1/selection"
    assert before_selection["primary_action"]["payload"]["run_id"] == "run_good"

    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_good", "decision": "promoted", "reviewer": "operator"},
    )
    after_selection = content_production_case_next_actions(project_root=tmp_path, case_id="case1")

    assert after_selection["status"] == "promoted"
    assert after_selection["selected_run_id"] == "run_good"
    assert after_selection["primary_action"]["action_id"] == "export_promoted_run"
    assert after_selection["primary_action"]["href"] == "/workflows/content-production/runs/case1/run_good/export"

    write_run(
        "run_bad",
        case_id="case2",
        status="failed",
        reference_sent=False,
        with_cover=False,
        evaluation_status="blocked",
        evaluation_score=10,
    )
    bad_case = content_production_case_next_actions(project_root=tmp_path, case_id="case2")

    assert bad_case["status"] == "needs_selection"
    assert bad_case["primary_action"]["action_id"] == "select_best_run"
    assert any(action["action_id"] == "fix_reference_transfer" for action in bad_case["actions"])
    assert any(action["action_id"] == "replay_or_rerun" for action in bad_case["actions"])

    write_run(
        "run_missing_provider_check",
        case_id="case3",
        reference_sent=True,
        with_cover=True,
        evaluation_status="passed",
        require_provider_check=True,
        session_id="session_3",
        backend_public_base_url="https://backend.nori.ai",
    )
    provider_check_case = content_production_case_next_actions(project_root=tmp_path, case_id="case3")
    provider_check_action = next(
        action for action in provider_check_case["actions"] if action["action_id"] == "check_reference_image_generation"
    )

    assert provider_check_action["href"] == "/sessions/session_3/assets/reference-image-generation-check"
    assert provider_check_action["payload"]["asset_ids"] == ["asset_1"]
    assert provider_check_action["payload"]["backend_public_base_url"] == "https://backend.nori.ai"
    assert provider_check_action["payload"]["metadata"]["run_id"] == "run_missing_provider_check"
    provider_replay_action = next(
        action for action in provider_check_case["actions"] if action["action_id"] == "replay_or_rerun"
    )
    assert provider_replay_action["payload"]["session_id"] == "session_3"
    assert provider_replay_action["payload"]["run_id"] == "run_missing_provider_check"

    new_case = content_production_case_next_actions(project_root=tmp_path, case_id="case_new")

    assert new_case["status"] == "needs_first_run"
    assert new_case["primary_action"]["action_id"] == "run_first_experiment"
    assert new_case["primary_action"]["method"] == "GET"
    assert new_case["primary_action"]["href"] == (
        "/experiments/content-production/run-template?case_id=case_new&human_gate_mode=skip"
    )
    assert new_case["primary_action"]["payload"]["case_id"] == "case_new"
    assert new_case["primary_action"]["links"]["run_template"] == (
        "/experiments/content-production/run-template?case_id=case_new&human_gate_mode=skip"
    )


def test_content_production_case_selection_persists_current_and_history(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run_accepted"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "brief": {"sha256": "brief"},
                "assets": [{"asset_id": "asset_1"}],
                "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                "run_options": {"require_image_references": False},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text('{"brief_text":"brief"}', encoding="utf-8")
    (run_dir / "experiment_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment": {"case_id": "case1", "run_id": "run_accepted", "status": "succeeded"},
                "inputs": {
                    "brief": {"sha256": "brief"},
                    "assets": [{"asset_id": "asset_1"}],
                    "market_evidence": {"queries": ["q"], "hot_note_count": 2},
                    "run_options": {"require_image_references": False},
                },
                "reference_images": {"status": "not_selected", "required": False, "sent": False},
                "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 91}},
            }
        ),
        encoding="utf-8",
    )

    empty = get_content_production_case_selection(project_root=tmp_path, case_id="case1")

    assert empty["current"] == {}
    assert empty["history"] == []
    assert empty["report"]["best_run"]["run_id"] == "run_accepted"

    recorded = record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={
            "run_id": "run_accepted",
            "decision": "promoted",
            "reviewer": "pm",
            "reason": "best visual fidelity",
            "notes": "Move to publishing review.",
            "metadata": {"batch_id": "batch_1"},
        },
    )

    assert recorded["selection"]["run_id"] == "run_accepted"
    assert recorded["selection"]["decision"] == "promoted"
    assert recorded["selection"]["reviewer"] == "pm"
    assert recorded["selection"]["matches_report_best"] is True
    assert recorded["selection"]["run"]["acceptance_status"] == "needs_review"
    assert recorded["history"] == [recorded["selection"]]
    assert recorded["report"]["selection"]["selection_id"] == recorded["selection"]["selection_id"]
    assert (tmp_path / "cases" / "case1" / "experiment_selection.json").is_file()

    loaded = get_content_production_case_selection(project_root=tmp_path, case_id="case1")

    assert loaded["current"]["selection_id"] == recorded["selection"]["selection_id"]
    assert loaded["history"][0]["metadata"] == {"batch_id": "batch_1"}

    try:
        record_content_production_case_selection(
            project_root=tmp_path,
            case_id="case1",
            selection={"run_id": "run_accepted", "decision": "winner"},
        )
    except ValueError as exc:
        assert "unsupported selection decision" in str(exc)
    else:
        raise AssertionError("expected selection decision validation")


def test_build_content_production_case_export_bundles_report_selection_and_run_summaries(tmp_path):
    def write_run(run_id: str, *, status: str = "succeeded") -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        covers_dir = run_dir / "covers"
        covers_dir.mkdir(parents=True)
        (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text(f'{{"workflow":"content_production","status":"{status}"}}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            f'{{"workflow_name":"content_production","status":"{status}","started_at":"{run_id}","finished_at":"{run_id}-done"}}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            json.dumps(
                {
                    "brief": {"sha256": f"brief-{run_id}"},
                    "assets": [],
                    "market_evidence": {"queries": [run_id], "hot_note_count": 1},
                    "run_options": {"require_image_references": False},
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "replay_request.json").write_text('{"brief_text":"brief"}', encoding="utf-8")
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": status},
                    "inputs": {
                        "brief": {"sha256": f"brief-{run_id}"},
                        "assets": [],
                        "market_evidence": {"queries": [run_id], "hot_note_count": 1},
                        "run_options": {"require_image_references": False},
                    },
                    "reference_images": {"status": "not_selected", "required": False, "sent": False},
                    "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 90}},
                }
            ),
            encoding="utf-8",
        )

    write_run("run_a")
    write_run("run_b")
    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_b", "decision": "promoted", "reviewer": "operator"},
    )

    bundle = build_content_production_case_export(project_root=tmp_path, case_id="case1")

    assert bundle["filename"] == "nori_content_production_case_case1.zip"
    assert bundle["media_type"] == "application/zip"
    with zipfile.ZipFile(io.BytesIO(bundle["content"])) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("case_export_manifest.json"))
        report = json.loads(archive.read("case_report.json"))
        selection = json.loads(archive.read("case_selection.json"))
        case_summary = json.loads(archive.read("case_summary.json"))
        run_b = json.loads(archive.read("runs/run_b/summary.json"))

    assert names == [
        "case_export_manifest.json",
        "case_report.json",
        "case_selection.json",
        "case_summary.json",
        "runs/run_a/summary.json",
        "runs/run_b/summary.json",
    ]
    assert manifest["schema_version"] == 1
    assert manifest["case_id"] == "case1"
    assert manifest["run_count"] == 2
    assert manifest["selected_run_id"] == "run_b"
    assert manifest["selected_run_export_url"] == "/workflows/content-production/runs/case1/run_b/export"
    assert report["selection"]["run_id"] == "run_b"
    assert selection["current"]["decision"] == "promoted"
    assert case_summary["selected_run_id"] == "run_b"
    assert run_b["run_id"] == "run_b"


def test_build_content_production_case_delivery_export_bundles_ready_run_artifacts(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run_ready"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    brief_text = "brief"
    market_evidence = {"queries": ["q"]}
    (run_dir / "original_brief.md").write_text(brief_text, encoding="utf-8")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text(
        '{"workflow_name":"content_production","status":"succeeded","started_at":"t1","finished_at":"t2"}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
    (run_dir / "replay_request.json").write_text(
        json.dumps({"brief_text": brief_text, "market_evidence": market_evidence, "config": {}, "metadata": {}}),
        encoding="utf-8",
    )
    fingerprints = {
        "brief_sha256": _sha256_bytes(brief_text.encode("utf-8")),
        "replay_request_sha256": experiments_module._file_sha256(run_dir / "replay_request.json"),
        "config_sha256": experiments_module._json_sha256({}),
        "market_evidence_sha256": experiments_module._json_sha256(market_evidence),
        "metadata_sha256": experiments_module._json_sha256({}),
        "asset_sha256s": [],
    }
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "replay_request_path": "replay_request.json",
                "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                "assets": [{"asset_id": "asset_1"}],
                "reference_transfer": {"required": False, "selected_count": 1, "provider_fetchable_count": 1},
                "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                "config": {},
                "metadata": {},
                "run_options": {"require_image_references": False},
                "fingerprints": fingerprints,
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment": {"case_id": "case1", "run_id": "run_ready", "status": "succeeded"},
                "inputs": {
                    "brief": {"text_path": "original_brief.md", "sha256": fingerprints["brief_sha256"]},
                    "assets": [{"asset_id": "asset_1", "sha256": "asset"}],
                    "reference_transfer": {"required": False, "selected_count": 1, "provider_fetchable_count": 1},
                    "market_evidence": {"queries": ["q"], "hot_note_count": 1},
                    "config": {},
                    "metadata": {},
                    "run_options": {"require_image_references": False},
                    "fingerprints": fingerprints,
                },
                "reference_images": {"status": "sent", "required": False, "sent": True, "selected_count": 1},
                "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": 92}},
            }
        ),
        encoding="utf-8",
    )

    try:
        build_content_production_case_delivery_export(project_root=tmp_path, case_id="case1")
    except ValueError as exc:
        assert "case delivery is not ready: not_promoted" in str(exc)
    else:
        raise AssertionError("expected delivery export to require promotion")

    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_ready", "decision": "promoted", "reviewer": "operator"},
    )
    bundle = build_content_production_case_delivery_export(project_root=tmp_path, case_id="case1")

    assert bundle["filename"] == "nori_content_production_delivery_case1_run_ready.zip"
    assert bundle["media_type"] == "application/zip"
    with zipfile.ZipFile(io.BytesIO(bundle["content"])) as archive:
        names = sorted(archive.namelist())
        manifest = json.loads(archive.read("delivery_export_manifest.json"))
        delivery = json.loads(archive.read("delivery.json"))
        artifact_inspection = json.loads(archive.read("artifact_inspection.json"))
        review_evidence = json.loads(archive.read("review_evidence.json"))
        summary = json.loads(archive.read("run_summary.json"))

    assert names == [
        "artifact_inspection.json",
        "case_compare.json",
        "delivery.json",
        "delivery_export_manifest.json",
        "next_actions.json",
        "review_evidence.json",
        "run/content_package.json",
        "run/covers/cover.png",
        "run/experiment_manifest.json",
        "run/input_manifest.json",
        "run/original_brief.md",
        "run/replay_request.json",
        "run/run.json",
        "run/workflow_run.json",
        "run_summary.json",
    ]
    assert manifest["ready"] is True
    assert manifest["run_id"] == "run_ready"
    assert delivery["ready"] is True
    assert delivery["delivery"]["visual_reference_review"]["status"] == "passed"
    assert artifact_inspection["visual_reference_review"]["status"] == "passed"
    assert review_evidence["visual_reference_review"]["status"] == "passed"
    assert review_evidence["acceptance"]["status"] == "accepted"
    assert summary["run_id"] == "run_ready"


def test_content_production_case_timeline_orders_runs_evaluations_and_selection(tmp_path):
    def write_run(run_id: str, *, started_at: str, finished_at: str) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        covers_dir = run_dir / "covers"
        covers_dir.mkdir(parents=True)
        (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            json.dumps(
                {
                    "workflow_name": "content_production",
                    "status": "succeeded",
                    "started_at": started_at,
                    "finished_at": finished_at,
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            '{"brief":{"sha256":"brief"},"assets":[],"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":false}}',
            encoding="utf-8",
        )
        (run_dir / "replay_request.json").write_text('{"brief_text":"brief"}', encoding="utf-8")
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": "succeeded"},
                    "inputs": {
                        "brief": {"sha256": "brief"},
                        "assets": [],
                        "market_evidence": {"queries": ["q"]},
                        "run_options": {"require_image_references": False},
                    },
                    "reference_images": {"status": "not_selected", "required": False, "sent": False},
                    "evaluations": {"items": [], "summary": {"count": 0, "status": "pending"}},
                }
            ),
            encoding="utf-8",
        )

    write_run("run_a", started_at="2026-06-01T10:00:00", finished_at="2026-06-01T10:10:00")
    write_run("run_b", started_at="2026-06-01T11:00:00", finished_at="2026-06-01T11:15:00")
    record_content_production_run_evaluation(
        project_root=tmp_path,
        case_id="case1",
        run_id="run_b",
        evaluation={"reviewer": "qa", "status": "passed", "score": 92},
    )
    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_b", "decision": "promoted", "reviewer": "pm"},
    )

    timeline = content_production_case_timeline(project_root=tmp_path, case_id="case1", limit=20)

    event_types = [event["event_type"] for event in timeline["events"]]
    assert timeline["schema_version"] == 1
    assert timeline["case_id"] == "case1"
    assert timeline["event_count"] == 6
    assert timeline["returned_count"] == 6
    assert timeline["summary"]["event_type_counts"] == {
        "selection_recorded": 1,
        "run_finished": 2,
        "run_started": 2,
        "evaluation_recorded": 1,
    }
    assert event_types[0] == "selection_recorded"
    assert "evaluation_recorded" in event_types
    evaluation = next(event for event in timeline["events"] if event["event_type"] == "evaluation_recorded")
    assert evaluation["run_id"] == "run_b"
    assert evaluation["reviewer"] == "qa"
    assert evaluation["status"] == "passed"
    assert timeline["links"]["selection"] == "/experiments/content-production/cases/case1/selection"


def test_content_production_case_selected_run_resolves_selection_or_best_run(tmp_path):
    def write_run(run_id: str, *, score: int) -> None:
        run_dir = tmp_path / "cases" / "case1" / "runs" / run_id
        covers_dir = run_dir / "covers"
        covers_dir.mkdir(parents=True)
        (covers_dir / "cover.png").write_bytes(b"png")
        (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
        (run_dir / "workflow_run.json").write_text(
            f'{{"workflow_name":"content_production","status":"succeeded","started_at":"{run_id}","finished_at":"{run_id}-done"}}',
            encoding="utf-8",
        )
        (run_dir / "content_package.json").write_text('{"package_id":"pkg"}', encoding="utf-8")
        (run_dir / "input_manifest.json").write_text(
            '{"brief":{"sha256":"brief"},"assets":[],"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":false}}',
            encoding="utf-8",
        )
        (run_dir / "replay_request.json").write_text('{"brief_text":"brief"}', encoding="utf-8")
        (run_dir / "experiment_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "experiment": {"case_id": "case1", "run_id": run_id, "status": "succeeded"},
                    "inputs": {
                        "brief": {"sha256": "brief"},
                        "assets": [],
                        "market_evidence": {"queries": ["q"]},
                        "run_options": {"require_image_references": False},
                    },
                    "reference_images": {"status": "not_selected", "required": False, "sent": False},
                    "evaluations": {"items": [], "summary": {"count": 1, "status": "passed", "score": score}},
                }
            ),
            encoding="utf-8",
        )

    write_run("run_a", score=80)
    write_run("run_b", score=95)

    fallback = get_content_production_case_selected_run(project_root=tmp_path, case_id="case1")
    no_fallback = get_content_production_case_selected_run(
        project_root=tmp_path,
        case_id="case1",
        fallback_to_best=False,
    )
    record_content_production_case_selection(
        project_root=tmp_path,
        case_id="case1",
        selection={"run_id": "run_a", "decision": "selected", "reviewer": "operator"},
    )
    selected = get_content_production_case_selected_run(project_root=tmp_path, case_id="case1")

    assert fallback["resolved"] is True
    assert fallback["source"] == "best_run"
    assert fallback["run_id"] == "run_b"
    assert fallback["run"]["run_id"] == "run_b"
    assert no_fallback["resolved"] is False
    assert no_fallback["reason"] == "no_selection_or_best_run"
    assert selected["resolved"] is True
    assert selected["source"] == "selection"
    assert selected["run_id"] == "run_a"
    assert selected["selection"]["run_id"] == "run_a"
    assert selected["links"]["run"] == "/workflows/content-production/runs/case1/run_a"


def test_compare_content_production_runs_rejects_missing_inputs(tmp_path):
    try:
        compare_content_production_runs(project_root=tmp_path, case_id="case1", run_ids=["run1"])
    except ValueError as exc:
        assert "at least two run_ids" in str(exc)
    else:
        raise AssertionError("expected run id validation")

    try:
        compare_content_production_runs(project_root=tmp_path, case_id="case1", run_ids=["run1", "run2"])
    except FileNotFoundError as exc:
        assert "content-production runs not found" in str(exc)
    else:
        raise AssertionError("expected missing run validation")


def test_record_content_production_run_evaluation_persists_and_updates_manifest(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "content_package.json").write_text("{}", encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        '{"brief":{"sha256":"brief"},"assets":[],"market_evidence":{"queries":["q"]},"run_options":{"require_image_references":false}}',
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        """
        {
          "schema_version": 1,
          "experiment": {"case_id": "case1", "run_id": "run1", "status": "succeeded"},
          "inputs": {"brief": {"sha256": "brief"}, "assets": [], "market_evidence": {"queries": ["q"]}, "run_options": {}},
          "reference_images": {"status": "not_selected", "required": false, "sent": false},
          "artifacts": {"paths": {}, "urls": {}}
        }
        """,
        encoding="utf-8",
    )

    recorded = record_content_production_run_evaluation(
        project_root=tmp_path,
        case_id="case1",
        run_id="run1",
        evaluation={
            "reviewer": "Tianfu",
            "source": "manual",
            "status": "needs_revision",
            "score": 72,
            "notes": "封面需要更像参考图",
            "issues": [{"code": "cover_reference", "severity": "medium"}],
            "metrics": {"reference_fit": 0.6},
        },
    )
    listed = list_content_production_run_evaluations(project_root=tmp_path, case_id="case1", run_id="run1")
    manifest = experiments_module._read_json(run_dir / "experiment_manifest.json")
    run2_dir = tmp_path / "cases" / "case1" / "runs" / "run2"
    run2_covers = run2_dir / "covers"
    run2_covers.mkdir(parents=True)
    (run2_covers / "cover.png").write_bytes(b"png")
    (run2_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run2_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run2_dir / "content_package.json").write_text("{}", encoding="utf-8")
    (run2_dir / "input_manifest.json").write_text('{"brief":{"sha256":"brief"},"assets":[]}', encoding="utf-8")
    (run2_dir / "experiment_manifest.json").write_text(
        '{"schema_version":1,"experiment":{"case_id":"case1","run_id":"run2","status":"succeeded"},"reference_images":{"status":"not_selected","required":false,"sent":false},"artifacts":{"paths":{},"urls":{}}}',
        encoding="utf-8",
    )
    record_content_production_run_evaluation(
        project_root=tmp_path,
        case_id="case1",
        run_id="run2",
        evaluation={"reviewer": "Tianfu", "status": "passed", "score": 91},
    )
    comparison = compare_content_production_runs(project_root=tmp_path, case_id="case1", run_ids=["run1", "run2"])

    assert recorded["summary"]["status"] == "needs_revision"
    assert recorded["summary"]["score"] == 72
    assert recorded["evaluation"]["reviewer"] == "Tianfu"
    assert listed["summary"]["count"] == 1
    assert listed["evaluations"][0]["issues"][0]["code"] == "cover_reference"
    assert (run_dir / "experiment_evaluations.json").is_file()
    assert manifest["evaluations"]["summary"]["status"] == "needs_revision"
    assert manifest["artifacts"]["paths"]["experiment_evaluations.json"] == (
        "cases/case1/runs/run1/experiment_evaluations.json"
    )
    assert comparison["summary"]["evaluation_status_counts"] == {"needs_revision": 1, "passed": 1}
    assert comparison["summary"]["ready_run_ids"] == ["run2"]
    run1 = next(row for row in comparison["runs"] if row["run_id"] == "run1")
    assert run1["candidate"]["blocking_reasons"] == ["evaluation_needs_revision"]


def test_build_content_production_evaluation_draft_uses_review_gate_and_can_persist(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        """
        {
          "session_id": "session_1",
          "task_id": "task_1",
          "brief": {"sha256": "brief"},
          "assets": [{"asset_id": "asset_1", "filename": "cover-reference.png"}],
          "market_evidence": {"queries": ["Holly"]},
          "run_options": {"require_image_references": false}
        }
        """,
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        """
        {
          "goal": "卖产品",
          "brief_text": "Holly 反焦虑怪趣文创",
          "config": {
            "client_name": "Holly",
            "brand_name": "Holly",
            "platform": "xhs",
            "topic": "反焦虑怪趣文创",
            "goals": ["卖产品"],
            "taboos": ["治疗"]
          }
        }
        """,
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        """
        {
          "package_id": "pkg_1",
          "task_id": "task_1",
          "platform": "xhs",
          "title": "Holly 100% 治疗焦虑",
          "body": "今天聊一个反焦虑怪趣文创产品。",
          "tags": ["Holly"],
          "prompts": {"cover_result": {"prompt": "Holly 怪趣封面"}},
          "material_usage": [{"asset_id": "asset_1", "filename": "cover-reference.png"}]
        }
        """,
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        '{"schema_version":1,"experiment":{"case_id":"case1","run_id":"run1","status":"succeeded"},"reference_images":{"status":"not_selected","required":false,"sent":false},"artifacts":{"paths":{},"urls":{}}}',
        encoding="utf-8",
    )

    draft = build_content_production_evaluation_draft(
        project_root=tmp_path,
        case_id="case1",
        run_id="run1",
        reviewer="auto",
    )
    persisted = build_content_production_evaluation_draft(
        project_root=tmp_path,
        case_id="case1",
        run_id="run1",
        reviewer="auto",
        persist=True,
        metadata={"batch_id": "batch_1"},
    )

    issue_codes = {row["code"] for row in draft["draft"]["issues"]}
    assert draft["persisted"] is False
    assert draft["draft"]["status"] == "blocked"
    assert draft["draft"]["score"] < 100
    assert {"unsupported_absolute_claim", "client_taboo_term"}.issubset(issue_codes)
    assert "run_reference_transfer" in issue_codes
    assert draft["draft"]["metrics"]["review_count"] == 4
    assert draft["draft"]["metrics"]["status_by_reviewer"]["run_health"] == "blocked"
    assert draft["context"]["intent_contract"]["brand_name"] == "Holly"
    assert persisted["persisted"] is True
    assert persisted["recorded"]["summary"]["status"] == "blocked"
    assert persisted["recorded"]["evaluation"]["metadata"]["batch_id"] == "batch_1"
    assert (run_dir / "experiment_evaluations.json").is_file()


def test_build_content_production_evaluation_draft_requires_visual_reference_review(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run_visual"
    covers_dir = run_dir / "covers"
    covers_dir.mkdir(parents=True)
    (covers_dir / "cover.png").write_bytes(b"png")
    (run_dir / "run.json").write_text('{"workflow":"content_production","status":"succeeded"}', encoding="utf-8")
    (run_dir / "workflow_run.json").write_text('{"status":"succeeded","stages":[]}', encoding="utf-8")
    (run_dir / "original_brief.md").write_text("brief", encoding="utf-8")
    (run_dir / "input_manifest.json").write_text(
        json.dumps(
            {
                "session_id": "session_1",
                "task_id": "task_1",
                "brief": {"text_path": "original_brief.md", "sha256": _sha256_bytes(b"brief")},
                "assets": [
                    {
                        "asset_id": "asset_1",
                        "filename": "ref.png",
                        "path": "/tmp/ref.png",
                        "public_reference_url": "https://assets.nori.ai/ref.png",
                    }
                ],
                "reference_transfer": {
                    "required": True,
                    "selected_count": 1,
                    "provider_fetchable_count": 1,
                    "items": [
                        {
                            "asset_id": "asset_1",
                            "filename": "ref.png",
                            "path": "/tmp/ref.png",
                            "public_reference_url": "https://assets.nori.ai/ref.png",
                            "provider_fetchable_url": "https://assets.nori.ai/ref.png",
                            "provider_fetchable": True,
                        }
                    ],
                },
                "market_evidence": {"queries": ["Holly"]},
                "run_options": {"require_image_references": True},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (run_dir / "replay_request.json").write_text(
        '{"goal":"做品牌种草","brief_text":"brief","market_evidence":{"queries":["Holly"]},"config":{"brand_name":"Holly"}}',
        encoding="utf-8",
    )
    (run_dir / "content_package.json").write_text(
        """
        {
          "package_id": "pkg_1",
          "task_id": "task_1",
          "platform": "xhs",
          "title": "Holly 怪趣文创",
          "body": "Holly 怪趣文创种草内容",
          "tags": ["Holly"],
          "prompts": {
            "cover_result": {
              "reference_paths": ["https://assets.nori.ai/ref.png"],
              "extra": {"reference_images_sent": true, "reference_public_urls": ["https://assets.nori.ai/ref.png"]}
            }
          }
        }
        """,
        encoding="utf-8",
    )
    (run_dir / "experiment_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment": {"case_id": "case1", "run_id": "run_visual", "status": "succeeded"},
                "inputs": {
                    "market_evidence": {"queries": ["Holly"]},
                    "run_options": {"require_image_references": True},
                    "reference_transfer": {
                        "required": True,
                        "selected_count": 1,
                        "provider_fetchable_count": 1,
                        "items": [
                            {
                                "asset_id": "asset_1",
                                "filename": "ref.png",
                                "path": "/tmp/ref.png",
                                "public_reference_url": "https://assets.nori.ai/ref.png",
                                "provider_fetchable_url": "https://assets.nori.ai/ref.png",
                                "provider_fetchable": True,
                            }
                        ],
                    },
                },
                "reference_images": {"status": "sent", "required": True, "sent": True, "selected_count": 1},
                "artifacts": {"paths": {}, "urls": {}},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    draft = build_content_production_evaluation_draft(
        project_root=tmp_path,
        case_id="case1",
        run_id="run_visual",
        reviewer="auto",
    )

    issue_codes = {row["code"] for row in draft["draft"]["issues"]}
    assert draft["context"]["visual_reference_review"]["status"] == "needs_human_review"
    assert draft["draft"]["metrics"]["status_by_reviewer"]["visual_reference"] == "pending"
    assert "visual_reference_needs_human_review" in issue_codes
    assert draft["draft"]["status"] in {"pending", "needs_revision", "blocked"}


def test_record_content_production_run_evaluation_validates_status_and_score(tmp_path):
    run_dir = tmp_path / "cases" / "case1" / "runs" / "run1"
    run_dir.mkdir(parents=True)

    try:
        record_content_production_run_evaluation(
            project_root=tmp_path,
            case_id="case1",
            run_id="run1",
            evaluation={"status": "approved"},
        )
    except ValueError as exc:
        assert "unsupported evaluation status" in str(exc)
    else:
        raise AssertionError("expected status validation")

    try:
        record_content_production_run_evaluation(
            project_root=tmp_path,
            case_id="case1",
            run_id="run1",
            evaluation={"status": "passed", "score": 120},
        )
    except ValueError as exc:
        assert "score must be between 0 and 100" in str(exc)
    else:
        raise AssertionError("expected score validation")
def test_experiment_readiness_reports_model_config_errors_without_raising(monkeypatch, tmp_path):
    def fake_get_active(usage):
        if usage == "image":
            raise RuntimeError("missing image model")
        return type(
            "Model",
            (),
            {
                "key": f"openai::{usage}",
                "provider_id": "openai",
                "model_id": usage,
                "type": usage,
                "supports_vision": usage == "vision",
                "supports_reference_image": False,
            },
        )()

    monkeypatch.setattr(experiments_module.llms, "get_active", fake_get_active)

    readiness = experiments_module.experiment_readiness(project_root=tmp_path, environ={})

    assert readiness["ready"] is False
    assert readiness["models"]["llm"]["ready"] is True
    assert readiness["models"]["vision"]["ready"] is True
    assert readiness["models"]["image"]["ready"] is False
    assert readiness["models"]["image"]["error_type"] == "RuntimeError"
    assert readiness["models"]["image"]["error"] == "missing image model"
    assert readiness["reference_images"]["supports_reference_image"] is False
    assert readiness["reference_images"]["strict_reference_mode_ready"] is False
    assert readiness["routes"]["run_evaluations"] == "/workflows/content-production/runs/{case_id}/{run_id}/evaluations"
    assert readiness["routes"]["content_production_case_evaluations"] == (
        "/experiments/content-production/cases/{case_id}/evaluations"
    )

    diagnostics = experiments_module.content_production_diagnostics(project_root=tmp_path, environ={})
    action_ids = {row["action_id"] for row in diagnostics["recommended_actions"]}
    assert diagnostics["ready"] is False
    assert diagnostics["status"] == "blocked"
    assert diagnostics["blocking_checks"] == ["models_ready", "image_reference_capability", "strict_reference_mode"]
    assert "configure_active_models" in action_ids
    assert "switch_reference_image_model" in action_ids
    assert "configure_reference_transfer" in action_ids
    assert diagnostics["readiness"]["models"]["image"]["error"] == "missing image model"


def test_content_production_diagnostics_reports_configuration_warnings(monkeypatch, tmp_path):
    def fake_get_active(usage):
        return type(
            "Model",
            (),
            {
                "key": f"relay::{usage}",
                "provider_id": "relay" if usage == "image" else "openai",
                "model_id": usage,
                "type": "image" if usage == "image" else "llm",
                "supports_vision": usage in {"llm", "vision"},
                "supports_reference_image": usage == "image",
            },
        )()

    monkeypatch.setattr(experiments_module.llms, "get_active", fake_get_active)

    diagnostics = experiments_module.content_production_diagnostics(
        project_root=tmp_path,
        environ={"NORI_BACKEND_PUBLIC_BASE_URL": "https://backend.nori.ai"},
    )

    assert diagnostics["ready"] is True
    assert diagnostics["status"] == "needs_configuration"
    assert "oss_reference_storage" in diagnostics["warning_checks"]
    assert "strict_reference_mode" not in diagnostics["blocking_checks"]
    assert diagnostics["readiness"]["reference_images"]["strict_reference_mode_ready"] is True
    assert any(row["action_id"] == "configure_oss_env" for row in diagnostics["recommended_actions"])
