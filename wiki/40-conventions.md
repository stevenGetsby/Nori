<!-- Last verified: 2026-05-26 | Current stage: P1 Account-Ops Backend -->

# Conventions

## Implementation

| Area | Rule |
| --- | --- |
| Models | Use dataclasses and explicit `to_dict`/`from_dict` in current backend layer. Do not introduce a DB or Pydantic unless a stage spec says so. |
| Dataclass compatibility | Shared model/result classes that need `slots=True` must import `dataclass` and `field` from `nori._compat`, not directly from stdlib `dataclasses`. |
| Model coercion | `from_dict()` methods should use shared helpers from `nori.core.contracts` for mapping/list/string/int/bool cleanup instead of duplicating private helper functions per model file. Do not use plain `bool(value)` for persisted strings such as `"false"`. |
| Shared layer dependencies | `nori/shared` may provide provider/runtime utilities, but must not import the five business modules. Business-specific helpers should live with their owning module, such as NoteSkill fixture IO in `nori.agents.market_analysis.note_skill_fixture`. |
| Business module package roots | Keep lightweight model/domain-contract exports eager. Route facade and concrete stage exports through `nori.core.lazy_exports.lazy_export` so public imports stay stable without reintroducing domain-module cycles. |
| Upstream facade dependencies | `UserProfilingFacade` and `MarketAnalysisFacade` should consume project-like dict/object shapes and must not import downstream business modules such as `nori.agents.planning`; architecture tests enforce this. |
| Workflow stage package layout | Each concrete runtime stage owns a package folder with a specifically named entry module plus its helper modules. Do not keep physical flat helper modules in canonical domains, and do not reintroduce compatibility aliases for removed roots. Add implementation only inside the owning stage folder. |
| Workflow stage package exports | Stage package `__init__.py` files should expose only explicit public entrypoints through `__all__`; tests that patch `llms` or other internals should import the concrete entry module, not the package root. |
| LLM calls | Route through `llms.*`; do not instantiate OpenAI clients inside workflow stages. |
| JSON LLM output | Prefer `llms.chat_json(...)` unless a helper intentionally returns structured error instead of exception. |
| JSON LLM stages | Required workflow stages that should raise domain-specific errors should use `nori.shared.call_stage_json(...)` instead of local `try/except llms.ChatJSONError` wrappers. |
| Pre-built JSON messages | Required JSON stages that need custom/multimodal messages should use `nori.shared.call_stage_messages_json(...)`, not direct `llms.chat_json(...)`. |
| Optional planner JSON stages | Planning stages that must preserve deterministic fallback should use `nori.shared.try_stage_json(...)`; optional stages that already build custom/multimodal messages should use `nori.shared.try_stage_messages_json(...)`. Store returned `error` metadata on the fallback artifact, preserving `reason=parse_error` vs `reason=empty_response`. |
| LLM fallback errors | Use `nori.shared.attach_llm_error(target, stage, error)` instead of per-stage helper functions so `metadata.llm_error` and `validation.llm_error` stay consistent. |
| Intake package contract | Keep text and vision prompt contracts in class-owned `nori.agents.user_profiling.intaker.package`; `IntakeAgent` and image tagging code should use builders instead of a shared `prompts.py` constants module. |
| Intake text normalization | Keep deterministic text fallback, optional text-LLM output cleanup, image-context construction, and metadata preservation in `nori.agents.user_profiling.intaker.normalizer`; `IntakeAgent` should only orchestrate text LLM and vision tagging. |
| Intake taxonomy | Keep goal/format/tone/asset/guardrail/data vocabularies, alias mapping, allowed-label cleanup, rule-based classification, and missing/question fallback text in `nori.agents.user_profiling.intaker.taxonomy`; `intake_normalizer` should assemble `IntakeResult`, not own taxonomy rules. |
| Intake vision tagging | Keep per-image multimodal tagging, tag vocabulary filtering, and image-tag failure isolation in `nori.agents.user_profiling.intaker.image_tagger`; `IntakeAgent` should only decide when to call it and how to attach resulting assets. |
| NoteMaker package contract | Keep skill selection, asset curation, note composition, prompt construction, selected-index normalization, and note-field cleanup in class-owned `nori.agents.content_generation.note_maker.package`; `NoteMakerAgent` should only orchestrate skill -> assets -> note draft. |
| CoverDirector package contract | Keep reference selection, reference input conversion, cover prompt construction, and related constants in class-owned `nori.agents.content_generation.cover_director.package`; `CoverDirectorAgent` should orchestrate reference selection, prompt writing, image generation, and persistence. |
| CoverDirector output persistence | Keep data-uri decoding, remote image download, filename sanitization, and output-domain error translation in `nori.agents.content_generation.cover_director.output`; `CoverDirectorAgent` should not own persistence mechanics. |
| AccountPlanner package contract | Keep `AccountPlannerInput` restoration, evidence merging, asset prompt context, and JSON-only planning prompt construction in class-owned `nori.agents.user_profiling.account_planner.package`; `AccountPlannerAgent` should orchestrate normalized input, search enrichment, and LLM calls only. |
| AccountPlanner fallback | Keep deterministic no-inference fallback result construction in `nori.agents.user_profiling.account_planner.fallback`; fallback may preserve platform and explicit goal but must not infer keywords, positioning, benchmarks, or IP portrait content without LLM/search evidence. |
| AccountPlanner search | Keep search provider protocol/fallback, keyword cleanup/dedupe, platform id normalization, provider-error isolation, and row defaulting in `nori.agents.user_profiling.account_planner.search`; `AccountPlannerAgent` should orchestrate search enrichment, not own provider mechanics. |
| AccountPlanner result normalization | Keep LLM result cleanup, search-only merge behavior, and `AccountPlanResult` assembly in `nori.agents.user_profiling.account_planner.normalizer`; `AccountPlannerAgent` should own orchestration, not output-shape mechanics. |
| AccountPlanner portrait normalization | Keep benchmark-account cleanup, IP portrait account names/keywords/pillars/creators/cover formats, and search-only benchmark creator refresh in `nori.agents.user_profiling.account_planner.portrait`; the result normalizer should delegate report mechanics. |
| AccountPlanner keyword normalization | Keep platform-token stripping, keyword-level normalization, reason fallback, search-keyword fallback, and keyword dedupe in `nori.agents.user_profiling.account_planner.keywords`; `account_plan_normalizer` should only call this boundary while assembling `AccountPlanResult`. |
| Tests | Default tests must not require live LLM, crawler, signing service, image generation, or real platform cookies. |
| Live workflows | Put live calls in `scripts/smoke_*.py` or explicitly marked tests. |
| Secrets | Do not write API keys/cookies to docs, logs, or fixtures. |
| Runtime config | Commit only `api_config.example.yaml`; keep private `api_config.yaml` ignored and prefer `api_key_env`. Model scalar fields from config should be normalized through shared coercion before reaching `ResolvedModel`. |
| Runtime config models | Keep `ProviderConfig`, `ModelConfig`, and `ResolvedModel` in `nori.core.contracts`; `nori.core` and `nori_config` may expose them, but should not own their definitions. |
| Runtime config normalization | Keep provider/model key parsing, mode/env-name cleanup, section-shape validation, and flat/nested `active_models` selection in `nori.config_normalization`; `NoriConfig` should own file loading and dataclass assembly only. |
| LLM chat execution | Keep sync/async chat client resolution, kwargs merging, capability guards, provider text extraction, and chat telemetry in `llms.chat_runner`; `llms.call` should expose thin public facades and JSON/image orchestration only. |
| LLM image execution | Keep active image-model resolution, reference input filtering, capability guards, provider dispatch, result validation, and image telemetry in `llms.image_runner`; `llms.call.image` should stay a thin public facade while preserving old monkeypatch compatibility. |
| LLM kwargs merging | Gateway helpers may inject model-level `temperature_fixed`, `max_output`, and `extra_body`, but must not mutate caller-provided kwargs or nested `extra_body` dicts. |
| Token limit parameter | Gateway kwargs must emit only the token-limit parameter expected by the active model: GPT-5 uses `max_completion_tokens`; other chat models use `max_tokens`. |
| Structured LLM helper results | Keep `StructuredCallResult`, `IntentLLMResult`, and `TargetSelectionResult` in `nori.core.contracts`; `llms`, intent, target, and call modules may expose them, but should not own their definitions. |
| Structured LLM helper prompts | Keep intent field descriptions, enum/candidate prompt text, target selector catalogs, history formatting, and summary truncation in `llms.structured_prompts`; `intent_extractor.py` and `target_selector.py` should own orchestration only. |
| Structured LLM helper normalization | Keep intent field-node cleanup, enum/candidate filtering, selector option cleanup, confidence fallback, and alternative selector filtering in `llms.structured_outputs`; intent/target helpers should not duplicate normalization mechanics. |
| Structured LLM helper calls | Keep non-throwing JSON-mode call handling, parse-error classification, raw capture, and provider-exception wrapping in `llms.structured_calls`; intent/target helpers should not duplicate try/except plumbing. |
| Stage boundaries | Intake sees images semantically; CoverDirector reads image bytes; NoteMaker consumes tags and text only. |
| Fallbacks | Planning stages may keep deterministic fallback; generation stages may fail loudly when LLM stages are required. |
| Market-analysis note loading | Keep local XHS `meta.json` reading, author fallback, tag extraction, and platform metric count parsing in `nori.agents.market_analysis.xhs_note_analyzer.loader`; `XHSNoteAnalyzer` should orchestrate analysis and collection, not own file-IO parsing details. |
| Market-analysis note rules | Keep single-note seed draft construction, scene/goal classification, title/opening/body/interaction/visual rules, CTA evidence, and confidence scoring in `nori.agents.market_analysis.xhs_note_analyzer.rules`; `XHSNoteAnalyzer` should only orchestrate rule draft, optional LLM enhancement, and session collection. |
| Market-analysis package contract | Keep XHS note enhancement, keyword generation, and label prompt contracts in class-owned `nori.agents.market_analysis.xhs_note_analyzer.package`; `note_llm` and `session_llm` should own call orchestration and output normalization only. |
| Market-analysis single-note LLM enhancement | Keep optional JSON routing, LLM output normalization, fallback draft construction, and `llm_error` attachment in `nori.agents.market_analysis.xhs_note_analyzer.note_llm`; `XHSNoteAnalyzer` should only decide whether to call it and pass compatibility-injected chat functions. |
| Market-analysis session clustering | Keep rule-goal fallback classification, required LLM-label coverage checks, top-four bucket selection, tone majority, and leftover note-id tracking in `nori.agents.market_analysis.xhs_note_analyzer.session_clustering`; `XHSNoteAnalyzer` should not own clustering mechanics. |
| Market-analysis session LLM | Keep session keyword generation, hot-note prompt shaping, label normalization, and fail-fast JSON helper routing in `nori.agents.market_analysis.xhs_note_analyzer.session_llm`; `XHSNoteAnalyzer` should only decide when the required stages are called. |
| Market-analysis session reporting | Keep session report stamping, full report JSON writing, and skills-only guide JSON writing in `nori.agents.market_analysis.xhs_note_analyzer.session_reporter`; `XHSNoteAnalyzer` should not own artifact naming or fixture shape. |
| Market-analysis skill building | Keep session `NoteSkill` construction, merged rule aggregation, evidence-note mapping, cover rules, metric percentiles, note-type majority, and cluster signals in `nori.agents.market_analysis.xhs_note_analyzer.skill_builder`; `XHSNoteAnalyzer` should only call it per cluster. |
| OperationPlanner package contract | Keep `ClientBrief` / `AccountPlanResult` restoration, run-window normalization, and JSON-only SOP planning prompt construction in class-owned `nori.agents.planning.operation_planner.package`; `OperationPlannerAgent` should orchestrate prepared inputs, fallback, LLM calls, and critic attachment only. |
| OperationPlanner fallback builder | Keep deterministic project fallback assembly and task/calendar construction in `nori.agents.planning.operation_planner.project_builder`; `OperationPlannerAgent` should not own rule-builder mechanics. |
| OperationPlanner fallback policy | Keep content-pillar/objective/topic/risk/reference derivation, default milestones, project labels, asset defaults, and operation-derived KPI policy in `nori.agents.planning.operation_planner.project_policy`; the builder should call this boundary instead of owning pure fallback rules. |
| OperationPlanner LLM normalization | Keep operation-plan/calendar JSON merging, LLM task-row normalization, milestone/task date clamping, and derived KPI snapshot creation in `nori.agents.planning.operation_planner.normalizer`; `OperationPlannerAgent` should own input normalization, LLM calls, and critic attachment only. |
| KPIPlanner package contract | Keep operation/project/composite-dict restoration, project-context derivation, and JSON-only KPI prompt construction in class-owned `nori.agents.planning.kpi_planner.package`; `KPIPlannerAgent` should orchestrate prepared inputs, LLM calls, and critic attachment only. |
| KPIPlanner normalization | Keep KPI fallback targets, project task-count defaults, KPI LLM output merge, milestone day clamping, and empty measurement-note fallback in `nori.agents.planning.kpi_planner.normalizer`; `KPIPlannerAgent` should own LLM calls and critic attachment only. |
| CalendarPlanner package contract | Keep operation/project/composite-dict restoration, KPI/brief override normalization, run-window selection, and JSON-only calendar prompt construction in class-owned `nori.agents.planning.calendar_planner.package`; `CalendarPlannerAgent` should orchestrate prepared inputs, LLM calls, and critic attachment only. |
| CalendarPlanner normalization | Keep `ContentCalendar` shell construction, LLM calendar merge, and empty-list fallback preservation in `nori.agents.planning.calendar_planner.normalizer`; `CalendarPlannerAgent` should own LLM calls and critic attachment only. |
| CalendarPlanner policy | Keep bounded horizon/start-date rules, task-count limits, scheduled-day clamping, cadence/topic labels, and required asset fallback in `nori.agents.planning.calendar_planner.policy`; normalizer modules should call this boundary instead of duplicating deterministic policy. |
| CalendarPlanner task construction | Keep fallback `ContentTask` rows and LLM task-row cleanup in `nori.agents.planning.calendar_planner.task_builder`; calendar normalizers should not duplicate task-level mapping, priority, brief, asset, or content-pillar defaults. |
| Planner critic policy | Keep Operation/KPI/Calendar structural completeness checks, fallback warnings, task readiness checks, and KPI/calendar alignment in `nori.agents.planning.planner_critics`; planner agents should attach critic metadata, not own critic rules. |
| Content package assembly | Keep deterministic package preparation and final `ContentPackage` assembly in `nori.agents.content_generation.content_producer.package.ContentPackageAssembler`; do not split tiny proxy modules for inputs/provenance/builder unless complexity or reuse justifies it. |
| Intent contract | Freeze user goals, required terms, tone, deliverables, and taboos in `nori.core.IntentContract` before generation. Generation and review stages should consume the contract instead of re-inferring user intent from free text. |
| Artifact checkpoints | Use `nori.core.ArtifactStore` for long-running live flows that need checkpoint/resume; each stage should write a JSON artifact and update `manifest.json` rather than relying on process memory. |
| Generation routing | Use `nori.agents.content_generation.GenerationAgent` as the coarse generation entrypoint. Keep `NoteMakerAgent`, `CoverDirectorAgent`, and `ContentProducerAgent` specialized; the router chooses routes, child agents own domain-specific generation. |
| Stable artifact builders | Shared slug/dedupe behavior belongs in `nori.core.StableArtifactAssembler`; concrete assemblers should inherit it when they produce stable local artifact IDs or media/reference lists. |
| Content production state | Keep production error formatting, note/cover/production stage classification, and task/project success/failure metadata updates in `nori.agents.content_generation.content_producer.state`; `ContentProducerAgent` should call this boundary instead of mutating state inline. |
| Review package contract | Keep persisted package/task/brief restoration and project-derived brief fallback in class-owned `nori.agents.learning_loop.review.package`; reviewer agents should call this boundary before policy evaluation. |
| Review policy | Keep compliance/consistency issue calculation in `nori.agents.learning_loop.review.policy`; reviewer agents should own policy invocation and gate ordering only. |
| Quality review | Use `QualityReviewerAgent` when an `IntentContract` is available so publish readiness checks include user-goal and must-include alignment, not only compliance and package consistency. |
| Review scoring | Keep issue-row construction, severity penalties, score/status mapping, severity counts, and fix suggestions in `nori.agents.learning_loop.review.scoring`; review policy modules should call this boundary instead of duplicating scoring logic. |
| Review state attachment | Keep optional project mutation in `nori.agents.learning_loop.review.state`; reviewer agents should not append compliance reviews inline. |
| Strategy iteration package contract | Keep review/metrics snapshot restoration and project-derived evidence fallback in class-owned `nori.agents.learning_loop.strategy.package`; iteration agents should call this boundary before policy evaluation. |
| Strategy iteration policy | Keep ref identity, metric alias normalization, engagement-rate aggregation, review summaries, diagnosis, decisions, and next-action rules in `nori.agents.learning_loop.strategy.policy`; `StrategyIterationAgent` should own orchestration only. |
| Strategy iteration state | Keep metrics snapshot and strategy iteration project attachment in `nori.agents.learning_loop.strategy.state`; iteration agents should not append project lists inline. |

## Documentation

| Change | Required wiki update |
| --- | --- |
| New/changed agent contract | [30-api-reference.md](./30-api-reference.md) and relevant stage file. |
| New module/data flow | [20-system-architecture.md](./20-system-architecture.md). |
| New planned task or debt | [85-backlog.md](./85-backlog.md). |
| Non-obvious failure pattern | [80-known-pitfalls.md](./80-known-pitfalls.md). |
| Stage-level capability completed | [01-project-roadmap.md](./01-project-roadmap.md), stage file, [90-changelog.md](./90-changelog.md). |

## File Placement

| Artifact | Location |
| --- | --- |
| Active feature spec | `wiki/specs/spec-{feature}.md` |
| External/system reference | `wiki/refs/{topic}.md` or existing `文档/codex-skills/.../references/` until migrated. |
| Review record | `wiki/reviews/review-YYYY-MM-DD-{subject}.md` |
| Completed spec | `wiki/archive/specs/` |
| Historical docs | Keep in `文档/` until migrated; do not add new canonical roadmap there. |

## Test Commands

| Purpose | Command |
| --- | --- |
| Full default suite | `python -m pytest tests -q` |
| Config contract | `python -m pytest tests/test_config_models.py tests/test_config_normalization.py tests/test_nori_config.py tests/test_llms_mode.py -q` |
| Model coercion | `python -m pytest tests/test_model_coercion.py -q` |
| LLM JSON helper | `python -m pytest tests/test_llms_call_json.py -q` |
| LLM chat runner | `python -m pytest tests/test_llms_chat_runner.py tests/test_llms_telemetry.py -q` |
| LLM image runner | `python -m pytest tests/test_llms_image_runner.py tests/test_llms_image_capabilities.py tests/test_llms_telemetry.py -q` |
| LLM structured helpers | `python -m pytest tests/test_llms_structured_models.py tests/test_llms_structured_prompts.py tests/test_llms_intent_target_helpers.py -q` |
| Generation core | `python -m pytest tests/test_content_generation_note_maker_note_composer.py tests/test_content_generation_note_maker_skill_picker.py tests/test_content_generation_note_maker_asset_curator.py tests/test_user_profiling_intaker_taxonomy.py tests/test_user_profiling_intaker_normalizer.py tests/test_user_profiling_intaker_image_tagger.py tests/test_user_profiling_intaker.py tests/test_content_generation_note_maker.py tests/test_content_generation_cover_director_refs.py tests/test_content_generation_cover_director_prompt.py tests/test_content_generation_cover_director_output.py tests/test_content_generation_cover_director.py -q` |
| Intent/checkpoint/quality routing | `python -m pytest tests/test_core_intent_contract.py tests/test_core_artifact_store.py tests/test_learning_loop_quality_review.py tests/test_content_generation_generation_agent.py -q` |
| Account planning | `python -m pytest tests/test_user_profiling_account_planner_inputs.py tests/test_user_profiling_account_planner_prompts.py tests/test_user_profiling_account_planner_fallback.py tests/test_user_profiling_account_planner_search.py tests/test_user_profiling_account_planner_keywords.py tests/test_user_profiling_account_planner_portrait.py tests/test_user_profiling_account_planner_normalizer.py tests/test_user_profiling_account_planner.py -q` |
| Market analysis | `python -m pytest tests/test_market_analysis_xhs_note_loader.py tests/test_market_analysis_xhs_note_rules.py tests/test_market_analysis_xhs_note_llm.py tests/test_market_analysis_xhs_session_clustering.py tests/test_market_analysis_xhs_session_llm.py tests/test_market_analysis_xhs_session_reporter.py tests/test_market_analysis_xhs_skill_builder.py tests/test_market_analysis_xhs_note_analyzer.py -q` |
| Ops backend | `python -m pytest tests/test_workflow_models.py tests/test_context_building_operation_planner_inputs.py tests/test_context_building_operation_planner_prompts.py tests/test_context_building_operation_planner_project_policy.py tests/test_context_building_operation_planner_project_builder.py tests/test_context_building_operation_planner_normalizer.py tests/test_context_building_operation_planner.py tests/test_context_building_kpi_planner_inputs.py tests/test_context_building_kpi_planner_prompts.py tests/test_context_building_kpi_planner_normalizer.py tests/test_context_building_kpi_planner.py tests/test_context_building_calendar_planner_inputs.py tests/test_context_building_calendar_planner_prompts.py tests/test_context_building_calendar_planner_policy.py tests/test_context_building_calendar_planner_task_builder.py tests/test_context_building_calendar_planner_normalizer.py tests/test_context_building_calendar_planner.py tests/test_context_building_planner_critics.py -q` |
| Production bridge | `python -m pytest tests/test_content_generation_content_producer_package.py tests/test_content_generation_content_producer_state.py tests/test_content_generation_content_producer.py -q` |
| Review and iteration gate | `python -m pytest tests/test_learning_loop_review_inputs.py tests/test_learning_loop_review_state.py tests/test_learning_loop_review_scoring.py tests/test_learning_loop_review_policy.py tests/test_learning_loop_review.py tests/test_learning_loop_strategy_inputs.py tests/test_learning_loop_strategy_state.py tests/test_learning_loop_strategy_policy.py tests/test_learning_loop_strategy.py -q` |

The current machine's bare `python` is Python 3.9.12. Shared dataclass model/result classes stay importable there through `nori._compat`.
