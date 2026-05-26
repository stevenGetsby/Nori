from __future__ import annotations

import llms
import llms.intent_extractor as intent_module
import llms.structured_calls as calls_module
import llms.target_selector as target_module
from nori.core import IntentLLMResult, StructuredCallResult, TargetSelectionResult
from nori.core import contracts


def test_structured_result_models_live_in_core_contracts_boundary():
    intent = IntentLLMResult(fields={"topic": "通勤香薰"})
    target = TargetSelectionResult(target_selector="cover#1")
    call = StructuredCallResult(data={"ok": True})

    assert intent.ok is True
    assert target.ok is True
    assert call.ok is True
    assert IntentLLMResult(error="parse_error").ok is False
    assert TargetSelectionResult(error="missing_selector").ok is False
    assert StructuredCallResult(error="api_error:RuntimeError").ok is False


def test_structured_result_model_import_identities_stay_compatible():
    assert contracts.IntentLLMResult is IntentLLMResult
    assert contracts.TargetSelectionResult is TargetSelectionResult
    assert contracts.StructuredCallResult is StructuredCallResult
    assert llms.IntentLLMResult is IntentLLMResult
    assert llms.TargetSelectionResult is TargetSelectionResult
    assert intent_module.IntentLLMResult is IntentLLMResult
    assert target_module.TargetSelectionResult is TargetSelectionResult
    assert calls_module.StructuredCallResult is StructuredCallResult
