from __future__ import annotations

from nori.agents.supervisor import (
    NoriSupervisorAgent,
    SupervisorTool,
    SupervisorToolResult,
    default_supervisor_tools,
)
from nori.core import LLMFactory


def test_supervisor_invokes_matching_subworkflow_tool_from_user_chat():
    calls = []

    def handler(request):
        calls.append(request)
        return SupervisorToolResult(
            status="succeeded",
            message="content package generated",
            output={"package_id": "pkg_001"},
            artifact_refs=["runs/demo/content_package.json"],
        )

    agent = NoriSupervisorAgent(
        tools=[
            SupervisorTool(
                name="content_production",
                description="Run the full content production workflow.",
                intent_names=("generate_content",),
                keywords=("生成", "小红书", "图文", "笔记"),
                handler=handler,
                is_workflow=True,
            )
        ],
        use_llm=False,
    )

    result = agent.run(
        "帮我生成一篇热点小红书图文",
        session_id="session_001",
        task_id="task_001",
        context={"platform": "xhs"},
    )

    assert result.status == "completed"
    assert result.intent.name == "generate_content"
    assert result.selected_tool == "content_production"
    assert result.tool_call is not None
    assert result.tool_call.arguments["user_message"] == "帮我生成一篇热点小红书图文"
    assert result.tool_result is not None
    assert result.tool_result.output == {"package_id": "pkg_001"}
    assert result.artifact_refs == ["runs/demo/content_package.json"]
    assert calls[0].session_id == "session_001"
    assert calls[0].task_id == "task_001"
    assert calls[0].context == {"platform": "xhs"}


def test_supervisor_can_plan_without_executing_the_selected_tool():
    called = False

    def handler(_request):
        nonlocal called
        called = True
        return SupervisorToolResult(status="succeeded")

    agent = NoriSupervisorAgent(
        tools=[
            SupervisorTool(
                name="content_design_spec",
                description="Create a design spec before generation.",
                intent_names=("create_design_spec",),
                keywords=("spec", "设计", "方案"),
                handler=handler,
            )
        ],
        use_llm=False,
    )

    result = agent.run("先帮我做一个设计 spec", execute=False)

    assert result.status == "planned"
    assert result.intent.name == "create_design_spec"
    assert result.selected_tool == "content_design_spec"
    assert result.tool_result is None
    assert called is False


def test_supervisor_asks_for_clarification_when_no_tool_matches():
    agent = NoriSupervisorAgent(tools=[], use_llm=False)

    result = agent.run("你好，我们聊一下")

    assert result.status == "needs_clarification"
    assert result.intent.name == "unknown"
    assert result.selected_tool == ""
    assert result.tool_call is None
    assert result.tool_result is None
    assert result.next_questions


def test_supervisor_uses_structured_llm_decision_when_enabled():
    calls = []

    def chat_json(_messages, **_kwargs):
        return {
            "intent": {
                "name": "review_content",
                "summary": "用户想审核内容包",
                "confidence": 0.88,
                "arguments": {"package_id": "pkg_001"},
            },
            "tool_name": "review_content_package",
            "rationale": "审核请求应进入 review gate",
        }

    def handler(request):
        calls.append(request)
        return SupervisorToolResult(status="succeeded", output={"review_status": "passed"})

    agent = NoriSupervisorAgent(
        tools=[
            SupervisorTool(
                name="review_content_package",
                description="Review a generated content package.",
                intent_names=("review_content",),
                keywords=("审核", "检查", "review"),
                handler=handler,
            )
        ],
        llm_factory=LLMFactory(chat_json_func=chat_json),
        use_llm=True,
    )

    result = agent.run("检查 pkg_001 这版内容能不能发")

    assert result.status == "completed"
    assert result.intent.name == "review_content"
    assert result.intent.arguments == {"package_id": "pkg_001"}
    assert result.selected_tool == "review_content_package"
    assert result.tool_result is not None
    assert result.tool_result.output == {"review_status": "passed"}
    assert calls[0].intent.arguments == {"package_id": "pkg_001"}


def test_default_supervisor_tools_describe_existing_nori_subsystems_without_handlers():
    tools = {tool.name: tool for tool in default_supervisor_tools()}

    assert {
        "content_production",
        "content_design_spec",
        "artifact_generation",
        "market_analysis",
        "review_content_package",
        "session_memory",
    } <= set(tools)
    assert tools["content_production"].is_workflow is True
    assert tools["content_production"].handler is None
