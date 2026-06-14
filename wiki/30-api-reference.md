<!-- Last verified: 2026-06-01 | Current stage: P1 Account-Ops Backend -->

# API Reference

This project exposes Python contracts plus a lightweight FastAPI backend for
local product and experiment integration.

## Backend Product API

The top-level `backend/` package exposes a lightweight FastAPI surface for
product integration. Responses use `{code, message, data}`. Swagger UI is
available at `/docs` and generated OpenAPI at `/openapi.json`.
Backend sessions are snapshotted as local JSON under `data/backend/sessions`,
so local experiment restarts can recover session turns, task status, uploaded
asset metadata, and stored `public_reference_url` values.

| Route | Contract |
| --- | --- |
| `GET /capabilities` | Lists product capability groups such as `content_generation` and `workflow_orchestration`. |
| `GET /experiments/readiness` | Reports active LLM/vision/image models, per-model readiness/errors, reference-image support, relay public-URL requirements, missing OSS env vars, and whether strict local-upload reference mode is ready. |
| `GET /experiments/content-production/diagnostics` | Wraps readiness into content-production setup checks, blocking/warning check names, and recommended actions for model config, reference-image capability, OSS, backend public URL, and strict-reference mode. |
| `POST /experiments/content-production/reference-publish-check` | Sends a backend-owned tiny PNG through the configured `ReferenceImagePublisher` and reports whether it produced a provider-fetchable HTTPS URL. Returns `ready`, `reason`, `public_reference_url`, `object_key`, `uploaded`, and `next_actions`. |
| `POST /experiments/content-production/reference-image-generation-check` | Opt-in live image-provider check. Request fields: `reference_images` provider-fetchable HTTPS URLs, optional `prompt`, `size`, and `metadata`. Returns `ready`, `reason`, reference counts, `image_count`, provider error details, and `next_actions`. Invalid/local references do not call the model. |
| `POST /sessions/{session_id}/assets/reference-image-generation-check` | Session-asset live image-provider check. Request fields: selected `asset_ids`, optional `backend_public_base_url`, `public_url_map`, `force_publish`, `verify_reference_urls`, `reference_url_probe_timeout`, `prompt`, `size`, and `metadata`. The backend publishes selected assets first, optionally probes resulting URLs, then calls the image model only when provider-fetchable references exist and probes pass. It records a compact `reference_image_generation_checked` session event and exposes the latest check on session/assets/template/preflight responses. |
| `GET /experiments/jobs` | Lists in-process background experiment jobs. Optional query params: `status`, `session_id`, `case_id`, and `job_type`. |
| `GET /experiments/jobs/{job_id}` | Returns one in-process background experiment job with status, timestamps, metadata, result, error, and polling link. |
| `POST /experiments/jobs/{job_id}/cancel` | Records an operator cancellation request for one in-process background experiment job. Body: `{ "reason": "..." }`. |
| `GET /experiments/content-production/workbench` | Builds a one-call experiment-console snapshot. Optional query params: `case_id`, `limit`, and `include_diagnostics`. Response includes diagnostics, overview, enriched case rows, and primary actions. |
| `GET/POST /experiments/content-production/run-template` | Builds a content-production launch request template. GET accepts query params such as `session_id`, optional `task_id`, `case_id`, `goal`, `brief_text`, repeated `asset_ids`, `backend_public_base_url`, `execution_mode`, `human_gate_mode`, and `require_image_references`; POST accepts the same draft fields plus JSON `market_evidence`, `config`, and `metadata`. Response includes `request`, `ready_for_preflight`, `missing_fields`, checks, asset/reference summaries, and next actions. |
| `GET /experiments/content-production/overview` | Aggregates recorded content-production experiment health by run and case. Latest run rows include proof status/check summaries. Optional query params: `case_id` and `limit`. |
| `GET /experiments/content-production/report` | Builds a case-level experiment report for product consoles. Optional query params: `case_id` and `limit`. Returns `best_run`, `latest_run`, accepted/needs-review/rejected run ids, status/check summaries, evaluation issue counts, links, and recommended next actions. |
| `GET /experiments/content-production/cases` | Lists case-level content-production summaries with latest run, current selection, status/reference/evaluation counts, readiness counts, and case-level action links for selection, review, replay, delivery, timeline, and export. |
| `GET /experiments/content-production/cases/{case_id}/selection` | Returns the current operator-selected run for a case, append-only selection history, and the latest case report. |
| `POST /experiments/content-production/cases/{case_id}/selection` | Records a case-level experiment decision. Request fields: `run_id`, optional `decision` (`selected`, `promoted`, `needs_revision`, `rejected`, `archived`), `reviewer`, `reason`, `notes`, and `metadata`. Writes `experiment_selection.json` under the case directory. |
| `GET /experiments/content-production/cases/{case_id}/selected-run` | Resolves the full run detail for the current selected run. Optional query param: `fallback_to_best` defaults to `true`, returning the report `best_run` when no operator selection exists. |
| `GET /experiments/content-production/cases/{case_id}/compare` | Builds the case-centered decision snapshot for experiment consoles. Optional query param: `limit` defaults to `500`. Response includes selected/best/recommended run ids, candidate rows, run differences when two or more runs exist, and next actions. |
| `GET /experiments/content-production/cases/{case_id}/next-actions` | Returns the backend-derived case action plan for experiment consoles. Optional query param: `limit` defaults to `500`. Response includes `status`, `primary_action`, ordered `actions`, selected/best/target run ids, and action method/href/payload hints. |
| `POST /experiments/content-production/cases/{case_id}/promotion` | Promotes an accepted run into the current case decision. Request fields: optional `run_id`, `reviewer`, `reason`, `notes`, `allow_unaccepted`, and `metadata`. By default it rejects runs whose acceptance status is not `accepted`; override promotions must pass `allow_unaccepted=true`. |
| `POST /experiments/content-production/cases/{case_id}/replay` | Replays the requested, selected, or report-best run for a case. Request body is `ContentProductionReplayRequest` with optional `run_id`, replay overrides, metadata, and sync/background execution fields. |
| `POST /experiments/content-production/cases/{case_id}/evaluations/draft` | Builds an evaluation draft for the current case target run. Request fields match the run-level draft route plus optional `run_id`; if omitted, the backend resolves the current selection and then falls back to the case report best run. |
| `POST /experiments/content-production/cases/{case_id}/evaluations` | Records an evaluation on the current case target run. Request fields match the run-level evaluation route plus optional `run_id`; the response includes the resolved `source_case_id`, `source_run_id`, and run selector. |
| `GET /experiments/content-production/cases/{case_id}/delivery` | Returns the case-level handoff readiness snapshot. Optional query param: `allow_unpromoted` defaults to `false`. Response includes `ready`, `status`, `blocking_reasons`, `warning_reasons`, selected run proof/acceptance, artifact inspection, case compare, next actions, and delivery links. |
| `GET /experiments/content-production/cases/{case_id}/delivery/export` | Streams the delivery-gated handoff zip for the resolved run. Optional query param: `allow_unready` defaults to `false`; without it, non-ready delivery returns HTTP 400. The zip includes `delivery_export_manifest.json`, `delivery.json`, `artifact_inspection.json`, `review_evidence.json`, compare/action/run summary JSON, and whitelisted run artifacts under `run/`. |
| `GET /experiments/content-production/cases/{case_id}/timeline` | Returns a read-only chronological case timeline derived from existing artifacts. Events include `run_started`, `run_finished`, `evaluation_recorded`, and `selection_recorded`; optional query param: `limit`. |
| `GET /experiments/content-production/cases/{case_id}/export` | Streams a case-level experiment archive zip with `case_report.json`, `case_selection.json`, `case_summary.json`, per-run summary JSON files, and `case_export_manifest.json`. Large artifacts remain available through per-run export links. |
| `GET /content/generation/options` | Returns selectable content-generation controls: platform, artifact type, image source, cover strategy, reference policy, human-gate mode, and entry mode. |
| `GET /content/generation/actions` | Returns direct content sub-capabilities and workflow-backed actions, including `content.design_spec`, `content.package`, `content.cover`, and `workflow.content_production`. |
| `POST /content/generation/plan` | Normalizes a content request and recommends a direct action or `content-production` workflow without requiring the caller to pass a workflow id. |
| `GET /workflows` / `GET /workflows/{workflow_id}` | Lists and inspects workflow catalog entries. |
| `POST /workflows/resolve` | Resolves a generic product request to a workflow or direct action. |
| `POST /sessions` / `GET /sessions/{session_id}` | Creates and inspects in-process sessions through `nori.sessions.SessionManager`. |
| `GET /sessions/{session_id}/assets` | Lists image assets uploaded for a session. |
| `POST /sessions/{session_id}/assets` | Accepts multipart image uploads, writes them under `data/backend/uploads/{session_id}`, stores asset metadata on the session, and returns `asset_id` rows. |
| `GET /sessions/{session_id}/assets/{asset_id}/file` | Streams one local uploaded asset by looking up the `asset_id` in session metadata. It does not accept arbitrary file paths. |
| `POST /sessions/{session_id}/assets/publish-references` | Publishes selected uploaded image assets so image providers can fetch them as HTTPS references. It can use `backend_public_base_url` for backend file-serving URLs or `nori.storage.ReferenceImagePublisher` for OSS. On success it writes `public_reference_url`, object key when available, and publish reason back to the session asset rows. |
| `POST /workflows/content-production/runs/preflight` | Validates a content-production run request without executing LLM/image calls. It uses the same session/task validation and asset selection path as the real run, then reports `ready`, per-check statuses, selected assets, market-evidence status, and whether selected references are provider-fetchable. |
| `POST /workflows/content-production/runs` | Executes the real `content-production` workflow from backend inputs. The request supplies `session_id`, optional `task_id`, `brief_text`/`goal`, selected `asset_ids` or local/public-URL `asset_paths`, `backend_public_base_url`, `market_evidence`, config overrides, `execution_mode`, `require_image_references`, optional `require_reference_image_generation_check`, and `human_gate_mode`. The backend resolves uploaded assets into `asset_paths` and passes them into `ContentProductionWorkflow.initial_state()`. |
| `GET /workflows/content-production/runs` | Lists recorded backend content-production runs for experiment-console tables. Optional query params: `case_id`, `status`, `proof_status`, `reference_status`, `evaluation_status`, `search`, `limit`, and `offset`. Returns run rows plus `total_count`, `filtered_count`, `returned_count`, `has_more`, active `filters`, and filtered status summaries. |
| `GET /workflows/content-production/runs/compare` | Compares two or more recorded runs from one case. Query params: `case_id`, repeated `run_id`, or comma-separated `run_ids`. Returns status/reference counts, input differences, artifact coverage, image-model differences, and per-run review-readiness blockers. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}` | Returns one run's `experiment_manifest`, `input_manifest`, derived `proof`, `artifact_catalog`, artifact paths/URLs, cover paths/URLs, workflow stages, and `image_reference` fidelity summary. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/acceptance` | Returns a derived run acceptance report with `accepted`, `status`, `blocking_checks`, `warning_checks`, named checks, and evidence for workflow completion, artifacts, export/replay, strict reference-image transfer, and evaluation status. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/evaluations` | Lists bounded manual/automated evaluation records attached to one run and returns an aggregate evaluation summary. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations/draft` | Builds a deterministic `ReviewGateAgent` evaluation draft from run artifacts and replay/config context. The request accepts `reviewer`, `persist`, and `metadata`; `persist=true` appends the draft through the normal evaluation writer. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/evaluations` | Records a run evaluation with `reviewer`, `source`, `status`, optional 0-100 `score`, `notes`, issue rows, metrics, and metadata. Supported statuses are `passed`, `needs_revision`, `blocked`, and `pending`. |
| `POST /workflows/content-production/runs/{case_id}/{run_id}/replay` | Loads the run's stored `replay_request.json` and reruns it through the same backend content-production route. The request can override safe fields such as `case_id`, `execution_mode`, `human_gate_mode`, `backend_public_base_url`, `require_image_references`, `require_reference_image_generation_check`, `market_evidence`, `config`, `asset_paths`, and metadata. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/export` | Streams a backend-built zip bundle for one recorded run, including whitelisted artifacts, covers, an export manifest, and optionally local input images with `include_inputs=true`. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/artifacts/inspect` | Builds a product-ready artifact inspection payload with content package data, input/experiment/replay manifests, Markdown text, cover previews, proof, acceptance, evaluations, missing core artifacts, and review/export/replay links. |
| `GET /workflows/content-production/runs/{case_id}/{run_id}/artifacts/{artifact_name}` | Streams whitelisted run artifacts. Allowed names are top-level `.json`/`.md` artifacts such as `input_manifest.json` and `replay_request.json`, plus `covers/<image>` files under the selected run directory. |

`market_evidence` is required for backend content-production runs unless the
server is constructed with a custom top-notes collector. This keeps the backend
from silently pretending that market research exists when the crawler/evidence
step has not been provided.

The diagnostics route is the setup-screen companion to readiness. It does not
need a session or run request; it converts current model/reference/OSS/backend
public URL state into named checks, `blocking_checks`, `warning_checks`, and
`recommended_actions`. Use it before showing strict reference mode as available
in the product UI.

The reference-publish check route is the runtime verification companion to
diagnostics. It creates a tiny backend-owned PNG and publishes that file through
the configured reference publisher, so it can validate OSS credentials,
endpoint/bucket permissions, and generated public URLs without accepting
arbitrary local file paths from the caller.

The reference-image generation check is a deeper opt-in diagnostic after
publishing and URL reachability have passed. It calls the active image model with
`reference_images`, so it can prove the provider accepts the reference payload.
It may spend image-model credits and should not be used as a default health
check.

The preflight route is the product-facing safety check before expensive or live
experiments. Structural problems such as a missing session, missing task, bad
asset id, unsupported execution mode, or missing local asset path still return
HTTP errors. Experiment-readiness problems return `200` with `ready=false` and
named checks, so the frontend can explain exactly what is missing before
running LLM/image calls. In strict reference mode it also proves whether the
selected uploaded images have provider-fetchable URLs or can be published
through OSS. The response also includes `actions` and `links`: ready preflights
return a `run_experiment` POST action, while failed preflights return repair
actions such as `attach_market_evidence`, `upload_reference_assets`,
`publish_reference_assets`, or `set_backend_public_base_url`. Ready
strict-reference preflights also include an optional
`check_reference_image_generation` action when selected references are already
provider-fetchable.
The optional action points at
`/sessions/{session_id}/assets/reference-image-generation-check` when the
request is backed by uploaded session assets, so product screens can verify the
same assets that will be used by the run. Provider-fetchable means a real public HTTPS URL; placeholder/local hosts such
as `backend.example.test`, `localhost`, private IPs, and RFC example domains are
not counted as fetchable references. This is a backend safety gate for known
bad URLs; actual live strict-reference generation still requires the supplied
backend URL or OSS object URL to be reachable by the image provider.
Set `verify_reference_urls=true` for live strict-reference preflight/run calls
when you want the backend to probe each selected reference URL first. The
response then includes a `reference_url_reachability` check and
`reference_images.url_probe` with per-URL status, content type, and error
details.

The real run route reuses the deterministic preflight gates before creating a
task or calling the workflow. With the default real experiment runner, unready
model configuration, missing required `market_evidence`, strict reference runs
with no selected image assets, and strict reference runs whose selected local
images cannot be sent to the provider return HTTP 400 with the failed check
rows. This keeps failed experiment setup from becoming a partially created
session task or a wasted model run. Injected fake/custom runners can skip the
model-readiness gate for deterministic offline tests, while still sharing the
same input and reference-transfer guards. Deterministic preflight-gate HTTP 400
responses include the same repair `actions` and `links` as the preflight route.

If the workflow fails after a run workspace has been created, the backend still
persists the failure as an experiment. It writes `workflow_run.json`,
`experiment_manifest.json`, and related run artifacts. Sync runs return HTTP 500
with `data.run` containing the failed run summary, artifact URLs, and structured
manifest error. Background jobs keep the same failed run summary in
`job.result`, which means failed jobs can still link to run detail, export,
evaluation, and replay surfaces. Successful and failed run results now also
carry backend-owned `links` and ordered `actions` so clients can inspect
artifacts, draft evaluations, ask for case next actions, replay, export, or
promote without reconstructing run/case URLs.

The asset reference publishing route is the explicit bridge from uploaded local
files to provider-fetchable references. It can publish all image assets in a
session or a selected `asset_ids` subset. If an asset already has a
`public_reference_url`, it is reused unless `force=true`. Passing a real
`backend_public_base_url` publishes local uploads as
`/sessions/{session_id}/assets/{asset_id}/file` URLs on that public backend;
without that, the route falls back to OSS/TOS publishing. If OSS/public mapping
is unavailable, the route returns `ready=false` with per-asset reasons such as
`local_bytes`; it does not fabricate a URL. Subsequent preflight and run calls
reuse the stored `public_reference_url` automatically.

`execution_mode` defaults to `"sync"`. Set it to `"background"` when the
caller wants HTTP 202 plus a pollable in-process job record instead of waiting
for a long LLM/image workflow in the request. Background jobs are visible at
`/experiments/jobs/{job_id}` and include `status`, timestamps, metadata,
`result`, and structured `error` fields. Use `/experiments/jobs` to list recent
jobs by `status`, `session_id`, `case_id`, or `job_type`. Job records are also
written as JSON snapshots under `data/backend/jobs`; if a new process loads a
snapshot that was still `queued` or `running`, it reports `interrupted` because
the in-process worker cannot be resumed. This is an audit/debug aid, not a
durable production queue. For session-backed jobs, backend startup also updates
the linked task to `interrupted` and appends `workflow_run_interrupted`, so
session/task views stay consistent after a local process restart.
Use `POST /experiments/jobs/{job_id}/cancel` to request cancellation. If the job
has not started, it becomes `cancelled`; if it is already inside a local worker
thread, it becomes `cancelling`, keeps `cancel_requested=true`, and remains
pollable until the underlying model/workflow call returns. For jobs created by
a backend session task, the cancel response also includes a lightweight
`session` sync summary; the backend updates the task status and appends either
`workflow_run_cancelled` or `workflow_run_cancel_requested` to the session event
log.
When a content-production job succeeds and returns a `run_id`, the job record
also exposes `links.run`, `links.export`, `links.evaluations`,
`links.evaluation_draft`, `links.replay`, `links.inspect_artifacts`, and
case-level links. Job records also include `actions`: queued/running jobs expose
`poll_job`, while terminal jobs mirror the run's post-run actions so product
clients can move from polling to review/export/replay without reconstructing URL
paths.

Set `require_image_references=true` when the product must prove that uploaded
images are actually sent to the image provider as `reference_images`. For relay
image models this requires public HTTPS reference URLs. Nori can obtain those
URLs from OSS, from `NORI_BACKEND_PUBLIC_BASE_URL`, from request-level
`backend_public_base_url`, or from already-public `asset_paths`; otherwise the
run fails with an explicit reference-transfer error instead of silently falling
back to text-only cover generation.

If `require_image_references=true` but no image assets are selected, the run API
returns HTTP 400 before creating a task. This prevents a strict-reference run
from producing a false positive when there was no image for the model to
reference.

The `image_reference` summary is the backend-facing proof surface for visual
reference fidelity. `status="sent"` means selected references were passed to the
image gateway; `status="fallback"` means references were selected but the run
fell back to text-only image generation; `status="failed_required"` is reserved
for strict mode failures where selected references were required but not sent.
`image_reference.trace` is the per-reference audit trail for product review. It
connects the selected path, uploaded asset id/filename when available,
public/provider-fetchable URL, publish reason, object key, and sent flag, so a
review screen can show exactly which user images reached the image gateway.

The `visual_reference_review` summary is the product-facing human-review panel
for that trace. It combines selected-reference counts, per-reference trace rows,
cover preview URLs, evaluation status, and explicit review questions. It does
not claim visual similarity automatically: a run with references sent and covers
available remains `needs_human_review` until a passing evaluation is recorded.
Evaluation drafts include this as a `visual_reference` reviewer when the run is
reference-driven, so visual-reference uncertainty becomes an explicit pending
review item rather than a hidden UI-only note.

The `input_manifest` summary is the backend-facing proof surface for experiment
inputs. It records the session/task ids, brief hash, selected assets, public
reference URL map, `reference_transfer`, `require_image_references`,
`require_reference_image_generation_check`, `execution_mode`,
`human_gate_mode`, config, market evidence counts, and stable `fingerprints`
for the brief, replay request, config, market evidence, metadata,
reference-image generation check, and selected asset hashes. `reference_transfer` is the pre-generation transfer
snapshot: selected asset count, local/remote counts, provider-fetchable URL
count, per-asset `provider_fetchable_url`, and whether a strict run was already
public-URL-ready. When present, `input_manifest.reference_image_generation_check`
records the latest session-level image-provider reference check and whether it
covers the selected provider-fetchable URLs for that run.
`require_reference_image_generation_check=true` turns that evidence into a hard
preflight/run gate, so public URLs alone are not enough for a strict experiment.
Product clients should
pair `input_manifest.reference_transfer` with `image_reference` to answer
whether the generated output actually had access to the user's uploaded visual
references.

The `experiment_manifest` summary is the product-facing proof surface for a run.
It is also persisted as `experiment_manifest.json` and groups run identity,
session/task ids, selected input assets, model readiness snapshot,
reference-image fidelity, input fingerprints, artifact URLs, replay endpoint,
and structured failure metadata when a workflow fails. Product clients should
prefer this object when rendering an experiment-detail page or comparing runs,
then drill into
`input_manifest`, `workflow_run`, and artifact files only when they need lower
level evidence. The same reference-check evidence is mirrored under
`experiment_manifest.inputs.reference_image_generation_check` and
`experiment_manifest.reference_images.latest_generation_check`.

The derived `proof` object is the product-facing judgment layer for run detail
pages. It does not replace manifests; it summarizes them into named checks such
as `workflow_succeeded`, `market_evidence`, `input_integrity`,
`reference_transfer`,
`reference_images_sent`, optional `reference_image_generation_check`,
`content_package`, `cover_output`, `evaluation`, `replay_snapshot`, and
`export_available`. `input_integrity` recomputes recorded
fingerprints against the current brief file, `replay_request.json`, replay
config, market evidence, metadata, and local asset hashes; missing fingerprints
are surfaced as warning evidence, while mismatches are blocking failures. Use
`proof.status`, `failed_checks`, and `warning_checks` for UI state, then link
users back to the manifest/artifact URLs inside `proof.artifacts` for evidence.

The derived `acceptance` object is the stricter final-verdict layer. It returns
`accepted` only when the workflow succeeded, core artifacts exist, strict
reference-image requirements are satisfied, required provider reference-image
checks are ready and cover selected references, replay/export surfaces are
available, and the latest evaluation status is `passed`. Runs with missing core
evidence or `blocked` / `needs_revision` evaluations are `rejected`; runs that
are structurally reviewable but still need judgment are `needs_review`.

The `artifact_catalog` array is the product-facing artifact panel source for a
run. It lists only backend-whitelisted artifacts: top-level `.json` / `.md`
files and cover images under `covers/`. Each row includes `artifact_name`,
download `url`, `media_type`, `size_bytes`, `sha256`, and a short text preview
for JSON/Markdown files. It intentionally omits arbitrary local filesystem
access; clients should download full content through the row's backend URL.

The artifact inspection route is the product-ready companion to
`artifact_catalog`. It keeps the same whitelist and download URLs, but groups
the run artifacts into sections a review panel can render directly:
`content_package`, `manifests`, `markdown`, `covers`, `core_artifacts`,
`missing_core_artifacts`, and the current `proof`, `acceptance`, and
`evaluations`. Use it when the frontend needs to show the generated package,
cover previews, evidence manifests, and review/export/replay actions in one
request.

The compare route turns those manifests into a product-level experiment table.
It does not call models or mutate sessions. It requires at least two run ids
from one case and reports which runs are ready for review, which are blocked,
and why. A strict-reference run is blocked when `reference_images.required` is
true but `reference_images.sent` is false; generated content is also blocked
when `content_package.json` or cover output is missing.

The overview route is the dashboard-level companion to list/detail/compare. It
summarizes all recorded content-production runs, or one `case_id`, into
status/reference/evaluation counts, latest run rows, case rows, review-ready
counts, and blocker counts. It is the preferred API for a Web experiment console
because it keeps filesystem manifests behind the backend boundary.

The workbench route is the preferred bootstrap API for a Web experiment console.
It returns diagnostics, the overview payload, enriched case rows, and a
`primary_actions` list in one response. Each case row includes `action_status`,
`target_run_id`, `primary_action`, ordered `actions`, and a `next_actions` link.
When `case_id` is provided, the same response also includes `case_compare`,
`case_delivery`, `active_run_id`, and `active_run_artifacts`; this lets a case
review page render the comparison table, formal handoff gate, and active run's
artifact panel without joining compare, selected-run, next-actions, delivery,
and artifact-inspection APIs in the browser. The response `links` and case-row
`links` include `run_template`, `case_evaluation_draft`, and `case_evaluations`,
so launch and review controls can call backend-owned case endpoints directly.
Use the lower-level
overview/report/next-actions routes when a screen
needs narrower refreshes.

The run-template route is the launch-form companion to preflight/run. It does
not create a task or call models. Instead, it resolves session metadata,
selected/latest task goal, uploaded image assets, backend public URL, market
evidence, and strict reference policy into a concrete `ContentProductionRunRequest`
payload. GET is convenient when the draft already lives in session metadata;
POST is preferred while a Web form is still editing brief text, market evidence,
config, and metadata. Product clients should render `missing_fields` and
`actions` first. Each action uses `method`, `href`, and optional `payload`;
field-repair actions also include `input_fields` such as `brief_text` or
`market_evidence`. When `ready_for_preflight=true`, the returned `request` can
be sent directly to `POST /workflows/content-production/runs/preflight` and then
to the live run route; strict-reference templates also include an optional
`check_reference_image_generation` action pointing at the session-asset
diagnostic endpoint when selected uploaded references already have
provider-fetchable URLs.

The cases route is the lightweight case index for sidebars and selectors. It
returns the overview's case rows and aggregate counts directly, including latest
run links and case-level launch-template, selection, review, replay, delivery,
timeline, and export links, so clients do not need to unpack the full dashboard
payload for common navigation or reconstruct action URLs.

The case `next-actions` route is the product-facing decision surface after a
case has runs. It turns the report, current selection, best run, acceptance,
evaluation, reference-transfer proof, and stale-selection checks into one
ordered action list. Common `status` values include `needs_first_run`,
`needs_selection`, `ready_to_promote`, `needs_review`, `blocked`, and
`selection_stale`; after a successful promotion it can return `promoted`.
Clients should treat `primary_action` as the default CTA and use the `method`,
`href`, and optional `payload` fields to wire buttons without duplicating
backend experiment rules. Reference repair actions use concrete
`/sessions/{session_id}/assets/...` hrefs and include `asset_ids` when that
context exists in the run manifest. Their paired replay actions carry the same
`session_id` so session-level provider-check evidence survives the repair/rerun
loop. For `needs_first_run`, the `run_first_experiment`
action points to `GET /experiments/content-production/run-template?...` first,
so product screens can resolve missing fields and preflight payloads through the
backend before executing a live run.

The case `replay` route is the product-facing rerun entrypoint. It accepts the
same replay body as the run-level route, plus optional `run_id`; when `run_id`
is omitted, the backend replays the current selection or falls back to the
report `best_run`. This keeps repair/rerun buttons behind the backend and still
supports `execution_mode="background"` for long model calls.

The case evaluation routes are the default product review write surface. Use
`/experiments/content-production/cases/{case_id}/evaluations/draft` and
`/experiments/content-production/cases/{case_id}/evaluations` from case review
screens instead of forcing the browser to resolve a run id first. Both routes
accept optional `run_id`; without it, the backend uses the current operator
selection and then falls back to the report's best run. The underlying record is
still stored on the resolved run, so run-detail screens and exports keep seeing
the same `experiment_evaluations.json` evidence.

The case `promotion` route closes the accepted-run path behind the backend. It
resolves the requested run, verifies the derived acceptance report is
`accepted`, records a `promoted` selection in the same append-only selection
history, and returns selected-run, artifact-inspection, export, replay, and
next-action links. If an operator intentionally promotes a non-accepted run,
the request must set `allow_unaccepted=true`; the response marks the action with
`override=true`.

The case `delivery` route is the product handoff gate. By default `ready=true`
requires a current `promoted` selection, an `accepted` run, complete core
artifacts from artifact inspection, and an export URL. Before promotion it
returns `status=needs_promotion`; with `allow_unpromoted=true`, it can return
`status=preview_ready` plus an `unpromoted_preview` warning so review pages can
preview the delivery payload without claiming the case is formally promoted.
Use `delivery/export` for the downloadable handoff package. It is protected by
the same gate by default and writes `delivery.json`, `artifact_inspection.json`,
`review_evidence.json`, `case_compare.json`, `next_actions.json`,
`run_summary.json`, and the selected run's whitelisted artifacts under `run/`.
Set `allow_unready=true` only for an explicit preview or debug bundle.

The case `compare` route is the preferred data source for a case decision page.
It keeps the lower-level run comparison available, but adds case semantics:
current operator selection, the report-derived `best_run`, the effective
`recommended_run`, all candidate rows, comparison differences when at least two
runs exist, and the same `primary_action` from `next-actions`. This lets a Web
workbench render the review/selection page with one backend call instead of
joining report, selection, compare, and next-action APIs in the browser.

The evaluation routes attach post-run judgment to the backend experiment record.
They do not rerun the workflow or overwrite generated artifacts. Each POST
appends to `experiment_evaluations.json`, refreshes the evaluation summary
inside `experiment_manifest`, and makes the latest evaluation status visible in
run detail and compare responses. `blocked` and `needs_revision` evaluations
become candidate blockers in run comparison.

The evaluation-draft route is the non-LLM automatic reviewer for experiment
workbenches. It restores `content_package.json`, task-like context, client
brief fields, and an intent contract from the run's manifests/replay snapshot,
then calls the existing `ReviewGateAgent`. The response includes raw
reviewer-specific reviews, a normalized evaluation `draft`, aggregate metrics,
and the context used for the review. It also adds a derived `run_health` review
from `proof` and `acceptance`, turning missing market evidence, missing covers,
reference-transfer failures, replay/export gaps, and other experiment-validity
problems into evaluation issues. It only mutates the run when `persist=true`.

`python scripts/backend_holly_smoke.py` is the local API smoke for the Holly
case. It builds the request through `backend.fixtures`, creates a backend
session, uploads selected Holly images through `/sessions/{session_id}/assets`,
publishes references when `--require-image-references` or
`--backend-public-base-url` is present, and runs preflight by default. It only
executes the live workflow when `--run` is passed. By default it uses an
in-process `TestClient`; pass
`--api-base-url http://127.0.0.1:8000` to exercise a real running backend API,
which is required when `--backend-public-base-url` points at an HTTPS tunnel for
that same backend instance. In live strict-reference mode the smoke
automatically sends `verify_reference_urls=true`, so unreachable
backend/tunnel/OSS reference URLs are rejected before model calls. Pass
`--verify-reference-urls` without `--run` to do the same reachability gate in a
preflight-only smoke. Pass `--check-reference-image-generation` when you want
the smoke to call `/sessions/{session_id}/assets/reference-image-generation-check`
with uploaded session assets before a full workflow run.
When preflight has no provider-fetchable reference URLs, the smoke returns
`no_provider_fetchable_reference_images` and stops without calling the image
model.
For a tunnel-backed live reference check, start the backend locally, expose it
with an HTTPS reverse tunnel, then keep `--api-base-url` on the local FastAPI
process and pass the tunnel URL as `--backend-public-base-url`. This avoids
tunnel multipart upload instability while still proving the image provider can
fetch uploaded files from a public URL. A successful strict diagnostic has
`published_references.ready=true`, `reference_images.url_probe.passed=true`,
`reference_image_generation_check.ready=true`, and
`generation.reason=image_generation_succeeded`. Free tunnel services can rotate
URLs or return non-JSON 5xx pages; the smoke script reports route, status, and a
body preview for those responses so the operator can rerun with the current
tunnel URL.
Live debugging can pass
`--stage-timeout-seconds` and `--content-package-timeout-seconds`; these map to
the backend run config and make stage timeouts appear in `workflow_run.json`
and failed-run export payloads, including whether timeout enforcement used a
main-thread signal or a worker-thread request guard.

The `replay_request.json` artifact is the backend-facing reproducibility
snapshot. It stores a request-shaped payload with the original brief, config,
full `market_evidence`, `execution_mode`, run options, and the actual
`asset_paths` selected for the run. Its SHA256 is mirrored into
`input_manifest.fingerprints.replay_request_sha256` and is rechecked by
`proof.input_integrity`. It is intended for local/backend reruns and debugging;
product clients should fetch it through `artifact_urls["replay_request.json"]`
when they need to reconstruct a prior experiment.

The replay route makes that snapshot executable. By default it creates a fresh
in-process session/task and clears stale `asset_ids`, because old uploaded asset
ids only exist in the original session metadata. The saved `asset_paths` are
still validated and passed to the workflow, so the rerun can use the same local
or public image references. Pass `session_id` and optionally `task_id` only when
the caller intentionally wants to replay inside an existing in-process session.
Strict provider-check replay is session-bound: if
`require_reference_image_generation_check=true`, the backend does not trust
`reference_image_generation_check` evidence persisted in `replay_request.json`.
It recomputes the gate from the replay session's latest
`reference_image_generation_checked` event and rejects the replay unless that
event covers the selected references.
Set `execution_mode="background"` on the replay request to get HTTP 202 plus the
same pollable job contract as normal backend runs.
Product screens should prefer the case replay route when the source run should
come from case selection or report state.

The export route is the portable delivery surface for a recorded run. It builds
a zip in the backend containing top-level `.json` / `.md` run artifacts, cover
images under `covers/`, and a generated `export_manifest.json` with file sizes
and SHA-256 hashes. It intentionally ignores non-artifact files and unsupported
paths so frontend/product clients do not need filesystem access and cannot fetch
arbitrary local files through the export endpoint. By default, input/reference
images are not embedded in the zip. Pass `include_inputs=true` to include local
image assets recorded in `input_manifest.assets` under `inputs/`; remote,
missing, duplicate, and unsupported inputs are listed in
`export_manifest.skipped_inputs`.

Run summaries include both filesystem paths and backend URLs. Frontend/product
clients should use `artifact_urls`, `cover_urls`, and uploaded asset `file_url`
instead of reading absolute paths directly.

Backend session persistence is local-experiment durability, not a production
database contract. It restores session/task/assets/events after a process
restart on one machine, but does not provide auth, locking across multiple
workers, tenant isolation, or database migrations.

## LLM Gateway

| API | Input | Output | Notes |
| --- | --- | --- | --- |
| `nori.core.llms.chat(messages, usage="llm", **kwargs)` | OpenAI-style messages | Text string | Uses active model for `usage` and executes through a LangChain chat adapter built by `init_chat_model`; active model must be `type=llm` or `type=vision`; `usage="vision"` or multimodal message parts require `supports_vision=true` or raise `ChatCapabilityError`. Empty or malformed provider output raises `ChatResultError`. |
| `nori.core.llms.chat_json(messages, usage="llm", schema=None, structured_method=None, json_mode=False, **kwargs)` | OpenAI-style messages | JSON object dict | Executes through LangChain `with_structured_output(..., include_raw=True)`. Without a schema it uses `method="json_mode"`; with a schema it defaults to `json_schema` unless `structured_method` is provided. LangChain parsing errors are wrapped as `ChatJSONError`; non-object structured outputs are rejected. |
| `nori.core.llms.image(prompt, usage="image", reference_images=None, size=...)` | Prompt + optional bytes refs | List of image outputs | Executes image generation through the core gateway: active model must be `type=image`; reference images require `supports_reference_image=true` or raise `ImageCapabilityError`; Google native image calls validate `api_key` before SDK dispatch. |
| `nori.core.llms.set_telemetry_sink(sink_or_none)` | Callable receiving dict metadata | None | Registers process-local redacted telemetry for `chat` / `achat` / `image`; never includes prompts, keys, image bytes, or response text. Canonical implementation lives in `nori.core.llms.telemetry`. |
| `nori.core.contracts.{LLMClientConfigError,ChatJSONError,ChatResultError,ChatCapabilityError,ImageCapabilityError,ImageResultError}` | Error contract fields | Exception classes | Canonical gateway exception classes; `nori.core.llms` re-exports them for normal public use. |
| `nori.core.llms.telemetry.emit_telemetry(...)` | Internal gateway metadata | None | Internal helper for gateway call sites; emits redacted metadata and swallows sink errors so telemetry cannot break business calls. |
| `nori.core.llms.NoriAIClient` | Optional injected LM/image clients | Aggregate gateway | Class-backed gateway behind package-root `chat`, `achat`, `chat_json`, and `image`; exposes `lm` and `imager` for tests and runtime composition. |
| `nori.core.llms.lm.LanguageModelClient.chat(...)` / `achat(...)` | OpenAI-style messages + usage + kwargs | Text string | Canonical sync/async chat execution path; resolves LangChain chat adapters, merges chat kwargs internally, guards chat/vision capability, reads LangChain message `content`, and emits telemetry. |
| `nori.core.llms.imager.ImageClient.image(...)` | Prompt + optional reference inputs + usage + kwargs | List of image outputs | Canonical image execution path; resolves active image model once, filters reference inputs, guards image capabilities, merges image kwargs internally, dispatches provider methods, validates non-empty outputs, and emits telemetry. |
| `nori.core.llms.capabilities.ensure_chat_capability(...)` | Resolved model + messages + usage | None / `ChatCapabilityError` | Canonical chat/vision capability guard used before provider dispatch. |
| `nori.core.llms.capabilities.ensure_image_capability(...)` | Resolved model + reference bytes | None / `ImageCapabilityError` | Canonical image/reference capability guard used before provider dispatch. |
| `nori.core.llms.capabilities.messages_need_vision(...)` | OpenAI-style messages | bool | Detects multimodal image parts for chat/vision capability enforcement. |
| `nori.storage.ReferenceImagePublisher.from_env().publish_paths(...)` | Local reference image paths + project/session context | Model-fetchable HTTPS URL inputs + upload metadata | Uploads local reference images to Volcengine TOS when OSS env is configured. Object keys follow `nori/reference-images/<project>/<session>/<YYYYMMDD>/<sha16>_<source>.<ext>`; signed query strings are not persisted in content artifacts. |
| `nori.core.llms.image_inputs.load_image_bytes(...)` | bytes, data-uri, path, base64 string, or unknown value | Image bytes or `b""` | Canonical reference-image input normalizer; unreadable/remote/invalid inputs return empty bytes so `nori.core.llms.image` can filter them before capability checks. |
| `nori.core.llms.image_inputs.sniff_mime(...)` | Image bytes | MIME string | Detects PNG/JPEG/GIF/WEBP and defaults unknown bytes to `image/png`. |
| `nori.core.llms.image_inputs.bytes_to_data_uri(...)` | Image bytes | `data:{mime};base64,...` string | Canonical data-uri encoder used by reference-image provider payloads. |
| `nori.core.llms.image_providers.ImageProviders.openai_edit(...)` | Resolved image bundle + prompt + reference bytes | List of image outputs | Canonical OpenAI-compatible `images.edit` wrapper; builds named in-memory files and normalizes URL/base64 image results. |
| `nori.core.llms.image_providers.ImageProviders.relay_generate_with_references(...)` | Resolved image bundle + prompt + reference bytes | List of image outputs | Canonical relay reference-image path; retries supported `extra_body` payload variants without mutating caller kwargs. |
| `nori.core.llms.image_providers.ImageProviders.google(...)` | Prompt + resolved Google image model + API key | List of data-uri image outputs | Canonical Google native image call; constructs `google-genai` parts and encodes inline image results. |
| `nori.core.llms.ensure_ready(usage)` | Usage key | None / exception | Reuses client config validation, then checks GHC proxy `/models` in `ghc` mode. |
| `nori.core.llms.lm.LanguageModelClient.chat_json(...)` | OpenAI-style messages + optional schema/method + usage + kwargs | JSON object dict / `ChatJSONError` | Canonical structured JSON execution path; owns capability checks, kwargs merge, LangChain structured-output binding, parsed dict extraction, and telemetry. |
| `NoriConfig(config_path=None)` | Optional config path | Config object | Loads `api_config.yaml`, supports `api_key_env`, `${ENV_VAR}`, nested `active_models`, and `NORI_MODE`. |
| `nori.core.contracts.{ProviderConfig,ModelConfig,ResolvedModel}` | Config model fields | Dataclass contracts | Canonical runtime-config dataclasses shared by `nori_config` and `nori.core.llms`; `nori.core` and `nori.nori_config` expose the same class identities. |
| `nori.config_normalization.parse_model_key(key)` / `format_model_key(...)` | Provider/model key text | Canonical provider and model ids | Pure config helper used before model lookup so whitespace and malformed keys are handled consistently. |
| `nori.config_normalization.select_active_models(active_models, mode, fallback_mode=...)` | Flat or mode-nested active model map | Canonical usage -> model-key map | Pure config helper for direct/ghc active-model selection, including missing-mode behavior for `NORI_MODE`. |
| `nori.config_normalization.resolve_api_key(raw_value, env_name="")` | Literal or `${ENV_VAR}` API key config | API key text | Pure config helper that trims env var names and resolves explicit `api_key_env` before literal config values. |

## Supervisor Agent

| API | Contract |
| --- | --- |
| `NoriSupervisorAgent(tools=None, use_llm=True).run(user_message, session_id="", task_id="", context=None, execute=True, use_llm=None) -> SupervisorTurnResult` | Route one main-chat user turn to a selected `SupervisorTool`. Uses structured LLM routing when enabled, falls back to keyword routing, supports plan-only mode, invokes injected handlers, and returns clarification questions when no tool matches. |
| `default_supervisor_tools() -> list[SupervisorTool]` | Built-in tool catalog for `content_production`, `content_design_spec`, `artifact_generation`, `market_analysis`, `review_content_package`, and `session_memory`. The catalog has no handlers; backend/workflow layers bind concrete subworkflow or subagent handlers. |
| `SupervisorTool(name, description, intent_names=..., keywords=..., handler=..., is_workflow=False)` | Tool contract used to expose a subagent/subworkflow to the supervisor without making the supervisor import workflow runtime modules. |

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
| `call_stage_json(system=..., user=..., timeout=..., error_type=...) -> dict` | Shared utility for generation-stage JSON stages. Calls `nori.core.llms.chat_json(json_mode=True)` and translates parse/provider failures into the supplied domain exception class. |
| `call_stage_messages_json(messages=..., timeout=..., error_type=..., usage=...) -> dict` | Shared utility for required JSON stages that already build OpenAI-style messages, including multimodal `usage="vision"` calls. Uses the same JSON-mode and domain-error translation contract as `call_stage_json`. |
| `try_stage_messages_json(messages=..., timeout=..., usage=...) -> (data, error)` | Shared utility for optional JSON stages that already build OpenAI-style messages, including multimodal/custom-message fallback paths. Calls `nori.core.llms.chat_json(json_mode=True)`, returns `data` on success, and returns redacted `error` metadata on parse/provider failure without raising. |
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
| `nori.workflows.WorkflowRunner(checkpointer=None).run(spec, initial, session_id=..., task_id=..., human_gate_mode="skip")` | Compiles and executes the workflow through LangGraph directly, returning `(output, WorkflowRun)`. `human_gate_mode="pause"` records `waiting_for_human` and raises `HumanGateRequired`. |
| `nori.workflows.HumanGateRequired` | Exception raised when a run reaches a human gate in pause mode; carries the partial `workflow_run`. |
| `WorkflowRunner` artifact refs | A stage can return a `StoredArtifact`, `_artifact_ref`, or `_artifact_refs` mapping; the runner normalizes these into `StageRun.output_ref` and `WorkflowRun.artifact_refs`. |

## Context Runtime

| API | Contract |
| --- | --- |
| `nori.context.ContextBundle` | Runtime envelope for one agent call: session/task/user ids, sources, memory, artifact rows, payload, and trace. |
| `nori.context.ContextCompiler().build(...)` | Compiles profile, task, market evidence, learned skills, platform rules, content strategy, and assets into a sliced `ContextPack`. |
| `nori.context.ContextPackBuilder` | Alias of `ContextCompiler`; this is the canonical owner. Planning no longer re-exports it. |
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

Owner-local schema packages should support `to_dict()` where the object crosses a stage boundary. Cross-stage contracts are split by owner: `UserAsset`, `AssetRecord`, and `AssetLibrary` live in `nori.core.asset_models`; `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, and `ContentCalendar` live in `nori.core.planning_models`; `UserProfile` lives in `nori.core.profile_models`; `ContextPack`, `CandidateSet`, `LearningSignal`, and `CapabilitySnapshot` live in `nori.core.capability_models`; `AccountOperationProject` lives in `nori.core.project`. Public runtime contracts that are shared with the LLM gateway live in `nori.core.contracts`, including config dataclasses, gateway errors, structured-helper result dataclasses, and shared model coercion helpers. `UserInput`, `IntakeResult`, `AccountPlannerInput`, and `AccountPlanResult` live in `nori.agents.user_profiling.schemas`; `ContentDesignSpec`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, `CoverResult`, and `ContentPackage` live in `nori.agents.content_generation.schemas`; `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteSkill`, `NoteEvidence`, and `SessionSkillReport` live in `nori.agents.market_analysis.schemas`. The old `nori.agent_models`, owner-local `models.py`, and `nori.core.models` compatibility roots have been removed; import schemas from the owning business module or from the `nori.core` public root. Schema `from_dict()` methods should use `nori.core.contracts` for shared mapping/list/string/int/bool cleanup.

Canonical business model ownership:

| Module | Models |
| --- | --- |
| `nori.agents.user_profiling.schemas` | `UserInput`, `IntakeResult`, `AccountPlannerInput`, `AccountPlanResult`, `AccountPositioning` |
| `nori.agents.market_analysis.schemas` | `CompetitorSample`, `CompetitorResearch`, `XHSNoteSample`, `XHSSeedSkillDraft`, `NoteEvidence`, `NoteSkill`, `SessionSkillReport` |
| `nori.core.asset_models` | `UserAsset`, `AssetRecord`, `AssetLibrary` |
| `nori.core.planning_models` | `ClientBrief`, `OperationPlan`, `KPIPlan`, `ContentTask`, `ContentCalendar`, `IntentContract` |
| `nori.core.profile_models` | `UserProfile` |
| `nori.core.capability_models` | `ContextPack`, `CandidateSet`, `LearningSignal`, `CapabilitySnapshot`, and related evidence/trace models |
| `nori.core.project` | `AccountOperationProject` cross-module aggregate; lazily coerces nested dicts into user/context/market/content/learning concrete models |
| `nori.agents.content_generation.schemas` | `ContentDesignSpec`, `AssetBundle`, `CandidateTitle`, `NoteDraft`, `CoverResult`, `ContentPackage` |
| `nori.agents.learning_loop.schemas` | `ComplianceReview`, `MetricsSnapshot`, `StrategyIteration` |

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
