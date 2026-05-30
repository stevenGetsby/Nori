from pathlib import Path
import importlib
import importlib.util
import ast


ROOT = Path(__file__).resolve().parents[1]


ALLOWED_NORI_TOP_LEVEL_DIRS = {
    "agents",
    "capabilities",
    "context",
    "core",
    "memory",
    "sessions",
    "shared",
    "workflows",
}


WORKFLOW_STAGE_PACKAGES = {
    "nori/agents/user_profiling/intaker": {"intaker.py", "package.py", "normalizer.py", "taxonomy.py", "image_tagger.py"},
    "nori/agents/user_profiling/account_planner": {
        "account_planner.py",
        "package.py",
        "fallback.py",
        "search.py",
        "normalizer.py",
        "portrait.py",
        "keywords.py",
    },
    "nori/agents/content_generation/note_maker": {"note_maker.py", "package.py"},
    "nori/agents/content_generation/cover_director": {"cover_director.py", "package.py", "output.py"},
    "nori/agents/content_generation/content_producer": {"content_producer.py", "package.py", "state.py"},
    "nori/agents/planning/operation_planner": {
        "operation_planner.py",
        "package.py",
        "project_builder.py",
        "project_policy.py",
        "normalizer.py",
    },
    "nori/agents/planning/kpi_planner": {"kpi_planner.py", "package.py", "normalizer.py"},
    "nori/agents/planning/calendar_planner": {
        "calendar_planner.py",
        "package.py",
        "normalizer.py",
        "policy.py",
        "task_builder.py",
    },
    "nori/agents/learning_loop/review": {"review_gate.py", "package.py", "policy.py", "scoring.py", "state.py"},
    "nori/agents/learning_loop/strategy": {"strategy_iteration.py", "package.py", "policy.py", "state.py"},
    "nori/agents/market_analysis/xhs_note_analyzer": {
        "xhs_note_analyzer.py",
        "package.py",
        "loader.py",
        "rules.py",
        "note_llm.py",
        "session_clustering.py",
        "session_llm.py",
        "session_reporter.py",
        "skill_builder.py",
    },
}


PROMPT_OWNING_STAGE_PACKAGES: set[str] = set()


DOMAIN_PACKAGE_ROOTS = [
    "nori.agents.user_profiling",
    "nori.agents.market_analysis",
    "nori.agents.planning",
    "nori.agents.content_generation",
    "nori.agents.learning_loop",
]


BUSINESS_MODULE_IMPORT_ROOTS = {
    "nori.agents.user_profiling",
    "nori.agents.market_analysis",
    "nori.agents.planning",
    "nori.agents.content_generation",
    "nori.agents.learning_loop",
}
UPSTREAM_DOMAIN_IMPORT_GUARDS = {
    "nori/agents/user_profiling": {"nori.agents.planning", "nori.agents.content_generation", "nori.agents.learning_loop", "nori.agents.market_analysis"},
    "nori/agents/market_analysis": {"nori.agents.planning", "nori.agents.content_generation", "nori.agents.learning_loop", "nori.agents.user_profiling"},
}
SHARED_WORKFLOW_CONTRACTS = {
    "AccountOperationProject",
    "AssetLibrary",
    "AssetRecord",
    "ClientBrief",
    "ContentCalendar",
    "ContentTask",
    "KPIPlan",
    "OperationPlan",
    "UserAsset",
}


REMOVED_FLAT_WRAPPER_FILES = [
    "nori/user_profiling/intake_normalizer.py",
    "nori/user_profiling/intake_taxonomy.py",
    "nori/user_profiling/image_tagger.py",
    "nori/user_profiling/intaker/prompts.py",
    "nori/user_profiling/account_plan_inputs.py",
    "nori/user_profiling/account_plan_prompts.py",
    "nori/user_profiling/account_plan_fallback.py",
    "nori/user_profiling/account_plan_search.py",
    "nori/user_profiling/account_plan_normalizer.py",
    "nori/user_profiling/account_plan_portrait.py",
    "nori/user_profiling/account_plan_keywords.py",
    "nori/content_generation/skill_picker.py",
    "nori/content_generation/asset_curator.py",
    "nori/content_generation/note_composer.py",
    "nori/content_generation/note_maker/prompts.py",
    "nori/content_generation/note_maker/skill_picker.py",
    "nori/content_generation/note_maker/asset_curator.py",
    "nori/content_generation/note_maker/note_composer.py",
    "nori/content_generation/cover_refs.py",
    "nori/content_generation/cover_prompt.py",
    "nori/content_generation/cover_output.py",
    "nori/content_generation/producer.py",
    "nori/content_generation/package_inputs.py",
    "nori/content_generation/package_builder.py",
    "nori/content_generation/package_refs.py",
    "nori/content_generation/content_producer/inputs.py",
    "nori/content_generation/content_producer/builder.py",
    "nori/content_generation/content_producer/refs.py",
    "nori/content_generation/cover_director/prompts.py",
    "nori/content_generation/cover_director/refs.py",
    "nori/content_generation/production_state.py",
    "nori/context_building/operation_planner/inputs.py",
    "nori/context_building/operation_planner/prompts.py",
    "nori/context_building/operation_planner_inputs.py",
    "nori/context_building/operation_planner_prompts.py",
    "nori/context_building/operation_project_builder.py",
    "nori/context_building/operation_project_policy.py",
    "nori/context_building/operation_plan_normalizer.py",
    "nori/context_building/kpi_planner/inputs.py",
    "nori/context_building/kpi_planner/prompts.py",
    "nori/context_building/kpi_planner_inputs.py",
    "nori/context_building/kpi_planner_prompts.py",
    "nori/context_building/kpi_plan_normalizer.py",
    "nori/context_building/calendar_planner/inputs.py",
    "nori/context_building/calendar_planner/prompts.py",
    "nori/context_building/calendar_planner_inputs.py",
    "nori/context_building/calendar_planner_prompts.py",
    "nori/context_building/calendar_plan_normalizer.py",
    "nori/context_building/calendar_plan_policy.py",
    "nori/context_building/calendar_task_builder.py",
    "nori/learning_loop/review_inputs.py",
    "nori/learning_loop/review/inputs.py",
    "nori/learning_loop/review_policy.py",
    "nori/learning_loop/review_scoring.py",
    "nori/learning_loop/review_state.py",
    "nori/learning_loop/strategy_inputs.py",
    "nori/learning_loop/strategy/inputs.py",
    "nori/learning_loop/strategy_policy.py",
    "nori/learning_loop/strategy_state.py",
    "nori/user_profiling/account_planner/inputs.py",
    "nori/user_profiling/account_planner/prompts.py",
    "nori/market_analysis/xhs_note_loader.py",
    "nori/market_analysis/xhs_note_analyzer/prompts.py",
    "nori/market_analysis/xhs_note_rules.py",
    "nori/market_analysis/xhs_note_llm.py",
    "nori/market_analysis/xhs_session_clustering.py",
    "nori/market_analysis/xhs_session_llm.py",
    "nori/market_analysis/xhs_session_reporter.py",
    "nori/market_analysis/xhs_skill_builder.py",
]


REMOVED_LEGACY_PACKAGES = [
    "nori/gen_agents",
    "nori/ops_agents",
    "nori/ana_agents",
    "nori/ops_models",
    "nori/agent_models",
    "nori/agent_utils",
]
REMOVED_COMPAT_FILES = [
    "nori/_module_alias.py",
    "nori/_model_coercion.py",
    "nori/config_models.py",
    "nori/context_building/models.py",
    "llms/errors.py",
    "llms/structured_models.py",
]
REMOVED_SHARED_DOMAIN_HELPERS = ["nori/shared/note_skill_fixture.py"]


REMOVED_LEGACY_IMPORTS = [
    "nori.gen_agents",
    "nori.ops_agents",
    "nori.ana_agents",
    "nori.ops_models",
    "nori.agent_models",
    "nori.agent_utils",
    "nori._model_coercion",
    "nori.config_models",
    "nori.agents.planning.models",
    "llms.errors",
    "llms.structured_models",
]


FORBIDDEN_PACKAGE_ROOT_EXPORTS = [
    "from .intaker import llms",
    "from .account_planner import llms",
    "from .note_maker import llms",
    "from .cover_director import llms",
    "from .operation_planner import llms",
    "from .kpi_planner import llms",
    "from .calendar_planner import llms",
    "from .xhs_note_analyzer import llms",
]


USER_PROFILING_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT = [
    "from nori.agent_models import AccountPlanResult",
    "from nori.agent_models import AccountPlannerInput",
    "from nori.agent_models import IntakeResult",
    "from nori.agent_models import UserInput",
    "from nori.agent_models.account_planner import",
    "from nori.agent_models.intake import",
]


CONTENT_GENERATION_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT = [
    "from nori.agent_models import AssetBundle",
    "from nori.agent_models import CandidateTitle",
    "from nori.agent_models import CoverResult",
    "from nori.agent_models import NoteDraft",
    "from nori.agent_models import UserAsset",
    "from nori.agent_models.cover_result import",
    "from nori.agent_models.note_draft import",
]


MARKET_ANALYSIS_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT = [
    "from nori.agent_models import NoteEvidence",
    "from nori.agent_models import NoteSkill",
    "from nori.agent_models import SessionSkillReport",
    "from nori.agent_models import XHSNoteSample",
    "from nori.agent_models import XHSSeedSkillDraft",
    "from nori.agent_models.xhs_note import",
]


def test_workflow_implementation_files_are_grouped_by_stage_package():
    for package, expected_files in WORKFLOW_STAGE_PACKAGES.items():
        package_path = ROOT / package
        assert package_path.is_dir(), package
        assert (package_path / "__init__.py").is_file(), package
        files = {path.name for path in package_path.glob("*.py")}
        assert expected_files <= files
        assert "agent.py" not in files
        assert "prompt.py" not in files


def test_workflow_stage_packages_keep_contracts_in_models_not_schema_reexports():
    for package in WORKFLOW_STAGE_PACKAGES:
        package_path = ROOT / package
        assert not (package_path / "schema.py").exists(), package


def test_workflow_stage_packages_only_keep_prompt_files_when_they_own_prompts():
    for package in WORKFLOW_STAGE_PACKAGES:
        package_path = ROOT / package
        expected = package in PROMPT_OWNING_STAGE_PACKAGES
        assert (package_path / "prompts.py").exists() is expected, package


def test_workflow_runtime_uses_core_llm_factory_instead_of_direct_llms_imports():
    allowed_llms_imports = {
        "nori/core/llm.py",
    }
    for package in WORKFLOW_STAGE_PACKAGES:
        package_path = ROOT / package
        for path in package_path.glob("*.py"):
            rel_path = path.relative_to(ROOT).as_posix()
            if rel_path in allowed_llms_imports:
                continue
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    assert not any(alias.name == "llms" for alias in node.names), rel_path
                if isinstance(node, ast.ImportFrom):
                    assert node.module != "llms", rel_path


def test_nori_top_level_packages_are_runtime_agent_or_shared_boundaries():
    package_dirs = {
        path.name
        for path in (ROOT / "nori").iterdir()
        if path.is_dir() and not path.name.startswith("__") and (path / "__init__.py").is_file()
    }
    assert package_dirs == ALLOWED_NORI_TOP_LEVEL_DIRS


def test_workflow_stage_roots_export_only_explicit_public_entrypoints():
    for package in WORKFLOW_STAGE_PACKAGES:
        init_path = ROOT / package / "__init__.py"
        source = init_path.read_text()
        assert "import *" not in source, package
        for forbidden in FORBIDDEN_PACKAGE_ROOT_EXPORTS:
            assert forbidden not in source, package


def test_domain_package_roots_use_shared_lazy_export_helper():
    for module_name in DOMAIN_PACKAGE_ROOTS:
        init_path = ROOT / module_name.replace(".", "/") / "__init__.py"
        source = init_path.read_text()
        assert "from nori.core.lazy_exports import lazy_export" in source, module_name
        assert "_LAZY_EXPORTS" in source, module_name
        assert "return lazy_export(__name__, _LAZY_EXPORTS, name)" in source, module_name


def test_domain_package_public_exports_are_importable():
    for module_name in DOMAIN_PACKAGE_ROOTS:
        module = importlib.import_module(module_name)
        for exported_name in module.__all__:
            assert getattr(module, exported_name) is not None, f"{module_name}.{exported_name}"


def test_old_flat_helper_files_are_not_kept_in_canonical_domains():
    for rel_path in REMOVED_FLAT_WRAPPER_FILES:
        assert not (ROOT / rel_path).exists(), rel_path


def test_legacy_packages_are_removed():
    for package in REMOVED_LEGACY_PACKAGES:
        assert not (ROOT / package).exists(), package


def test_legacy_alias_helpers_are_removed():
    for rel_path in REMOVED_COMPAT_FILES:
        assert not (ROOT / rel_path).exists(), rel_path


def test_shared_layer_does_not_import_business_modules():
    for path in (ROOT / "nori" / "shared").glob("*.py"):
        rel_path = path.relative_to(ROOT)
        assert not _imports_from_forbidden_modules(path, modules=BUSINESS_MODULE_IMPORT_ROOTS), rel_path


def test_upstream_domain_facades_do_not_import_downstream_domains():
    for rel_root, forbidden_modules in UPSTREAM_DOMAIN_IMPORT_GUARDS.items():
        facade_path = ROOT / rel_root / "facade.py"
        assert not _imports_from_forbidden_modules(facade_path, modules=forbidden_modules), rel_root


def test_user_profiling_runtime_does_not_import_content_generation():
    for path in (ROOT / "nori" / "agents" / "user_profiling").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        assert not _imports_from_forbidden_modules(path, modules={"nori.agents.content_generation"}), rel_path


def test_downstream_runtime_imports_shared_workflow_contracts_from_core():
    forbidden_roots = {
        "nori.agents.content_generation",
        "nori.agents.learning_loop",
    }
    forbidden_sources = {
        "nori.agents.content_generation.models",
        "nori.agents.planning.models",
        "nori.agents.user_profiling.models",
    }
    for root in forbidden_roots:
        for path in (ROOT / root.replace(".", "/")).rglob("*.py"):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.module not in forbidden_sources:
                    continue
                imported = {alias.name for alias in node.names}
                assert not (imported & SHARED_WORKFLOW_CONTRACTS), path.relative_to(ROOT)


def test_runtime_imports_shared_workflow_contracts_from_core():
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if not _imports_from_legacy_contract_owner(rel_path, node):
                continue
            imported = {alias.name for alias in node.names}
            assert not (imported & SHARED_WORKFLOW_CONTRACTS), rel_path


def test_domain_specific_helpers_are_not_kept_in_shared_layer():
    for rel_path in REMOVED_SHARED_DOMAIN_HELPERS:
        assert not (ROOT / rel_path).exists(), rel_path


def test_runtime_code_imports_public_contracts_from_core_boundary():
    private_contract_modules = {
        "nori._model_coercion",
        "nori.config_models",
        "llms.errors",
        "llms.structured_models",
    }
    private_llms_relative_contract_modules = {"errors", "structured_models"}
    for root in (ROOT / "nori", ROOT / "llms"):
        for path in root.rglob("*.py"):
            rel_path = path.relative_to(ROOT)
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported = {alias.name for alias in node.names}
                    assert not (imported & private_contract_modules), rel_path
                if isinstance(node, ast.ImportFrom):
                    assert node.module not in private_contract_modules, rel_path
                    if rel_path.parts[0] == "llms" and node.level == 1:
                        assert node.module not in private_llms_relative_contract_modules, rel_path


def test_legacy_import_roots_are_not_importable():
    for module_name in REMOVED_LEGACY_IMPORTS:
        assert importlib.util.find_spec(module_name) is None, module_name


def test_runtime_code_uses_user_profiling_model_owner_imports():
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path.parts[:2] == ("nori", "agent_models"):
            continue
        source = path.read_text()
        for forbidden in USER_PROFILING_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT:
            assert forbidden not in source, rel_path
        assert not _imports_forbidden_names(
            path,
            module="nori.agent_models",
            names={"AccountPlanResult", "AccountPlannerInput", "IntakeResult", "UserInput"},
        ), rel_path
        assert not _imports_from_forbidden_modules(
            path,
            modules={"nori.agent_models.account_planner", "nori.agent_models.intake"},
        ), rel_path


def test_runtime_code_uses_content_generation_model_owner_imports():
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path.parts[:2] == ("nori", "agent_models"):
            continue
        source = path.read_text()
        for forbidden in CONTENT_GENERATION_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT:
            assert forbidden not in source, rel_path
        assert not _imports_forbidden_names(
            path,
            module="nori.agent_models",
            names={"AssetBundle", "CandidateTitle", "CoverResult", "NoteDraft", "UserAsset"},
        ), rel_path
        assert not _imports_from_forbidden_modules(
            path,
            modules={"nori.agent_models.cover_result", "nori.agent_models.note_draft"},
        ), rel_path


def test_runtime_code_uses_market_analysis_model_owner_imports():
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path.parts[:2] == ("nori", "agent_models"):
            continue
        source = path.read_text()
        for forbidden in MARKET_ANALYSIS_MODEL_IMPORTS_FROM_REMOVED_MODEL_ROOT:
            assert forbidden not in source, rel_path
        assert not _imports_forbidden_names(
            path,
            module="nori.agent_models",
            names={"NoteEvidence", "NoteSkill", "SessionSkillReport", "XHSNoteSample", "XHSSeedSkillDraft"},
        ), rel_path
        assert not _imports_from_forbidden_modules(
            path,
            modules={"nori.agent_models.xhs_note"},
        ), rel_path


def _imports_forbidden_names(path: Path, *, module: str, names: set[str]) -> bool:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            if any(alias.name in names for alias in node.names):
                return True
    return False


def _imports_from_forbidden_modules(path: Path, *, modules: set[str]) -> bool:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if any(node.module == module or node.module.startswith(f"{module}.") for module in modules):
                return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(alias.name == module or alias.name.startswith(f"{module}.") for module in modules):
                    return True
    return False


def _imports_from_legacy_contract_owner(path: Path, node: ast.ImportFrom) -> bool:
    if node.module in {"nori.agents.user_profiling.models", "nori.agents.planning.models", "nori.agents.content_generation.models"}:
        return True
    if node.level == 1 and node.module == "models":
        if path.parts[:2] in {
            ("nori", "user_profiling"),
            ("nori", "context_building"),
            ("nori", "content_generation"),
        }:
            return True
    return False
