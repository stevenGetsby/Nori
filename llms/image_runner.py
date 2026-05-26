"""Image generation execution for the LLM gateway."""
from __future__ import annotations

import time
from typing import Any, Callable

from .capabilities import ensure_image_capability
from .client import build_client_bundle, validate_api_key
from .config import get_active
from .image_inputs import load_image_bytes
from .image_providers import (
    image_google,
    image_openai_edit,
    image_relay_generate_with_references,
)
from .request_params import merge_image_kwargs
from .results import collect_image_results, ensure_image_results
from .telemetry import emit_telemetry


def image_outputs(
    prompt: str,
    *,
    usage: str = "image",
    size: str | None = None,
    reference_images: list[Any] | None = None,
    _get_active: Callable[[str], Any] | None = None,
    _build_client_bundle: Callable[[Any, str], Any] | None = None,
    _image_google_func: Callable[..., list[str]] | None = None,
    _image_openai_edit_func: Callable[..., list[str]] | None = None,
    _image_relay_generate_with_references_func: Callable[..., list[str]] | None = None,
    **kwargs: Any,
) -> list[str]:
    """Run an image request and return normalized image outputs."""
    ref_bytes_list: list[bytes] = []
    if reference_images:
        ref_bytes_list = [load_image_bytes(item) for item in reference_images]
        ref_bytes_list = [b for b in ref_bytes_list if b]

    active_model = (_get_active or get_active)(usage)
    started = time.perf_counter()
    try:
        ensure_image_capability(active_model, ref_bytes_list)

        if active_model.provider_id == "google":
            api_key = validate_api_key(active_model, usage)
            google_func = _image_google_func or image_google
            results = google_func(prompt, active_model, size, ref_bytes_list, api_key=api_key)
            ensure_image_results(results, active_model)
            emit_telemetry("image", usage, active_model, started)
            return results

        bundle = (_build_client_bundle or build_client_bundle)(active_model, usage)
        request_kwargs = merge_image_kwargs(bundle.model, kwargs)
        if size is None and bundle.model.resolution_options:
            size = bundle.model.resolution_options[0]
        if active_model.provider_id == "relay":
            request_kwargs.setdefault("response_format", "b64_json")

        if ref_bytes_list and active_model.provider_id == "relay":
            relay_func = _image_relay_generate_with_references_func or image_relay_generate_with_references
            results = relay_func(bundle, prompt, ref_bytes_list, size, request_kwargs)
        elif ref_bytes_list:
            edit_func = _image_openai_edit_func or image_openai_edit
            results = edit_func(bundle, prompt, ref_bytes_list, size, request_kwargs)
        else:
            resp = bundle.client.images.generate(
                model=bundle.model_id,
                prompt=prompt,
                size=size,
                **request_kwargs,
            )
            results = collect_image_results(resp)
    except Exception as exc:  # noqa: BLE001
        emit_telemetry("image", usage, active_model, started, error=exc)
        raise
    emit_telemetry("image", usage, active_model, started)
    return results
