<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# API Reference

This project currently exposes Python contracts, not stable HTTP routes.

## LLM Gateway

| API | Input | Output | Notes |
| --- | --- | --- | --- |
| `llms.chat(messages, usage="llm", **kwargs)` | OpenAI-style messages | Text string | Uses active model for `usage`; active model must be `type=llm` or `type=vision`; `usage="vision"` or multimodal message parts require `supports_vision=true` or raise `ChatCapabilityError`. Empty or malformed provider choices raise `ChatResultError`. |
| `llms.chat_json(messages, usage="llm", json_mode=False, retry_without_response_format=True, **kwargs)` | OpenAI-style messages | JSON object dict | Parses whole/fenced/embedded JSON object. Embedded parsing returns the first valid JSON object, so extra prose or later JSON blocks do not break a valid first object. `json_mode=True` requests JSON object mode and retries without `response_format` only when the provider rejects JSON/response-format behavior. |
| `llms.chat_json_with_raw(messages, usage="llm", json_mode=False, retry_without_response_format=True, **kwargs)` | OpenAI-style messages | `(data, raw)` tuple | Same JSON-mode and retry semantics as `chat_json`, but returns the original model text for structured helpers that need debug/error context. |
| `llms.parse_json_object(raw)` | Model text | JSON object dict / `ChatJSONError` | Canonical implementation lives in `llms.json_parser`; package and `llms.call` imports preserve the same function identity. |
| `llms.json_calls.chat_json_raw(...)` | Messages + injected chat function + JSON-mode flags | Raw model text | Canonical raw-call helper behind `chat_json` / `chat_json_with_raw`; copies params, injects JSON object mode when requested, and retries without `response_format` only for JSON-mode compatibility failures. |
| `llms.json_calls.is_response_format_error(...)` | Exception | bool | Canonical retry classifier for response-format / JSON-object incompatibility. |
| `llms.image(prompt, usage="image", reference_images=None, size=...)` | Prompt + optional bytes refs | List of image outputs | Public facade over `llms.image_runner.image_outputs`; active model must be `type=image`; reference images require `supports_reference_image=true` or raise `ImageCapabilityError`; Google native image calls validate `api_key` before SDK dispatch. |
| `llms.set_telemetry_sink(sink_or_none)` | Callable receiving dict metadata | None | Registers process-local redacted telemetry for `chat` / `achat` / `image`; never includes prompts, keys, image bytes, or response text. Canonical implementation lives in `llms.telemetry`; package and `llms.call` imports preserve the same function identity. |
| `llms.build_client_bundle(model, usage)` | Resolved model + usage | `ClientBundle` | Builds an OpenAI-compatible sync client from an already-resolved model, preserving capability checks and client construction on the same model. |
| `llms.build_async_client_bundle(model, usage)` | Resolved model + usage | `ClientBundle` | Async equivalent of `build_client_bundle`. |
| `llms.validate_api_key(model, usage)` | Resolved model + usage | Trimmed API key / exception | Shared provider-key validator used by OpenAI-compatible client config and native Google image calls; blank key raises `LLMClientConfigError`. |
| `llms.validate_client_config(model, usage)` | Resolved model + usage | Trimmed client options / exception | Shared config validator used by client factories and readiness checks; blank `api_key` / `base_url` raises `LLMClientConfigError`. |
| `nori.core.contracts.{LLMClientConfigError,ChatJSONError,ChatResultError,ChatCapabilityError,ImageCapabilityError,ImageResultError}` | Error contract fields | Exception classes | Canonical gateway exception classes; `llms`, `llms.call`, and `llms.client` export the same class objects for normal public use. |
| `llms.telemetry.emit_telemetry(...)` | Internal gateway metadata | None | Internal helper for gateway call sites; emits redacted metadata and swallows sink errors so telemetry cannot break business calls. |
| `llms.chat_runner.chat_text(...)` / `achat_text(...)` | OpenAI-style messages + usage + kwargs | Text string | Canonical sync/async chat execution helpers behind `llms.chat` / `llms.achat`; resolve clients, merge chat kwargs, guard chat/vision capability, normalize provider text, and emit telemetry. |
| `llms.image_runner.image_outputs(...)` | Prompt + optional reference inputs + usage + kwargs | List of image outputs | Canonical image execution helper behind `llms.image`; resolves active image model once, filters reference inputs, guards image capabilities, dispatches provider helpers, validates non-empty outputs, and emits telemetry. |
| `llms.request_params.merge_chat_kwargs(...)` | Resolved model + caller kwargs | Request kwargs copy | Canonical chat request-parameter merger; normalizes token-limit fields, applies `temperature_fixed`, and copies/merges `extra_body` without mutating caller state. |
| `llms.request_params.merge_image_kwargs(...)` | Resolved model + caller kwargs | Request kwargs copy | Canonical image request-parameter merger; applies model-level `extra_body` without adding chat-only token/temperature fields. |
| `llms.capabilities.ensure_chat_capability(...)` | Resolved model + messages + usage | None / `ChatCapabilityError` | Canonical chat/vision capability guard used before provider dispatch. |
| `llms.capabilities.ensure_image_capability(...)` | Resolved model + reference bytes | None / `ImageCapabilityError` | Canonical image/reference capability guard used before provider dispatch. |
| `llms.capabilities.messages_need_vision(...)` | OpenAI-style messages | bool | Detects multimodal image parts for chat/vision capability enforcement. |
| `llms.results.extract_chat_text(...)` | Provider chat response + model | Text / `ChatResultError` | Canonical chat response normalizer; supports object and dict-shaped responses and raises stable empty-result errors. |
| `nori.storage.ReferenceImagePublisher.from_env().publish_paths(...)` | Local reference image paths + project/session context | Model-fetchable HTTPS URL inputs + upload metadata | Uploads local reference images to Volcengine TOS when OSS env is configured. Object keys follow `nori/reference-images/<project>/<session>/<YYYYMMDD>/<sha16>_<source>.<ext>`; signed query strings are not persisted in content artifacts. |
| `llms.results.collect_image_results(...)` | Provider image response | List of URL/data-uri strings / `ImageResultError` | Canonical image response normalizer for URL and `b64_json` outputs. |
| `llms.image_inputs.load_image_bytes(...)` | bytes, data-uri, path, base64 string, or unknown value | Image bytes or `b""` | Canonical reference-image input normalizer; unreadable/remote/invalid inputs return empty bytes so `llms.image` can filter them before capability checks. |
| `llms.image_inputs.sniff_mime(...)` | Image bytes | MIME string | Detects PNG/JPEG/GIF/WEBP and defaults unknown bytes to `image/png`. |
| `llms.image_inputs.bytes_to_data_uri(...)` | Image bytes | `data:{mime};base64,...` string | Canonical data-uri encoder used by reference-image provider payloads. |
| `llms.image_providers.image_openai_edit(...)` | Resolved image bundle + prompt + reference bytes | List of image outputs | Canonical OpenAI-compatible `images.edit` wrapper; builds named in-memory files and delegates response parsing to `llms.results`. |
| `llms.image_providers.image_relay_generate_with_references(...)` | Resolved image bundle + prompt + reference bytes | List of image outputs | Canonical relay reference-image path; retries supported `extra_body` payload variants without mutating caller kwargs. |
| `llms.image_providers.image_google(...)` | Prompt + resolved Google image model + API key | List of data-uri image outputs | Canonical Google native image call; constructs `google-genai` parts and encodes inline image results. |
| `llms.structured_outputs.clean_str(...)` | Unknown scalar value | Clean string or `None` | Canonical cleanup for optional structured LLM outputs; treats blanks and null-like tokens as missing. |
| `llms.structured_outputs.chat_json_error_reason(...)` | `ChatJSONError` | `empty_response` / `parse_error` | Canonical parse-failure classifier for optional structured helpers. |
| `llms.structured_outputs.normalize_field_value(...)` | LLM field node | `(value, candidates)` | Canonical intent field-node normalizer for string/dict/list outputs, enum filtering, dedupe, and candidate caps. |
| `llms.structured_outputs.normalize_selector_options(...)` | Selector option rows | Clean option rows | Canonical edit-target option cleanup and selector dedupe. |
| `llms.structured_outputs.normalize_selector_alternatives(...)` | Raw alternatives + whitelist | Alternative selectors | Canonical whitelist, target-exclusion, dedupe, and cap logic for edit-target alternatives. |
| `llms.structured_outputs.normalize_confidence(...)` | Unknown confidence value | `high` / `medium` / `low` | Canonical confidence cleanup; unknown values fall back to `low`. |
| `nori.core.contracts.{StructuredCallResult,IntentLLMResult,TargetSelectionResult}` | Structured helper fields | Dataclass contracts | Canonical non-throwing structured-helper result models; `llms`, intent, target, and structured-call modules export the same class objects for normal public use. |
| `llms.structured_calls.call_structured_json(messages, usage=..., timeout=...)` | JSON messages | `StructuredCallResult(data, raw, error)` | Canonical non-throwing JSON-mode call wrapper for optional structured helpers; classifies parse failures and provider exceptions. |
| `llms.structured_prompts.build_*_prompt(...)` | Intent/target prompt inputs | Prompt text | Canonical prompt builders for intent extraction and edit-target selection, including field descriptions, enum/candidate instructions, target catalogs, history formatting, and summary truncation. |
| `llms.ensure_ready(usage)` | Usage key | None / exception | Reuses client config validation, then checks GHC proxy `/models` in `ghc` mode. |
| `llms.extract_intent(text, needed_fields=...)` | Normalized prompt | `IntentLLMResult` | Uses shared `chat_json(json_mode=True)` and returns structured failure via `error`. |
| `llms.select_edit_target(instruction, options)` | Instruction + selector options | `TargetSelectionResult` | Uses shared `chat_json(json_mode=True)`, validates selector whitelist, and does not throw on model failure. |
| `NoriConfig(config_path=None)` | Optional config path | Config object | Loads `api_config.yaml`, supports `api_key_env`, `${ENV_VAR}`, nested `active_models`, and `NORI_MODE`. |
| `nori.core.contracts.{ProviderConfig,ModelConfig,ResolvedModel}` | Config model fields | Dataclass contracts | Canonical runtime-config dataclasses shared by `nori_config` and `llms`; `nori.core` and `nori.nori_config` expose the same class identities. |
| `nori.config_normalization.parse_model_key(key)` / `format_model_key(...)` | Provider/model key text | Canonical provider and model ids | Pure config helper used before model lookup so whitespace and malformed keys are handled consistently. |
| `nori.config_normalization.select_active_models(active_models, mode, fallback_mode=...)` | Flat or mode-nested active model map | Canonical usage -> model-key map | Pure config helper for direct/ghc active-model selection, including missing-mode behavior for `NORI_MODE`. |
| `nori.config_normalization.resolve_api_key(raw_value, env_name="")` | Literal or `${ENV_VAR}` API key config | API key text | Pure config helper that trims env var names and resolves explicit `api_key_env` before literal config values. |

## Generation Agents

| API | Contract |
| --- | --- |
| `IntakeAgent().run(UserInput | str, images=None, use_llm=None, use_vision=None) -> IntakeResult` | Normalize text/images into intention/context/missing/questions/assets. |
| `nori.agents.user_profiling.intaker.normalizer.rule_intake(UserInput) -> IntakeResult` | Internal generation helper for deterministic Intake text fallback. Extracts goal/format/tone/assets/guardrails/data refs, builds image context, and produces missing/questions. |
| `nori.agents.user_profiling.intaker.normalizer.normalize_llm_result(data, UserInput, fallback) -> IntakeResult` | Internal generation helper for optional Intake text LLM output. Applies taxonomy cleanup, missing/question repair, image context, and fallback metadata preservation. |
| `nori.agents.user_profiling.intaker.taxonomy.{pick_first,pick_many,allowed_label,allowed_list}(...)` | Internal generation helpers for Intake taxonomy classification and LLM label cleanup. Owns goal/format/tone/asset/guardrail/data vocabularies and alias maps. |
| `nori.agents.user_profiling.intaker.taxonomy.{normalize_missing,normalize_questions}(...)` | Internal generation helpers for Intake missing-field repair and question fallback text. |
| `nori.agents.user_profiling.intaker.image_tagger.build_tagged_assets(UserInput, use_vision=...) -> list[UserAsset]` | Internal generation helper for Intake vision assets. Builds per-image multimodal JSON calls when vision is enabled, isolates failed image tags, and filters tag vocabularies before returning `UserAsset` records. |
| `NoteMakerAgent().run(skills, assets, intent=None, context=None) -> NoteDraft` | Select skill, curate assets, compose XHS note. Fails with `NoteMakerLLMError` for LLM-stage failures. |
| `nori.agents.content_generation.note_maker.package.NoteSkillSelector` | Class-owned NoteMaker skill-selection boundary. Sends a compact candidate summary to the JSON stage and raises the caller's domain error when the selected `skill_id` is unknown. |
| `nori.agents.content_generation.note_maker.package.NoteAssetCurator` | Class-owned NoteMaker asset boundary. Builds the asset-curation JSON prompt, normalizes selected image indices/text buckets, and keeps cover/gallery path selection together. |
| `nori.agents.content_generation.note_maker.package.NoteComposer` | Class-owned NoteMaker copy boundary. Builds the note-composition JSON prompt, normalizes candidate titles/tags/validation, and raises the caller's domain error when title/body is missing. |
| `nori.agents.content_generation.cover_director.package.CoverReferenceSelector` | Class-owned CoverDirector reference boundary. Selects tagged-asset references with LLM, collects legacy draft/reference paths, filters missing paths, dedupes, caps, and converts local/remote references into image inputs. |
| `nori.agents.content_generation.cover_director.package.CoverPromptBuilder` | Class-owned CoverDirector prompt boundary. Builds the image-generation prompt JSON call from draft asset facts, skill rules, intent, and reference count; raises the caller's domain error for empty prompts. |
| `nori.agents.content_generation.cover_director.output.save_image(payload, out_dir, skill_id, error_type=...) -> Path` | Internal generation helper for CoverDirector output persistence. Writes data-uri or remote image payloads, sanitizes cover filenames, and raises the caller's domain error on base64/download failures. |
| `CoverDirectorAgent().run(draft, skill, reference_assets=None, out_dir=..., size=..., intent=None, tagged_assets=None) -> CoverResult` | Select references, write image prompt, call image API, save cover. |
| `nori.agents.user_profiling.account_planner.package.AccountPlannerInputPreparer` | Class-owned AccountPlanner input boundary for merging raw/string input, existing planner input, extra image/link evidence, platform defaults, search settings, and compact asset prompt context. |
| `nori.agents.user_profiling.account_planner.package.AccountPlannerPromptBuilder` | Class-owned AccountPlanner prompt boundary for serializing normalized evidence, intention/context, and optional search rows into the JSON-only account-planning prompt. |
| `nori.agents.user_profiling.account_planner.fallback.fallback_plan(normalized) -> AccountPlanResult` | Internal AccountPlanner helper for deterministic no-inference fallback with platform/goal tags and empty benchmark/IP portrait sections. |
| `nori.agents.user_profiling.account_planner.search.run_search(search_provider, normalized, result) -> list[dict]` | Internal generation helper for AccountPlanner search enrichment. Cleans/dedupes search keywords, applies platform ids, isolates provider failures, and adds default `platform` / `keyword` fields to rows. |
| `nori.agents.user_profiling.account_planner.search.EmptySearchProvider` | Internal fallback search provider that returns no rows, keeping AccountPlanner tests and offline runs deterministic. |
| `nori.agents.user_profiling.account_planner.normalizer.normalize_llm_result(data, fallback, search_results) -> AccountPlanResult` | Internal generation helper for AccountPlanner output cleanup. Normalizes tags, three-level keywords, benchmark accounts, IP portrait report, and fallback metadata. |
| `nori.agents.user_profiling.account_planner.normalizer.merge_search_results(result, search_results) -> AccountPlanResult` | Internal generation helper for AccountPlanner search-only enrichment when no LLM refinement is used. |
| `nori.agents.user_profiling.account_planner.portrait.normalize_ip_portrait_report(...) -> dict` | Internal AccountPlanner helper for IP portrait cleanup. Normalizes account names, keywords, content pillars, benchmark creators, and cover design formats, deriving creators from benchmark accounts when needed. |
| `nori.agents.user_profiling.account_planner.portrait.merge_report_benchmarks(report, benchmark_accounts) -> dict` | Internal AccountPlanner helper for refreshing IP portrait benchmark creators after search-only enrichment. |
| `nori.agents.user_profiling.account_planner.keywords.normalize_keyword_levels(value, fallback=..., search_keywords=...) -> list[dict]` | Internal generation helper for AccountPlanner keyword rows. Cleans platform tokens, enforces level/role fallbacks, dedupes keywords, and preserves deterministic search-keyword fallback behavior. |
| `nori.agents.user_profiling.account_planner.keywords.clean_keyword(value) -> str` | Internal generation helper for stripping platform labels/separators from planner/search keywords. |
| `AccountPlannerAgent().run(user_input, images=None, links=None, enable_search=None) -> AccountPlanResult` | Produce account positioning and IP portrait; optional `SearchProvider`. |

`IntakeResult.metadata` and `AccountPlanResult.metadata` are optional dicts for control-plane data. LLM fallback paths may attach redacted `llm_error`; empty metadata is omitted from `to_dict()`.

## Ops Agents

| API | Contract |
| --- | --- |
| `OperationPlannerAgent().run(client_brief, account_plan, project_id="", start_date=None, horizon_days=None, use_llm=None) -> AccountOperationProject` | Build operation plan, calendar, tasks, and metadata. |
| `nori.agents.planning.operation_planner.package.OperationPlannerInputPreparer` | Class-owned OperationPlanner input boundary for restoring `ClientBrief` / `AccountPlanResult`, parsing start dates, and bounding horizons. |
| `nori.agents.planning.operation_planner.package.OperationPlannerPromptBuilder` | Class-owned OperationPlanner prompt boundary for serializing normalized client/account context into the JSON-only SOP planning prompt. |
| `nori.agents.planning.operation_planner.project_builder.fallback_project(brief, account_plan, project_id=..., project_name=..., start_date=..., horizon_days=...) -> AccountOperationProject` | Internal ops helper for OperationPlanner deterministic fallback. Builds operation plan, content calendar, planned tasks, derived KPI snapshot, account positioning, asset requirements, and benchmark references without live LLM calls. |
| `nori.agents.planning.operation_planner.project_policy.*` | Internal OperationPlanner fallback policy helpers for content pillars, objectives, risk controls, topic pools, task references, milestones, project labels, asset defaults, and operation-derived KPI plans. |
| `nori.agents.planning.operation_planner.normalizer.merge_llm_project(data, fallback, start_date=..., horizon_days=...) -> AccountOperationProject` | Internal ops helper for OperationPlanner LLM output. Merges operation plan/calendar JSON into a fallback project, normalizes task rows, clamps dates, and refreshes derived KPI snapshots. |
| `KPIPlannerAgent().run(operation_plan_or_project, project_context=None, use_llm=None) -> KPIPlan` | Build measurable targets; default fallback includes content task count and review pass rate. |
| `nori.agents.planning.kpi_planner.package.KPIPlannerInputPreparer` | Class-owned KPIPlanner input boundary for restoring operation plans and project context from project objects or composite dict payloads. |
| `nori.agents.planning.kpi_planner.package.KPIPlannerPromptBuilder` | Class-owned KPIPlanner prompt boundary for serializing normalized operation plans and project context into the JSON-only KPI planning prompt. |
| `nori.agents.planning.kpi_planner.normalizer.fallback_kpi_plan(plan, context) -> KPIPlan` | Internal ops helper for deterministic KPI fallback from an `OperationPlan`, project task count, review-pass defaults, manual metric cadence, and safe milestone defaults. |
| `nori.agents.planning.kpi_planner.normalizer.merge_llm_kpi_plan(data, fallback, plan) -> KPIPlan` | Internal ops helper for KPI LLM output. Merges targets, clamps milestone days, caps measurement notes, and preserves fallback notes when the LLM returns empty notes. |
| `CalendarPlannerAgent().run(operation_plan_or_project, kpi_plan=None, client_brief=None, start_date=None, horizon_days=None, use_llm=None) -> ContentCalendar` | Build scheduled tasks. |
| `nori.agents.planning.calendar_planner.package.CalendarPlannerInputPreparer` | Class-owned CalendarPlanner input boundary for restoring `OperationPlan` / `AccountOperationProject` / composite dict inputs, applying KPI/brief overrides, and normalizing run windows. |
| `nori.agents.planning.calendar_planner.package.CalendarPlannerPromptBuilder` | Class-owned CalendarPlanner prompt boundary for serializing operation, KPI, client context, and run window into the JSON-only content-calendar prompt. |
| `nori.agents.planning.calendar_planner.normalizer.fallback_calendar(plan, kpi, brief, start_date=..., horizon_days=...) -> ContentCalendar` | Internal ops helper for deterministic calendar fallback from operation objectives, KPI task targets, brief assets, bounded horizon, and safe scheduled dates. |
| `nori.agents.planning.calendar_planner.normalizer.merge_llm_calendar(data, fallback, plan, brief, start_date=..., horizon_days=...) -> ContentCalendar` | Internal ops helper for CalendarPlanner LLM output. Merges cadence/themes/notes/tasks, clamps task days to the horizon, injects missing content pillars, and preserves fallback lists when LLM sections are empty. |
| `nori.agents.planning.calendar_planner.policy.*` | Internal CalendarPlanner policy helpers for bounded horizons, start dates, task counts, scheduled dates, day clamping, cadence strings, topic/brand labels, and required asset defaults. |
| `nori.agents.planning.calendar_planner.task_builder.{fallback_tasks,tasks_from_llm}` | Internal CalendarPlanner task-row helpers for fallback `ContentTask` construction, LLM task row cleanup, content-pillar fallback, and invalid-row fallback preservation. |
| `nori.agents.planning.planner_critics.critic_operation_project(project, brief, account_plan) -> dict` | Internal ops helper for OperationPlanner critic metadata. Checks objectives, pillars, tasks, calendar, risk controls, platform alignment, and rule-fallback status. |
| `nori.agents.planning.planner_critics.critic_kpi_plan(plan, operation_plan) -> dict` | Internal ops helper for KPIPlanner critic metadata. Checks targets, milestones, measurement notes, short-horizon cadence, and rule-fallback status. |
| `nori.agents.planning.planner_critics.critic_calendar(calendar, plan, kpi) -> dict` | Internal ops helper for CalendarPlanner critic metadata. Checks themes, task count, date range, planned status, task briefs, KPI target coverage, content-pillar coverage, and rule-fallback status. |
| `ContextCompiler().build(...) -> ContextPack` | Compile task, profile, platform strategy, market hotspots, learned skills, content strategy, assets, and constraints into typed `ContextSlice` rows. |
| `ContextResolver().for_agent(agent_name, context_pack) -> ContextView` | Project a task `ContextPack` into the slice set a specific agent should consume. |
| `ContentSpecAgent().run(context_view=...) -> ContentDesignSpec` | Preferred production path. Freeze generation strategy from an agent-specific context view: artifact type, selected skill refs, evidence refs, structure, media plan, copy/visual rules, constraints, and acceptance checks. |
| `ContentSpecAgent().run(task, skills, assets=None, client_brief=None, project=None, intent_contract=None, intent=None, context=None) -> ContentDesignSpec` | Focused-test/manual path for direct inputs when a compiled `ContextView` is not available. |
| `ArtifactGenerationAgent().run(spec, task, skills, assets, out_dir, client_brief=None, project=None, intent=None, context=None, intent_contract=None, use_cover=True) -> ContentPackage` | Execute a frozen `ContentDesignSpec`, filter skills to selected refs, inject the spec into intent/context, and delegate package production to concrete generators. |
| `ContentProducerAgent().run(task, skills, assets, out_dir, client_brief=None, project=None, intent=None, context=None, use_cover=True) -> ContentPackage` | Produce a draft package from a planned task; attaches structured failure metadata before raising `ContentProductionError`. This is an execution detail behind `ArtifactGenerationAgent` for production workflows. |
| `produce_content_package(task, **kwargs) -> ContentPackage` | Convenience wrapper; accepts fake `note_maker` / `cover_director` dependencies for tests. |
| `nori.agents.content_generation.content_producer.package.ContentPackageAssembler.prepare(...)` | ContentTask + ClientBrief + assets + optional project/overrides | `PreparedContentPackageInput` | Restores `UserAsset` rows, adds task/brief text fallback, and builds production `intent` / `context`. |
| `nori.agents.content_generation.content_producer.package.ContentPackageAssembler.build(...)` | Task + `NoteDraft` + optional `CoverResult` + sources | `ContentPackage` | Maps generated outputs into package prompts, media paths, material usage, source refs, stable package ID, and production metadata. |
| `nori.agents.content_generation.content_producer.package.ContentPackageAssembler` | Deterministic package assembly methods | Class | Inherits `nori.core.StableArtifactAssembler` for shared slug/dedupe behavior. |
| `nori.agents.content_generation.content_producer.state.*` | Internal production state helpers for success/failure task/project metadata, production-error formatting, and note/cover/production failure classification. |
| `ComplianceReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview` | Text-only compliance checks for title/body, client taboos, unsupported claims, and NoteMaker validation. |
| `ConsistencyReviewerAgent().run(package, task=None, client_brief=None, project=None) -> ComplianceReview` | Checks task identity, topic/objective alignment, cover prompt alignment, required assets, and brand presence. |
| `nori.agents.learning_loop.review.package.ReviewInputPreparer` | Class-owned review input boundary for persisted package/task/brief restoration and project-derived brief fallback. |
| `nori.agents.learning_loop.review.policy.compliance_issues(package, brief) -> list[dict]` | Internal review helper for text compliance issue calculation. |
| `nori.agents.learning_loop.review.policy.consistency_issues(package, task, brief) -> list[dict]` | Internal review helper for task/package/cover/material alignment issue calculation. |
| `nori.agents.learning_loop.review.policy.build_review(package=..., task=..., reviewer=..., issues=..., metadata=...) -> ComplianceReview` | Internal review helper for score/status/severity/fix-suggestion construction. |
| `nori.agents.learning_loop.review.scoring.{issue,score_issues,status_for_issues,severity_counts,suggestions}` | Internal review helper set for normalized issue rows, severity penalties, status mapping, severity metadata, and deduped fix suggestions. |
| `nori.agents.learning_loop.review.state.attach_review(project, review) -> None` | Internal review state helper that appends reviews to an optional project context. |
| `ReviewGateAgent().run(package, task=None, client_brief=None, project=None) -> list[ComplianceReview]` | Runs compliance then consistency reviewers and optionally attaches reviews to a project. |
| `review_content_package(package, **kwargs) -> list[ComplianceReview]` | Convenience wrapper for the default review gate. |
| `MetricsSnapshotAgent().run(ref, metrics, captured_at=None, source="manual", notes=None, project=None) -> MetricsSnapshot` | Records manual metrics for a package/task/ref and optionally appends to project. |
| `record_metrics_snapshot(ref, metrics, **kwargs) -> MetricsSnapshot` | Convenience wrapper for manual metrics. |
| `nori.agents.learning_loop.strategy.package.StrategyIterationInputPreparer` | Class-owned iteration input boundary for persisted review/metric restoration and project-derived evidence fallback. |
| `nori.agents.learning_loop.strategy.policy.metric_summary(metrics) -> dict` | Internal iteration helper for raw metric alias normalization and engagement-rate calculation. |
| `nori.agents.learning_loop.strategy.policy.review_summary(reviews) -> dict` | Internal iteration helper for review status counts, issue severity counts, and top issue codes. |
| `nori.agents.learning_loop.strategy.policy.{diagnosis,decisions,next_actions}(review_summary, metrics_summary) -> list[str]` | Internal iteration policy for turning review/metric evidence into strategy text. |
| `nori.agents.learning_loop.strategy.state.{attach_metrics_snapshot,attach_strategy_iteration}` | Internal iteration state helpers for optional project attachment. |
| `StrategyIterationAgent().run(project=None, reviews=None, metrics_snapshots=None, project_id="") -> StrategyIteration` | Turns reviews + metrics into diagnosis, decisions, and next actions. |
| `create_strategy_iteration(**kwargs) -> StrategyIteration` | Convenience wrapper for strategy iteration. |

## Data Collection

| API | Contract |
| --- | --- |
| `DataCollector.search(SearchRule(...))` | Platform keyword search. |
| `DataCollector.fetch_detail(DetailRule(...))` | Fetch detail pages/comments depending on platform support. |
| `DataCollector.download(DownloadRule(...))` | Download media assets. |
| `DataCollector.collect_top_notes(TopNotesRule(...)) -> TopNotesResult` | XHS high-performing note pool for skill learning. |

## Skill Fixture Helpers

| API | Contract |
| --- | --- |
| `call_stage_json(system=..., user=..., timeout=..., error_type=...) -> dict` | Shared utility for generation-stage JSON stages. Calls `llms.chat_json(json_mode=True, _chat=llms.chat)` and translates parse/provider failures into the supplied domain exception class. |
| `call_stage_messages_json(messages=..., timeout=..., error_type=..., usage=...) -> dict` | Shared utility for required JSON stages that already build OpenAI-style messages, including multimodal `usage="vision"` calls. Uses the same JSON-mode and domain-error translation contract as `call_stage_json`. |
| `try_stage_messages_json(messages=..., timeout=..., usage=...) -> (data, error)` | Shared utility for optional JSON stages that already build OpenAI-style messages, including multimodal/custom-message fallback paths. Calls `llms.chat_json(json_mode=True, _chat=llms.chat)`, returns `data` on success, and returns redacted `error` metadata on parse/provider failure without raising. |
| `try_stage_json(system=..., user=..., timeout=...) -> (data, error)` | System/user convenience wrapper over `try_stage_messages_json(...)` for optional planner JSON stages. `reason` distinguishes `empty_response`, `parse_error`, and `api_error`. |
| `attach_llm_error(target, stage, error) -> None` | Shared formatter for optional-LLM fallback errors. Writes `target["llm_error"] = {...error, "stage": stage}` so metadata/validation containers share one field shape and caller stage cannot be overwritten by error input. |
| `nori.agents.market_analysis.load_note_skills(source) -> list[NoteSkill]` | Load `NoteSkill` objects from a full `SessionSkillReport`, skills-only dict/list, or JSON path. |
| `nori.agents.market_analysis.note_skill_fixture(source) -> dict` | Convert a report/list/single skill into stable `{"skills": [...]}` JSON. |
| `nori.agents.market_analysis.write_note_skill_fixture(source, path) -> Path` | Write the skills-only fixture JSON for tests or smoke scripts. |

## Market Analysis Helpers

| API | Contract |
| --- | --- |
| `nori.agents.market_analysis.xhs_note_analyzer.loader.load_note_sample(meta_path) -> XHSNoteSample` | Restore a local XHS note `meta.json` plus optional author `meta.json` into analyzer evidence. |
| `nori.agents.market_analysis.xhs_note_analyzer.loader.{read_json_object,tags_from_meta,count_text}` | Internal market-analysis loader helpers for JSON object validation, tag extraction, and platform metric count parsing. |
| `nori.agents.market_analysis.xhs_note_analyzer.rules.rule_analyze_note(note) -> XHSSeedSkillDraft` | Build a rule-only single-note seed-skill draft without LLM calls or session collection. |
| `nori.agents.market_analysis.xhs_note_analyzer.rules.{content_lines,title_rules,scene_for_note,goals_for_note}` | Internal single-note rule helpers for text cleanup, title/opening/body rule extraction, scene classification, goals, evidence, and confidence. |
| `nori.agents.market_analysis.xhs_note_analyzer.note_llm.enhance_note(note, rule_draft) -> XHSSeedSkillDraft` | Optional single-note LLM enhancement stage. Routes JSON through `try_stage_json(timeout=60)`, normalizes model output over the rule draft, and returns a fallback draft with `validation.llm_error` on optional-stage failure. |
| `nori.agents.market_analysis.xhs_note_analyzer.note_llm.{normalize_llm_draft,mark_llm_fallback}` | Internal single-note LLM helpers for capped/deduped output normalization and explicit fallback pipeline/error metadata. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_clustering.cluster_hot_notes(hot_notes, label_notes=...) -> (clusters, leftover_ids, llm_used)` | Group session hot notes by required LLM labels, validate label coverage, cap kept buckets to four, and return leftover note ids. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_clustering.rule_goal(title, desc) -> str` | Rule fallback classifier for tutorial/planting/debrief/opinion/news/rant/general session goals. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_llm.generate_keywords(context, max_n=3) -> list[str]` | Required session LLM stage for generating deduped XHS search keywords through `call_stage_json(timeout=30)`. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_llm.label_notes(hot_notes) -> dict[str, dict[str, str]]` | Required session LLM stage for normalizing per-note goal/tone labels through `call_stage_json(timeout=120)`, with prompt truncation for descriptions and tags. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_reporter.write_session_outputs(report) -> dict[str, Path]` | Write the full session report and skills-only guide JSON files when `source_data_dir` is present. |
| `nori.agents.market_analysis.xhs_note_analyzer.session_reporter.{report_stamp,skills_output}` | Internal reporter helpers for timestamp-derived artifact names and learned-skill fixture shape. |
| `nori.agents.market_analysis.xhs_note_analyzer.skill_builder.build_note_skill(cluster, context=None) -> NoteSkill` | Build one session-level `NoteSkill` from a goal cluster, including merged rules, evidence notes, cover rules, metrics summary, and cluster signals. |
| `nori.agents.market_analysis.xhs_note_analyzer.skill_builder.{percentile,majority_note_type,goal_label,goal_creative}` | Internal skill-builder helpers for metric summaries, note-type labels, goal labels, and creative-goal defaults. |

## Model Serialization

## Workflow Runtime

| API | Contract |
| --- | --- |
| `nori.core.WorkflowBase(workflow_name="", steps=None)` | Shared base for agents and domain facades that need a stable workflow name and ordered step metadata. `run_steps(initial)` executes registered callables in order. |
| `nori.core.named_workflow_steps(*names)` | Build named no-op steps for facades whose public methods own execution but still need inspectable `step_names`. |
| `nori.workflows.workflow_spec_from_base(workflow, human_gates=None)` | Adapter from the core `WorkflowBase` abstraction to a runtime `WorkflowSpec`. This keeps `nori.core.workflow` backend-free while allowing LangGraph execution when needed. |
| `nori.workflows.WorkflowSpec(name, stages)` | LangGraph workflow definition made of ordered coarse-grained `StageSpec` rows. |
| `nori.workflows.StageSpec(name, handler, human_gate=None)` | One workflow stage; `WorkflowRunner` wraps `handler` with LangChain Core `RunnableLambda`. Optional `human_gate` declares a runtime control point before the stage. |
| `nori.workflows.HumanGateSpec(name, prompt="", metadata={...})` | Human review control point owned by workflow runtime, not a business agent. Default execution skips gates for tests and automation. |
| `nori.workflows.WorkflowRunner().run(spec, initial, session_id=..., task_id=..., human_gate_mode="skip")` | Executes the workflow through `LangGraphWorkflowRunner`, returning `(output, WorkflowRun)`. `human_gate_mode="pause"` records `waiting_for_human` and raises `HumanGateRequired`. |
| `nori.workflows.HumanGateRequired` | Exception raised when a run reaches a human gate in pause mode; carries the partial `workflow_run`. |
| `nori.workflows.LangGraphWorkflowRunner` | Builds a LangGraph `StateGraph`, wires `START -> stages -> END`, records `StageRun` status, human-gate traces, and artifact refs returned in state. A stage can return a `StoredArtifact`, `_artifact_ref`, or `_artifact_refs` mapping; the runner normalizes these into `StageRun.output_ref` and `WorkflowRun.artifact_refs`. |

## Context Runtime

| API | Contract |
| --- | --- |
| `nori.context.ContextBundle` | Runtime envelope for one agent call: session/task/user ids, sources, memory, artifact rows, payload, and trace. |
| `nori.context.ContextCompiler().build(...)` | Compiles profile, task, market evidence, learned skills, platform rules, content strategy, and assets into a sliced `ContextPack`. |
| `nori.context.ContextPackBuilder` | Alias of `ContextCompiler`; this is the canonical owner. `nori.agents.planning.ContextPackBuilder` re-exports the same class for compatibility. |
| `nori.context.ContextResolver` | Builds a `ContextBundle` from current input, memory, and artifact references. |
| `nori.context.ContextResolver().for_agent(agent_name, context_pack)` | Projects a sliced `ContextPack` into an agent-specific `ContextView`, so stages consume relevant context slices instead of loose dicts. |
| `nori.context.attach_context_pack(bundle, context_pack, ref="")` | Attaches the business `ContextPack` compiled by the context layer into a runtime `ContextBundle` as a `ContextSource` and `payload["context_pack"]`. This is the explicit bridge between business context and one-call runtime context. |

Domain facade workflow names and declared steps:

| Facade | `workflow_name` | `step_names` |
| --- | --- | --- |
| `UserProfilingFacade` | `user_profiling` | `client_brief`, `account_positioning`, `user_profile` |
| `MarketAnalysisFacade` | `market_analysis` | `competitor_research`, `market_analysis` |
| `ContextPackBuilder` | `context` | `profile`, `task`, `market`, `assets`, `skills`, `context_pack` |
| `ContentGenerationFacade` | `content_generation` | `context_pack`, `content_packages`, `candidate_set` |
| `LearningLoopFacade` | `learning_loop` | `performance`, `strategy`, `capability_snapshot` |

Business-module model files should support `to_dict()` where the object crosses a stage boundary. Cross-stage contracts are split by owner: `UserAsset`, `AssetRecord`, and `AssetLibrary` live in `nori.core.asset_models`; `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, and `ContentCalendar` live in `nori.core.planning_models`; `UserProfile` lives in `nori.core.profile_models`; `ContextPack`, `CandidateSet`, `LearningSignal`, and `CapabilitySnapshot` live in `nori.core.capability_models`. `nori.core.models` remains a compatibility facade for the historical single-module API, and `AccountOperationProject` lives in `nori.core.project`. Public runtime contracts that are shared with the LLM gateway live in `nori.core.contracts`, including config dataclasses, gateway errors, structured-helper result dataclasses, and shared model coercion helpers. `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` live in `nori.agents.user_profiling.models`; `ContentDesignSpec`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, `CoverResult`, and `ContentPackage` live in `nori.agents.content_generation.models`; `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteSkill`, `NoteEvidence`, and `SessionSkillReport` live in `nori.agents.market_analysis.models`. The old `nori.agent_models` compatibility root has been removed; import models from the owning business module. Model `from_dict()` methods should use `nori.core.contracts` for shared mapping/list/string/int/bool cleanup.

Canonical business model ownership:

| Module | Models |
| --- | --- |
| `nori.agents.user_profiling.models` | `UserInput`, `IntakeResult`, `AccountPlannerInput`, `AccountPlanResult`, `AccountPositioning` |
| `nori.agents.market_analysis.models` | `CompetitorSample`, `CompetitorResearch`, `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, `SessionSkillReport` |
| `nori.core.asset_models` | `UserAsset`, `AssetRecord`, `AssetLibrary` |
| `nori.core.planning_models` | `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, `ContentCalendar`, `IntentContract` |
| `nori.core.profile_models` | `UserProfile` |
| `nori.core.capability_models` | `ContextPack`, `CandidateSet`, `LearningSignal`, `CapabilitySnapshot`, and related evidence/trace models |
| `nori.core.models` | Compatibility facade re-exporting the public core model contracts above |
| `nori.core.project` | `AccountOperationProject` cross-module aggregate; lazily coerces nested dicts into user/context/market/content/learning concrete models |
| `nori.agents.content_generation.models` | `ContentDesignSpec`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, `CoverResult`, `ContentPackage` |
| `nori.agents.learning_loop.models` | `ComplianceReview`, `MetricsSnapshot`, `StrategyIteration` |

The old account-ops model compatibility root has been removed. Import models from the owning module listed above.

Ops evidence helpers:

| API | Contract |
| --- | --- |
| `AccountPositioning.from_account_plan(account_plan, positioning_id="")` | Normalize `AccountPlanResult` into typed positioning, pillars, keywords, cover formats, and benchmark refs. |
| `AccountPositioning.from_dict(data)` | Load current or legacy `account_positioning` dict shapes without dropping unknown fields. |
| `AccountPositioning.summary()` | Return the recommended positioning, or a legacy persona fallback. |
| `AssetLibrary.get(asset_id)` | Return matching `AssetRecord` or `None`. |
| `AssetLibrary.usable_assets(usage=None)` | Return available assets, optionally filtered by usage. |
| `CompetitorResearch.top_samples(metric="liked", limit=5)` | Return benchmark samples sorted by metric, supporting aliases like `liked` / `likes`. |
| `CompetitorResearch.to_task_references(limit=5)` | Convert top samples into `ContentTask.references`-compatible dicts. |
