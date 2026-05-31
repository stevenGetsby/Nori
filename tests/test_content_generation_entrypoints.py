from __future__ import annotations

import ast
import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_content_generation_public_entrypoint_no_longer_exports_generation_agent():
    module = importlib.import_module("nori.agents.content_generation")

    assert "GenerationAgent" not in module.__all__
    assert not hasattr(module, "GenerationAgent")
    assert not (ROOT / "nori" / "agents" / "content_generation" / "generation.py").exists()


def test_holly_live_workflow_uses_spec_then_artifact_execution_stages():
    path = ROOT / "scripts" / "run_holly_live_case.py"
    source = path.read_text()
    tree = ast.parse(source)
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "nori.agents.content_generation"
        for alias in node.names
    }
    stage_names = [
        call.args[0].value
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "StageSpec"
        and call.args
        and isinstance(call.args[0], ast.Constant)
    ]

    assert {"ContentSpecAgent", "ArtifactGenerationAgent"} <= imported_names
    assert "ContentProducerAgent" not in imported_names
    assert "content_design_spec" in stage_names
    assert stage_names.index("content_design_spec") < stage_names.index("content_package")


def test_continue_holly_live_case_uses_spec_before_artifact_execution():
    path = ROOT / "scripts" / "continue_holly_live_case.py"
    source = path.read_text()
    tree = ast.parse(source)
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "nori.agents.content_generation"
        for alias in node.names
    }

    assert {"ContentSpecAgent", "ArtifactGenerationAgent"} <= imported_names
    assert "ContentProducerAgent" not in imported_names
    assert source.index("ContentSpecAgent") < source.index("ArtifactGenerationAgent")
