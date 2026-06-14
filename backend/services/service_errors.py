"""Shared error mapping for backend route-facing services."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from ..contracts import ApiError


@contextmanager
def map_service_errors(
    *,
    file_not_found_status_code: int = 404,
    value_error_status_code: int = 400,
) -> Iterator[None]:
    """Map domain/storage exceptions to API errors at service boundaries."""

    try:
        yield
    except FileNotFoundError as exc:
        raise ApiError(str(exc), status_code=file_not_found_status_code) from exc
    except ValueError as exc:
        raise ApiError(str(exc), status_code=value_error_status_code) from exc
