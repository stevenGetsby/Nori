"""Compatibility helpers shared by Nori runtime modules."""
from __future__ import annotations

import inspect
from dataclasses import dataclass as _stdlib_dataclass
from dataclasses import field
from typing import Any, Callable


_DATACLASS_SUPPORTS_SLOTS = "slots" in inspect.signature(_stdlib_dataclass).parameters


def dataclass(_cls: type | None = None, **kwargs: Any) -> Callable[[type], type] | type:
    """Version-tolerant dataclass decorator.

    The project targets Python 3.10+ semantics in code, but some local agent
    environments still run Python 3.9 where ``dataclasses.dataclass`` rejects
    ``slots=True``. Preserve slots where supported and degrade gracefully where
    they are not.
    """
    if not _DATACLASS_SUPPORTS_SLOTS:
        kwargs.pop("slots", None)
    return _stdlib_dataclass(_cls, **kwargs)


__all__ = ["dataclass", "field"]
