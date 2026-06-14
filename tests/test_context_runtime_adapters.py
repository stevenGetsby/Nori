from __future__ import annotations

from nori.context import ContextBundle, attach_context_pack
from nori.core import ContextPack, ContentTask, UserProfile


def test_attach_context_pack_adds_business_context_to_runtime_bundle():
    pack = ContextPack(
        context_pack_id="ctx_task_001",
        user_profile=UserProfile(user_id="user_001"),
        task_intent={"task_id": "task_001", "topic": "反焦虑文创"},
    )
    bundle = ContextBundle(session_id="session_001", task_id="task_001", user_id="user_001")

    updated = attach_context_pack(bundle, pack)

    assert updated is not bundle
    assert updated.session_id == "session_001"
    assert updated.sources[-1].source_type == "context_pack"
    assert updated.sources[-1].ref == "ctx_task_001"
    assert updated.payload["context_pack"]["task_intent"]["topic"] == "反焦虑文创"
    assert updated.trace.source_refs == ["ctx_task_001"]
    assert updated.trace.notes == ["attached_context_pack"]


def test_attach_context_pack_accepts_dict_and_ref_override():
    pack = ContextPack(
        context_pack_id="ctx_task_001",
        task_intent=ContentTask(task_id="task_001", topic="Holly").to_dict(),
    )

    updated = attach_context_pack(ContextBundle(), pack.to_dict(), ref="manual_context")

    assert updated.sources[0].ref == "manual_context"
    assert updated.payload["context_pack"]["context_pack_id"] == "ctx_task_001"
