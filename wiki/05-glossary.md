<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# Glossary

| Term | Meaning | Canonical owner |
| --- | --- | --- |
| Intention | User goal, content format, tone, anti-preferences, and task intent. | `IntakeAgent` / `nori.agents.user_profiling.models.IntakeResult` |
| Context | User assets and constraints: creative assets, commercial assets, guardrails, data references. | `IntakeAgent` |
| UserAsset | One image or text asset. Image assets may carry `vision_roles`, `subject`, `brand_signals`, `usable_for`, `quality`. | `nori/core/asset_models.py` |
| NoteSkill | Reusable XHS note-making skill learned from evidence or provided by fixtures. | `nori/agents/market_analysis/models.py` |
| NoteDraft | Title, body, tags, comment hook, selected skill, asset bundle, cover seed. | `nori/agents/content_generation/models.py` |
| CoverResult | Generated cover path, prompt, size, reference paths, and source metadata. | `nori/agents/content_generation/models.py` |
| ClientBrief | Client-facing account-ops requirements: goals, audience, platform, constraints, source materials. | `nori/core/planning_models.py` |
| OperationPlan | Strategy, horizon, objectives, content pillars, cadence, KPI targets, milestones, risks. | `nori/core/planning_models.py` |
| KPIPlan | Measurable targets and manual measurement notes for an operation plan. | `nori/core/planning_models.py` |
| ContentCalendar | Scheduled content themes and `ContentTask` list. | `nori/core/planning_models.py` |
| ContentTask | One planned content unit that should later bridge into content generation. | `nori/core/planning_models.py` |
| ContentPackage | Generated title/body/tags/cover/images attached to a content task. | P3 production bridge |
| ComplianceReview | Review report for a generated package before publish/export handoff; currently used by compliance and consistency reviewers. | P4 review gate |
| MetricsSnapshot | Manual or future platform metric observation for a package, task, or operation cycle. | P4 iteration loop |
| StrategyIteration | Review and metrics synthesis that produces diagnosis, decisions, and next actions for the next cycle. | P4 iteration loop |
| AccountPositioning | Typed account positioning snapshot derived from `AccountPlanResult`; includes positioning, audience, pillars, keywords, cover formats, and benchmark refs. | P1 account-ops backend |
| AssetRecord | One client/source/generated asset reference with usage, status, tags, source, and metadata. | `nori/core/asset_models.py` |
| AssetLibrary | Typed project-level index for client/source/generated assets. | `nori/core/asset_models.py` |
| CompetitorResearch | Typed project-level benchmark evidence set for competitor or reference notes. | P1 account-ops backend |
| DataCollector | Unified data collection facade over crawler/sign/downloader services. | `data_collect/adapter.py` |
| GHC mode | Local GitHub Copilot proxy mode checked via `/models`; selected with `NORI_MODE=ghc`. | `llms/mode.py` |
