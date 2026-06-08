from nori.core import AccountOperationProject, ClientBrief, ContentCalendar, ContentTask, KPIPlan, OperationPlan
from nori.agents.content_generation.schemas import ContentPackage
from nori.agents.learning_loop.schemas import ComplianceReview, MetricsSnapshot, StrategyIteration


def test_client_brief_serializes_with_defaults_and_copies_lists():
    brief = ClientBrief(
        client_name="花店主理人",
        brand_name="春日花房",
        goals=["涨粉", "到店转化"],
        audience=["本地年轻女性"],
        taboos=["夸大疗效"],
        source_materials=[{"asset_id": "logo", "kind": "image"}],
        context={"city": "上海"},
    )

    data = brief.to_dict()
    data["goals"].append("不应回写")
    data["source_materials"][0]["asset_id"] = "mutated"

    assert brief.platform == "xhs"
    assert brief.goals == ["涨粉", "到店转化"]
    assert brief.source_materials[0]["asset_id"] == "logo"

    restored = ClientBrief.from_dict(brief.to_dict())
    assert restored.to_dict() == brief.to_dict()


def test_content_task_and_calendar_round_trip_nested_tasks():
    task = ContentTask(
        task_id="task_001",
        title="母亲节花束选题",
        scheduled_date="2026-05-01",
        topic="母亲节花束搭配",
        objective="收藏转化",
        priority=2,
        brief={"cover_title": "母亲节花别乱买"},
        required_assets=["product_photo"],
        references=[{"source": "competitor_note", "note_id": "xhs_001"}],
        metadata={"pillar": "节日节点"},
    )
    calendar = ContentCalendar(
        calendar_id="cal_may",
        start_date="2026-05-01",
        end_date="2026-05-07",
        cadence="每周 3 篇",
        themes=["节日节点"],
        tasks=[task],
    )

    restored = ContentCalendar.from_dict(calendar.to_dict())

    assert restored.to_dict() == calendar.to_dict()
    assert restored.tasks[0].platform == "xhs"
    assert restored.tasks[0].status == "planned"


def test_account_operation_project_round_trips_core_contract():
    task = ContentTask(task_id="task_001", title="开业福利笔记", topic="新店开业")
    project = AccountOperationProject(
        project_id="ops_001",
        name="春日花房小红书代运营",
        status="planning",
        client_brief=ClientBrief(
            client_name="花店主理人",
            brand_name="春日花房",
            goals=["涨粉"],
            audience=["周边 3 公里用户"],
        ),
        account_positioning={"persona": "懂生活的社区花艺顾问"},
        operation_plan=OperationPlan(
            plan_id="plan_30d",
            horizon_days=30,
            objectives=["建立本地认知"],
            content_pillars=["花艺知识", "门店日常"],
            kpi_targets={"followers": 300},
            milestones=[{"day": 7, "target": "完成账号基础搭建"}],
        ),
        kpi_plan=KPIPlan(
            plan_id="kpi_30d",
            horizon_days=30,
            targets={"followers": 300},
            milestones=[{"day": 7, "target": "完成账号基础搭建"}],
        ),
        content_calendar=ContentCalendar(calendar_id="cal_30d", tasks=[task]),
        content_tasks=[task],
        content_packages=[
            ContentPackage(
                package_id="pkg_001",
                task_id="task_001",
                title="开业福利别错过",
                body="春日花房开业啦。",
                tags=["花店", "开业"],
                cover_path="/tmp/cover.png",
            )
        ],
        compliance_reviews=[
            ComplianceReview(
                review_id="review_001",
                package_id="pkg_001",
                task_id="task_001",
                status="passed",
                score=9,
            )
        ],
        metrics_snapshots=[
            MetricsSnapshot(
                snapshot_id="metric_001",
                ref_id="pkg_001",
                captured_at="2026-05-08",
                metrics={"likes": 120},
            )
        ],
        strategy_iterations=[
            StrategyIteration(
                iteration_id="iter_001",
                project_id="ops_001",
                diagnosis=["节日节点表现更好"],
                next_actions=["增加节日花束选题"],
            )
        ],
        artifacts={"workspace": "runs/ops_001"},
    )

    data = project.to_dict()
    restored = AccountOperationProject.from_dict(data)

    assert restored.to_dict() == data
    assert restored.client_brief.brand_name == "春日花房"
    assert restored.operation_plan.kpi_targets["followers"] == 300
    assert restored.kpi_plan.targets["followers"] == 300
    assert restored.content_calendar.tasks[0].task_id == "task_001"
    assert restored.content_tasks[0].topic == "新店开业"
    assert restored.content_packages[0].package_id == "pkg_001"
    assert restored.compliance_reviews[0].score == 9
    assert restored.metrics_snapshots[0].metrics["likes"] == 120
    assert restored.strategy_iterations[0].next_actions == ["增加节日花束选题"]


def test_workflow_models_are_owned_by_canonical_modules():
    assert AccountOperationProject.__module__ == "nori.core.project"
    assert ContentTask.__module__ == "nori.core.planning_models"
    assert KPIPlan.__module__ == "nori.core.planning_models"
    assert ContentPackage.__module__ == "nori.agents.content_generation.schemas.generation"
    assert ComplianceReview.__module__ == "nori.agents.learning_loop.schemas.learning"
    assert MetricsSnapshot.__module__ == "nori.agents.learning_loop.schemas.learning"
    assert StrategyIteration.__module__ == "nori.agents.learning_loop.schemas.learning"
