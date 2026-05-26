from __future__ import annotations

import inspect

import llms
from nori.core import AgentBase, LLMFactory, WorkflowBase, named_workflow_steps
from nori.core import contracts
from nori.content_generation.content_producer import ContentProducerAgent
from nori.content_generation.cover_director import CoverDirectorAgent
from nori.content_generation.note_maker import NoteMakerAgent
from nori.context_building.calendar_planner import CalendarPlannerAgent
from nori.context_building.kpi_planner import KPIPlannerAgent
from nori.context_building.operation_planner import OperationPlannerAgent
from nori.learning_loop.review import ComplianceReviewerAgent, ConsistencyReviewerAgent, ReviewGateAgent
from nori.learning_loop.strategy import MetricsSnapshotAgent, StrategyIterationAgent
from nori.market_analysis.xhs_note_analyzer import XHSNoteAnalyzer
from nori.user_profiling.account_planner import AccountPlannerAgent
from nori.user_profiling.intaker import IntakeAgent


AGENT_CLASSES = [
    IntakeAgent,
    AccountPlannerAgent,
    NoteMakerAgent,
    CoverDirectorAgent,
    ContentProducerAgent,
    OperationPlannerAgent,
    KPIPlannerAgent,
    CalendarPlannerAgent,
    ComplianceReviewerAgent,
    ConsistencyReviewerAgent,
    ReviewGateAgent,
    MetricsSnapshotAgent,
    StrategyIterationAgent,
    XHSNoteAnalyzer,
]


def test_core_exports_runtime_base_abstractions():
    assert LLMFactory.__module__ == "nori.core.llm"
    assert AgentBase.__module__ == "nori.core.agent"
    assert WorkflowBase.__module__ == "nori.core.workflow"
    assert contracts.ProviderConfig.__module__ == "nori.core.contracts"
    assert contracts.LLMClientConfigError.__module__ == "nori.core.contracts"


def test_llm_factory_delegates_to_project_llm_gateway():
    calls = []

    def chat(messages, **kwargs):
        calls.append(("chat", messages, kwargs))
        return '{"ok": true}'

    def chat_json(messages, **kwargs):
        calls.append(("chat_json", messages, kwargs))
        return {"ok": True}

    factory = LLMFactory(chat_func=chat, chat_json_func=chat_json)
    messages = [{"role": "user", "content": "hello"}]

    assert factory.chat(messages, usage="unit") == '{"ok": true}'
    assert factory.chat_json(messages, usage="unit", json_mode=True) == {"ok": True}
    assert calls == [
        ("chat", messages, {"usage": "unit"}),
        ("chat_json", messages, {"usage": "unit", "json_mode": True, "_chat": chat}),
    ]


def test_agent_base_provides_shared_json_helpers():
    class DemoError(RuntimeError):
        pass

    agent = AgentBase(stage_name="demo", llm_factory=LLMFactory(chat_json_func=lambda *_args, **_kwargs: {"ok": 1}))

    assert agent.messages("sys", "usr") == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ]
    assert agent.call_json(system="sys", user="usr", error_type=DemoError) == {"ok": 1}


def test_workflow_base_runs_named_steps_in_order():
    class DemoWorkflow(WorkflowBase):
        def run(self, value):
            return self.run_steps(value)

    workflow = DemoWorkflow(
        workflow_name="demo_workflow",
        steps=[
            ("double", lambda value: value * 2),
            ("increment", lambda value: value + 1),
        ],
    )

    assert workflow.run(3) == 7
    assert workflow.step_names == ["double", "increment"]


def test_named_workflow_steps_declare_noop_stage_names():
    workflow = WorkflowBase(workflow_name="declared", steps=named_workflow_steps("ingest", "emit"))

    assert workflow.step_names == ["ingest", "emit"]
    assert workflow.run_steps({"value": 1}) == {"value": 1}


def test_concrete_agents_inherit_agent_base_and_keep_run_entrypoint():
    for agent_class in AGENT_CLASSES:
        assert issubclass(agent_class, AgentBase), agent_class
        assert "run" in agent_class.__dict__, agent_class
        assert inspect.isfunction(agent_class.__dict__["run"]), agent_class


def test_llm_factory_defaults_to_project_gateway():
    factory = LLMFactory()

    assert factory.chat_func is llms.chat
    assert factory.chat_json_func is llms.chat_json
