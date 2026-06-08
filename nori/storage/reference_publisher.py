"""Publish local reference images so external image models can fetch them."""
from __future__ import annotations

import mimetypes
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from nori.shared.image_io import image_to_bytes

from .paths import DEFAULT_REFERENCE_PREFIX, reference_image_key, slug
from .volcengine_tos import ObjectStoreError, StoredObject, VolcengineTOSObjectStore


@dataclass(frozen=True)
class PublishedReference:
    original_path: str
    input_value: bytes | str
    url: str = ""
    public_url: str = ""
    key: str = ""
    uploaded: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "original_path": self.original_path,
            "url": self.url,
            "public_url": self.public_url,
            "url_public": self.public_url,
            "key": self.key,
            "uploaded": self.uploaded,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class PublishedReferences:
    items: list[PublishedReference] = field(default_factory=list)

    @property
    def inputs(self) -> list[bytes | str]:
        return [item.input_value for item in self.items if item.input_value]

    @property
    def uploads(self) -> list[PublishedReference]:
        return [item for item in self.items if item.uploaded]

    def to_extra(self) -> dict[str, Any]:
        return {
            "reference_images_uploaded": bool(self.uploads),
            "reference_upload_count": len(self.uploads),
            "reference_object_keys": [item.key for item in self.uploads],
            "reference_public_urls": [item.public_url for item in self.uploads],
            "reference_items": [item.to_dict() for item in self.items],
        }


class ReferenceImagePublisher:
    """Convert local reference image paths into model-fetchable HTTPS URLs."""

    def __init__(
        self,
        *,
        store: Any | None = None,
        prefix: str = DEFAULT_REFERENCE_PREFIX,
        enabled: bool = False,
    ) -> None:
        self.store = store
        self.prefix = prefix
        self.enabled = enabled and store is not None

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> "ReferenceImagePublisher":
        store = VolcengineTOSObjectStore.from_env(environ)
        prefix = ""
        if environ is None:
            import os

            prefix = os.environ.get("NORI_OSS_PREFIX", "")
        else:
            prefix = environ.get("NORI_OSS_PREFIX", "")
        return cls(store=store, prefix=prefix or DEFAULT_REFERENCE_PREFIX, enabled=store is not None)

    @classmethod
    def disabled(cls) -> "ReferenceImagePublisher":
        return cls(enabled=False)

    def publish_paths(
        self,
        paths: list[str],
        *,
        project: str = "",
        session: str = "",
        now: datetime | None = None,
        public_url_map: dict[str, str] | None = None,
    ) -> PublishedReferences:
        items = [
            self.publish_path(path, project=project, session=session, now=now, public_url_map=public_url_map)
            for path in paths
            if path
        ]
        return PublishedReferences(items=items)

    def publish_path(
        self,
        path: str,
        *,
        project: str = "",
        session: str = "",
        now: datetime | None = None,
        public_url_map: dict[str, str] | None = None,
    ) -> PublishedReference:
        if path.startswith(("http://", "https://")):
            return PublishedReference(original_path=path, input_value=path, url=path, public_url=path, reason="remote")
        mapped_url = _public_url_for_path(path, public_url_map)
        if mapped_url:
            return PublishedReference(
                original_path=path,
                input_value=mapped_url,
                url=mapped_url,
                public_url=mapped_url,
                uploaded=True,
                reason="public_url_map",
            )
        if not self.enabled:
            raw = image_to_bytes(path)
            return PublishedReference(original_path=path, input_value=raw, reason="local_bytes")
        raw = image_to_bytes(path)
        if not raw:
            return PublishedReference(original_path=path, input_value=b"", reason="unreadable")
        content_type = image_content_type(path, raw)
        key = reference_image_key(
            prefix=self.prefix,
            project=project or "nori",
            session=session or "session",
            source_path=path,
            payload=raw,
            content_type=content_type,
            now=now,
        )
        stored: StoredObject = self.store.put_bytes(key=key, payload=raw, content_type=content_type)
        return PublishedReference(
            original_path=path,
            input_value=stored.url,
            url=stored.url,
            public_url=stored.public_url,
            key=stored.key,
            uploaded=True,
            reason="uploaded",
        )


def image_content_type(path: str, raw: bytes) -> str:
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if raw.startswith(b"\x89PNG"):
        return "image/png"
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    guessed, _ = mimetypes.guess_type(Path(path).name)
    return guessed if guessed and guessed.startswith("image/") else "image/png"


def reference_publish_context(intent: dict[str, Any], out_dir: str | Path) -> dict[str, str]:
    """Derive storage path context without requiring every caller to know OSS."""
    raw_project = (
        intent.get("project_id")
        or intent.get("project_name")
        or (intent.get("content_design_spec") or {}).get("task_id")
        or "nori"
    )
    raw_session = (
        intent.get("session_id")
        or intent.get("run_id")
        or intent.get("case_id")
        or Path(out_dir).resolve().parent.name
        or "session"
    )
    return {"project": slug(str(raw_project)), "session": slug(str(raw_session))}


def _public_url_for_path(path: str, public_url_map: dict[str, str] | None) -> str:
    if not isinstance(public_url_map, dict) or not public_url_map:
        return ""
    candidates = [path]
    try:
        candidates.append(str(Path(path).resolve()))
    except Exception:  # noqa: BLE001
        pass
    for key in candidates:
        value = str(public_url_map.get(key) or "").strip()
        if value.startswith(("http://", "https://")):
            return value
    return ""


__all__ = [
    "ObjectStoreError",
    "PublishedReference",
    "PublishedReferences",
    "ReferenceImagePublisher",
    "image_content_type",
    "reference_publish_context",
]
