"""Main-chat supervisor agent for routing user requests into Nori tools."""
from __future__ import annotations

import json
from typing import Any

from nori.core import AgentBase, LLMFactory

from .schemas import (
    SupervisorIntent,
    SupervisorTool,
    SupervisorToolCall,
    SupervisorToolRequest,
    SupervisorToolResult,
    SupervisorTurnResult,
)


class SupervisorDecisionError(RuntimeError):
    """Raised when an LLM supervisor decision cannot be parsed."""


class NoriSupervisorAgent(AgentBase):
    """Route one user-facing chat turn to a subagent or subworkflow tool.

    The supervisor owns intent/tool selection and result synthesis. Concrete
    subworkflow execution is injected through `SupervisorTool.handler`, so this
    agent can orchestrate without importing workflow runtime modules.
    """

    stage_name = "nori_supervisor"

    def __init__(
        self,
        *,
        tools: list[SupervisorTool] | None = None,
        use_llm: bool = True,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)
        self.tools = list(default_supervisor_tools() if tools is None else tools)

    def run(
        self,
        user_message: str,
        *,
        session_id: str = "",
        task_id: str = "",
        context: dict[str, Any] | None = None,
        execute: bool = True,
        use_llm: bool | None = None,
    ) -> SupervisorTurnResult:
        message = str(user_message or "").strip()
        decision = (
            self._llm_decision(message, context=context or {}, tools=self.tools)
            if self.should_use_llm(use_llm)
            else None
        )
        selected_tool = _selected_tool(decision, self.tools, message)
        if selected_tool is None:
            return _clarification_result(message, decision=decision)

        intent = _intent_for(decision, selected_tool, message)
        arguments = {
            **intent.arguments,
            "user_message": message,
        }
        tool_call = SupervisorToolCall(
            tool_name=selected_tool.name,
            arguments=arguments,
            reason=intent.rationale or _reason_for(selected_tool, message),
        )
        if not execute or selected_tool.handler is None:
            return SupervisorTurnResult(
                status="planned",
                intent=intent,
                selected_tool=selected_tool.name,
                tool_call=tool_call,
                assistant_message=_planned_message(selected_tool),
                metadata={
                    "tool_catalog": [tool.to_dict() for tool in self.tools],
                    "execute": execute,
                    "has_handler": selected_tool.handler is not None,
                },
            )

        request = SupervisorToolRequest(
            user_message=message,
            intent=intent,
            session_id=session_id,
            task_id=task_id,
            context=dict(context or {}),
            arguments=arguments,
            metadata={"tool": selected_tool.to_dict()},
        )
        try:
            raw_result = selected_tool.handler(request)
            tool_result = _normalize_tool_result(raw_result)
        except Exception as exc:
            tool_result = SupervisorToolResult(
                status="failed",
                message=f"{type(exc).__name__}: {exc}",
                metadata={"tool_name": selected_tool.name},
            )
        status = "completed" if tool_result.status in {"succeeded", "success", "completed"} else tool_result.status
        return SupervisorTurnResult(
            status=status,
            intent=intent,
            selected_tool=selected_tool.name,
            tool_call=tool_call,
            tool_result=tool_result,
            assistant_message=tool_result.message or _completed_message(selected_tool, tool_result),
            artifact_refs=list(tool_result.artifact_refs),
            metadata={
                "tool_catalog": [tool.to_dict() for tool in self.tools],
                "execute": execute,
            },
        )

    def _llm_decision(
        self,
        user_message: str,
        *,
        context: dict[str, Any],
        tools: list[SupervisorTool],
    ) -> dict[str, Any] | None:
        if not user_message or not tools:
            return None
        system = (
            "You are NoriSupervisorAgent. Route the user request to exactly one Nori tool. "
            "Return JSON with keys: intent{name,summary,confidence,arguments}, tool_name, rationale. "
            "Only choose a tool_name from the provided tool catalog. If unclear, use an empty tool_name."
        )
        user = {
            "user_message": user_message,
            "context": context,
            "tools": [tool.to_dict() for tool in tools],
        }
        user_prompt = json.dumps(user, ensure_ascii=False, sort_keys=True)
        try:
            decision = self.call_messages_json(
                messages=self.messages(system, user_prompt),
                error_type=SupervisorDecisionError,
                timeout=30,
                usage="supervisor_router",
            )
        except Exception:
            return None
        return decision if isinstance(decision, dict) else None


def default_supervisor_tools() -> list[SupervisorTool]:
    """Return the built-in Nori tool catalog without concrete handlers."""

    return [
        SupervisorTool(
            name="content_production",
            description="Run the full content-production workflow from brief/assets to package/review artifacts.",
            intent_names=("generate_content", "run_content_workflow"),
            keywords=("生成", "产出", "小红书", "图文", "笔记", "视频", "公众号", "content", "generate"),
            is_workflow=True,
            metadata={"owner": "nori.workflows.content_production"},
        ),
        SupervisorTool(
            name="content_design_spec",
            description="Create an inspectable content design spec before artifact generation.",
            intent_names=("create_design_spec",),
            keywords=("spec", "design spec", "设计", "方案", "策略", "内容规格"),
            metadata={"owner": "nori.agents.content_generation.ContentSpecAgent"},
        ),
        SupervisorTool(
            name="artifact_generation",
            description="Instantiate a content design spec into concrete copy/image artifacts.",
            intent_names=("generate_artifact",),
            keywords=("实例化", "生成图片", "封面", "文案", "artifact", "cover"),
            metadata={"owner": "nori.agents.content_generation.ArtifactGenerationAgent"},
        ),
        SupervisorTool(
            name="market_analysis",
            description="Analyze market hotspots, competitor notes, and reusable content skills.",
            intent_names=("analyze_market", "learn_skill"),
            keywords=("热点", "市场", "竞品", "小红书案例", "skill", "分析", "趋势"),
            metadata={"owner": "nori.agents.market_analysis.XHSNoteAnalyzer"},
        ),
        SupervisorTool(
            name="review_content_package",
            description="Review a generated content package for compliance and task consistency.",
            intent_names=("review_content",),
            keywords=("审核", "检查", "review", "能不能发", "合规", "质量"),
            metadata={"owner": "nori.agents.learning_loop.ReviewGateAgent"},
        ),
        SupervisorTool(
            name="session_memory",
            description="Query or update session/task memory for the current user interaction.",
            intent_names=("query_memory", "update_memory"),
            keywords=("记忆", "上下文", "session", "历史", "偏好"),
            metadata={"owner": "nori.memory"},
        ),
    ]


def _selected_tool(decision: dict[str, Any] | None, tools: list[SupervisorTool], message: str) -> SupervisorTool | None:
    tool_by_name = {tool.name: tool for tool in tools}
    decision_tool = str((decision or {}).get("tool_name") or "").strip()
    if decision_tool in tool_by_name:
        return tool_by_name[decision_tool]
    return _keyword_selected_tool(tools, message)


def _keyword_selected_tool(tools: list[SupervisorTool], message: str) -> SupervisorTool | None:
    normalized = message.lower()
    best: tuple[int, SupervisorTool] | None = None
    for tool in tools:
        score = sum(1 for keyword in tool.keywords if str(keyword).lower() and str(keyword).lower() in normalized)
        if score <= 0:
            continue
        if best is None or score > best[0]:
            best = (score, tool)
    return best[1] if best else None


def _intent_for(decision: dict[str, Any] | None, tool: SupervisorTool, message: str) -> SupervisorIntent:
    intent_data = (decision or {}).get("intent")
    if isinstance(intent_data, dict):
        intent = SupervisorIntent.from_dict({
            **intent_data,
            "rationale": str((decision or {}).get("rationale") or intent_data.get("rationale") or ""),
        })
        if intent.name and intent.name != "unknown":
            return intent
    return SupervisorIntent(
        name=tool.intent_names[0] if tool.intent_names else tool.name,
        summary=message[:160],
        confidence=0.55,
        rationale=_reason_for(tool, message),
    )


def _reason_for(tool: SupervisorTool, message: str) -> str:
    matched = [keyword for keyword in tool.keywords if str(keyword).lower() in message.lower()]
    if matched:
        return f"matched keywords: {', '.join(str(item) for item in matched[:3])}"
    return f"selected tool {tool.name}"


def _normalize_tool_result(value: Any) -> SupervisorToolResult:
    if isinstance(value, SupervisorToolResult):
        return value
    if isinstance(value, dict):
        if any(key in value for key in {"status", "message", "output", "artifact_refs", "metadata"}):
            return SupervisorToolResult.from_dict(value)
        return SupervisorToolResult(output=dict(value))
    return SupervisorToolResult(output={"value": value})


def _clarification_result(message: str, *, decision: dict[str, Any] | None) -> SupervisorTurnResult:
    intent = SupervisorIntent(
        name="unknown",
        summary=message[:160],
        confidence=0.0,
        rationale=str((decision or {}).get("rationale") or ""),
    )
    return SupervisorTurnResult(
        status="needs_clarification",
        intent=intent,
        assistant_message="我需要先确认你想让 Nori 做哪类工作。",
        next_questions=[
            "你是想生成内容、做设计 spec、分析热点、审核已有内容，还是查询上下文记忆？",
        ],
        metadata={"llm_decision": decision or {}},
    )


def _planned_message(tool: SupervisorTool) -> str:
    if tool.handler is None:
        return f"已选择 {tool.name}，但当前没有绑定执行 handler。"
    return f"已规划调用 {tool.name}，等待执行确认。"


def _completed_message(tool: SupervisorTool, result: SupervisorToolResult) -> str:
    if result.artifact_refs:
        return f"{tool.name} 已完成，产生 {len(result.artifact_refs)} 个 artifact。"
    return f"{tool.name} 已完成。"


__all__ = ["NoriSupervisorAgent", "SupervisorDecisionError", "default_supervisor_tools"]
