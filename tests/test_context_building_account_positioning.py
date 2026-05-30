from nori.core import AccountOperationProject
from nori.core import ClientBrief
from nori.agents.user_profiling.models import AccountPlanResult
from nori.agents.planning import OperationPlannerAgent
from nori.agents.user_profiling.models import AccountPositioning


def _account_plan() -> AccountPlanResult:
    return AccountPlanResult(
        tags={"track": "花艺", "platform": "小红书"},
        recommended_positioning="懂生活的社区花艺顾问",
        audience_profile=["周边 3 公里年轻家庭"],
        content_directions=["节日花束搭配", "门店日常"],
        benchmark_accounts={
            "search_keywords": ["花艺", "社区花店"],
            "accounts": [{"name": "本地花艺号", "url": "https://example.com/a"}],
            "search_results": [{"title": "母亲节花束", "url": "https://example.com/note", "keyword": "花艺"}],
        },
        unique_selling_points=["本地配送快", "审美稳定"],
        ip_portrait_report={
            "content_pillars": [
                {"name": "花艺知识", "description": "花材养护和搭配"},
                "门店日常",
            ],
            "account_keywords": ["花艺", "本地生活"],
            "cover_design_formats": [{"ratio": "3:4", "style": "清爽大字"}],
        },
    )


def test_account_positioning_extracts_account_plan_contract():
    positioning = AccountPositioning.from_account_plan(_account_plan(), positioning_id="pos_001")

    assert positioning.positioning_id == "pos_001"
    assert positioning.recommended_positioning == "懂生活的社区花艺顾问"
    assert positioning.content_pillars[0]["name"] == "花艺知识"
    assert positioning.content_pillars[1]["name"] == "门店日常"
    assert positioning.account_keywords == ["花艺", "本地生活"]
    assert positioning.cover_design_formats == [{"ratio": "3:4", "style": "清爽大字"}]
    assert {"source": "benchmark_keyword", "keyword": "花艺"} in positioning.benchmark_refs
    assert positioning.summary() == "懂生活的社区花艺顾问"


def test_account_positioning_keeps_legacy_dict_shape_round_trip():
    project = AccountOperationProject(
        project_id="ops_001",
        account_positioning={"persona": "懂生活的社区花艺顾问"},
    )

    data = project.to_dict()
    restored = AccountOperationProject.from_dict(data)

    assert isinstance(project.account_positioning, AccountPositioning)
    assert dict(project.account_positioning) == {"persona": "懂生活的社区花艺顾问"}
    assert project.account_positioning == {"persona": "懂生活的社区花艺顾问"}
    assert restored.to_dict() == data
    assert restored.account_positioning["persona"] == "懂生活的社区花艺顾问"


def test_operation_planner_outputs_typed_account_positioning():
    project = OperationPlannerAgent(use_llm=False).run(
        ClientBrief(
            client_name="花店主理人",
            brand_name="春日花房",
            goals=["提升到店咨询"],
            audience=["周边 3 公里年轻家庭"],
        ),
        _account_plan(),
        start_date="2026-05-25",
        horizon_days=7,
    )

    assert isinstance(project.account_positioning, AccountPositioning)
    assert project.account_positioning.recommended_positioning == "懂生活的社区花艺顾问"
    assert project.account_positioning.account_keywords == ["花艺", "本地生活"]
    assert project.to_dict()["account_positioning"]["source"] == "account_plan"
