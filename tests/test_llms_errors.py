from __future__ import annotations

import llms
import llms.call as call_module
import llms.client as client_module
from nori.core import contracts


def test_public_gateway_errors_share_single_identity():
    assert llms.LLMClientConfigError is contracts.LLMClientConfigError
    assert client_module.LLMClientConfigError is contracts.LLMClientConfigError

    assert llms.ChatJSONError is contracts.ChatJSONError

    assert llms.ChatResultError is contracts.ChatResultError

    assert llms.ChatCapabilityError is contracts.ChatCapabilityError

    assert llms.ImageCapabilityError is contracts.ImageCapabilityError

    assert llms.ImageResultError is contracts.ImageResultError


def test_chat_json_error_preview_stays_on_shared_error_class():
    error = contracts.ChatJSONError("bad json", "x" * 250)

    assert error.raw == "x" * 250
    assert error.preview == "x" * 200
