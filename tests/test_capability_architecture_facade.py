from nori.core import AssetLibrary, AssetRecord
from nori.core import AccountOperationProject
from nori.core import ContentTask, ClientBrief
from nori.content_generation import ContentGenerationFacade
from nori.context_building import ContextPackBuilder
from nori.learning_loop import LearningLoopFacade
from nori.market_analysis import MarketAnalysisFacade
from nori.content_generation.models import ContentPackage
from nori.learning_loop.models import MetricsSnapshot, StrategyIteration
from nori.market_analysis.models import CompetitorResearch, CompetitorSample
from nori.user_profiling.models import AccountPositioning
from nori.user_profiling import UserProfilingFacade
from nori.core import (
    CandidateSet,
    CapabilitySnapshot,
    ContextPack,
    DecisionPoint,
    ExplanationTrace,
    LearningSignal,
    UserProfile,
    WorkflowBase,
)
from nori.core.models import DomainSnapshot


def test_shared_core_contracts_exist_and_round_trip():
    profile = UserProfile(user_id="u1", display_name="Alice", platform="xhs")
    decision = DecisionPoint(
        decision_id="d1",
        kind="topic",
        options=[{"id": "a", "label": "A"}],
        recommended_option="a",
    )
    trace = ExplanationTrace(
        trace_id="t1",
        input_refs=["r1"],
        decisions=[decision.to_dict()],
        stage_steps=[{"stage": "ContextPackBuilder"}],
    )
    candidates = CandidateSet(candidate_set_id="c1", candidates=[{"id": "a"}], selected_candidate_id="a")
    signal = LearningSignal(signal_id="s1", source="review", target="preference")
    pack = ContextPack(context_pack_id="cp1", user_profile=profile, decision_points=[decision], explanation_trace=trace)

    assert profile.to_dict()["user_id"] == "u1"
    assert pack.to_dict()["user_profile"]["display_name"] == "Alice"
    assert DecisionPoint.from_dict(decision.to_dict()).to_dict() == decision.to_dict()
    assert CandidateSet.from_dict(candidates.to_dict()).to_dict() == candidates.to_dict()
    assert LearningSignal.from_dict(signal.to_dict()).to_dict() == signal.to_dict()
    assert ExplanationTrace.from_dict(trace.to_dict()).to_dict() == trace.to_dict()
    assert "stage_steps" in trace.to_dict()
    assert "agent_steps" not in trace.to_dict()


def test_explanation_trace_reads_legacy_agent_steps_as_stage_steps():
    trace = ExplanationTrace.from_dict({
        "trace_id": "legacy",
        "agent_steps": [{"agent": "OldFacade", "output_count": 1}],
    })

    assert trace.stage_steps == [{"stage": "OldFacade", "output_count": 1}]
    assert trace.to_dict()["stage_steps"] == [{"stage": "OldFacade", "output_count": 1}]
    assert "agent_steps" not in trace.to_dict()


def test_facades_are_importable_and_composable():
    user = UserProfilingFacade()
    market = MarketAnalysisFacade()
    builder = ContextPackBuilder()
    generation = ContentGenerationFacade()
    learning = LearningLoopFacade()

    assert user.module_name == "user_profiling"
    assert market.module_name == "market_analysis"
    assert builder.module_name == "context_building"
    assert generation.module_name == "content_generation"
    assert learning.module_name == "learning_loop"


def test_business_facades_share_workflow_base_contract():
    facades = [
        UserProfilingFacade(),
        MarketAnalysisFacade(),
        ContextPackBuilder(),
        ContentGenerationFacade(),
        LearningLoopFacade(),
    ]

    assert all(isinstance(facade, WorkflowBase) for facade in facades)
    assert [facade.workflow_name for facade in facades] == [
        "user_profiling",
        "market_analysis",
        "context_building",
        "content_generation",
        "learning_loop",
    ]
    assert [facade.step_names for facade in facades] == [
        ["client_brief", "account_positioning", "user_profile"],
        ["competitor_research", "market_analysis"],
        ["profile", "task", "market", "assets", "context_pack"],
        ["context_pack", "content_packages", "candidate_set"],
        ["performance", "strategy", "capability_snapshot"],
    ]


def test_capability_architecture_registry_exposes_agent_owned_modules():
    from nori.core import CAPABILITY_MODULES, CapabilityModule, capability_module_names, get_capability_module

    assert capability_module_names() == [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    assert all(isinstance(module, CapabilityModule) for module in CAPABILITY_MODULES)

    planning = get_capability_module("planning")
    assert planning.package == "nori.agents.planning"
    assert planning.agents == ("OperationPlannerAgent", "KPIPlannerAgent", "CalendarPlannerAgent")
    assert "ContentCalendar" in planning.contracts

    generation = get_capability_module("content_generation")
    assert generation.depends_on == ("planning", "market_analysis")
    assert "ContentProducerAgent" in generation.agents

    learning = get_capability_module("learning_loop")
    assert "StrategyIterationAgent" in learning.agents
    assert learning.depends_on == ("content_generation",)

    assert get_capability_module("missing") is None


def test_five_modules_compose_existing_project_models():
    brief = ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        goals=["提升到店咨询"],
        constraints=["不夸大疗效"],
        taboos=["最低价"],
        context={"preferences": {"tone": "清爽自然"}},
    )
    positioning = AccountPositioning(
        recommended_positioning="社区花艺顾问",
        account_keywords=["花艺", "本地生活"],
    )
    research = CompetitorResearch(
        research_id="research_001",
        keywords=["母亲节花束"],
        samples=[
            CompetitorSample(
                sample_id="sample_001",
                title="母亲节花别乱买",
                metrics={"liked": 200},
            )
        ],
        insights=["避坑标题表现更好"],
    )
    assets = AssetLibrary(
        assets=[
            AssetRecord(asset_id="logo", kind="image", path="/tmp/logo.png", usage=["cover"]),
            AssetRecord(asset_id="old", kind="image", status="archived", usage=["cover"]),
        ]
    )
    task = ContentTask(
        task_id="task_001",
        topic="母亲节花束搭配",
        objective="提升咨询",
        brief={"cover_title": "母亲节花别乱买"},
        references=research.to_task_references(limit=1),
    )

    profile = UserProfilingFacade().build_profile(
        user_id="u1",
        client_brief=brief,
        account_positioning=positioning,
    )
    market = MarketAnalysisFacade().build_analysis(research)
    context_pack = ContextPackBuilder().build(
        context_pack_id="ctx_001",
        user_profile=profile,
        task=task,
        market_analysis=market,
        asset_library=assets,
        decision_points=[DecisionPoint(decision_id="d_topic", kind="topic", recommended_option="topic_a")],
    )

    assert context_pack.user_profile.brand_profile["brand_name"] == "春日花房"
    assert context_pack.market_analysis.trend_insights == ["避坑标题表现更好"]
    assert context_pack.assets == [assets.assets[0].to_dict()]
    assert context_pack.task_intent["topic"] == "母亲节花束搭配"
    assert context_pack.explanation_trace.retrieved_evidence[0]["source"] == "competitor_research"

    package = ContentPackage(
        package_id="pkg_001",
        task_id="task_001",
        title="母亲节花别乱买",
        body="春日花房帮你避坑。",
        status="draft",
    )
    candidate_set = ContentGenerationFacade().candidate_set([package], task=task, selected_candidate_id="pkg_001")

    assert candidate_set.candidates[0]["package"]["title"] == "母亲节花别乱买"
    assert candidate_set.decision_point.kind == "candidate_selection"
    assert candidate_set.selected_candidate_id == "pkg_001"

    learning = LearningLoopFacade()
    performance = learning.performance_snapshot(
        MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001", metrics={"likes": 20})
    )
    signal = learning.learning_signal(
        source="metrics",
        target="preference",
        strategy_iteration=StrategyIteration(
            iteration_id="iter_001",
            diagnosis=["互动率偏弱"],
            decisions=["测试更强标题钩子"],
            next_actions=["下一条内容强化首段钩子"],
        ),
        confidence=0.7,
    )

    assert performance.ref_id == "pkg_001"
    assert signal.signal_id == "signal_iter_001"
    assert signal.update_suggestion["next_actions"] == ["下一条内容强化首段钩子"]


def test_account_operation_project_projects_into_five_capability_modules():
    task = ContentTask(
        task_id="task_001",
        topic="母亲节花束搭配",
        objective="提升咨询",
        references=[{"source": "manual_ref", "title": "节日花束案例"}],
    )
    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(
            client_name="花店主理人",
            brand_name="春日花房",
            goals=["提升到店咨询"],
            constraints=["不夸大疗效"],
            context={"preferences": {"tone": "清爽自然"}},
        ),
        account_positioning=AccountPositioning(
            positioning_id="pos_001",
            recommended_positioning="社区花艺顾问",
            account_keywords=["花艺", "本地生活"],
        ),
        asset_library=AssetLibrary(
            assets=[AssetRecord(asset_id="cover_001", kind="image", path="/tmp/cover.png", usage=["cover"])]
        ),
        competitor_research=CompetitorResearch(
            research_id="research_001",
            keywords=["母亲节花束"],
            samples=[CompetitorSample(sample_id="sample_001", title="母亲节花别乱买")],
            insights=["避坑标题表现更好"],
        ),
        content_tasks=[task],
        content_packages=[
            ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买", body="正文 A"),
            ContentPackage(package_id="pkg_002", task_id="task_002", title="其他任务", body="正文 B"),
        ],
        metrics_snapshots=[MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001", metrics={"likes": 20})],
        strategy_iterations=[
            StrategyIteration(
                iteration_id="iter_001",
                input_refs=["metric_001"],
                diagnosis=["互动率偏弱"],
                decisions=["测试更强标题钩子"],
                next_actions=["下一条内容强化首段钩子"],
            )
        ],
    )

    profile = UserProfilingFacade().build_from_project(project)
    market = MarketAnalysisFacade().build_from_project(project)
    context_pack = ContextPackBuilder().build_from_project(project, task_id="task_001")
    candidates = ContentGenerationFacade().candidate_set_from_project(
        project,
        task_id="task_001",
        selected_candidate_id="pkg_001",
    )
    snapshots = LearningLoopFacade().performance_snapshots_from_project(project)
    signals = LearningLoopFacade().learning_signals_from_project(
        project,
        source="metrics",
        target="preference",
    )

    assert profile.metadata["project_id"] == "project_001"
    assert profile.brand_profile["brand_name"] == "春日花房"
    assert market.metadata["project_id"] == "project_001"
    assert context_pack.context_pack_id == "ctx_task_001"
    assert context_pack.metadata["project_id"] == "project_001"
    assert context_pack.assets[0]["asset_id"] == "cover_001"
    assert candidates.task_id == "task_001"
    assert [candidate["id"] for candidate in candidates.candidates] == ["pkg_001"]
    assert candidates.explanation_trace.input_refs == ["ctx_task_001", "task_001"]
    assert candidates.explanation_trace.stage_steps == [{"stage": "ContentGenerationFacade", "output_count": 1}]
    assert snapshots[0].snapshot_id == "metric_001"
    assert signals[0].signal_id == "signal_iter_001"


def test_upstream_facades_accept_persisted_project_dicts_without_project_model_dependency():
    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        account_positioning=AccountPositioning(recommended_positioning="社区花艺顾问"),
        competitor_research=CompetitorResearch(
            research_id="research_001",
            keywords=["母亲节花束"],
            insights=["避坑标题表现更好"],
        ),
    ).to_dict()

    profile = UserProfilingFacade().build_from_project(project)
    market = MarketAnalysisFacade().build_from_project(project)

    assert profile.user_id == "project_001"
    assert profile.brand_profile["brand_name"] == "春日花房"
    assert profile.account_profile["recommended_positioning"] == "社区花艺顾问"
    assert market.analysis_id == "research_001"
    assert market.keywords == ["母亲节花束"]
    assert market.metadata["project_name"] == "春日花房运营"


def test_learning_loop_builds_round_trippable_capability_snapshot_from_project():
    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        account_positioning=AccountPositioning(recommended_positioning="社区花艺顾问"),
        asset_library=AssetLibrary(
            assets=[AssetRecord(asset_id="cover_001", kind="image", path="/tmp/cover.png", usage=["cover"])]
        ),
        competitor_research=CompetitorResearch(
            research_id="research_001",
            keywords=["母亲节花束"],
            insights=["避坑标题表现更好"],
        ),
        content_tasks=[
            ContentTask(task_id="task_001", topic="母亲节花束搭配"),
            ContentTask(task_id="task_002", topic="毕业季花束"),
        ],
        content_packages=[
            ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买"),
            ContentPackage(package_id="pkg_002", task_id="task_002", title="毕业花束怎么选"),
        ],
        metrics_snapshots=[MetricsSnapshot(snapshot_id="metric_001", ref_id="pkg_001", metrics={"likes": 20})],
        strategy_iterations=[StrategyIteration(iteration_id="iter_001", next_actions=["强化首段钩子"])],
    )

    snapshot = LearningLoopFacade().capability_snapshot_from_project(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
        signal_source="metrics",
        signal_target="preference",
    )

    assert isinstance(snapshot, CapabilitySnapshot)
    assert snapshot.snapshot_id == "capability_project_001"
    assert snapshot.project_id == "project_001"
    assert snapshot.capability_names == [
        "user_profiling",
        "market_analysis",
        "planning",
        "content_generation",
        "learning_loop",
    ]
    assert [pack.context_pack_id for pack in snapshot.context_packs] == ["ctx_task_001", "ctx_task_002"]
    assert [candidate_set.task_id for candidate_set in snapshot.candidate_sets] == ["task_001", "task_002"]
    assert snapshot.candidate_sets[0].selected_candidate_id == "pkg_001"
    assert snapshot.performance_snapshots[0].snapshot_id == "metric_001"
    assert snapshot.learning_signals[0].signal_id == "signal_iter_001"
    assert CapabilitySnapshot.from_dict(snapshot.to_dict()).to_dict() == snapshot.to_dict()
    assert snapshot.validate() == []
    assert snapshot.is_valid()


def test_capability_snapshot_validation_reports_structural_issues():
    snapshot = CapabilitySnapshot(
        snapshot_id="capability_bad",
        project_id="project_001",
        capability_names=["user_profiling"],
        context_packs=[
            ContextPack(
                context_pack_id="ctx_task_001",
                task_intent={"task_id": "task_001"},
            )
        ],
        candidate_sets=[
            CandidateSet(
                candidate_set_id="candidates_task_002",
                task_id="task_002",
                candidates=[{"id": "pkg_002"}],
                selected_candidate_id="pkg_missing",
            )
        ],
    )

    issues = snapshot.validate()
    issue_codes = [issue["code"] for issue in issues]

    assert "missing_required_capability" in issue_codes
    assert "candidate_set_without_context" in issue_codes
    assert "selected_candidate_missing" in issue_codes
    assert not snapshot.is_valid()


def test_public_capability_entrypoint_builds_and_validates_snapshot():
    from nori import __all__ as nori_exports
    from nori.capabilities import build_capability_snapshot, validate_capability_snapshot

    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        account_positioning=AccountPositioning(recommended_positioning="社区花艺顾问"),
        content_tasks=[ContentTask(task_id="task_001", topic="母亲节花束搭配")],
        content_packages=[ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买")],
    )

    snapshot = build_capability_snapshot(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
    )

    assert "capabilities" in nori_exports
    assert snapshot.snapshot_id == "capability_project_001"
    assert snapshot.is_valid()
    assert validate_capability_snapshot(snapshot) == []
    assert validate_capability_snapshot(snapshot.to_dict()) == []


def test_legacy_domain_entrypoint_builds_and_validates_compat_snapshot():
    from nori.domain import build_domain_snapshot, validate_domain_snapshot

    project = AccountOperationProject(
        project_id="project_001",
        name="春日花房运营",
        client_brief=ClientBrief(client_name="花店主理人", brand_name="春日花房"),
        account_positioning=AccountPositioning(recommended_positioning="社区花艺顾问"),
        content_tasks=[ContentTask(task_id="task_001", topic="母亲节花束搭配")],
        content_packages=[ContentPackage(package_id="pkg_001", task_id="task_001", title="母亲节花别乱买")],
    )

    snapshot = build_domain_snapshot(
        project,
        selected_candidate_ids={"task_001": "pkg_001"},
    )

    assert isinstance(snapshot, DomainSnapshot)
    assert snapshot.snapshot_id == "domain_project_001"
    assert snapshot.is_valid()
    assert validate_domain_snapshot(snapshot) == []
