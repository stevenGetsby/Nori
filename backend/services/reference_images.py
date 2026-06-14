"""Reference-image publishing and generation service coordination."""
from __future__ import annotations

from typing import Any

from nori.core import llms
from nori.sessions import SessionEvent
from nori.storage import ReferenceImagePublisher

from ..assets import append_session_assets, select_assets
from ..contracts import (
    ApiError,
    AssetReferencePublishRequest,
    ReferenceImageGenerationCheckRequest,
    ReferencePublishCheckRequest,
    SessionReferenceImageGenerationCheckRequest,
)
from .reference_image_generation import ReferenceImageGenerationChecker
from .reference_image_publishers import ReferencePublishDiagnostic, SessionReferenceAssetPublisher
from .reference_image_results import (
    _provider_fetchable_urls_from_publish_result,
    _session_reference_image_generation_check_result,
    _session_reference_image_generation_event_payload,
)
from .session_assets import assert_asset_paths_exist, reference_url_probe_summary
from .session_store import BackendSessionStore

__all__ = [
    "BackendReferenceImageService",
    "ReferenceImageGenerationChecker",
    "ReferencePublishDiagnostic",
    "SessionReferenceAssetPublisher",
    "llms",
]


class BackendReferenceImageService:
    """Coordinates session state with reference publishing and provider checks."""

    def __init__(
        self,
        *,
        session_store: BackendSessionStore,
        reference_publisher: Any | None = None,
        publish_diagnostic: ReferencePublishDiagnostic | None = None,
        asset_publisher: SessionReferenceAssetPublisher | None = None,
        generation_checker: ReferenceImageGenerationChecker | None = None,
    ) -> None:
        self.session_store = session_store
        self.session_manager = session_store.session_manager
        self.reference_publisher = reference_publisher or ReferenceImagePublisher.from_env()
        self.publish_diagnostic = publish_diagnostic or ReferencePublishDiagnostic(self.reference_publisher)
        self.asset_publisher = asset_publisher or SessionReferenceAssetPublisher(self.reference_publisher)
        self.generation_checker = generation_checker or ReferenceImageGenerationChecker()

    def check_reference_publish(self, request: ReferencePublishCheckRequest) -> dict[str, Any]:
        return self.publish_diagnostic.check(request)

    def check_reference_image_generation(self, request: ReferenceImageGenerationCheckRequest) -> dict[str, Any]:
        return self.generation_checker.check(request)

    def check_session_reference_image_generation(
        self,
        session_id: str,
        request: SessionReferenceImageGenerationCheckRequest,
    ) -> dict[str, Any]:
        """Publish selected session assets, then verify image-provider reference support."""

        publish_request = AssetReferencePublishRequest(
            asset_ids=list(request.asset_ids or []),
            project=str(request.project or ""),
            force=bool(request.force_publish),
            backend_public_base_url=str(request.backend_public_base_url or ""),
            public_url_map=dict(request.public_url_map or {}),
            metadata={**dict(request.metadata or {}), "source": "session_reference_image_generation_check"},
        )
        publish = self.publish_session_asset_references(session_id, publish_request)
        refs = _provider_fetchable_urls_from_publish_result(publish)
        url_probe = reference_url_probe_summary(
            {
                "verify_reference_urls": bool(request.verify_reference_urls),
                "reference_url_probe_timeout": request.reference_url_probe_timeout,
            },
            refs,
        )
        if not refs:
            result = _session_reference_image_generation_check_result(
                ready=False,
                reason="no_provider_fetchable_reference_images",
                publish=publish,
                generation=None,
                reference_images=[],
                url_probe=url_probe,
                metadata=dict(request.metadata or {}),
            )
            self._record_session_reference_image_generation_check(session_id, result)
            return result
        if bool(request.verify_reference_urls) and not bool(url_probe.get("passed")):
            result = _session_reference_image_generation_check_result(
                ready=False,
                reason="reference_url_probe_failed",
                publish=publish,
                generation=None,
                reference_images=refs,
                url_probe=url_probe,
                metadata=dict(request.metadata or {}),
            )
            self._record_session_reference_image_generation_check(session_id, result)
            return result
        generation = self.check_reference_image_generation(
            ReferenceImageGenerationCheckRequest(
                prompt=str(request.prompt or ""),
                reference_images=refs,
                size=str(request.size or ""),
                metadata={
                    **dict(request.metadata or {}),
                    "source": "session_reference_image_generation_check",
                    "session_id": session_id,
                },
            )
        )
        result = _session_reference_image_generation_check_result(
            ready=bool(generation.get("ready")),
            reason=str(generation.get("reason") or ""),
            publish=publish,
            generation=generation,
            reference_images=refs,
            url_probe=url_probe,
            metadata=dict(request.metadata or {}),
        )
        self._record_session_reference_image_generation_check(session_id, result)
        return result

    def publish_session_asset_references(
        self,
        session_id: str,
        request: AssetReferencePublishRequest,
    ) -> dict[str, Any]:
        session = self.session_store.require_session(session_id)
        try:
            selected_assets = select_assets(session.metadata.get("assets", []), asset_ids=list(request.asset_ids or []))
            assert_asset_paths_exist(selected_assets)
        except ValueError as exc:
            raise ApiError(str(exc), status_code=400) from exc

        project = str(request.project or session.metadata.get("project") or session_id)
        result, updated_rows = self.asset_publisher.publish_selected(
            selected_assets,
            session_id=session_id,
            project=project,
            request=request,
        )
        if updated_rows:
            session.metadata["assets"] = append_session_assets(session.metadata.get("assets"), updated_rows)
            session.events.append(
                SessionEvent(
                    event_type="asset_references_published",
                    payload={
                        "asset_ids": [row.get("asset_id") for row in updated_rows],
                        "metadata": dict(request.metadata or {}),
                    },
                )
            )
            self.session_store.save_session(session_id)

        return result

    def _record_session_reference_image_generation_check(self, session_id: str, result: dict[str, Any]) -> None:
        session = self.session_store.get_session(session_id)
        if session is None:
            return
        session.events.append(
            SessionEvent(
                event_type="reference_image_generation_checked",
                payload=_session_reference_image_generation_event_payload(result),
            )
        )
        self.session_store.save_session(session_id)
