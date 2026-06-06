import json

from nori.shared import (
    attach_llm_error,
    call_stage_json,
    call_stage_messages_json,
    try_stage_json,
    try_stage_messages_json,
    write_stage_log,
)
from nori.shared.case_log import write_stage_log as direct_write_stage_log
from nori.shared.llm_json import attach_llm_error as direct_attach_llm_error
from nori.shared.llm_json import call_stage_json as direct_call_stage_json
from nori.shared.llm_json import call_stage_messages_json as direct_call_stage_messages_json
from nori.shared.llm_json import try_stage_json as direct_try_stage_json
from nori.shared.llm_json import try_stage_messages_json as direct_try_stage_messages_json


class StageTestError(RuntimeError):
    pass


def test_shared_utils_reexports_case_log_helper():
    import nori.shared as shared

    assert write_stage_log is direct_write_stage_log
    assert write_stage_log.__module__ == "nori.shared.case_log"
    assert attach_llm_error is direct_attach_llm_error
    assert call_stage_json is direct_call_stage_json
    assert call_stage_messages_json is direct_call_stage_messages_json
    assert try_stage_json is direct_try_stage_json
    assert try_stage_messages_json is direct_try_stage_messages_json
    for removed_name in [
        "write_agent_log",
        "call_agent_json",
        "call_agent_messages_json",
        "load_note_skills",
        "note_skill_fixture",
        "try_agent_json",
        "try_agent_messages_json",
        "write_note_skill_fixture",
    ]:
        assert not hasattr(shared, removed_name)


def test_write_stage_log_keeps_input_output_and_config(tmp_path):
    path = write_stage_log(
        stage="account_planner",
        case="unit case",
        input_data={"text": "hello"},
        output_data={"tags": {"platform": "小红书"}},
        config={"mode": "test"},
        log_dir=tmp_path,
    )

    assert path.exists()
    assert path.name.startswith("account_planner_unit_case_")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["stage"] == "account_planner"
    assert data["case"] == "unit case"
    assert data["config"] == {"mode": "test"}
    assert data["input"] == {"text": "hello"}
    assert data["output"]["tags"]["platform"] == "小红书"


def test_call_stage_json_routes_through_injected_chat_json():
    sentinel_chat = object()
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return {"ok": True}

    data = call_stage_json(
        system="system prompt",
        user="user prompt",
        timeout=7,
        error_type=StageTestError,
        chat_func=sentinel_chat,
        chat_json_func=fake_chat_json,
    )

    assert data == {"ok": True}
    assert calls[0]["messages"] == [
        {"role": "system", "content": "system prompt"},
        {"role": "user", "content": "user prompt"},
    ]
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["timeout"] == 7
    assert calls[0]["kwargs"]["json_mode"] is True


def test_call_stage_json_translates_parse_errors():
    import llms

    def fake_chat_json(*args, **kwargs):
        raise llms.ChatJSONError("bad json", "not json")

    try:
        call_stage_json(
            system="system",
            user="user",
            timeout=1,
            error_type=StageTestError,
            chat_json_func=fake_chat_json,
        )
    except StageTestError as exc:
        assert "无法解析为 JSON" in str(exc)
        assert "not json" in str(exc)
    else:
        raise AssertionError("expected StageTestError")


def test_call_stage_json_retries_parse_errors_with_larger_token_budget():
    import llms

    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):  # noqa: ARG001
        calls.append(dict(kwargs))
        if len(calls) == 1:
            raise llms.ChatJSONError("bad json", '{"items": [1, 2')
        return {"ok": True}

    data = call_stage_json(
        system="system",
        user="user",
        timeout=1,
        error_type=StageTestError,
        chat_json_func=fake_chat_json,
    )

    assert data == {"ok": True}
    assert calls[0]["json_mode"] is True
    assert "max_tokens" not in calls[0]
    assert calls[1]["max_tokens"] == 8192


def test_call_stage_messages_json_supports_prebuilt_multimodal_messages():
    sentinel_chat = object()
    messages = [
        {"role": "system", "content": "vision json"},
        {"role": "user", "content": [{"type": "text", "text": "tag"}, {"type": "image_url", "image_url": {"url": "data:"}}]},
    ]
    calls: list[dict] = []

    def fake_chat_json(messages_arg, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages_arg, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return {"vision_roles": ["product_shot"]}

    data = call_stage_messages_json(
        messages=messages,
        usage="vision",
        timeout=11,
        error_type=StageTestError,
        chat_func=sentinel_chat,
        chat_json_func=fake_chat_json,
    )

    assert data == {"vision_roles": ["product_shot"]}
    assert calls[0]["messages"] == messages
    assert calls[0]["usage"] == "vision"
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["timeout"] == 11
    assert calls[0]["kwargs"]["json_mode"] is True


def test_try_stage_json_returns_data_and_no_error():
    sentinel_chat = object()
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return {"planned": True}

    data, error = try_stage_json(
        system="system",
        user="user",
        chat_func=sentinel_chat,
        chat_json_func=fake_chat_json,
    )

    assert data == {"planned": True}
    assert error is None
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["json_mode"] is True


def test_try_stage_messages_json_supports_prebuilt_multimodal_messages():
    sentinel_chat = object()
    messages = [
        {"role": "system", "content": "vision fallback json"},
        {"role": "user", "content": [{"type": "text", "text": "tag"}, {"type": "image_url", "image_url": {"url": "data:"}}]},
    ]
    calls: list[dict] = []

    def fake_chat_json(messages_arg, *, usage="llm", _chat=None, **kwargs):
        calls.append({"messages": messages_arg, "usage": usage, "_chat": _chat, "kwargs": kwargs})
        return {"fallback_plan": True}

    data, error = try_stage_messages_json(
        messages=messages,
        usage="vision",
        timeout=11,
        chat_func=sentinel_chat,
        chat_json_func=fake_chat_json,
    )

    assert data == {"fallback_plan": True}
    assert error is None
    assert calls[0]["messages"] == messages
    assert calls[0]["usage"] == "vision"
    assert calls[0]["_chat"] is sentinel_chat
    assert calls[0]["kwargs"]["timeout"] == 11
    assert calls[0]["kwargs"]["json_mode"] is True


def test_try_stage_json_returns_redacted_error_metadata():
    import llms

    def fake_chat_json(*args, **kwargs):
        raise llms.ChatJSONError("bad json", "not json")

    data, error = try_stage_json(
        system="system",
        user="user",
        chat_json_func=fake_chat_json,
    )

    assert data is None
    assert error == {
        "reason": "parse_error",
        "error_type": "ChatJSONError",
        "preview": "not json",
    }


def test_try_stage_json_classifies_empty_json_response():
    import llms

    def fake_chat_json(*args, **kwargs):
        raise llms.ChatJSONError("empty", "   ")

    data, error = try_stage_json(
        system="system",
        user="user",
        chat_json_func=fake_chat_json,
    )

    assert data is None
    assert error == {
        "reason": "empty_response",
        "error_type": "ChatJSONError",
        "preview": "   ",
    }


def test_try_stage_messages_json_classifies_empty_json_response():
    import llms

    def fake_chat_json(*args, **kwargs):
        raise llms.ChatJSONError("empty", "   ")

    data, error = try_stage_messages_json(
        messages=[{"role": "user", "content": "json"}],
        chat_json_func=fake_chat_json,
    )

    assert data is None
    assert error == {
        "reason": "empty_response",
        "error_type": "ChatJSONError",
        "preview": "   ",
    }


def test_attach_llm_error_uses_shared_field_shape():
    metadata = {"planner": "rule_fallback"}

    attach_llm_error(
        metadata,
        "calendar_planner",
        {"reason": "api_error", "error_type": "RuntimeError", "message": "failed"},
    )

    assert metadata == {
        "planner": "rule_fallback",
        "llm_error": {
            "stage": "calendar_planner",
            "reason": "api_error",
            "error_type": "RuntimeError",
            "message": "failed",
        },
    }


def test_attach_llm_error_keeps_caller_stage_authoritative():
    metadata = {}

    attach_llm_error(metadata, "xhs_note_analyzer", {"stage": "wrong_stage", "reason": "api_error"})

    assert metadata["llm_error"] == {
        "stage": "xhs_note_analyzer",
        "reason": "api_error",
    }
