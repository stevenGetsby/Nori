# Nori Account-Ops SOP System

## Positioning

Nori should become an account-operations SOP Agent system, not only a one-shot content generator.

The closed loop:

```text
规划账号 -> 制作内容 -> 发布运营 -> 数据复盘 -> 策略优化 -> 下一轮内容
```

## Stage A: Account Planning

| Step | System Module | Output |
| --- | --- | --- |
| A1 需求沟通 | Intake / Client Brief | goals, audience, budget, taboos, platform |
| A2 素材交接 | Asset Store | brand assets, product docs, images, links |
| A3 竞品与行业分析 | Research Agent | competitors, high-performing notes, trends |
| A4 账号定位 | Account Planner | persona, positioning, differentiated value |
| A5 运营计划 | Operation Planner | monthly/quarterly strategy |
| A6 KPI 与里程碑 | KPI Planner | follower, exposure, engagement, conversion goals |
| A7 排期规划 | Calendar Planner | content calendar, publish windows, themes |
| A8 账号搭建与合规 | Compliance Setup | profile rules, red lines, account norms |

## Stage B: Content Production And Operations

| Step | System Module | Output |
| --- | --- | --- |
| B1 选题策划 | Topic Planner | topic pool, content briefs |
| B2 素材搜集 | Asset Collector | usable images, cases, reference content |
| B3 内容制作 | Content Generator | title, body, tags, cover, images |
| B4 合规前置审核 | Compliance Reviewer | risks, required changes |
| B5 审核与发布 | Publish Workflow | publish-ready package, publish record |
| B6 互动与社群运营 | Community Operator | comment replies, DM scripts |
| B7 数据监测 | Metrics Monitor | exposure, likes, saves, comments, conversions |
| B8 复盘分析 | Review Analyzer | performance diagnosis and attribution |

## Stage C: Strategy Optimization

| Step | System Module | Output |
| --- | --- | --- |
| C1 策略优化 | Strategy Optimizer | next topic direction, structure adjustments |
| C2 多平台适配 | Platform Adapter | XHS/Douyin/Video Account/WeChat variants |

Delay Stage C2 until the single-platform backend loop is stable.

## Core Data Model

```text
AccountOperationProject
  client_brief
  asset_library
  competitor_research
  account_positioning
  operation_plan
  kpi_plan
  content_calendar
  content_tasks[]
  content_packages[]
  compliance_reports[]
  publish_records[]
  metrics_snapshots[]
  strategy_iterations[]
```

## Minimal Implementable Loop

Implement this first:

```text
需求沟通
-> 账号定位
-> 运营计划
-> 内容排期
-> 选题策划
-> 内容制作
-> 合规审核
-> 复盘优化
```

Do not implement real publishing, automatic comments, or multi-platform sync until the backend loop is stable.
