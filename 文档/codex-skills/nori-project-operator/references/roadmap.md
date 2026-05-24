# Nori Implementation Roadmap

## Product Target

Build Nori into an account-operations Agent system:

```text
需求沟通 -> 素材交接 -> 竞品/行业分析 -> 账号定位 -> 运营计划
-> KPI/里程碑 -> 排期 -> 内容策划 -> 素材搜集 -> 内容制作
-> 合规审核 -> 发布预留 -> 互动运营 -> 数据监测 -> 复盘 -> 策略优化
```

## Priority Order

### P0: Stabilize Existing Core

1. LLM gateway hardening: secret handling, vision usage routing, central JSON helper, tests.
2. Document the true executable chain and remove/mark stale doc claims.
3. Keep `python -m pytest tests -q` green.

### P1: Account-Ops Backend Models

Add project-level models before adding new agents:

- `AccountOperationProject`
- `ClientBrief`
- `AssetLibrary`
- `CompetitorResearch`
- `AccountPositioning`
- `OperationPlan`
- `KPIPlan`
- `ContentCalendar`
- `ContentTask`
- `ContentPackage`
- `ComplianceReview`
- `PublishRecord`
- `MetricsSnapshot`
- `StrategyIteration`

Use dataclasses first unless the repo moves to Pydantic.

### P2: Planning Agents

Add ops agents in small increments:

- `OperationPlanner`: account plan -> weekly/monthly operation plan.
- `KPIPlanner`: plan -> measurable milestones.
- `CalendarPlanner`: plan -> content calendar.
- `TopicPlanner`: account plan + calendar -> topic pool and task briefs.

### P3: Production Orchestration

Bridge ops models to existing generation:

- content task -> `NoteMakerAgent`;
- task assets -> `CoverDirectorAgent`;
- generated package -> review contract.

### P4: Review and Iteration

Add:

- `ComplianceReviewer`
- `ContentConsistencyReviewer`
- `ReviewAnalyzer`
- `StrategyOptimizer`

Start with text-only/mocked tests, then add optional live smoke scripts.

### Later

Delay until backend loop is stable:

- real publish adapter;
- automatic community operations;
- automatic metrics ingestion;
- multi-platform adaptation;
- full frontend workbench.

## Per-Iteration Definition of Done

Each automated iteration should finish with:

- one small task completed or a documented blocker;
- focused tests added/updated;
- tests run and reported;
- progress document updated;
- next task named.
