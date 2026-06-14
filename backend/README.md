# Nori Backend

`backend/` is the product-service boundary for Nori.

It is intentionally separate from:

- `nori/`: agent runtime, workflows, context, memory, session contracts, and storage.
- `web/`: product frontend and prototypes.
- `view/`: architecture diagrams and static documentation visuals.
- `scripts/`: local smoke/live-run adapters.

## Current Status

This is a lightweight FastAPI backend, not a production deployment stack. It
provides framework-native routes, Swagger UI at `/docs`, and generated OpenAPI
at `/openapi.json` so the product frontend can integrate against stable
request/response shapes without pulling API code back into `nori/`.
In-process sessions are snapshotted as JSON under `data/backend/sessions` by
default, so local experiment sessions, task status, uploaded asset metadata, and
published reference URLs survive backend restarts.

Run locally:

```bash
python -m backend.server --host 127.0.0.1 --port 8000
```

Backend API smoke with the local Holly case:

```bash
python scripts/backend_holly_smoke.py
```

Strict reference preflight with a public backend URL:

```bash
python scripts/backend_holly_smoke.py \
  --backend-public-base-url https://your-public-backend.example \
  --require-image-references
```

That command creates a session, uploads the selected Holly fixture images
through the FastAPI surface, and runs `/workflows/content-production/runs/preflight`.
It does not call live LLM/image providers unless `--run` is passed.
For live strict-reference runs, pass a real provider-fetchable HTTPS
`--backend-public-base-url` or configure OSS; placeholder/local hosts such as
`backend.example.test`, `localhost`, private IPs, and RFC example domains are
not counted as provider-fetchable references by backend preflight or live runs.
For real live generation, the accepted URL must still be reachable by the image
provider through a tunnel, deployed backend, or OSS object URL.

Tunnel-backed provider reference check:

```bash
python -m backend.server --host 127.0.0.1 --port 8000
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
python scripts/backend_holly_smoke.py \
  --api-base-url http://127.0.0.1:8000 \
  --backend-public-base-url https://your-tunnel.example \
  --require-image-references \
  --verify-reference-urls \
  --check-reference-image-generation \
  --reference-url-probe-timeout 10
```

That live diagnostic proves three things before a full workflow run: the backend
can serve uploaded Holly images over HTTPS, the backend can probe those URLs,
and the active image provider can fetch the same references and return
`image_generation_succeeded`. Keep `--api-base-url` on localhost when testing
the local FastAPI process; the public tunnel only needs to be used as
`--backend-public-base-url` so external providers can fetch uploaded files. Free
tunnel services may rotate URLs or return non-JSON 5xx pages; the smoke script
reports those responses with route, status, and body preview so the operator can
rerun with the current tunnel URL.

## Code Layout

- `app.py` owns FastAPI app creation, exception handling, and route registration.
- `facade.py` owns the `NoriBackend` composition root and keeps direct access to
  the constructed service graph for tests and compatibility.
- `route_services.py` owns route-facing service facets grouped by product
  surface, so route modules depend on focused objects instead of one large
  backend facade.
- `services/runtime.py` owns backend service composition and dependency wiring
  through `BackendServiceBundle`; `facade.py` creates the route facets from that
  bundle without constructing each domain service directly.
- `services/content_production_admin.py` owns content-production readiness,
  diagnostics, and workbench service methods used by admin routes.
- `services/catalogs.py` owns workflow, content-generation, and capability catalogs used by the facade.
- `services/content_production_console.py` owns content-production case/run reporting, review, artifact, and export operations.
- `services/content_production_runs.py` owns content-production preflight,
  run, and replay orchestration.
- `services/content_production_run_templates.py` owns UI-ready content-production
  launch template construction from session/task/asset context.
- `services/content_production_run_payloads.py` owns request/replay payload
  normalization helpers shared by run and template services.
- `services/content_production_preflight.py` is a compatibility export surface
  for preflight helpers used by older imports.
- `services/content_production_preflight_checks.py` owns content-production
  readiness gates and deterministic run rejection.
- `services/content_production_preflight_actions.py` owns repair/next-step
  actions and preflight links returned to the UI.
- `services/content_production_preflight_summaries.py` owns asset, market, and
  reference-image preflight summaries.
- `services/experiment_jobs.py` owns experiment job lookup/cancellation and session task status synchronization.
- `services/session_store.py` is the backend session persistence port around
  `nori.sessions.SessionManager`; backend services use it for session lookup,
  save, task lookup, and 404 normalization instead of reaching into manager
  internals. Session assets, reference-image checks, experiment job sync, and
  content-production run orchestration all share this port.
- `services/session_assets.py` owns backend sessions, uploaded assets, and asset file access.
- `services/reference_images.py` coordinates session state for reference
  publishing and image-provider reference checks.
- `services/reference_image_publishers.py` owns publish diagnostics and
  session-asset URL publishing strategies.
- `services/reference_image_generation.py` owns live image-provider reference
  checks.
- `services/reference_image_results.py` owns reference-image result payloads,
  event payloads, and next-action builders.
- `routing.py` is the route composition root; it includes the focused routers in `routes/`.
- `routes/system.py` owns health and capability endpoints.
- `routes/workflows.py` owns workflow catalog and workflow resolution endpoints.
- `routes/content_generation.py` owns content-generation option/action planning endpoints.
- `routes/sessions.py` owns session, task, upload, and reference-asset endpoints.
- `routes/experiment_jobs.py` owns background experiment job endpoints.
- `routes/content_production_admin.py` owns content-production readiness, diagnostics, run-template, overview, workbench, and report endpoints.
- `routes/content_production_cases.py` owns case selection, replay, evaluation, delivery, timeline, and export endpoints.
- `routes/content_production_runs.py` owns run execution, preflight, listing, comparison, replay, evaluation, artifact, and export endpoints.
- `contracts.py` owns API request models and shared response/error shapes.
- `experiments/runner.py` owns content-production execution and workflow invocation.
- `experiments/runner_manifests.py` owns runner input manifests, experiment
  manifests, replay snapshots, and run-response projection.
- `experiments/models.py` owns typed case/run identifiers used at storage boundaries.
- `experiments/repositories.py` owns the current JSON/filesystem experiment repository boundary.
- `experiments/diagnostics.py` owns model/reference readiness and diagnostic action planning.
- `experiments/runs.py` owns run listing, run summaries, filters, and run
  comparison row projection plus shared count helpers for experiment summaries.
- `experiments/presenters.py` owns shared product-facing report projections
  such as run report rows and best-run scoring.
- `experiments/artifacts.py` owns artifact catalogs, artifact resolution, and
  zip exports.
- `experiments/reference_images.py` owns image-reference summary and trace
  projections for run manifests and reports.
- `experiments/cases.py` owns case overview, reports, selected-run resolution,
  comparisons, and case listing.
- `experiments/workbench.py` owns the product-console workbench snapshot that
  combines diagnostics, overview, comparison, delivery, and active artifacts.
- `experiments/selections.py` owns case selection state, selection history,
  and run promotion decisions.
- `experiments/actions.py` owns case-level next-action planning, repair
  actions, review actions, and rerun prompts.
- `experiments/delivery.py` owns case-level delivery readiness, handoff payloads,
  and review evidence for delivery/export bundles.
- `experiments/timelines.py` owns read-only case timeline assembly for runs,
  evaluations, and selections.
- `experiments/visual_reviews.py` owns visual-reference review panels and their
  rule-based evaluation-review adapter.
- `experiments/acceptance.py` owns run proof and operator acceptance report
  assembly.
- `experiments/reference_acceptance.py` owns reference-transfer snapshots,
  strict-reference proof checks, and provider reference-image acceptance checks.
- `experiments/auto_reviews.py` owns automatic review-gate assembly, run-health
  review scoring, and evaluation draft projection from review signals.
- `experiments/reviews.py` owns evaluation draft entrypoints, evaluation
  summaries, persistence, and manifest refresh.
- `jobs.py` owns the current process-local background job model, store,
  execution state, and JSON persistence.
- `job_presenters.py` owns background job/run links, actions, and
  content-production run result enrichment returned to API clients.

## Routes

| Route | Role |
| --- | --- |
| `GET /health` | Basic service health. |
| `GET /docs` | FastAPI Swagger UI. |
| `GET /openapi.json` | FastAPI-generated OpenAPI description for tools/frontend work. |
| `GET /capabilities` | Product capability groups exposed by the backend. |
| `GET /experiments/readiness` | Inspect active models, reference-image support, and OSS readiness for backend experiments. |
| `GET /experiments/content-production/diagnostics` | Diagnose content-production model/reference/OSS/backend-public-URL readiness with checks and recommended actions. |
| `POST /experiments/content-production/reference-publish-check` | Verify reference-image publishing by sending a backend-owned tiny PNG through the configured reference publisher. |
| `POST /experiments/content-production/reference-image-generation-check` | Opt-in live image-provider check that calls the active image model with provider-fetchable `reference_images`. |
| `POST /sessions/{session_id}/assets/reference-image-generation-check` | Publish selected session image assets, optionally probe resulting URLs, then call the active image model with provider-fetchable references. |
| `GET /experiments/jobs` | List in-process background experiment jobs, filterable by `status`, `session_id`, `case_id`, or `job_type`. |
| `GET /experiments/jobs/{job_id}` | Inspect one in-process background experiment job. |
| `POST /experiments/jobs/{job_id}/cancel` | Request cancellation for one in-process background experiment job. |
| `GET /experiments/content-production/workbench` | Build a one-call experiment-console snapshot with diagnostics, overview, case rows, and primary actions. |
| `GET/POST /experiments/content-production/run-template` | Build a validated content-production launch request template with missing fields, selected assets, reference readiness, and next actions. GET infers from session metadata; POST accepts a form draft body. |
| `GET /experiments/content-production/overview` | Aggregate recorded content-production run health for dashboards and operators. |
| `GET /experiments/content-production/report` | Build a case-level experiment report with best/latest run, accepted/needs-review/rejected ids, blocker summaries, and recommended next actions. |
| `GET /experiments/content-production/cases` | List recorded content-production cases with latest run, current selection, status/reference/evaluation counts, readiness counts, and case-level action links. |
| `GET/POST /experiments/content-production/cases/{case_id}/selection` | Read or record the current operator selection for a case, with append-only decision history. |
| `GET /experiments/content-production/cases/{case_id}/selected-run` | Resolve the current selected run detail for a case, optionally falling back to the report's `best_run`. |
| `GET /experiments/content-production/cases/{case_id}/compare` | Build a case-centered decision snapshot with candidates, selected/best/recommended run ids, differences, and next actions. |
| `GET /experiments/content-production/cases/{case_id}/next-actions` | Return a backend-derived action plan for the case: select best run, draft/record evaluation, fix blockers, rerun, or promote. |
| `POST /experiments/content-production/cases/{case_id}/promotion` | Promote an accepted run into the current case decision, writing a `promoted` selection and returning review/export links. |
| `POST /experiments/content-production/cases/{case_id}/replay` | Replay a case's requested, selected, or best run without the frontend resolving a run-level replay URL. |
| `POST /experiments/content-production/cases/{case_id}/evaluations/draft` | Build an evaluation draft for the selected or best case run without the frontend resolving a run-level evaluation URL. |
| `POST /experiments/content-production/cases/{case_id}/evaluations` | Record an evaluation on the selected or best case run, with optional explicit `run_id` override. |
| `GET /experiments/content-production/cases/{case_id}/delivery` | Inspect whether a case is ready to hand off: promoted selection, accepted run, complete core artifacts, export link, and delivery payload. |
| `GET /experiments/content-production/cases/{case_id}/delivery/export` | Download the delivery-gated handoff zip for the promoted run, including delivery metadata and whitelisted run artifacts. |
| `GET /experiments/content-production/cases/{case_id}/timeline` | Inspect a read-only case timeline of run, evaluation, and selection events. |
| `GET /experiments/content-production/cases/{case_id}/export` | Download a case-level experiment archive containing report, selection history, case summary, and run summaries. |
| `GET /workflows` | List workflow catalog entries available to product surfaces. |
| `POST /workflows/resolve` | Resolve a generic product request to a workflow or direct action. |
| `GET /workflows/content-production` | Inspect the content-production workflow catalog entry. |
| `GET /content/generation/options` | List selectable content-generation option groups. |
| `GET /content/generation/options/{group_id}` | Inspect one option group such as `image_source` or `cover_strategy`. |
| `GET /content/generation/actions` | List direct content-generation sub-capabilities and workflow-backed actions. |
| `GET /content/generation/actions/{action_id}` | Inspect one action such as `content.cover`. |
| `POST /content/generation/plan` | Normalize a content request and recommend direct action versus workflow. |
| `POST /sessions` | Create an in-process session through `nori.sessions.SessionManager`. |
| `GET /sessions` | List in-process sessions. |
| `GET /sessions/{session_id}` | Inspect one session. |
| `POST /sessions/{session_id}/turns` | Append a user/assistant/system turn. |
| `POST /sessions/{session_id}/tasks` | Start a task goal for a session. |
| `GET /sessions/{session_id}/assets` | List image assets uploaded for a session. |
| `POST /sessions/{session_id}/assets` | Upload one or more image assets for later generation runs. |
| `GET /sessions/{session_id}/assets/{asset_id}/file` | Download one uploaded local asset through the backend. |
| `POST /sessions/{session_id}/assets/publish-references` | Publish uploaded image assets into provider-fetchable reference URLs and store them on the session asset rows. |
| `POST /workflows/content-production/runs/preflight` | Validate a content-production run request without executing LLM/image calls. |
| `POST /workflows/content-production/runs` | Run the content-production workflow with session assets, brief text, market evidence, human-gate mode, and optional background execution. |
| `GET /workflows/content-production/runs` | List recorded content-production experiment runs with `case_id`, status/proof/reference/evaluation filters, search, and pagination metadata. |
| `GET /workflows/content-production/runs/compare` | Compare two or more recorded runs from one case by input differences, artifact coverage, reference-image fidelity, and review readiness. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}` | Inspect one run's experiment manifest, input manifest, artifacts, workflow stages, covers, and image-reference fidelity. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/acceptance` | Return the derived run acceptance report with accepted/needs_review/rejected status, blocking checks, warnings, and evidence. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/evaluations` | List manual or automated evaluation records attached to one run. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft` | Build a deterministic review-gate evaluation draft from run artifacts, optionally persisting it with `persist=true`. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations` | Record a bounded evaluation for one run, including reviewer, status, score, issues, metrics, and notes. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/replay` | Replay one run from its stored `replay_request.json`, with optional request overrides and sync/background execution. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/export` | Download a zip bundle for one recorded run, including whitelisted artifacts, covers, an export manifest, and optionally local input images with `include_inputs=true`. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect` | Build a product-ready artifact inspection payload with content package data, manifests, markdown text, cover previews, proof, acceptance, evaluations, and download links. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name}` | Download a whitelisted run artifact such as `input_manifest.json`, `replay_request.json`, `summary.md`, `content_package.json`, or `covers/<cover>.png`. |

Responses use:

```json
{"code": 0, "message": "ok", "data": {}}
```

Errors use the same shape with `code` set to the HTTP status code.

## Product Capability Shape

The backend exposes workflow orchestration and direct product sub-capabilities
side by side:

- Use `/content/generation/options` when the frontend needs to render controls
  such as platform, artifact type, image source, cover strategy, reference
  policy, and human-gate mode.
- Use `/content/generation/actions` when the frontend needs to know which
  content sub-capabilities exist, such as spec design, package generation, or
  cover generation.
- Use `/content/generation/plan` when the frontend has a user intent and wants
  a recommended next API route without forcing the user to choose a workflow id.
- Use `/workflows/resolve` when the product explicitly wants generic
  workflow-or-direct-action routing.
- Use `/experiments/readiness` before enabling strict reference-image runs; it
  reports active models, whether the image model supports references, whether
  relay needs public URLs, and which OSS env vars are missing. The top-level
  `ready` flag is false when any active model lookup fails; per-model entries
  include `ready`, `error_type`, and `error` for product diagnostics instead of
  making the readiness route fail with 500.
- Use `/experiments/content-production/diagnostics` for operator/product setup
  screens. It wraps readiness into named checks, `blocking_checks`,
  `warning_checks`, and `recommended_actions` for model configuration,
  reference-image capability, OSS reference storage, backend public URL, and
  strict-reference mode.
- Use `/experiments/content-production/workbench` as the default experiment
  console bootstrap call. It combines diagnostics, overview rows, case summaries,
  and each case's backend-derived `primary_action`, so product clients can render
  state and CTA buttons without issuing N+1 case action requests or duplicating
  backend experiment rules. Optional query params: `case_id`, `limit`, and
  `include_diagnostics`. When `case_id` is provided, the response also includes
  `case_compare`, `case_delivery`, `active_run_id`, and
  `active_run_artifacts` so a case review page can render comparison state, the
  formal handoff gate, and the active run's artifact panel from the same
  bootstrap call. The response `links` and each case row's `links` also include
  `run_template`, `case_evaluation_draft`, and `case_evaluations`, so launch and
  review buttons can call backend-owned endpoints without reconstructing URLs.
- Use `/experiments/content-production/run-template` before preflight/run forms.
  GET builds a concrete `ContentProductionRunRequest` from session metadata,
  selected task, uploaded assets, backend public URL, market evidence, and
  reference policy. POST accepts the same draft fields in a JSON body, so a Web
  form can pass unsaved `brief_text`, `market_evidence`, `config`, `asset_ids`,
  and metadata to the backend planner. The response includes
  `ready_for_preflight`, `missing_fields`, preflight-compatible `checks`,
  selected asset/reference summaries, and action hints such as create session,
  upload references, attach market evidence, publish references, run preflight,
  run experiment, or optionally check whether the active image provider accepts
  the selected public references. Template actions use a consistent
  `method`/`href`/`payload` shape, and field-repair actions include
  `input_fields` so the frontend can render missing controls without duplicating
  backend readiness rules.
- Use `POST /experiments/content-production/reference-publish-check` when
  readiness says OSS/backend reference transfer should work and you want to
  verify the actual publisher path. The backend generates a tiny PNG itself,
  sends it through the configured `ReferenceImagePublisher`, and returns
  `ready`, `public_reference_url`, `object_key`, `reason`, and `next_actions`.
  It does not read arbitrary user-provided file paths.
- Use `POST /experiments/content-production/reference-image-generation-check`
  only when you explicitly want a live provider call proving the active image
  model accepts `reference_images`. The request accepts provider-fetchable HTTPS
  `reference_images`, optional `prompt`, `size`, and `metadata`; invalid/local
  references return `ready=false` without calling the model. This route may spend
  image-model credits, so keep it out of default health checks.
- Use `POST /sessions/{session_id}/assets/reference-image-generation-check`
  when the product flow starts from uploaded session assets. The backend first
  publishes selected assets through `backend_public_base_url`, `public_url_map`,
  or OSS, then calls the active image model only if provider-fetchable reference
  URLs exist. Set `verify_reference_urls=true` to probe those URLs first; probe
  failures return `reference_url_probe_failed` without spending an image-model
  call. This is the preferred one-call diagnostic before a strict reference-image
  live run, and it records a compact `reference_image_generation_checked`
  session event for audit/replay context. The latest check is also surfaced as
  `latest_reference_image_generation_check` on session/session-assets responses
  and as `reference_images.latest_check` in run-template/preflight responses.
  Content-production runs copy the latest check into
  `input_manifest.reference_image_generation_check` and
  `experiment_manifest.reference_images.latest_generation_check`, including
  whether the checked URLs cover the selected references for that run. Set
  `require_reference_image_generation_check=true` on preflight/run requests when
  a strict experiment must refuse generation until the latest provider check is
  successful and covers the selected references.
- Use `POST /sessions/{session_id}/assets/publish-references` after image
  upload when the image provider needs provider-fetchable HTTPS references.
  The route reuses `nori.storage.ReferenceImagePublisher`, writes
  `public_reference_url` and object-key metadata back onto session asset rows
  when publishing succeeds, and returns `ready=false` instead of inventing a URL
  when OSS/public mapping is unavailable. If the request includes a real
  `backend_public_base_url`, uploaded local assets are published as backend
  file-serving URLs without calling OSS.
- Session state is local but durable by default for backend experiments:
  `NoriBackend` writes session snapshots under `data/backend/sessions`.
  Restarts can recover session turns, task goals/status, events, uploaded asset
  rows, and stored `public_reference_url` values. This is not a production DB
  or multi-worker consistency layer.
- Use `/workflows/content-production/runs/{case_id}/{run_id}` after a run to
  inspect `experiment_manifest`, `input_manifest`, `image_reference.status`,
  `sent`, `fallback`, `reference_transfer`, uploaded object keys, cover paths,
  stage status, `artifact_catalog`, the derived `proof` summary, and
  `visual_reference_review`.
  `artifact_catalog` is the recommended source for product artifact panels: it
  includes whitelisted artifact names, URLs, media types, sizes, SHA-256 hashes,
  and short text previews for JSON/Markdown. `proof.status`, `failed_checks`,
  and `warning_checks` are the product-facing aggregate for experiment detail
  pages; `input_integrity` verifies recorded fingerprints against the current
  brief, replay request, config, market evidence, metadata, and local asset
  hashes. The manifests remain the underlying evidence. Run results also include
  backend-owned `links` and ordered `actions` for artifact inspection, case-level
  evaluation drafts, case next actions, replay, export, and promotion.
- Use `/workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect`
  for the main run review panel. It wraps the whitelisted catalog into
  product-ready sections: content package JSON data, input/experiment/replay
  manifests, Markdown text, cover preview URLs, missing core artifacts, proof,
  acceptance, evaluations, `visual_reference_review`, and
  export/replay/evaluation links.
- Use `/workflows/content-production/runs/{case_id}/{run_id}/acceptance` when a
  product UI or operator needs the final experiment verdict. The report is
  derived from current run files and returns `accepted`, `needs_review`, or
  `rejected` plus named blocking/warning checks for workflow completion, proof
  readiness, input integrity, core artifacts, export/replay availability, strict
  image-reference transfer, provider reference-image generation-check evidence,
  and evaluation status.
- Use `/workflows/content-production/runs/compare?case_id=...&run_id=a&run_id=b`
  to compare recorded experiments without rerunning models. The backend reads
  each run's manifests and returns status/reference counts, changed inputs,
  image-model differences, artifact-name coverage, and per-run
  `candidate.ready_for_review` blockers.
- Use `/experiments/content-production/cases/{case_id}/next-actions` after a
  rejected strict-reference run. Reference repair actions include concrete
  session hrefs and payloads when the run manifest has `session_id` and
  `asset_ids`, so product clients can call publish/check routes directly rather
  than reconstructing them from artifacts. The paired replay action also carries
  the same `session_id`, preserving session-level provider-check evidence after
  a repair step.
- Use `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations`
  to attach manual or automated experiment judgment after inspecting a run.
  Evaluations are persisted as `experiment_evaluations.json`, summarized back
  into `experiment_manifest`, and included in run detail and run comparison.
  Supported statuses are `passed`, `needs_revision`, `blocked`, and `pending`;
  scores are bounded to 0-100.
- Use `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft`
  to let the backend generate a deterministic evaluation draft from
  `content_package.json`, replay/config context, and the existing
  `ReviewGateAgent`. It returns reviewer-specific issues, aggregate metrics,
  and a bounded evaluation payload. By default it does not mutate the run; pass
  `persist=true` to append the draft through the normal evaluation writer. The
  draft also includes a `run_health` reviewer derived from `proof` and
  `acceptance`, so missing market evidence, cover output, replay snapshots,
  exportability, strict reference-image transfer, or missing provider
  reference-check proof become evaluation issues instead of being hidden outside
  the review flow. When visual references were
  selected or required, the draft also includes a `visual_reference` reviewer:
  sent references without a passing human evaluation stay `pending` instead of
  being treated as automatically visually faithful.
- Use `/workflows/content-production/runs` for experiment-console tables. It
  supports `case_id`, `status`, `proof_status`, `reference_status`,
  `evaluation_status`, `search`, `limit`, and `offset`; responses include
  `total_count`, `filtered_count`, `returned_count`, `has_more`, active
  `filters`, and filtered status summaries.
- Use `/experiments/content-production/overview` when the frontend or operator
  needs a dashboard-level experiment view. It aggregates recorded runs by case,
  status, reference-image fidelity, evaluation status, review readiness, and
  blocking reasons without rerunning models or reading local files directly
  from the product client. Latest run rows include `proof_status`,
  `proof_failed_checks`, and `proof_warning_checks` for list/table views.
- Use `/experiments/content-production/report?case_id=...` when the frontend or
  operator needs a case-level conclusion. It selects the strongest run,
  separates accepted/needs_review/rejected ids, summarizes blocking and warning
  checks, and returns recommended actions such as promoting an accepted run,
  fixing reference transfer, rerunning cover generation, or recording an
  evaluation.
- Use `/experiments/content-production/cases/{case_id}/selection` when an
  operator or product flow needs to persist the actual experiment decision. The
  POST route records `run_id`, `decision`, reviewer, reason, notes, metadata,
  whether the selected run matched the report's `best_run`, and a compact run
  status snapshot in `experiment_selection.json`; the GET route returns the
  current selection, full history, and latest report.
- Use `/experiments/content-production/cases/{case_id}/selected-run` when the
  product UI needs the full detail for the current experiment decision in one
  request. It resolves the current selection when present; with the default
  `fallback_to_best=true`, it returns the report's `best_run` when no operator
  selection has been recorded yet. It does not write selection state.
- Use `/experiments/content-production/cases/{case_id}/compare` for the main
  case decision page. It combines the case report, operator selection,
  candidate rows, run differences when two or more runs exist, and the same
  backend-derived primary action returned by `next-actions`.
- Use `/experiments/content-production/cases/{case_id}/next-actions` when the
  experiment console needs a product-ready action model instead of rebuilding
  backend rules in the browser. It returns `status`, `primary_action`, ordered
  `actions`, the selected/best/target run ids, and method/href/payload hints for
  flows such as selecting the best run, drafting or recording an evaluation,
  fixing reference transfer, replaying a run, or promoting an accepted result.
  For a new case, `run_first_experiment` points to
  `/experiments/content-production/run-template?...` so the UI first gets the
  backend launch template, missing-field checks, and preflight payload instead
  of POSTing an incomplete run.
- Use `POST /experiments/content-production/cases/{case_id}/replay` when the UI
  wants to rerun a case without resolving the run-level replay route itself. The
  request accepts the same body as run replay plus optional `run_id`; if omitted,
  the backend replays the current selection or falls back to the report best run.
  Sync and background execution modes are both supported.
- Use `POST /experiments/content-production/cases/{case_id}/evaluations/draft`
  and `POST /experiments/content-production/cases/{case_id}/evaluations` as the
  default product review endpoints. Both routes accept an optional `run_id`; when
  omitted, the backend targets the current case selection and then falls back to
  the report best run. Drafts can still pass `persist=true`, and records are
  written to the resolved run's normal `experiment_evaluations.json`. Keep the
  run-level evaluation routes for explicit run-detail/debug screens.
- Use `POST /experiments/content-production/cases/{case_id}/promotion` to close
  the accepted-run path. The backend resolves the requested run, verifies the
  acceptance report is `accepted`, records a `promoted` selection, and returns
  selected-run, artifact-inspection, export, replay, and next-action links.
  Set `allow_unaccepted=true` only for explicit operator overrides; the response
  marks those promotions with `override=true`.
- Use `/experiments/content-production/cases/{case_id}/delivery` as the
  handoff gate. By default `ready=true` requires a `promoted` selection, an
  `accepted` run, complete core artifacts, and an export URL. Pass
  `allow_unpromoted=true` only for preview UIs; the response then returns
  `status=preview_ready` with an `unpromoted_preview` warning instead of treating
  the case as formally promoted.
- Use `/experiments/content-production/cases/{case_id}/delivery/export` for the
  actual handoff package. It is protected by the same delivery gate and returns
  HTTP 400 when the case is not ready, unless `allow_unready=true` is explicitly
  passed for a preview/debug bundle. The zip includes `delivery.json`,
  `artifact_inspection.json`, `review_evidence.json`, `case_compare.json`,
  `next_actions.json`, `run_summary.json`, and whitelisted run artifacts under
  `run/`.
- Use `/experiments/content-production/cases/{case_id}/timeline` for experiment
  audit and replay-oriented UI. It derives run started/finished events,
  evaluation records, and selection records from existing backend artifacts,
  orders them by timestamp, and does not write new state.
- Use `/experiments/content-production/cases/{case_id}/export` when a case-level
  experiment decision needs to be archived or handed off. The zip contains
  `case_report.json`, `case_selection.json`, `case_summary.json`, per-run
  `runs/{run_id}/summary.json`, and `case_export_manifest.json`. Large run
  artifacts and cover images stay behind the existing per-run export links.
- Use `/experiments/content-production/cases` for lightweight sidebar or case
  selector views. It returns case-level summaries, current selection snapshots,
  latest-run links, and backend-owned launch-template, review, replay, delivery,
  timeline, and export links without requiring the client to extract them from the full
  overview payload or issue N+1 selection lookups.
- Use `python scripts/backend_holly_smoke.py` as the default backend closure
  check for the local Holly fixture. Add `--run` only when you explicitly want
  live workflow/model execution. Add `--api-base-url http://127.0.0.1:8000`
  when you want the smoke to exercise a real running FastAPI backend instead of
  the default in-process TestClient. This is the right mode for local runs even
  when `--backend-public-base-url` points at an HTTPS tunnel/domain for that
  same backend instance; the API can stay local while provider-fetchable file
  URLs use the public tunnel. When `--require-image-references` or
  `--backend-public-base-url` is present, the smoke publishes uploaded assets
  through `/sessions/{session_id}/assets/publish-references` before preflight,
  so preflight and run requests consume the same stored `public_reference_url`
  rows that the product UI uses. If `--run --require-image-references` is used,
  the script now rejects placeholder/local `--backend-public-base-url` values
  before model calls when a base URL is supplied; use a real HTTPS
  tunnel/production backend URL, configure OSS, or omit strict references for
  non-strict live smoke runs. Backend
  preflight and run gates share the same provider-fetchable URL rule, so
  placeholder/local URLs no longer produce `ready=true` in strict mode. Live
  strict Holly smoke also sends `verify_reference_urls=true`, which probes each
  selected reference URL before model calls. Add `--verify-reference-urls` to
  run the same URL reachability probe during preflight-only smoke, which is the
  cheapest way to catch a broken tunnel/public backend before spending model
  calls. Add `--check-reference-image-generation` when you explicitly want one
  small image-provider call proving the active image model accepts the published
  reference URLs before a full workflow run; if preflight has no provider-fetchable
  reference URL, the smoke returns `no_provider_fetchable_reference_images` and
  stops without calling the image model. For live debugging, pass
  `--stage-timeout-seconds` and `--content-package-timeout-seconds` to force
  backend stage timeouts and verify that failed runs write `workflow_run.json`,
  `experiment_manifest.json`, replay links, and stage-level timeout metadata
  instead of hanging without artifacts. Timeout metadata includes whether the
  stage was interrupted by a main-thread signal or returned from a worker-thread
  guard while the underlying provider call may still complete later.
- Use `POST /workflows/content-production/runs/preflight` before expensive
  live/backend runs. It uses the same session/task validation and asset
  selection path as the real run, but does not create a task or call LLM/image
  providers. The response includes `ready`, per-check statuses, selected asset
  rows, provider-fetchable reference URL counts, market-evidence status, and
  reference-image readiness. It also includes backend-derived `actions` and
  `links`: ready preflights expose a `run_experiment` POST action and, when
  strict references are already provider-fetchable, an optional
  `check_reference_image_generation` action that points at the session-asset
  diagnostic endpoint; failed preflights expose repair
  actions such as `attach_market_evidence`,
  `upload_reference_assets`, `publish_reference_assets`, or
  `set_backend_public_base_url`.
  Set `verify_reference_urls=true` when preparing a live strict-reference run;
  preflight then adds `reference_url_reachability` and
  `reference_images.url_probe` with per-URL status/error details.
- Real `/workflows/content-production/runs` calls reuse the deterministic
  preflight gates before task creation. For the default real experiment runner,
  unready model configuration, missing required `market_evidence`, no selected
  images in strict reference mode, or selected local references that cannot
  reach the image provider return HTTP 400 without starting a task or calling
  the workflow. Injected fake/custom runners can skip the model-readiness gate
  for deterministic offline tests, while still sharing the same input and
  reference-transfer guards. Deterministic preflight-gate HTTP 400 responses
  include the same repair `actions` and `links` as preflight responses.
- Every run now records `input_manifest.reference_transfer` and mirrors it under
  `experiment_manifest.inputs.reference_transfer`. This is the pre-generation
  audit snapshot for selected assets, provider-fetchable URLs, and strict
  public-URL readiness; the post-generation truth still lives in
  `experiment_manifest.reference_images.sent/status`. Run detail also exposes
  `image_reference.trace`, a per-reference audit row that connects selected
  path, uploaded asset id/filename when available, public/provider-fetchable
  URL, publish reason, upload/object key, and whether that reference was sent to
  the image gateway.
- When a workflow fails after a run workspace is created, the backend still
  writes `workflow_run.json`, `experiment_manifest.json`, and related failure
  artifacts. Sync runs return HTTP 500 with `data.run` pointing to the failed
  run summary, including artifact URLs and the structured manifest error.
  Background jobs keep the same failed run summary in `job.result`, so polling
  clients still get `links.run`, `links.export`, `links.evaluations`,
  `links.inspect_artifacts`, `links.replay`, and ordered failure-review actions.
- Use `execution_mode="background"` on
  `/workflows/content-production/runs` for long-running local/backend
  experiments. The route returns HTTP 202 with a `job_id`; poll
  `/experiments/jobs/{job_id}` until `status` is terminal.
  Use `/experiments/jobs` to list recent jobs by `status`, `session_id`,
  `case_id`, or `job_type`. Job records are also written as JSON snapshots
  under `data/backend/jobs` for audit/debug. Execution is still in-process:
  jobs found on disk as `queued` or `running` after a restart are marked
  `interrupted`, not resumed. For session-backed jobs, backend startup also
  updates the linked task to `interrupted` and records
  `workflow_run_interrupted`, so product clients do not keep showing a stale
  running task after a local process restart.
  `POST /experiments/jobs/{job_id}/cancel` records an operator cancellation
  request. A still-queued job becomes `cancelled`; an already-running in-process
  thread becomes `cancelling` and remains pollable until the model/workflow call
  returns because the local worker cannot be safely force-killed. If the job was
  created by a backend session task, the cancel route also updates the task
  status to `cancelled` or `cancelling` and records either
  `workflow_run_cancelled` or `workflow_run_cancel_requested` on the session
  event log.
  Successful content-production jobs expose direct `links.run`,
  `links.export`, `links.evaluations`, `links.evaluation_draft`,
  `links.inspect_artifacts`, and `links.replay` fields once the runner returns a
  `run_id`. Job records also include `actions`: queued/running jobs expose
  `poll_job`, while terminal jobs mirror the run's inspect/review/next-action/
  export/replay/promote actions so product clients can continue without
  reconstructing URLs.
- Use the returned `artifact_urls`, `cover_urls`, and asset `file_url` fields
  for frontend rendering/downloads. Absolute filesystem paths stay in the
  response for local debugging, but product clients should not read them
  directly.
- Use `input_manifest` as the experiment audit surface. It records the
  `session_id`, `task_id`, brief hash, selected assets, public reference URL
  mapping, `execution_mode`, `require_image_references`, `human_gate_mode`,
  config, market-evidence counts, and stable `fingerprints` for the brief,
  replay request, config, market evidence, metadata, and selected asset hashes.
  It does not duplicate image bytes or secrets. Run proof recomputes these hashes
  and reports `input_integrity=failed` if a replay request, brief, config, market
  payload, metadata, or local asset no longer matches the manifest.
- Use `experiment_manifest` as the product-facing run summary. It is also
  persisted as `experiment_manifest.json` and groups the run identity, session
  and task ids, selected input assets, model readiness snapshot, reference-image
  fidelity, input fingerprints, artifact URLs, replay endpoint, and structured
  failure metadata when a workflow fails.
- Use `/workflows/content-production/runs/{case_id}/{run_id}/export` when a
  reviewer, frontend, or experiment notebook needs a portable run bundle. The
  zip is built by the backend from whitelisted run files only: top-level
  `.json` / `.md` artifacts, cover images under `covers/`, and a generated
  `export_manifest.json` with file sizes and hashes. It does not expose
  arbitrary local paths or private non-artifact files. Add
  `?include_inputs=true` when the reviewer also needs local image inputs from
  `input_manifest.assets`; included files are copied under `inputs/`, while
  remote, missing, duplicate, or unsupported inputs are reported in
  `export_manifest.skipped_inputs`.
- Use `artifact_urls["replay_request.json"]` when you need a reproducibility
  snapshot. It stores the request-shaped payload with full `market_evidence`,
  selected `asset_paths`, config, and run options so a later local/backend
  experiment can replay the same inputs with minimal manual reconstruction.
- Use `POST /workflows/content-production/runs/{case_id}/{run_id}/replay`
  when the backend should rerun that snapshot directly. By default replay
  creates a new in-process session and task, clears stale old `asset_ids`, and
  uses the saved `asset_paths`. Pass `session_id`/`task_id` only when you want
  to intentionally attach replay to an existing in-process session. The same
  `execution_mode="background"` job path is supported for long replays.
  When `require_reference_image_generation_check=true`, replay ignores any
  stale provider-check evidence stored in `replay_request.json`; the replay
  session must have a current `reference_image_generation_checked` event that
  covers the selected references.
  Prefer the case-level replay route from product screens when the source run
  should be derived from the case decision state.

Direct content actions such as `content.cover` are still cataloged before they
become standalone execution routes. The end-to-end executable path is now the
backend `content-production` run API: upload images to the session, pass their
`asset_ids` plus `market_evidence`, and the backend forwards the selected image
paths into the workflow's `asset_paths`.

Minimal experiment shape:

```bash
curl -F "files=@/path/to/reference.png" \
  http://127.0.0.1:8000/sessions/{session_id}/assets

curl -X POST http://127.0.0.1:8000/sessions/{session_id}/assets/publish-references \
  -H 'content-type: application/json' \
  -d '{
    "asset_ids": ["asset_xxx"],
    "project": "Holly",
    "backend_public_base_url": "https://your-public-backend.example"
  }'

curl -X POST http://127.0.0.1:8000/workflows/content-production/runs/preflight \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "{session_id}",
    "brief_text": "参考上传图片生成一篇小红书图文",
    "asset_ids": ["asset_xxx"],
    "backend_public_base_url": "https://your-public-backend.example",
    "market_evidence": {"platform":"xhs","queries":["关键词"],"hot_notes":[],"insufficient":[]},
    "require_image_references": true,
    "human_gate_mode": "skip"
  }'

curl -X POST http://127.0.0.1:8000/workflows/content-production/runs \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "{session_id}",
    "brief_text": "参考上传图片生成一篇小红书图文",
    "asset_ids": ["asset_xxx"],
    "market_evidence": {"platform":"xhs","queries":["关键词"],"hot_notes":[],"insufficient":[]},
    "execution_mode": "sync",
    "require_image_references": true,
    "human_gate_mode": "skip"
  }'
```

When `require_image_references=true`, local uploaded images must be publishable
as provider-fetchable HTTPS URLs. This can happen through the OSS reference
publisher, through `NORI_BACKEND_PUBLIC_BASE_URL`, or by passing
`backend_public_base_url` in a publish, preflight, or run request when the
backend is reachable through a public HTTPS tunnel/domain. Public image URLs can
also be supplied through `asset_paths`.

## Boundary Rules

- Do not put prompt construction, agent policy, LLM calls, crawler calls, or
  artifact-generation logic in `backend/`.
- Do not import deep `nori.agents.*` implementation modules here. Call stable
  runtime/session/workflow contracts.
- Keep HTTP/request validation, FastAPI route declarations, and response shaping
  here, close to the product surface.
- Uploads and job snapshots are local experiment files under `data/backend`;
  session snapshots are local JSON files under the same backend data area.
  Production auth, database-backed storage, streaming, durable queues, and
  deployment middleware are still future backend concerns.
