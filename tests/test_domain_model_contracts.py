from pathlib import Path

from nori.core import UserAsset
from nori.core import (
    AccountOperationProject,
    AssetLibrary,
    AssetRecord,
    ClientBrief,
    ContentCalendar,
    ContentTask,
    KPIPlan,
    OperationPlan,
)
from nori.content_generation.models import (
    AssetBundle,
    CandidateTitle,
    CoverResult,
    NoteDraft,
)
from nori.market_analysis.models import (
    NoteEvidence,
    NoteSkill,
    SessionSkillReport,
    XHSNoteSample,
    XHSSeedSkillDraft,
)
from nori.user_profiling.models import (
    AccountPlanResult,
    AccountPlannerInput,
    IntakeResult,
    UserInput,
)
from nori.shared import attach_llm_error


def test_user_input_model_serializes():
    user_input = UserInput(text="做一篇小红书", images=["a.png"])

    assert user_input.to_dict() == {"text": "做一篇小红书", "images": ["a.png"]}
    assert UserInput.from_dict(user_input.to_dict()).to_dict() == user_input.to_dict()


def test_account_planner_input_from_intaker_model():
    intaker_result = IntakeResult(
        intention={"goal": "涨粉"},
        context={"images": [{"path": "a.png", "kind": "png"}]},
        missing=[],
        questions=[],
    )

    planner_input = AccountPlannerInput.from_intaker(intaker_result, text="品牌理念", platform="xhs")

    assert planner_input.intention == {"goal": "涨粉"}
    assert planner_input.context["images"][0]["path"] == "a.png"
    assert planner_input.images == ["a.png"]
    assert planner_input.to_dict()["platform"] == "xhs"
    assert AccountPlannerInput.from_dict(planner_input.to_dict()).to_dict() == planner_input.to_dict()


def test_intake_result_metadata_is_optional_in_serialization():
    result = IntakeResult(
        intention={"goal": "涨粉"},
        context={},
        missing=[],
        questions=[],
    )
    assert "metadata" not in result.to_dict()

    attach_llm_error(result.metadata, "intake_text", {"reason": "api_error"})
    assert result.to_dict()["metadata"]["llm_error"]["stage"] == "intake_text"


def test_front_pipeline_result_models_round_trip_from_dict():
    intake = IntakeResult(
        intention={"goal": "种草"},
        context={"images": [{"path": "a.png"}]},
        missing=["品牌名"],
        questions=["品牌叫什么？"],
        assets=[
            UserAsset(
                kind="image",
                path="a.png",
                vision_roles=["product_shot"],
                usable_for=["cover"],
            )
        ],
        metadata={"llm_enhanced": True},
    )
    plan = AccountPlanResult(
        tags={"platform": "xhs", "category": "香薰"},
        recommended_positioning="通勤香氛生活方式账号",
        audience_profile=["城市通勤女性"],
        content_directions=["通勤场景", "香味测评"],
        benchmark_accounts={"search_keywords": ["通勤香薰"]},
        unique_selling_points=["小众不撞香"],
        ip_portrait_report={"account_keywords": ["通勤", "香薰"]},
        metadata={"llm_enhanced": True},
    )

    assert IntakeResult.from_dict(intake.to_dict()).to_dict() == intake.to_dict()
    assert AccountPlanResult.from_dict(plan.to_dict()).to_dict() == plan.to_dict()
    assert AccountPlannerInput.from_dict({"search_limit": True}).search_limit == 5
    assert AccountPlannerInput.from_dict({"enable_search": "false"}).enable_search is False


def test_models_are_defined_in_dedicated_modules():
    assert UserInput.__module__ == "nori.user_profiling.models"
    assert AccountPlannerInput.__module__ == "nori.user_profiling.models"
    assert UserAsset.__module__ == "nori.core.models"
    assert ClientBrief.__module__ == "nori.core.models"
    assert OperationPlan.__module__ == "nori.core.models"
    assert KPIPlan.__module__ == "nori.core.models"
    assert ContentTask.__module__ == "nori.core.models"
    assert ContentCalendar.__module__ == "nori.core.models"
    assert AccountOperationProject.__module__ == "nori.core.project"
    assert AssetRecord.__module__ == "nori.core.models"
    assert AssetLibrary.__module__ == "nori.core.models"
    assert NoteDraft.__module__ == "nori.content_generation.models"
    assert CoverResult.__module__ == "nori.content_generation.models"
    assert NoteEvidence.__module__ == "nori.market_analysis.models"
    assert NoteSkill.__module__ == "nori.market_analysis.models"
    assert SessionSkillReport.__module__ == "nori.market_analysis.models"
    assert XHSNoteSample.__module__ == "nori.market_analysis.models"
    assert XHSSeedSkillDraft.__module__ == "nori.market_analysis.models"


def test_xhs_note_models_round_trip_from_dict():
    note = XHSNoteSample(
        meta_path=Path("cold_start_data/xhs/设计/a/posts/b/meta.json"),
        category="设计",
        author_id="a",
        author_name="设计作者",
        note_id="b",
        title="设计案例｜测试",
        desc="项目说明",
        tags=["#设计"],
        metrics={"liked": 1},
        image_count=3,
        note_type="图文",
        note_url="https://example.com",
    )
    draft = XHSSeedSkillDraft(
        skill_id="seed.xhs.test",
        category="设计",
        match={"scene": "设计案例解析型 note"},
        craft={"title_rules": []},
        evidence={"source_note": note.to_dict()},
        validation={"result": "draft_only"},
    )

    assert note.to_dict()["meta_path"] == "cold_start_data/xhs/设计/a/posts/b/meta.json"
    assert draft.to_dict()["id"] == "seed.xhs.test"
    assert draft.to_dict()["evidence"]["source_note"]["note_id"] == "b"
    assert XHSNoteSample.from_dict(note.to_dict()).to_dict() == note.to_dict()
    assert XHSSeedSkillDraft.from_dict(draft.to_dict()).to_dict() == draft.to_dict()
    assert XHSNoteSample.from_dict({"metrics": {"liked": "12", "shared": True}}).metrics == {
        "liked": 12,
        "shared": 0,
    }


def test_generation_artifact_models_round_trip_from_dict():
    main_asset = UserAsset(
        kind="image",
        path="/tmp/main.png",
        vision_roles=["product_shot"],
        subject="香薰瓶",
        brand_signals=["Nori"],
        usable_for=["cover"],
        quality="high",
    )
    bundle = AssetBundle(
        main_images=[main_asset],
        text_points=["随身香薰"],
        brand_facts=["小众品牌"],
        data_points=["复购率高"],
    )
    draft = NoteDraft(
        skill_id="skill_001",
        title="通勤香薰｜轻巧不撞香",
        body="这支随身香薰适合通勤。",
        tags=["通勤香薰"],
        comment_hook="你会带香薰出门吗？",
        cover_path="/tmp/cover.png",
        image_paths=["/tmp/main.png"],
        candidate_titles=[
            CandidateTitle(text="通勤香薰｜轻巧不撞香", rule_name="场景钩子", rationale="命中通勤")
        ],
        metrics_target={"liked_target": 1200},
        asset_bundle=bundle.to_dict(),
        validation={"status": "pass"},
        llm_enhanced=True,
    )
    cover = CoverResult(
        cover_path="/tmp/cover.png",
        prompt="小红书封面，通勤香薰",
        size="1024x1024",
        reference_paths=["/tmp/main.png"],
        source="data:image/png;base64,...",
        extra={"model": "image-model"},
    )

    assert UserAsset.from_dict({"path": "/tmp/inferred.png"}).kind == "image"
    assert AssetBundle.from_dict(bundle.to_dict()).to_dict() == bundle.to_dict()
    assert NoteDraft.from_dict(draft.to_dict()).to_dict() == draft.to_dict()
    assert NoteDraft.from_dict({"llm_enhanced": "false"}).llm_enhanced is False
    assert CoverResult.from_dict(cover.to_dict()).to_dict() == cover.to_dict()
