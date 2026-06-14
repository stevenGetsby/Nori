from __future__ import annotations

from nori.agents.content_generation import ContentSpecAgent
from nori.agents.market_analysis.schemas import NoteSkill
from nori.context import ContextCompiler, ContextResolver, ContextSlice, ContextView
from nori.core import AssetLibrary, AssetRecord, ClientBrief, ContentTask, MarketAnalysis, UserProfile


def _task() -> ContentTask:
    return ContentTask(
        task_id="task_001",
        platform="xhs",
        content_type="image_text_post",
        topic="反焦虑文创",
        objective="让用户理解 Holly Shit 的怪趣价值",
        brief={"angle": "把便便精神讲成反焦虑生活态度"},
    )


def _skill() -> NoteSkill:
    return NoteSkill(
        skill_id="xhs_anti_anxiety_seed",
        label="反焦虑怪趣种草",
        goal="planting",
        note_type="图文",
        tone="怪趣但真诚",
        creative_goal="用荒诞幽默把产品变成情绪出口。",
        title_rules=[{"name": "反差钩子", "rule": "标题先给一个反差鲜明的情绪判断。"}],
        visual_rules=[{"name": "IP 主体", "rule": "优先露出 IP 表情和产品轮廓。"}],
        avoid_rules=["不要低俗猎奇"],
    )


def test_context_compiler_builds_business_context_slices_for_generation():
    pack = ContextCompiler().build(
        context_pack_id="ctx_task_001",
        task=_task(),
        user_profile=UserProfile(
            user_id="holly",
            platform="xhs",
            brand_profile={"brand_name": "Holly Shit"},
            constraints=["不要低俗"],
        ),
        market_analysis=MarketAnalysis(
            analysis_id="market_001",
            platform="xhs",
            keywords=["反焦虑文创"],
            hot_examples=[{"title": "年轻人需要一点怪东西"}],
            trend_insights=["情绪价值标题更容易被收藏"],
            source_refs=[{"source": "xhs_hot_note", "note_id": "n1"}],
        ),
        asset_library=AssetLibrary(
            assets=[AssetRecord(asset_id="asset_001", kind="image", path="/tmp/ip.png", tags=["ip"])]
        ),
        skills=[_skill()],
        platform_rules=[{"rule": "小红书图文封面需要一眼读懂情绪利益点"}],
        content_strategy={"creative_angle": "怪趣反焦虑", "artifact_type": "image_text_post"},
    )

    kinds = {row["kind"] for row in pack.context_slices}

    assert pack.context_pack_id == "ctx_task_001"
    assert {
        "brand_profile",
        "task_intent",
        "platform_strategy",
        "market_hotspots",
        "learned_skills",
        "content_strategy",
        "asset_context",
        "constraints",
    } <= kinds
    assert pack.metadata["context_layer"] == "orchestration"
    assert pack.context_slices_by_kind("platform_strategy")[0].payload["rules"][0]["rule"].startswith("小红书")
    assert pack.context_slices_by_kind("learned_skills")[0].payload["skills"][0]["skill_id"] == "xhs_anti_anxiety_seed"


def test_context_resolver_returns_agent_specific_context_view():
    pack = ContextCompiler().build(
        task=_task(),
        user_profile=UserProfile(user_id="holly", brand_profile={"brand_name": "Holly Shit"}),
        market_analysis=MarketAnalysis(trend_insights=["情绪价值标题更容易被收藏"]),
        skills=[_skill()],
        platform_rules=[{"rule": "小红书首图要强钩子"}],
        content_strategy={"creative_angle": "怪趣反焦虑"},
    )

    view = ContextResolver().for_agent("ContentSpecAgent", pack)

    assert isinstance(view, ContextView)
    assert view.agent_name == "ContentSpecAgent"
    assert view.task_id == "task_001"
    assert view.kinds == [
        "task_intent",
        "brand_profile",
        "platform_strategy",
        "market_hotspots",
        "learned_skills",
        "content_strategy",
        "asset_context",
        "constraints",
    ]
    assert view.payload["content_strategy"]["creative_angle"] == "怪趣反焦虑"
    assert view.payload["learned_skills"]["skills"][0]["label"] == "反焦虑怪趣种草"


def test_content_spec_agent_can_design_from_context_view_without_loose_context_dicts():
    pack = ContextCompiler().build(
        task=_task(),
        user_profile=UserProfile(
            user_id="holly",
            brand_profile={"brand_name": "Holly Shit"},
            constraints=["不要低俗"],
        ),
        market_analysis=MarketAnalysis(trend_insights=["情绪价值标题更容易被收藏"]),
        skills=[_skill()],
        platform_rules=[{"rule": "小红书首图要强钩子"}],
        content_strategy={"creative_angle": "怪趣反焦虑", "artifact_type": "image_text_post"},
    )
    view = ContextResolver().for_agent("ContentSpecAgent", pack)

    spec = ContentSpecAgent().run(context_view=view)

    assert spec.task_id == "task_001"
    assert spec.artifact_type == "image_text_post"
    assert spec.creative_angle == "怪趣反焦虑"
    assert spec.selected_skill_refs == [{"skill_id": "xhs_anti_anxiety_seed", "label": "反焦虑怪趣种草"}]
    assert "不要低俗" in spec.constraints
    assert spec.metadata["context_view"]["agent_name"] == "ContentSpecAgent"


def test_context_pack_builder_canonical_owner_is_context_layer():
    import nori.agents.planning as planning
    from nori.context import ContextPackBuilder

    assert ContextPackBuilder.__module__ == "nori.context.compiler"
    assert "ContextPackBuilder" not in planning.__all__
    assert not hasattr(planning, "ContextPackBuilder")
