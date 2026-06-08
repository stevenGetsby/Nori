from __future__ import annotations

import json
from datetime import datetime

from nori.core import CaseWorkspace


def _jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_case_workspace_creates_human_readable_case_and_artifact_index(tmp_path):
    workspace = CaseWorkspace(tmp_path, case_id="Holly", title="Holly Shit开心拉屎")

    workspace.ensure()
    run_dir = workspace.create_run_dir("holly_live", at=datetime(2026, 6, 1, 0, 0, 0))
    artifact = workspace.record_artifact(
        run_id=run_dir.name,
        artifact_type="content_design_spec",
        path=run_dir / "artifacts" / "content_design_spec.json",
        created_by="ContentSpecAgent",
        input_artifacts=["content_context_pack"],
        status="passed",
    )

    assert workspace.case_dir == tmp_path / "cases" / "Holly"
    assert workspace.brief_dir == workspace.case_dir / "brief"
    assert workspace.raw_assets_dir == workspace.case_dir / "assets" / "raw"
    assert workspace.runs_dir == workspace.case_dir / "runs"
    assert workspace.showcase_dir == workspace.case_dir / "showcase"
    assert run_dir == workspace.runs_dir / "20260601_000000_holly_live"
    assert artifact["path"] == "cases/Holly/runs/20260601_000000_holly_live/artifacts/content_design_spec.json"

    case_manifest = json.loads((workspace.case_dir / "case.json").read_text(encoding="utf-8"))
    assert case_manifest["case_id"] == "Holly"
    assert case_manifest["title"] == "Holly Shit开心拉屎"
    assert case_manifest["directories"]["runs"] == "runs"

    cases = _jsonl(tmp_path / "data" / "artifact_index" / "cases.jsonl")
    runs = _jsonl(tmp_path / "data" / "artifact_index" / "runs.jsonl")
    artifacts = _jsonl(tmp_path / "data" / "artifact_index" / "artifacts.jsonl")
    assert cases[-1]["case_id"] == "Holly"
    assert runs[-1]["run_id"] == "20260601_000000_holly_live"
    assert artifacts[-1]["artifact_id"] == "Holly:20260601_000000_holly_live:content_design_spec"
