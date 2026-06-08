"""Small helper for package-root lazy public exports."""
from __future__ import annotations

from importlib import import_module
from typing import Mapping


def lazy_export(package_name: str, export_map: Mapping[str, str | None], name: str):
    """Resolve a lazily exported object from a package root.

    Package roots use this when eager imports would create domain-module cycles.
    The map values are relative module paths inside ``package_name``. Use
    ``None`` when the public export is the submodule itself.
    """
    if name not in export_map:
        raise AttributeError(f"module {package_name!r} has no attribute {name!r}")
    module_path = export_map[name] or name
    module = import_module(f"{package_name}.{module_path}")
    if export_map[name] is None:
        return module
    return getattr(module, name)


__all__ = ["lazy_export"]
