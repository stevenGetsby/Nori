export type ApiEnvelope<T> = {
  code: number;
  message: string;
  data: T;
};

export class ApiClientError extends Error {
  readonly status: number;
  readonly code?: number;

  constructor(message: string, options: { status: number; code?: number }) {
    super(message);
    this.name = 'ApiClientError';
    this.status = options.status;
    this.code = options.code;
  }
}

export type WorkbenchBootstrap = {
  ready?: boolean;
  status?: string;
  case_id?: string;
  active_run_id?: string;
  diagnostics?: Record<string, unknown>;
  context_layer?: WorkbenchContextLayer;
  overview?: {
    active_account?: string;
    run_count?: number;
    case_count?: number;
    summary?: {
      ready_count?: number;
      blocked_count?: number;
      [key: string]: unknown;
    };
    [key: string]: unknown;
  };
  cases?: WorkbenchCase[];
  primary_actions?: WorkbenchAction[];
  links?: Record<string, string>;
  source?: 'mock' | 'backend';
};

export type WorkbenchContextLayer = {
  context_pack_id?: string;
  status?: string;
  active_case_id?: string;
  active_run_id?: string;
  summary?: string;
  slices?: WorkbenchContextSlice[];
  source_refs?: string[];
  links?: Record<string, string>;
  [key: string]: unknown;
};

export type WorkbenchContextSlice = {
  kind?: string;
  title?: string;
  summary?: string;
  signal?: string;
  source_refs?: string[];
  payload?: Record<string, unknown>;
  [key: string]: unknown;
};

export type WorkbenchAction = {
  action_id?: string;
  case_id?: string;
  label?: string;
  severity?: string;
  message?: string;
  method?: string;
  href?: string;
  [key: string]: unknown;
};

export type WorkbenchCase = {
  case_id?: string;
  run_count?: number;
  latest_run_id?: string;
  action_status?: string;
  primary_action?: WorkbenchAction;
  links?: Record<string, string>;
  [key: string]: unknown;
};

export type RunTemplateDraft = {
  session_id?: string;
  task_id?: string;
  case_id?: string;
  case_title?: string;
  platform?: string;
  goal?: string;
  brief_text?: string;
  asset_ids?: string[];
  backend_public_base_url?: string;
  execution_mode?: 'sync' | 'async' | string;
  human_gate_mode?: 'skip' | 'require' | string;
  require_image_references?: boolean;
  require_reference_image_generation_check?: boolean;
  verify_reference_urls?: boolean;
  reference_url_probe_timeout?: number;
  market_evidence?: unknown;
  config?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
};

export type RunTemplateCheck = {
  name: string;
  status: string;
  message?: string;
  [key: string]: unknown;
};

export type RunTemplateAction = {
  action_id: string;
  label?: string;
  severity?: string;
  method?: string;
  href?: string;
  message?: string;
  payload?: unknown;
  input_fields?: string[];
  [key: string]: unknown;
};

export type ContentDesignSpecDraft = {
  spec_id?: string;
  task_id?: string;
  platform?: string;
  artifact_type?: string;
  content_type?: string;
  goal?: string;
  audience?: string[];
  creative_angle?: string;
  selected_skill_refs?: Array<Record<string, unknown>>;
  evidence_refs?: Array<Record<string, unknown>>;
  structure?: Array<Record<string, unknown>>;
  media_plan?: Record<string, unknown>;
  copy_rules?: Record<string, unknown>;
  visual_rules?: Record<string, unknown>;
  constraints?: string[];
  acceptance_checks?: string[];
  metadata?: Record<string, unknown>;
  [key: string]: unknown;
};

export type RunTemplateResponse = {
  schema_version?: number;
  ready_for_preflight: boolean;
  ready_for_run?: boolean;
  missing_fields?: string[];
  checks?: RunTemplateCheck[];
  actions?: RunTemplateAction[];
  links?: Record<string, string>;
  request?: Record<string, unknown>;
  session?: Record<string, unknown>;
  assets?: Record<string, unknown>;
  market_evidence?: Record<string, unknown>;
  reference_images?: Record<string, unknown>;
  content_design_spec?: ContentDesignSpecDraft;
};

export type RunTemplateRequestConfig = {
  path: string;
  init: RequestInit;
};

export type PreflightPayload = {
  session_id?: string;
  task_id?: string;
  case_id?: string;
  brief_text?: string;
  asset_ids?: string[];
  backend_public_base_url?: string;
  execution_mode?: 'sync' | 'async' | string;
  human_gate_mode?: 'skip' | 'require' | string;
  require_image_references?: boolean;
  require_reference_image_generation_check?: boolean;
  verify_reference_urls?: boolean;
  reference_url_probe_timeout?: number;
  market_evidence?: unknown;
  config?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  [key: string]: unknown;
};

export type PreflightCheck = {
  name: string;
  status: string;
  message?: string;
  [key: string]: unknown;
};

export type PreflightAction = {
  action_id: string;
  label?: string;
  severity?: string;
  method?: string;
  href?: string;
  message?: string;
  payload?: unknown;
  [key: string]: unknown;
};

export type PreflightResponse = {
  ready: boolean;
  checks?: PreflightCheck[];
  session?: Record<string, unknown>;
  run_options?: Record<string, unknown>;
  assets?: Record<string, unknown>;
  market_evidence?: Record<string, unknown>;
  reference_images?: Record<string, unknown>;
  readiness?: Record<string, unknown>;
  actions?: PreflightAction[];
  links?: Record<string, string>;
};

export type ContentRunResult = {
  workflow_name?: string;
  run_id?: string;
  run_dir?: string;
  status?: string;
  session_id?: string;
  task_id?: string;
  job_id?: string;
  job_type?: string;
  artifact_paths?: Record<string, string>;
  cover_paths?: string[];
  image_reference?: Record<string, unknown>;
  workflow_run?: Record<string, unknown>;
  actions?: PreflightAction[];
  links?: Record<string, string>;
  metadata?: Record<string, unknown>;
  [key: string]: unknown;
};

export type ArtifactInspectionEntry = {
  available?: boolean;
  artifact_name?: string;
  name?: string;
  url?: string;
  data?: Record<string, unknown>;
  json_summary?: {
    keys?: string[];
    field_count?: number;
  };
  preview?: {
    kind?: string;
    available?: boolean;
    url?: string;
    text?: string;
    [key: string]: unknown;
  };
  text?: string;
  [key: string]: unknown;
};

export type ArtifactInspectionResult = {
  schema_version?: number;
  case_id?: string;
  run_id?: string;
  generated_at?: string;
  status?: string;
  workflow_name?: string;
  created_at?: string;
  finished_at?: string;
  ready_for_review?: boolean;
  proof?: Record<string, unknown>;
  acceptance?: Record<string, unknown>;
  evaluations?: Record<string, unknown>;
  image_reference?: Record<string, unknown>;
  visual_reference_review?: Record<string, unknown>;
  core_artifacts?: Record<string, unknown>;
  content_package?: ArtifactInspectionEntry;
  manifests?: Record<string, ArtifactInspectionEntry>;
  markdown?: ArtifactInspectionEntry[];
  covers?: ArtifactInspectionEntry[];
  artifact_catalog?: ArtifactInspectionEntry[];
  artifact_counts?: {
    total?: number;
    json?: number;
    markdown?: number;
    covers?: number;
    [key: string]: unknown;
  };
  missing_core_artifacts?: string[];
  links?: Record<string, string>;
  [key: string]: unknown;
};

export type ContentProductionRunListQuery = {
  case_id?: string;
  status?: string;
  acceptance_status?: string;
  proof_status?: string;
  reference_status?: string;
  evaluation_status?: string;
  search?: string;
  limit?: number;
  offset?: number;
};

export type ContentProductionRunRow = {
  case_id?: string;
  run_id: string;
  workflow_name?: string;
  status?: string;
  created_at?: string;
  finished_at?: string;
  reference_status?: string;
  reference_required?: boolean;
  reference_sent?: boolean;
  cover_count?: number;
  artifact_count?: number;
  evaluation_status?: string;
  evaluation_score?: number;
  evaluation_count?: number;
  proof_status?: string;
  acceptance_status?: string;
  accepted?: boolean;
  candidate?: {
    ready_for_review?: boolean;
    [key: string]: unknown;
  };
  image_reference?: Record<string, unknown>;
  evaluations?: Record<string, unknown>;
  links?: Record<string, string>;
  [key: string]: unknown;
};

export type ContentProductionRunList = {
  total_count?: number;
  filtered_count?: number;
  returned_count?: number;
  runs: ContentProductionRunRow[];
  [key: string]: unknown;
};

export type ContentGenerationOption = {
  option_id: string;
  label: string;
  description?: string;
  default?: boolean;
  metadata?: Record<string, unknown>;
};

export type ContentGenerationOptions = {
  option_groups: Record<string, ContentGenerationOption[]>;
};

export type ContentGenerationPlanRequest = {
  goal?: string;
  platform?: string;
  artifact_type?: string;
  image_source?: string;
  cover_strategy?: string;
  human_gate_mode?: string;
  entry_mode?: string;
  workflow_id?: string;
  action_id?: string;
  metadata?: Record<string, unknown>;
};

export type ContentGenerationPlan = {
  capability_id?: string;
  selected_action_id?: string;
  selected_route?: string;
  workflow_id?: string;
  normalized_options?: Record<string, string>;
  requires_workflow_id?: boolean;
  rationale?: string;
  [key: string]: unknown;
};

export type SessionCreateRequest = {
  user_id?: string;
  profile_id?: string;
  metadata?: Record<string, unknown>;
};

export type SessionResponse = {
  session_id: string;
  user_id?: string;
  profile_id?: string;
  metadata?: Record<string, unknown>;
  created_at?: string;
  updated_at?: string;
  [key: string]: unknown;
};

export type SessionAsset = {
  asset_id: string;
  session_id?: string;
  task_id?: string;
  kind?: string;
  usage?: string;
  filename?: string;
  content_type?: string;
  size_bytes?: number;
  metadata?: Record<string, unknown>;
  file_url?: string;
  path?: string;
  public_reference_url?: string;
  provider_fetchable_url?: string;
  [key: string]: unknown;
};

export type SessionAssetsResponse = {
  assets: SessionAsset[];
  session_id?: string;
  latest_reference_image_generation_check?: Record<string, unknown>;
  [key: string]: unknown;
};

export type SessionAssetUploadOptions = {
  task_id?: string;
  usage?: string;
  metadata?: Record<string, unknown>;
};

export type ReferenceImageGenerationCheckRequest = {
  asset_ids?: string[];
  project?: string;
  force_publish?: boolean;
  backend_public_base_url?: string;
  public_url_map?: Record<string, string>;
  verify_reference_urls?: boolean;
  reference_url_probe_timeout?: number;
  prompt?: string;
  size?: string;
  metadata?: Record<string, unknown>;
};

export type ReferenceImageGenerationCheckResult = {
  ready?: boolean;
  reason?: string;
  published_count?: number;
  provider_fetchable_count?: number;
  provider_fetchable_reference_images?: string[];
  publish?: Record<string, unknown>;
  generation?: Record<string, unknown>;
  next_actions?: PreflightAction[];
  [key: string]: unknown;
};

const defaultHeaders = {
  Accept: 'application/json',
};

export async function requestJson<T>(
  path: string,
  init: RequestInit = {},
  fetcher: typeof fetch = fetch,
): Promise<T> {
  const response = await fetcher(path, {
    ...init,
    headers: {
      ...defaultHeaders,
      ...init.headers,
    },
  });

  let payload: ApiEnvelope<T> | undefined;
  try {
    payload = (await response.json()) as ApiEnvelope<T>;
  } catch {
    payload = undefined;
  }

  if (!response.ok || !payload || payload.code !== 0) {
    throw new ApiClientError(payload?.message || response.statusText || 'Request failed', {
      status: response.status,
      code: payload?.code,
    });
  }

  return payload.data;
}

export function getWorkbenchBootstrap(fetcher?: typeof fetch, pathOverride?: string) {
  const bootstrapPath =
    pathOverride ||
    (import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1'
      ? '/mock/workbench-bootstrap.json'
      : '/api/experiments/content-production/workbench');
  return requestJson<WorkbenchBootstrap>(
    bootstrapPath,
    undefined,
    fetcher,
  );
}

export function buildRunTemplate(draft: RunTemplateDraft, fetcher?: typeof fetch) {
  const request = runTemplateRequest(draft, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<RunTemplateResponse>(request.path, request.init, fetcher);
}

export function runTemplateRequest(
  draft: RunTemplateDraft,
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/run-template.json',
      init: {},
    };
  }

  return {
    path: '/api/experiments/content-production/run-template',
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(draft),
    },
  };
}

export function runPreflight(payload: PreflightPayload, fetcher?: typeof fetch) {
  const request = preflightRequest(payload, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<PreflightResponse>(request.path, request.init, fetcher);
}

export function preflightRequest(
  payload: PreflightPayload,
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/preflight.json',
      init: {},
    };
  }

  return {
    path: '/api/workflows/content-production/runs/preflight',
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  };
}

export function runContentProduction(payload: PreflightPayload, fetcher?: typeof fetch) {
  const request = contentRunRequest(payload, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ContentRunResult>(request.path, request.init, fetcher);
}

export function contentRunRequest(
  payload: PreflightPayload,
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/content-run.json',
      init: {},
    };
  }

  return {
    path: '/api/workflows/content-production/runs',
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  };
}

export function getContentGenerationOptions(fetcher?: typeof fetch) {
  const request = contentGenerationOptionsRequest({
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ContentGenerationOptions>(request.path, request.init, fetcher);
}

export function contentGenerationOptionsRequest(
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/content-generation-options.json',
      init: {},
    };
  }

  return {
    path: '/api/content/generation/options',
    init: {},
  };
}

export function planContentGeneration(payload: ContentGenerationPlanRequest, fetcher?: typeof fetch) {
  const request = contentGenerationPlanRequest(payload, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ContentGenerationPlan>(request.path, request.init, fetcher);
}

export function contentGenerationPlanRequest(
  payload: ContentGenerationPlanRequest,
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/content-generation-plan.json',
      init: {},
    };
  }

  return {
    path: '/api/content/generation/plan',
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  };
}

export function createSession(payload: SessionCreateRequest = {}, fetcher?: typeof fetch) {
  const request = createSessionRequest(payload, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<SessionResponse>(request.path, request.init, fetcher);
}

export function createSessionRequest(
  payload: SessionCreateRequest = {},
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/session.json',
      init: {},
    };
  }

  return {
    path: '/api/sessions',
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  };
}

export function uploadSessionAssets(
  sessionId: string,
  files: File[],
  options: SessionAssetUploadOptions = {},
  fetcher?: typeof fetch,
) {
  const request = uploadSessionAssetsRequest(sessionId, files, options, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<SessionAssetsResponse>(request.path, request.init, fetcher);
}

export function uploadSessionAssetsRequest(
  sessionId: string,
  files: File[],
  options: SessionAssetUploadOptions = {},
  requestOptions: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (requestOptions.useLocalMock) {
    return {
      path: '/mock/session-assets.json',
      init: {},
    };
  }

  const body = new FormData();
  files.forEach((file) => body.append('files', file));
  body.append('task_id', options.task_id || '');
  body.append('usage', options.usage || 'reference');
  body.append('metadata_json', options.metadata ? JSON.stringify(options.metadata) : '');

  return {
    path: `/api/sessions/${encodeURIComponent(sessionId)}/assets`,
    init: {
      method: 'POST',
      body,
    },
  };
}

export function checkSessionReferenceImageGeneration(
  sessionId: string,
  payload: ReferenceImageGenerationCheckRequest = {},
  fetcher?: typeof fetch,
) {
  const request = referenceImageGenerationCheckRequest(sessionId, payload, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ReferenceImageGenerationCheckResult>(request.path, request.init, fetcher);
}

export function referenceImageGenerationCheckRequest(
  sessionId: string,
  payload: ReferenceImageGenerationCheckRequest = {},
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/reference-image-generation-check.json',
      init: {},
    };
  }

  return {
    path: `/api/sessions/${encodeURIComponent(sessionId)}/assets/reference-image-generation-check`,
    init: {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    },
  };
}

export function inspectRunArtifacts(caseId: string, runId: string, fetcher?: typeof fetch) {
  const request = inspectRunArtifactsRequest(caseId, runId, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ArtifactInspectionResult>(request.path, request.init, fetcher);
}

export function inspectRunArtifactsRequest(
  caseId: string,
  runId: string,
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    if (runId && runId !== 'run_ready' && runId !== 'mock_run_ready') {
      return {
        path: `/mock/artifact-inspection-${encodeURIComponent(runId)}.json`,
        init: {},
      };
    }
    return {
      path: '/mock/artifact-inspection.json',
      init: {},
    };
  }

  const encodedCaseId = encodeURIComponent(caseId);
  const encodedRunId = encodeURIComponent(runId);
  return {
    path: `/api/workflows/content-production/runs/${encodedCaseId}/${encodedRunId}/artifacts/inspect`,
    init: {},
  };
}

export function listContentProductionRuns(query: ContentProductionRunListQuery = {}, fetcher?: typeof fetch) {
  const request = listContentProductionRunsRequest(query, {
    useLocalMock: !fetcher && import.meta.env.DEV && import.meta.env.VITE_NORI_USE_API !== '1',
  });
  return requestJson<ContentProductionRunList>(request.path, request.init, fetcher);
}

export function listContentProductionRunsRequest(
  query: ContentProductionRunListQuery = {},
  options: { useLocalMock?: boolean } = {},
): RunTemplateRequestConfig {
  if (options.useLocalMock) {
    return {
      path: '/mock/content-production-runs.json',
      init: {},
    };
  }

  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    params.set(key, String(value));
  });
  const suffix = params.toString() ? `?${params.toString()}` : '';

  return {
    path: `/api/workflows/content-production/runs${suffix}`,
    init: {},
  };
}
