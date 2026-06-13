"""Reference-image publishing strategies."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from nori.storage import ObjectStoreError

from ..contracts import ApiError, AssetReferencePublishRequest, ReferencePublishCheckRequest
from ..reference_urls import provider_fetchable_reference_url
from .reference_image_results import _asset_publish_result, _reference_publish_check_result
from .session_assets import backend_asset_public_reference_url, is_remote_url


class ReferencePublishDiagnostic:
    """Verifies that the configured publisher can produce provider-fetchable reference URLs."""

    def __init__(self, reference_publisher: Any) -> None:
        self.reference_publisher = reference_publisher

    def check(self, request: ReferencePublishCheckRequest) -> dict[str, Any]:
        """Verify the configured reference publisher using a backend-owned tiny image."""

        with tempfile.TemporaryDirectory(prefix="nori_reference_publish_check_") as tmp_dir:
            path = Path(tmp_dir) / "reference_check.png"
            path.write_bytes(_TINY_REFERENCE_PNG)
            try:
                published = self.reference_publisher.publish_path(
                    str(path),
                    project=str(request.project or "diagnostics"),
                    session=str(request.session or "reference_publish_check"),
                    public_url_map=dict(request.public_url_map or {}),
                )
            except ObjectStoreError as exc:
                return _reference_publish_check_result(
                    ready=False,
                    path=path,
                    reason="object_store_error",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    metadata=dict(request.metadata or {}),
                )
            except Exception as exc:  # noqa: BLE001
                return _reference_publish_check_result(
                    ready=False,
                    path=path,
                    reason="publish_error",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    metadata=dict(request.metadata or {}),
                )
            public_url = str(getattr(published, "public_url", "") or getattr(published, "url", "") or "").strip()
            ready = bool(provider_fetchable_reference_url(public_url))
            return _reference_publish_check_result(
                ready=ready,
                path=path,
                reason=str(getattr(published, "reason", "") or ("public_url" if ready else "no_public_url")),
                public_reference_url=public_url,
                object_key=str(getattr(published, "key", "") or ""),
                uploaded=bool(getattr(published, "uploaded", False)),
                metadata=dict(request.metadata or {}),
            )


class SessionReferenceAssetPublisher:
    """Publishes selected session asset rows into provider-fetchable reference URLs."""

    def __init__(self, reference_publisher: Any) -> None:
        self.reference_publisher = reference_publisher

    def publish_selected(
        self,
        selected_assets: list[dict[str, Any]],
        *,
        session_id: str,
        project: str,
        request: AssetReferencePublishRequest,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        results: list[dict[str, Any]] = []
        updated_rows: list[dict[str, Any]] = []
        for row in selected_assets:
            updated, result = self._publish_one_reference_asset(
                row,
                project=project,
                session_id=session_id,
                force=bool(request.force),
                backend_public_base_url=str(request.backend_public_base_url or ""),
                public_url_map=dict(request.public_url_map or {}),
            )
            results.append(result)
            if updated:
                updated_rows.append(updated)

        failed = [item for item in results if not item.get("public_reference_url")]
        return (
            {
                "ready": not failed and bool(results),
                "selected_count": len(selected_assets),
                "published_count": len(results) - len(failed),
                "failed_count": len(failed),
                "assets": results,
            },
            updated_rows,
        )

    def _publish_one_reference_asset(
        self,
        row: dict[str, Any],
        *,
        project: str,
        session_id: str,
        force: bool,
        backend_public_base_url: str,
        public_url_map: dict[str, str],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        asset_id = str(row.get("asset_id") or "")
        path = str(row.get("path") or "")
        existing_url = str(row.get("public_reference_url") or "").strip()
        if provider_fetchable_reference_url(existing_url) and not force:
            result = _asset_publish_result(
                row,
                public_reference_url=existing_url,
                reason="existing_public_reference_url",
            )
            return dict(row), result
        if is_remote_url(path):
            updated = {**row, "public_reference_url": path}
            return updated, _asset_publish_result(updated, public_reference_url=path, reason="remote")
        backend_asset_url = backend_asset_public_reference_url(
            session_id,
            asset_id=asset_id,
            path=path,
            public_base_url=backend_public_base_url,
        )
        if backend_asset_url:
            updated = {
                **row,
                "public_reference_url": backend_asset_url,
                "reference_publish_reason": "backend_public_base_url",
            }
            return updated, _asset_publish_result(
                updated,
                public_reference_url=backend_asset_url,
                reason="backend_public_base_url",
            )
        try:
            published = self.reference_publisher.publish_path(
                path,
                project=project,
                session=session_id,
                public_url_map=public_url_map,
            )
        except ObjectStoreError as exc:
            raise ApiError(f"reference asset publish failed: {exc}", status_code=502) from exc
        public_url = str(getattr(published, "public_url", "") or getattr(published, "url", "") or "").strip()
        updated = dict(row)
        if provider_fetchable_reference_url(public_url):
            updated["public_reference_url"] = public_url
            updated["reference_object_key"] = str(getattr(published, "key", "") or "")
            updated["reference_publish_reason"] = str(getattr(published, "reason", "") or "")
        return updated, {
            **_asset_publish_result(
                updated,
                public_reference_url=public_url,
                reason=str(getattr(published, "reason", "") or ""),
            ),
            "uploaded": bool(getattr(published, "uploaded", False)),
            "object_key": str(getattr(published, "key", "") or ""),
            "asset_id": asset_id,
        }


_TINY_REFERENCE_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xf8\x0f"
    b"\x00\x01\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
)
