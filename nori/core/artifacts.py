"""Shared base classes for deterministic artifact assemblers."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Iterable

from nori._compat import dataclass, field
from nori.shared.normalization import dedupe_preserve_order


class StableArtifactAssembler:
    """Base behavior for assemblers that produce stable local artifacts."""

    default_slug = "artifact"

    def slug(self, value: str) -> str:
        text = re.sub(r"[^\w\-]+", "_", value.strip())
        return text[:80].strip("_") or self.default_slug

    def dedupe(self, values: Iterable[str]) -> list[str]:
        return dedupe_preserve_order(value for value in values if value)


@dataclass(slots=True)
class StoredArtifact:
    """One persisted stage artifact in a resumable local run."""

    stage: str
    path: Path
    input_refs: list[str] = field(default_factory=list)

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def to_manifest_row(self, root: Path) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(root)),
            "input_refs": list(self.input_refs),
        }


class ArtifactStore:
    """Small JSON checkpoint store for stage-by-stage resumable runs."""

    def __init__(self, root: str | Path, *, manifest_name: str = "manifest.json") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.root / manifest_name

    def path_for(self, stage: str) -> Path:
        return self.root / f"{self.slug(stage)}.json"

    def save_stage(
        self,
        stage: str,
        data: Any,
        *,
        input_refs: list[str] | None = None,
    ) -> StoredArtifact:
        artifact = StoredArtifact(stage=stage, path=self.path_for(stage), input_refs=list(input_refs or []))
        artifact.path.write_text(
            json.dumps(_jsonable(data), ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        self._write_manifest_row(artifact)
        return artifact

    def load_stage(self, stage: str) -> Any:
        return json.loads(self.path_for(stage).read_text(encoding="utf-8"))

    def has_stage(self, stage: str) -> bool:
        return self.path_for(stage).is_file()

    def get_or_build(self, stage: str, builder: Callable[[], Any], *, input_refs: list[str] | None = None) -> Any:
        if self.has_stage(stage):
            return self.load_stage(stage)
        value = builder()
        self.save_stage(stage, value, input_refs=input_refs)
        return value

    def manifest(self) -> dict[str, Any]:
        if not self.manifest_path.is_file():
            return {"artifacts": {}}
        data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"artifacts": {}}

    def _write_manifest_row(self, artifact: StoredArtifact) -> None:
        manifest = self.manifest()
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
        artifacts[artifact.stage] = artifact.to_manifest_row(self.root)
        manifest["artifacts"] = artifacts
        self.manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def slug(value: str) -> str:
        text = re.sub(r"[^\w\-]+", "_", str(value or "").strip())
        return text[:80].strip("_") or "artifact"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


__all__ = ["ArtifactStore", "StableArtifactAssembler", "StoredArtifact"]
