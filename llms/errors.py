"""Stable exception types for the project LLM gateway."""
from __future__ import annotations


class LLMClientConfigError(ValueError):
    """Raised when an active model cannot build a provider client."""


class ChatJSONError(ValueError):
    """Raised when a chat response cannot be parsed as a JSON object."""

    def __init__(self, message: str, raw: str | None = None) -> None:
        super().__init__(message)
        self.raw = raw or ""

    @property
    def preview(self) -> str:
        return self.raw[:200]


class ChatResultError(ValueError):
    """Raised when a chat provider response contains no usable text content."""


class ChatCapabilityError(ValueError):
    """Raised when a chat request asks for unsupported model capabilities."""


class ImageCapabilityError(ValueError):
    """Raised when an image request asks for unsupported model capabilities."""


class ImageResultError(ValueError):
    """Raised when an image provider response contains no usable image result."""
