"""Small helper for package-root lazy public exports."""
from __future__ import annotations

from importlib import import_module
from typing import Mapping


def lazy_export(package_name: str, export_map: Mapping[str, str], name: str):
    """Resolve a lazily exported object from a package root.

    Package roots use this when eager imports would create domain-module cycles.
    The map values are relative module paths inside ``package_name``.
    """
    module_path = export_map.get(name)
    if module_path is None:
        raise AttributeError(f"module {package_name!r} has no attribute {name!r}")
    module = import_module(f"{package_name}.{module_path}")
    return getattr(module, name)


__all__ = ["lazy_export"]
