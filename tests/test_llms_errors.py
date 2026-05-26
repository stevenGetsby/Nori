from __future__ import annotations

import llms
import llms.call as call_module
import llms.client as client_module
import llms.errors as errors
from nori.core import contracts


def test_public_gateway_errors_share_single_identity():
    assert contracts.LLMClientConfigError is errors.LLMClientConfigError
    assert contracts.ChatJSONError is errors.ChatJSONError
    assert contracts.ChatResultError is errors.ChatResultError
    assert contracts.ChatCapabilityError is errors.ChatCapabilityError
    assert contracts.ImageCapabilityError is errors.ImageCapabilityError
    assert contracts.ImageResultError is errors.ImageResultError

    assert llms.LLMClientConfigError is errors.LLMClientConfigError
    assert client_module.LLMClientConfigError is errors.LLMClientConfigError

    assert llms.ChatJSONError is errors.ChatJSONError
    assert call_module.ChatJSONError is errors.ChatJSONError

    assert llms.ChatResultError is errors.ChatResultError
    assert call_module.ChatResultError is errors.ChatResultError

    assert llms.ChatCapabilityError is errors.ChatCapabilityError
    assert call_module.ChatCapabilityError is errors.ChatCapabilityError

    assert llms.ImageCapabilityError is errors.ImageCapabilityError
    assert call_module.ImageCapabilityError is errors.ImageCapabilityError

    assert llms.ImageResultError is errors.ImageResultError
    assert call_module.ImageResultError is errors.ImageResultError


def test_chat_json_error_preview_stays_on_shared_error_class():
    error = errors.ChatJSONError("bad json", "x" * 250)

    assert error.raw == "x" * 250
    assert error.preview == "x" * 200
