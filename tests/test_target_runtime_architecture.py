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
    "storage",
    "workflows",
}


def test_nori_top_level_has_runtime_first_package_boundaries():
    top_level_entries = {
        path.name
        for path in (ROOT / "nori").iterdir()
        if not path.name.startswith("__")
    }
    package_dirs = {
        name
        for name in top_level_entries
        if (ROOT / "nori" / name).is_dir() and (ROOT / "nori" / name / "__init__.py").is_file()
    }
    forbidden_legacy_entries = {
        "content_generation",
        "context_building",
        "capabilities",
        "domain.py",
        "learning_loop",
        "market_analysis",
        "skill_base",
        "user_profiling",
    }

    assert EXPECTED_RUNTIME_PACKAGES <= package_dirs
    assert not (forbidden_legacy_entries & top_level_entries)


def test_agent_business_capabilities_are_importable_from_agents_boundary():
    expected_exports = {
        "nori.agents.user_profiling": ["IntakeAgent", "AccountPlannerAgent"],
        "nori.agents.planning": ["OperationPlannerAgent", "KPIPlannerAgent", "CalendarPlannerAgent"],
        "nori.agents.content_generation": [
            "ContentSpecAgent",
            "ArtifactGenerationAgent",
            "ContentProducerAgent",
            "NoteMakerAgent",
            "CoverDirectorAgent",
        ],
        "nori.agents.market_analysis": ["XHSNoteAnalyzer"],
        "nori.agents.learning_loop": ["ReviewGateAgent", "StrategyIterationAgent"],
        "nori.agents.supervisor": ["NoriSupervisorAgent"],
    }

    for module_name, names in expected_exports.items():
        module = importlib.import_module(module_name)
        for name in names:
            assert getattr(module, name) is not None, f"{module_name}.{name}"


def test_runtime_state_contracts_are_owned_by_first_class_packages():
    from nori.context import (
        ContextBundle,
        ContextCompiler,
        ContextPackBuilder,
        ContextResolver,
        ContextSlice,
        ContextView,
        attach_context_pack,
    )
    from langgraph.store.memory import InMemoryStore

    from nori.memory import InMemoryMemoryStore, MemoryStore, StableProfile, TaskMemory
    from nori.sessions import Session, SessionManager, TaskGoal
    from nori.workflows import (
        HumanGateRequired,
        HumanGateSpec,
        RuntimeRun,
        RuntimeRunRecorder,
        StageRun,
        WorkflowRun,
        WorkflowRunner,
        workflow_spec_from_base,
    )

    assert StableProfile.__module__ == "nori.memory.schemas.memory"
    assert TaskMemory.__module__ == "nori.memory.schemas.memory"
    assert MemoryStore.__module__ == "nori.memory.store"
    assert isinstance(InMemoryMemoryStore(), InMemoryStore)
    assert ContextBundle.__module__ == "nori.context.schemas.context"
    assert ContextSlice.__module__ == "nori.context.schemas.context"
    assert ContextView.__module__ == "nori.context.schemas.context"
    assert ContextCompiler.__module__ == "nori.context.compiler"
    assert ContextPackBuilder.__module__ == "nori.context.compiler"
    assert ContextResolver.__module__ == "nori.context.resolver"
    assert attach_context_pack.__module__ == "nori.context.adapters"
    assert Session.__module__ == "nori.sessions.schemas.session"
    assert TaskGoal.__module__ == "nori.sessions.schemas.session"
    assert SessionManager.__module__ == "nori.sessions.manager"
    assert WorkflowRun.__module__ == "nori.workflows.schemas.workflow"
    assert StageRun.__module__ == "nori.workflows.schemas.workflow"
    assert HumanGateSpec.__module__ == "nori.workflows.schemas.workflow"
    assert HumanGateRequired.__module__ == "nori.workflows.schemas.workflow"
    assert workflow_spec_from_base.__module__ == "nori.workflows.adapters"
    assert WorkflowRunner.__module__ == "nori.workflows.runner"
    assert not hasattr(importlib.import_module("nori.workflows"), "LangGraphWorkflowRunner")
    assert not (ROOT / "nori" / "workflows" / "langgraph_runner.py").exists()
    assert RuntimeRun.__module__ == "nori.workflows.runtime"
    assert RuntimeRunRecorder.__module__ == "nori.workflows.runtime"


def test_capability_registry_replaces_domain_registry_for_new_architecture():
    from nori.core import CAPABILITY_MODULES, CapabilityModule, capability_module_names, get_capability_module
    from nori.core import capability_registry_snapshot

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
    assert get_capability_module("supervisor") is None


def test_memory_store_adapts_langgraph_store_without_breaking_retrieval():
    from nori.memory import InMemoryMemoryStore, MemoryQuery, MemoryRecord, MemoryRetriever, SessionMemory

    store = InMemoryMemoryStore()
    store.save_session_memory(
        SessionMemory(
            session_id="session_001",
            user_id="user_001",
            records=[
                MemoryRecord(record_id="m1", text="Holly prefers visual tote bag references", tags=["preference"]),
            ],
        )
    )

    records = MemoryRetriever(store).retrieve(
        MemoryQuery(text="tote", user_id="user_001", session_id="session_001", limit=3)
    )

    assert [record.record_id for record in records] == ["m1"]
    assert store.get(("nori", "memory", "sessions"), "session_001") is not None


def test_public_capability_entrypoint_builds_and_validates_project_snapshot():
    from nori.agents.content_generation.schemas import ContentPackage
    from nori.agents.learning_loop import build_capability_snapshot, validate_capability_snapshot
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
    from nori.agents.content_generation.schemas import ContentPackage
    from nori.agents.learning_loop import LearningLoopFacade
    from nori.core import AccountOperationProject, CapabilitySnapshot, ClientBrief, ContentTask

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
    assert not hasattr(facade, "domain_snapshot_from_project")


def test_new_runtime_code_does_not_call_legacy_domain_snapshot_builder():
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        assert "domain_snapshot_from_project(" not in path.read_text(), rel_path


def test_agent_learning_loop_public_root_does_not_export_legacy_domain_snapshot():
    import nori.agents.learning_loop as learning_loop

    assert "DomainSnapshot" not in learning_loop.__all__
    assert not hasattr(learning_loop, "DomainSnapshot")


def test_core_public_root_does_not_export_legacy_domain_symbols():
    import nori.core as core

    legacy_symbols = {
        "DomainModule",
        "DomainSnapshot",
    }

    assert not (legacy_symbols & set(core.__all__))
    for symbol in legacy_symbols:
        assert not hasattr(core, symbol), symbol


def test_legacy_domain_registry_is_not_used_by_new_runtime_code():
    legacy_terms = ("DOMAIN_MODULES", "DomainModule", "DomainSnapshot", "domain_module_names", "get_domain_module")
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        source = path.read_text()
        assert not any(term in source for term in legacy_terms), rel_path


def test_agent_implementation_does_not_import_removed_top_level_agent_roots():
    removed_roots = (
        "nori.content_generation",
        "nori.context_building",
        "nori.learning_loop",
        "nori.market_analysis",
        "nori.user_profiling",
        "nori.domain",
    )
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        source = path.read_text()
        assert not any(root in source for root in removed_roots), rel_path


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
        source="brief/original.md",
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
    tree = ast.parse(source)

    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }

    assert "nori.workflows" in imported_modules
    assert "nori.workflows.content_production" in imported_modules
    assert "RuntimeRunRecorder" in imported_names
    assert "ContentProductionWorkflow" in imported_names
    assert "ContentProductionConfig" in imported_names
    assert 'human_gate_mode=os.getenv("NORI_HUMAN_GATE_MODE", "skip")' in source
    assert "workflow.run(" in source
    assert "StageSpec(" not in source
    assert "WorkflowSpec(" not in source
    assert "HumanGateSpec(" not in source
    assert "from nori.agents" not in source
    assert "class HollyRuntimeRun" not in source
    assert "def _create_runtime_run" not in source
    assert "def _record_stage" not in source


def test_holly_live_case_uses_case_workspace_artifact_store():
    path = ROOT / "scripts" / "run_holly_live_case.py"
    source = path.read_text(encoding="utf-8")

    assert "CaseWorkspace" in source
    assert "CASE.create_run_dir" in source
    assert "record_content_production_artifacts" in source
    assert 'ROOT / "data" / "Holly"' not in source
    assert 'CASE.brief_dir / "original.md"' in source
