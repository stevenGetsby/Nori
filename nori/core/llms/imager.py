"""Image-generation client for the LLM gateway."""
from __future__ import annotations

import time
from typing import Any, Callable

from .capabilities import ensure_image_capability
from .client import build_client_bundle, get_active, validate_api_key
from .image_inputs import split_reference_images
from .image_providers import ImageProviders
from .telemetry import emit_telemetry
from nori.core.contracts import ImageCapabilityError


class ImageClient:
    """Image gateway with provider-specific behavior delegated to ImageProviders."""

    def __init__(
        self,
        *,
        active_model_factory: Callable[[str], Any] = get_active,
        client_bundle_factory: Callable[[Any, str], Any] = build_client_bundle,
        providers: ImageProviders | None = None,
    ) -> None:
        self._active_model_factory = active_model_factory
        self._client_bundle_factory = client_bundle_factory
        self.providers = providers or ImageProviders()

    def image(
        self,
        prompt: str,
        *,
        usage: str = "image",
        size: str | None = None,
        reference_images: list[Any] | None = None,
        **kwargs: Any,
    ) -> list[str]:
        ref_bytes_list, ref_urls = split_reference_images(reference_images)

        active_model = self._active_model_factory(usage)
        started = time.perf_counter()
        try:
            ensure_image_capability(active_model, ref_bytes_list, ref_urls)

            if active_model.provider_id == "google":
                api_key = validate_api_key(active_model, usage)
                results = self.providers.google(
                    prompt,
                    active_model,
                    size,
                    ref_bytes_list,
                    api_key=api_key,
                )
                self.providers.ensure_results(results, active_model)
                emit_telemetry("image", usage, active_model, started)
                return results

            bundle = self._client_bundle_factory(active_model, usage)
            request_kwargs = self._merge_image_kwargs(bundle.model, kwargs)
            if size is None and bundle.model.resolution_options:
                size = bundle.model.resolution_options[0]
            if active_model.provider_id == "relay":
                request_kwargs.setdefault("response_format", "b64_json")
                if ref_bytes_list and not ref_urls:
                    raise ImageCapabilityError(
                        "relay image reference generation requires public HTTPS image URLs; "
                        "local files/data-uri/base64 references are rejected by this provider"
                    )

            if (ref_bytes_list or ref_urls) and active_model.provider_id == "relay":
                results = self.providers.relay_generate_with_references(
                    bundle,
                    prompt,
                    ref_bytes_list,
                    size,
                    request_kwargs,
                    ref_urls=ref_urls,
                )
            elif ref_bytes_list:
                results = self.providers.openai_edit(
                    bundle,
                    prompt,
                    ref_bytes_list,
                    size,
                    request_kwargs,
                )
            elif ref_urls:
                raise ImageCapabilityError(
                    f"active image provider {active_model.provider_id!r} does not support URL reference_images"
                )
            else:
                resp = bundle.client.images.generate(
                    model=bundle.model_id,
                    prompt=prompt,
                    size=size,
                    **request_kwargs,
                )
                results = self.providers.collect_results(resp)
        except Exception as exc:  # noqa: BLE001
            emit_telemetry("image", usage, active_model, started, error=exc)
            raise
        emit_telemetry("image", usage, active_model, started)
        return results

    @staticmethod
    def _merge_image_kwargs(model: Any, kwargs: dict) -> dict:
        out = dict(kwargs)
        model_extra_body = getattr(model, "extra_body", {}) or {}
        if not model_extra_body:
            return out
        caller_extra_body = out.get("extra_body") if isinstance(out.get("extra_body"), dict) else {}
        extra_body = dict(caller_extra_body)
        extra_body.update(model_extra_body)
        out["extra_body"] = extra_body
        return out
