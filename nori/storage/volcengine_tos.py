"""Volcengine TOS object store adapter."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


DEFAULT_TOS_ENDPOINT = "tos-cn-beijing.volces.com"
DEFAULT_TOS_REGION = "cn-beijing"
DEFAULT_TOS_BUCKET = "nori"
DEFAULT_SIGNED_URL_EXPIRES = 24 * 60 * 60


class ObjectStoreError(RuntimeError):
    """Raised when object storage cannot publish a runtime asset."""


@dataclass(frozen=True)
class StoredObject:
    bucket: str
    key: str
    url: str
    content_type: str
    size: int
    signed: bool = True
    expires_in: int = DEFAULT_SIGNED_URL_EXPIRES

    @property
    def public_url(self) -> str:
        return self.url.split("?", 1)[0]


@dataclass(frozen=True)
class VolcengineTOSConfig:
    access_key_id: str
    secret_access_key: str
    bucket: str = DEFAULT_TOS_BUCKET
    endpoint: str = DEFAULT_TOS_ENDPOINT
    region: str = DEFAULT_TOS_REGION
    public_base_url: str = ""
    signed_url_expires: int = DEFAULT_SIGNED_URL_EXPIRES

    @property
    def configured(self) -> bool:
        return bool(self.access_key_id and self.secret_access_key and self.bucket)


class VolcengineTOSObjectStore:
    """Small wrapper around the official TOS SDK.

    Credentials are intentionally environment-driven so AK/SK never need to
    live in repository files.
    """

    def __init__(self, config: VolcengineTOSConfig) -> None:
        if not config.configured:
            raise ObjectStoreError("Volcengine TOS config is incomplete")
        self.config = config
        try:
            import tos
            from tos.enum import HttpMethodType
        except Exception as exc:  # noqa: BLE001
            raise ObjectStoreError("Python package `tos` is required for Volcengine TOS uploads") from exc
        self._tos = tos
        self._http_method_get = HttpMethodType.Http_Method_Get
        self._client = tos.TosClientV2(
            config.access_key_id,
            config.secret_access_key,
            config.endpoint,
            config.region,
        )

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> "VolcengineTOSObjectStore | None":
        env = environ or os.environ
        config = VolcengineTOSConfig(
            access_key_id=_first_env(env, "NORI_OSS_ACCESS_KEY_ID", "TOS_ACCESS_KEY_ID", "VOLCENGINE_ACCESS_KEY_ID"),
            secret_access_key=_first_env(
                env,
                "NORI_OSS_SECRET_ACCESS_KEY",
                "TOS_SECRET_ACCESS_KEY",
                "VOLCENGINE_SECRET_ACCESS_KEY",
            ),
            bucket=_first_env(env, "NORI_OSS_BUCKET", "TOS_BUCKET") or DEFAULT_TOS_BUCKET,
            endpoint=_first_env(env, "NORI_OSS_ENDPOINT", "TOS_ENDPOINT") or DEFAULT_TOS_ENDPOINT,
            region=_first_env(env, "NORI_OSS_REGION", "TOS_REGION") or DEFAULT_TOS_REGION,
            public_base_url=_first_env(env, "NORI_OSS_PUBLIC_BASE_URL", "TOS_PUBLIC_BASE_URL"),
            signed_url_expires=_positive_int(
                _first_env(env, "NORI_OSS_SIGNED_URL_EXPIRES", "TOS_SIGNED_URL_EXPIRES"),
                default=DEFAULT_SIGNED_URL_EXPIRES,
            ),
        )
        if not config.configured:
            return None
        return cls(config)

    def put_bytes(self, *, key: str, payload: bytes, content_type: str) -> StoredObject:
        if not payload:
            raise ObjectStoreError(f"refusing to upload empty object: {key}")
        try:
            self._client.put_object(
                self.config.bucket,
                key,
                content=payload,
                content_type=content_type or "application/octet-stream",
            )
        except Exception as exc:  # noqa: BLE001
            raise ObjectStoreError(f"TOS upload failed for {key}: {type(exc).__name__}: {exc}") from exc
        return StoredObject(
            bucket=self.config.bucket,
            key=key,
            url=self._object_url(key),
            content_type=content_type,
            size=len(payload),
            signed=not bool(self.config.public_base_url),
            expires_in=self.config.signed_url_expires,
        )

    def _object_url(self, key: str) -> str:
        if self.config.public_base_url:
            return f"{self.config.public_base_url.rstrip('/')}/{key.lstrip('/')}"
        signed = self._client.pre_signed_url(
            self._http_method_get,
            self.config.bucket,
            key,
            expires=self.config.signed_url_expires,
        )
        return str(signed.signed_url)


def _first_env(env: dict[str, str], *names: str) -> str:
    for name in names:
        value = str(env.get(name) or "").strip()
        if value:
            return value
    return ""


def _positive_int(value: Any, *, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


__all__ = [
    "DEFAULT_SIGNED_URL_EXPIRES",
    "DEFAULT_TOS_BUCKET",
    "DEFAULT_TOS_ENDPOINT",
    "DEFAULT_TOS_REGION",
    "ObjectStoreError",
    "StoredObject",
    "VolcengineTOSConfig",
    "VolcengineTOSObjectStore",
]
