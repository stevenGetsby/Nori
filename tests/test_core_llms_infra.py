from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace

from langchain_core.messages import HumanMessage


ROOT = Path(__file__).resolve().parents[1]


def test_core_llms_package_is_canonical_runtime_infra():
    import nori.core.llms as core_llms

    assert core_llms.__name__ == "nori.core.llms"
    assert callable(core_llms.chat)
    assert callable(core_llms.image)
    assert issubclass(core_llms.ChatJSONError, Exception)


def test_top_level_llms_package_has_been_removed():
    assert not (ROOT / "llms").exists()
    assert importlib.util.find_spec("llms") is None


def test_over_split_llm_json_call_module_has_been_folded_into_client():
    module_name = "json_" + "calls"
    assert not (ROOT / "nori" / "core" / "llms" / f"{module_name}.py").exists()
    assert importlib.util.find_spec(f"nori.core.llms.{module_name}") is None


def test_over_split_structured_call_module_has_been_folded_into_client():
    module_name = "structured_" + "calls"
    assert not (ROOT / "nori" / "core" / "llms" / f"{module_name}.py").exists()
    assert importlib.util.find_spec(f"nori.core.llms.{module_name}") is None


def test_core_llms_module_layout_is_explicit_runtime_infra():
    allowed = {
        "__init__.py",
        "capabilities.py",
        "client.py",
        "image_inputs.py",
        "image_providers.py",
        "imager.py",
        "lm.py",
        "telemetry.py",
    }

    actual = {
        path.name
        for path in (ROOT / "nori" / "core" / "llms").glob("*.py")
    }

    assert actual == allowed


def test_internal_runner_and_config_splits_have_been_folded_into_gateway_core():
    old_chat_module = "nori.core.llms.chat_" + "runner"
    old_image_module = "nori.core.llms.image_" + "runner"
    removed = (
        old_chat_module,
        old_image_module,
        "nori.core.llms.config",
        "nori.core.llms.mode",
        "nori.core.llms.request_" + "params",
        "nori.core.llms." + "results",
        "nori.core.llms.json_" + "parser",
        "nori.core.llms.intent_extractor",
        "nori.core.llms.target_selector",
        "nori.core.llms.structured_prompts",
        "nori.core.llms.structured_outputs",
    )

    for module in removed:
        assert importlib.util.find_spec(module) is None


def test_llms_submodules_do_not_reexport_legacy_contract_aliases():
    import nori.core.llms as llms
    import nori.core.llms.client as client_module
    import nori.core.llms.image_providers as image_provider_module
    import nori.core.llms.imager as imager_module
    import nori.core.llms.lm as lm_module

    assert set(llms.__all__) == {
        "NoriAIClient",
        "achat",
        "chat",
        "chat_json",
        "current_mode",
        "ensure_ready",
        "get_active",
        "image",
        "set_mode",
        "set_telemetry_sink",
        "LLMClientConfigError",
        "ChatCapabilityError",
        "ChatJSONError",
        "ChatResultError",
        "ImageCapabilityError",
        "ImageResultError",
    }
    assert llms.set_telemetry_sink.__module__ == "nori.core.llms.telemetry"
    assert not hasattr(llms, "parse_json_object")
    assert not hasattr(llms, "chat_json_with_raw")
    assert not hasattr(llms, "chat_json_raw")
    assert not hasattr(llms, "get_client")
    assert not hasattr(llms, "build_client_bundle")
    assert not hasattr(llms, "validate_client_config")
    assert not hasattr(client_module, "LLMClientConfigError")
    assert not hasattr(client_module, "_client_options")
    assert hasattr(client_module, "NoriAIClient")
    assert hasattr(lm_module, "LanguageModelClient")
    assert hasattr(imager_module, "ImageClient")
    assert hasattr(image_provider_module, "ImageProviders")
    assert not hasattr(image_provider_module, "collect_image_" + "results")
    assert not hasattr(image_provider_module, "image_openai_" + "edit")


def test_chat_model_factory_uses_langchain_init_chat_model_not_direct_chat_openai():
    source = (ROOT / "nori" / "core" / "llms" / "client.py").read_text()

    assert "from langchain.chat_models import init_chat_model" in source
    assert "init_chat_model(" in source
    assert "ChatOpenAI" not in source
    assert "_load_chat_openai" not in source


def test_language_model_client_uses_langchain_structured_output_with_narrow_sdk_fallback():
    source = (ROOT / "nori" / "core" / "llms" / "lm.py").read_text()

    assert "get_chat_model" in source
    assert "build_client_bundle" in source
    assert ".invoke(" in source
    assert ".ainvoke(" in source
    assert "with_structured_output" in source
    assert "parse_json_markdown" not in source
    assert "JSONDecoder" not in source
    assert "raw_decode" not in source
    assert "_is_structured_output_parse_error" not in source
    assert "_is_openai_raw_response_parse_adapter_error" in source
    assert "_chat_json_via_direct_json_mode" in source
    assert source.count(".chat.completions." + "create") == 1


def test_pyproject_packages_nori_core_llms_not_top_level_llms():
    pyproject = (ROOT / "pyproject.toml").read_text()

    assert 'include = ["backend*", "nori*", "data_collect*"]' in pyproject
    assert '"llms*"' not in pyproject


def test_nori_runtime_imports_core_llms_not_top_level_compat_package():
    allowed_roots = {
        ("nori", "core", "llms"),
    }
    for path in (ROOT / "nori").rglob("*.py"):
        rel_path = path.relative_to(ROOT)
        if rel_path.parts[:3] in allowed_roots:
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert not any(alias.name == "llms" for alias in node.names), rel_path
            if isinstance(node, ast.ImportFrom):
                assert node.module != "llms", rel_path


def test_source_tree_imports_core_llms_not_top_level_compat_package():
    scanned_roots = ("nori", "backend", "scripts", "tests")
    for root_name in scanned_roots:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            rel_path = path.relative_to(ROOT)
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    assert not any(
                        alias.name == "llms" or alias.name.startswith("llms.")
                        for alias in node.names
                    ), rel_path
                if isinstance(node, ast.ImportFrom) and node.module:
                    assert node.module != "llms" and not node.module.startswith("llms."), rel_path


def test_core_chat_capability_accepts_langchain_messages():
    from nori.core.llms.capabilities import ensure_chat_capability, messages_need_vision

    model = SimpleNamespace(
        key="openai::gpt-4o-mini",
        type="vision",
        supports_vision=True,
    )
    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe this"},
            {"type": "image_url", "image_url": {"url": "https://example.test/image.png"}},
        ]
    )

    assert messages_need_vision([message]) is True
    ensure_chat_capability(model, [message], "vision")
