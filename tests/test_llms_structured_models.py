from __future__ import annotations

import llms
import llms.intent_extractor as intent_module
import llms.structured_calls as calls_module
import llms.structured_models as models
import llms.target_selector as target_module


def test_structured_result_models_live_in_dedicated_boundary():
    intent = models.IntentLLMResult(fields={"topic": "通勤香薰"})
    target = models.TargetSelectionResult(target_selector="cover#1")
    call = models.StructuredCallResult(data={"ok": True})

    assert intent.ok is True
    assert target.ok is True
    assert call.ok is True
    assert models.IntentLLMResult(error="parse_error").ok is False
    assert models.TargetSelectionResult(error="missing_selector").ok is False
    assert models.StructuredCallResult(error="api_error:RuntimeError").ok is False


def test_structured_result_model_import_identities_stay_compatible():
    assert llms.IntentLLMResult is models.IntentLLMResult
    assert llms.TargetSelectionResult is models.TargetSelectionResult
    assert intent_module.IntentLLMResult is models.IntentLLMResult
    assert target_module.TargetSelectionResult is models.TargetSelectionResult
    assert calls_module.StructuredCallResult is models.StructuredCallResult
