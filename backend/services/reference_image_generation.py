"""Reference-image generation provider checks."""
from __future__ import annotations

from typing import Any

from nori.core import llms

from ..contracts import ReferenceImageGenerationCheckRequest
from ..reference_urls import provider_fetchable_reference_url
from .reference_image_results import _reference_image_generation_check_result


class ReferenceImageGenerationChecker:
    """Checks whether the active image provider accepts provider-fetchable reference images."""

    def check(self, request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        """Verify that the active image provider accepts reference_images."""

        refs = [provider_fetchable_reference_url(str(item or "")) for item in request.reference_images]
        refs = [item for item in refs if item]
        if not refs:
            return _reference_image_generation_check_result(
                ready=False,
                reason="invalid_reference_images",
                prompt=str(request.prompt or ""),
                reference_images=list(request.reference_images or []),
                provider_fetchable_refs=[],
                size=str(request.size or ""),
                metadata=dict(request.metadata or {}),
            )
        prompt = str(request.prompt or "Generate a simple product image using the provided reference image.").strip()
        size = str(request.size or "1024x1024").strip() or "1024x1024"
        try:
            images = llms.image(prompt, usage="image", size=size, reference_images=refs)
        except Exception as exc:  # noqa: BLE001
            return _reference_image_generation_check_result(
                ready=False,
                reason="image_generation_error",
                prompt=prompt,
                reference_images=list(request.reference_images or []),
                provider_fetchable_refs=refs,
                size=size,
                error_type=type(exc).__name__,
                error=str(exc),
                metadata=dict(request.metadata or {}),
            )
        return _reference_image_generation_check_result(
            ready=bool(images),
            reason="image_generation_succeeded" if images else "empty_image_result",
            prompt=prompt,
            reference_images=list(request.reference_images or []),
            provider_fetchable_refs=refs,
            size=size,
            image_count=len(images or []),
            first_image_preview=str(images[0])[:80] if images else "",
            metadata=dict(request.metadata or {}),
        )
