from __future__ import annotations

import importlib
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_RUNTIME_PACKAGES = {
    "agents",
    "context",
    "core",
    "memory",
    "sessions",
    "shared",
    "workflows",
}


def test_nori_top_level_has_runtime_first_package_boundaries():
    package_dirs = {
        path.name
        for path in (ROOT / "nori").iterdir()
        if path.is_dir() and not path.name.startswith("__") and (path / "__init__.py").is_file()
    }

    assert EXPECTED_RUNTIME_PACKAGES <= package_dirs
    assert "domains" not in package_dirs


def test_agent_business_capabilities_are_importable_from_agents_boundary():
    expected_exports = {
        "nori.agents.user_profiling": ["IntakeAgent", "AccountPlannerAgent"],
        "nori.agents.planning": ["OperationPlannerAgent", "KPIPlannerAgent", "CalendarPlannerAgent"],
        "nori.agents.content_generation": ["NoteMakerAgent", "CoverDirectorAgent", "ContentProducerAgent"],
        "nori.agents.market_analysis": ["XHSNoteAnalyzer"],
        "nori.agents.learning_loop": ["ReviewGateAgent", "StrategyIterationAgent"],
    }

    for module_name, names in expected_exports.items():
        module = importlib.import_module(module_name)
        for name in names:
            assert getattr(module, name) is not None, f"{module_name}.{name}"


def test_runtime_state_contracts_are_owned_by_first_class_packages():
    from nori.context import ContextBundle, ContextResolver
    from nori.memory import MemoryStore, StableProfile, TaskMemory
    from nori.sessions import Session, SessionManager, TaskGoal
    from nori.workflows import RuntimeRun, RuntimeRunRecorder, StageRun, WorkflowRun, WorkflowRunner

    assert StableProfile.__module__ == "nori.memory.models"
    assert TaskMemory.__module__ == "nori.memory.models"
    assert MemoryStore.__module__ == "nori.memory.store"
    assert ContextBundle.__module__ == "nori.context.models"
    assert ContextResolver.__module__ == "nori.context.resolver"
    assert Session.__module__ == "nori.sessions.models"
    assert TaskGoal.__module__ == "nori.sessions.models"
    assert SessionManager.__module__ == "nori.sessions.manager"
    assert WorkflowRun.__module__ == "nori.workflows.models"
    assert StageRun.__module__ == "nori.workflows.models"
    assert WorkflowRunner.__module__ == "nori.workflows.runner"
    assert RuntimeRun.__module__ == "nori.workflows.runtime"
    assert RuntimeRunRecorder.__module__ == "nori.workflows.runtime"


def test_capability_registry_replaces_domain_registry_for_new_architecture():
    from nori.core import CAPABILITY_MODULES, CapabilityModule, capability_module_names, get_capability_module
    from nori.capabilities import capability_registry_snapshot

    assert capability_module_names() == [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    assert all(isinstance(module, CapabilityModule) for module in CAPABILITY_MODULES)

    planning = get_capability_module("planning")
    assert planning is not None
    assert planning.package == "nori.agents.planning"
    assert "OperationPlannerAgent" in planning.agents

    assert get_capability_module("domains") is None
    snapshot = capability_registry_snapshot()
    assert snapshot["module_names"] == capability_module_names()
    assert snapshot["modules"][2]["package"] == "nori.agents.planning"


def test_public_capability_entrypoint_builds_and_validates_project_snapshot():
    from nori.capabilities import build_capability_snapshot, validate_capability_snapshot
    from nori.content_generation.models import ContentPackage
    from nori.core import AccountOperationProject, CapabilitySnapshot, ClientBrief, ContentTask

    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        content_tasks=[ContentTask(task_id="task_001", topic="母亲节花束搭配")],
        content_packages=[ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买")],
    )

    snapshot = build_capability_snapshot(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
    )

    assert isinstance(snapshot, CapabilitySnapshot)
    assert snapshot.snapshot_id == "capability_project_001"
    assert snapshot.capability_names == [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    assert snapshot.is_valid()
    assert validate_capability_snapshot(snapshot) == []
    assert validate_capability_snapshot(snapshot.to_dict()) == []


def test_learning_loop_facade_owns_capability_snapshot_primary_method():
    from nori.content_generation.models import ContentPackage
    from nori.core import AccountOperationProject, CapabilitySnapshot, ClientBrief, ContentTask
    from nori.learning_loop import LearningLoopFacade

    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        content_tasks=[ContentTask(task_id="task_001", topic="母亲节花束搭配")],
        content_packages=[ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买")],
    )

    facade = LearningLoopFacade()
    snapshot = facade.capability_snapshot_from_project(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
        signal_source="metrics",
        signal_target="preference",
    )
    legacy = facade.domain_snapshot_from_project(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
        signal_source="metrics",
        signal_target="preference",
    )

    assert isinstance(snapshot, CapabilitySnapshot)
    assert snapshot.snapshot_id == "capability_project_001"
    assert snapshot.capability_names == [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    assert snapshot.is_valid()
    assert legacy.snapshot_id == "domain_project_001"
    assert legacy.context_packs[0].to_dict() == snapshot.context_packs[0].to_dict()


def test_legacy_domain_entrypoint_delegates_to_capability_snapshot(monkeypatch):
    import nori.domain as domain
    from nori.core import CapabilitySnapshot

    calls = []

    def fake_build(project, **kwargs):
        calls.append((project, kwargs))
        return CapabilitySnapshot(
            snapshot_id="capability_project_001",
            project_id="project_001",
            capability_names=[
                "user_profiling",
                "market_analysis",
                "planning",
                "content_generation",
                "learning_loop",
            ],
        )

    monkeypatch.setattr(domain, "_build_capability_snapshot", fake_build)

    snapshot = domain.build_domain_snapshot({"project_id": "project_001"}, confidence=0.7)

    assert calls
    assert calls[0][1]["confidence"] == 0.7
    assert snapshot.snapshot_id == "domain_project_001"


def test_new_runtime_code_does_not_call_legacy_domain_snapshot_builder():
    allowed = {
        Path("nori/learning_loop/facade.py"),
    }
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path in allowed:
            continue
        assert "domain_snapshot_from_project(" not in path.read_text(), rel_path


def test_learning_loop_public_root_does_not_export_legacy_domain_snapshot():
    import nori.learning_loop as learning_loop

    assert "DomainSnapshot" not in learning_loop.__all__
    assert not hasattr(learning_loop, "DomainSnapshot")


def test_core_public_root_does_not_export_legacy_domain_symbols():
    import nori.core as core

    legacy_symbols = {
        "DOMAIN_MODULES",
        "DomainModule",
        "DomainSnapshot",
        "domain_module_names",
        "get_domain_module",
    }

    assert not (legacy_symbols & set(core.__all__))
    for symbol in legacy_symbols:
        assert not hasattr(core, symbol), symbol


def test_legacy_domain_registry_is_not_used_by_new_runtime_code():
    legacy_terms = ("DOMAIN_MODULES", "DomainModule", "domain_module_names", "get_domain_module")
    allowed = {
        Path("nori/core/__init__.py"),
        Path("nori/core/architecture.py"),
        Path("nori/domain.py"),
    }
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path in allowed:
            continue
        source = path.read_text()
        assert not any(term in source for term in legacy_terms), rel_path


def test_holly_live_case_uses_agents_public_boundary():
    path = ROOT / "scripts" / "run_holly_live_case.py"
    tree = ast.parse(path.read_text())
    forbidden_roots = {
        "nori.content_generation",
        "nori.context_building",
        "nori.learning_loop",
        "nori.market_analysis.xhs_note_analyzer",
        "nori.user_profiling",
    }

    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        assert not any(
            node.module == root or node.module.startswith(f"{root}.")
            for root in forbidden_roots
        ), node.module


def test_holly_live_case_records_runtime_session_context_and_workflow(tmp_path):
    from nori.workflows import RuntimeRunRecorder

    brief_text = "Holly Shit 是一个怪趣文创品牌。"
    runtime = RuntimeRunRecorder(
        user_id="holly",
        profile_id="holly",
        workflow_name="holly_live_content_generation",
        goal="用 Holly 真实素材和小红书市场证据生成一篇图文内容，并生成封面图片。",
    ).start(
        user_input={"brief_text": brief_text},
        run_dir=tmp_path,
        source="设计理念.md",
        acceptance=[
            "生成 content_package.json",
            "生成 cover png",
            "生成 summary.md",
        ],
    )

    assert runtime.session.user_id == "holly"
    assert runtime.task_goal.workflow_name == "holly_live_content_generation"
    assert runtime.context.session_id == runtime.session.session_id
    assert runtime.workflow_run.session_id == runtime.session.session_id
    assert runtime.workflow_run.task_id == runtime.task_goal.task_id

    RuntimeRunRecorder.write_snapshot(runtime, tmp_path)

    assert (tmp_path / "session.json").is_file()
    assert (tmp_path / "context_bundle.json").is_file()
    assert (tmp_path / "workflow_run.json").is_file()


def test_holly_live_case_delegates_runtime_bookkeeping_to_workflows_package():
    path = ROOT / "scripts" / "run_holly_live_case.py"
    source = path.read_text()

    assert "from nori.workflows import RuntimeRunRecorder" in source
    assert "class HollyRuntimeRun" not in source
    assert "def _create_runtime_run" not in source
    assert "def _record_stage" not in source
