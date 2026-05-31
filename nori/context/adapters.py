"""Adapters between runtime context bundles and business context packs."""
from __future__ import annotations

from nori.core import ContextPack

from .models import ContextBundle, ContextSource, ContextTrace


def attach_context_pack(
    bundle: ContextBundle,
    context_pack: ContextPack | dict,
    *,
    ref: str = "",
) -> ContextBundle:
    """Return a runtime ContextBundle with a business ContextPack attached.

    ``ContextPack`` is the business-generation context compiled by the context
    layer. ``ContextBundle`` is the runtime envelope for one agent call.
    This adapter makes the nesting explicit instead of treating them as
    competing context systems.
    """
    normalized = context_pack if isinstance(context_pack, ContextPack) else ContextPack.from_dict(context_pack)
    payload = normalized.to_dict()
    source_ref = str(ref or normalized.context_pack_id or "context_pack")
    source = ContextSource(source_type="context_pack", ref=source_ref, payload=payload)
    return ContextBundle(
        session_id=bundle.session_id,
        task_id=bundle.task_id,
        user_id=bundle.user_id,
        goal=bundle.goal,
        sources=[*bundle.sources, source],
        memory=[dict(item) for item in bundle.memory],
        artifacts=[dict(item) for item in bundle.artifacts],
        payload={**dict(bundle.payload), "context_pack": payload},
        trace=ContextTrace(
            resolver=bundle.trace.resolver,
            source_refs=[*bundle.trace.source_refs, source_ref],
            notes=[*bundle.trace.notes, "attached_context_pack"],
        ),
    )


__all__ = ["attach_context_pack"]
