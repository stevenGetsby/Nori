"""Language-model client built on LangChain chat adapters."""
from __future__ import annotations

import time
from typing import Any, Callable

from langchain_core.output_parsers import JsonOutputParser

from .capabilities import ensure_chat_capability, normalize_chat_messages
from .client import build_client_bundle, get_async_chat_model, get_chat_model
from .telemetry import emit_telemetry
from nori.core.contracts import ChatJSONError, ChatResultError


class LanguageModelClient:
    """Text/vision LLM gateway using LangChain chat adapters."""

    def __init__(
        self,
        *,
        chat_model_factory: Callable[[str], Any] = get_chat_model,
        async_chat_model_factory: Callable[[str], Any] = get_async_chat_model,
        chat_completion_client_factory: Callable[[Any, str], Any] = build_client_bundle,
    ) -> None:
        self._chat_model_factory = chat_model_factory
        self._async_chat_model_factory = async_chat_model_factory
        self._chat_completion_client_factory = chat_completion_client_factory

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        **kwargs: Any,
    ) -> str:
        bundle = self._chat_model_factory(usage)
        params = self._merge_chat_kwargs(bundle.model, kwargs)
        normalized_messages = normalize_chat_messages(messages)
        started = time.perf_counter()
        try:
            ensure_chat_capability(bundle.model, normalized_messages, usage)
            resp = bundle.client.invoke(normalized_messages, **params)
            text = self._extract_chat_text(resp, bundle.model)
        except Exception as exc:  # noqa: BLE001
            emit_telemetry("chat", usage, bundle.model, started, error=exc)
            raise
        emit_telemetry("chat", usage, bundle.model, started)
        return text

    async def achat(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        **kwargs: Any,
    ) -> str:
        bundle = self._async_chat_model_factory(usage)
        params = self._merge_chat_kwargs(bundle.model, kwargs)
        normalized_messages = normalize_chat_messages(messages)
        started = time.perf_counter()
        try:
            ensure_chat_capability(bundle.model, normalized_messages, usage)
            resp = await bundle.client.ainvoke(normalized_messages, **params)
            text = self._extract_chat_text(resp, bundle.model)
        except Exception as exc:  # noqa: BLE001
            emit_telemetry("achat", usage, bundle.model, started, error=exc)
            raise
        emit_telemetry("achat", usage, bundle.model, started)
        return text

    def chat_json(
        self,
        messages: list[dict[str, Any]],
        *,
        usage: str = "llm",
        schema: Any | None = None,
        structured_method: str | None = None,
        structured_strict: bool | None = None,
        json_mode: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        self._reject_removed_chat_json_kwargs(kwargs)
        if "strict" in kwargs:
            structured_strict = kwargs.pop("strict")

        bundle = self._chat_model_factory(usage)
        params = self._merge_chat_kwargs(bundle.model, kwargs)
        params.pop("response_format", None)
        normalized_messages = normalize_chat_messages(messages)
        method = self._structured_output_method(
            schema=schema,
            json_mode=json_mode,
            structured_method=structured_method,
        )
        started = time.perf_counter()
        try:
            ensure_chat_capability(bundle.model, normalized_messages, usage)
            structured_kwargs = {
                "method": method,
                "include_raw": True,
                **params,
            }
            if structured_strict is not None:
                structured_kwargs["strict"] = structured_strict
            try:
                structured_model = bundle.client.with_structured_output(
                    schema,
                    **structured_kwargs,
                )
                result = structured_model.invoke(normalized_messages)
                data = self._extract_structured_json_object(result)
            except Exception as exc:  # noqa: BLE001
                if not self._is_openai_raw_response_parse_adapter_error(exc):
                    raise
                data = self._chat_json_via_direct_json_mode(
                    self._chat_completion_client_factory(bundle.model, usage).client,
                    normalized_messages,
                    bundle.model,
                    params,
                )
        except Exception as exc:  # noqa: BLE001
            emit_telemetry("chat_json", usage, bundle.model, started, error=exc)
            raise
        emit_telemetry("chat_json", usage, bundle.model, started)
        return data

    @staticmethod
    def _reject_removed_chat_json_kwargs(kwargs: dict[str, Any]) -> None:
        for name in ("_chat", "chat_func", "retry_without_response_format"):
            if name in kwargs:
                raise TypeError(f"chat_json no longer accepts legacy parameter {name!r}")

    @staticmethod
    def _structured_output_method(
        *,
        schema: Any | None,
        json_mode: bool,
        structured_method: str | None,
    ) -> str:
        if structured_method:
            allowed = {"function_calling", "json_mode", "json_schema"}
            if structured_method not in allowed:
                raise ValueError(f"Unsupported structured_method: {structured_method}")
            return structured_method
        if json_mode or schema is None:
            return "json_mode"
        return "json_schema"

    @staticmethod
    def _extract_structured_json_object(result: Any) -> dict[str, Any]:
        if isinstance(result, dict) and (
            "parsed" in result or "parsing_error" in result or "raw" in result
        ):
            raw = LanguageModelClient._structured_raw_text(result.get("raw"))
            parsing_error = result.get("parsing_error")
            if parsing_error is not None:
                raise ChatJSONError(
                    f"LLM 输出无法解析为 JSON object: {parsing_error}",
                    raw,
                )
            data = result.get("parsed")
        else:
            raw = ""
            data = result

        data = LanguageModelClient._structured_data_to_dict(data)
        if not isinstance(data, dict):
            raise ChatJSONError(f"LLM 输出 JSON 不是 object: {type(data).__name__}", raw)
        return data

    @staticmethod
    def _chat_json_via_direct_json_mode(
        chat_completion_client: Any,
        messages: list[Any],
        model: Any,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        fallback_params = {
            **params,
            "response_format": {"type": "json_object"},
        }
        resp = chat_completion_client.chat.completions.create(
            model=model.model_id,
            messages=messages,
            **fallback_params,
        )
        raw = LanguageModelClient._extract_chat_completion_text(resp, model)
        try:
            data = JsonOutputParser().parse(raw)
        except Exception as exc:  # noqa: BLE001
            raise ChatJSONError(f"LLM 输出无法解析为 JSON object: {exc}", raw) from exc
        data = LanguageModelClient._structured_data_to_dict(data)
        if not isinstance(data, dict):
            raise ChatJSONError(f"LLM 输出 JSON 不是 object: {type(data).__name__}", raw)
        return data

    @staticmethod
    def _extract_chat_completion_text(resp: Any, model: Any) -> str:
        completions = getattr(resp, "choices", None) or []
        if not completions:
            raise ChatResultError(f"文本模型未返回可用文本: {getattr(model, 'key', '')}")
        first = completions[0]
        message = LanguageModelClient._get_field(first, "message", {})
        content = LanguageModelClient._get_field(message, "content", None)
        text = LanguageModelClient._normalize_chat_content(content).strip()
        if text:
            return text
        raise ChatResultError(f"文本模型未返回可用文本: {getattr(model, 'key', '')}")

    @staticmethod
    def _is_openai_raw_response_parse_adapter_error(exc: Exception) -> bool:
        message = str(exc)
        return (
            isinstance(exc, AttributeError)
            and "CompletionsWithRawResponse" in message
            and "parse" in message
        )

    @staticmethod
    def _structured_data_to_dict(data: Any) -> Any:
        if hasattr(data, "model_dump"):
            return data.model_dump()
        if hasattr(data, "dict"):
            return data.dict()
        return data

    @staticmethod
    def _structured_raw_text(raw: Any) -> str:
        if raw is None:
            return ""
        content = LanguageModelClient._get_field(raw, "content", raw)
        return LanguageModelClient._normalize_chat_content(content)

    @staticmethod
    def _merge_chat_kwargs(model: Any, kwargs: dict) -> dict:
        out = dict(kwargs)
        if model.temperature_fixed is not None:
            out["temperature"] = model.temperature_fixed
        max_output_param = LanguageModelClient._max_output_param_name(model)
        if max_output_param == "max_completion_tokens":
            if "max_completion_tokens" in out:
                out.pop("max_tokens", None)
            elif "max_tokens" in out:
                out["max_completion_tokens"] = out.pop("max_tokens")
            elif model.max_output:
                out["max_completion_tokens"] = model.max_output
        else:
            if "max_tokens" in out:
                out.pop("max_completion_tokens", None)
            elif "max_completion_tokens" in out:
                out["max_tokens"] = out.pop("max_completion_tokens")
            elif model.max_output:
                out["max_tokens"] = model.max_output
        LanguageModelClient._merge_model_extra_body(out, model)
        return out

    @staticmethod
    def _extract_chat_text(resp: Any, model: Any) -> str:
        text = LanguageModelClient._normalize_chat_content(getattr(resp, "content", None)).strip()
        if text:
            return text
        raise ChatResultError(f"文本模型未返回可用文本: {getattr(model, 'key', '')}")

    @staticmethod
    def _normalize_chat_content(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                text = LanguageModelClient._get_field(item, "text", None)
                if text is None and LanguageModelClient._get_field(item, "type", "") == "text":
                    text = LanguageModelClient._get_field(item, "content", None)
                if text is not None:
                    parts.append(str(text))
            return "\n".join(parts)
        return str(content or "")

    @staticmethod
    def _merge_model_extra_body(out: dict, model: Any) -> None:
        model_extra_body = getattr(model, "extra_body", {}) or {}
        if not model_extra_body:
            return
        caller_extra_body = out.get("extra_body") if isinstance(out.get("extra_body"), dict) else {}
        extra_body = dict(caller_extra_body)
        extra_body.update(model_extra_body)
        out["extra_body"] = extra_body

    @staticmethod
    def _max_output_param_name(model: Any) -> str:
        if model.model_id.lower().startswith("gpt-5"):
            return "max_completion_tokens"
        return "max_tokens"

    @staticmethod
    def _get_field(value: Any, key: str, default: Any = None) -> Any:
        if isinstance(value, dict):
            return value.get(key, default)
        return getattr(value, key, default)
