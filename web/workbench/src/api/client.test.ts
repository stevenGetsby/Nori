import { describe, expect, it } from 'vitest';
import {
  ApiClientError,
  checkSessionReferenceImageGeneration,
  createSession,
  getContentGenerationOptions,
  inspectRunArtifacts,
  inspectRunArtifactsRequest,
  listContentProductionRuns,
  listContentProductionRunsRequest,
  uploadSessionAssets,
  referenceImageGenerationCheckRequest,
  buildRunTemplate,
  contentRunRequest,
  contentGenerationOptionsRequest,
  contentGenerationPlanRequest,
  planContentGeneration,
  preflightRequest,
  requestJson,
  runContentProduction,
  runPreflight,
  runTemplateRequest,
} from './client';

describe('api client', () => {
  it('unwraps backend ApiEnvelope data', async () => {
    const fetcher = async () =>
      new Response(JSON.stringify({ code: 0, message: 'ok', data: { ready: true } }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });

    await expect(requestJson('/api/test', {}, fetcher as typeof fetch)).resolves.toEqual({
      ready: true,
    });
  });

  it('throws a typed error when backend code is not ok', async () => {
    const fetcher = async () =>
      new Response(JSON.stringify({ code: 422, message: 'missing brief', data: {} }), {
        status: 422,
        headers: { 'Content-Type': 'application/json' },
      });

    await expect(requestJson('/api/test', {}, fetcher as typeof fetch)).rejects.toMatchObject<
      Partial<ApiClientError>
    >({
      name: 'ApiClientError',
      status: 422,
      code: 422,
      message: 'missing brief',
    });
  });

  it('posts a content-production run template draft through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/experiments/content-production/run-template');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual({
        case_id: 'Holly',
        brief_text: '生成一篇小红书图文',
        platform: 'xhs',
        require_image_references: true,
        human_gate_mode: 'skip',
      });
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            ready_for_preflight: false,
            missing_fields: ['session'],
            checks: [{ name: 'session', status: 'failed', message: 'Create a session first.' }],
            actions: [{ action_id: 'create_session', label: 'Create session', href: '/sessions' }],
            links: { preflight: '/workflows/content-production/runs/preflight' },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(
      buildRunTemplate(
        {
          case_id: 'Holly',
          brief_text: '生成一篇小红书图文',
          platform: 'xhs',
          require_image_references: true,
          human_gate_mode: 'skip',
        },
        fetcher as typeof fetch,
      ),
    ).resolves.toMatchObject({
      ready_for_preflight: false,
      missing_fields: ['session'],
      actions: [{ action_id: 'create_session' }],
    });
  });

  it('can resolve run-template requests to the local fixture for mock development', () => {
    expect(runTemplateRequest({ brief_text: 'draft' }, { useLocalMock: true })).toEqual({
      path: '/mock/run-template.json',
      init: {},
    });
  });

  it('preserves a run-template ContentDesignSpec draft when present', async () => {
    const fetcher = async () =>
      new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            ready_for_preflight: true,
            content_design_spec: {
              spec_id: 'spec_1',
              selected_skill_refs: [{ skill_id: 'xhs_hotspot_image_post' }],
              acceptance_checks: ['封面必须有结论'],
            },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );

    await expect(buildRunTemplate({ brief_text: 'draft' }, fetcher as typeof fetch)).resolves.toMatchObject({
      ready_for_preflight: true,
      content_design_spec: {
        spec_id: 'spec_1',
        acceptance_checks: ['封面必须有结论'],
      },
    });
  });

  it('posts a content-production preflight through the API boundary', async () => {
    const payload = {
      session_id: 'session_1',
      brief_text: '生成一篇小红书图文',
      case_id: 'Holly',
    };
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/workflows/content-production/runs/preflight');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual(payload);
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            ready: false,
            checks: [{ name: 'reference_transfer', status: 'failed' }],
            actions: [{ action_id: 'publish_reference_assets', label: 'Publish references' }],
            links: { run: '/workflows/content-production/runs' },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(runPreflight(payload, fetcher as typeof fetch)).resolves.toMatchObject({
      ready: false,
      checks: [{ name: 'reference_transfer', status: 'failed' }],
      actions: [{ action_id: 'publish_reference_assets' }],
    });
  });

  it('can resolve preflight requests to the local fixture for mock development', () => {
    expect(preflightRequest({ brief_text: 'draft' }, { useLocalMock: true })).toEqual({
      path: '/mock/preflight.json',
      init: {},
    });
  });

  it('posts a content-production run through the API boundary', async () => {
    const payload = {
      session_id: 'session_1',
      case_id: 'Holly',
      brief_text: '生成一篇小红书图文',
    };
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/workflows/content-production/runs');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual(payload);
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            workflow_name: 'content_production',
            run_id: 'run_ready',
            status: 'succeeded',
            links: {
              export: '/workflows/content-production/runs/Holly/run_ready/export',
            },
          },
        }),
        {
          status: 201,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(runContentProduction(payload, fetcher as typeof fetch)).resolves.toMatchObject({
      run_id: 'run_ready',
      status: 'succeeded',
    });
  });

  it('can resolve content run requests to the local fixture for mock development', () => {
    expect(contentRunRequest({ brief_text: 'draft' }, { useLocalMock: true })).toEqual({
      path: '/mock/content-run.json',
      init: {},
    });
  });

  it('loads content generation options through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/content/generation/options');
      expect(init?.method).toBeUndefined();
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            option_groups: {
              platform: [{ option_id: 'xhs', label: 'Xiaohongshu', default: true }],
              artifact_type: [{ option_id: 'image_text_post', label: 'Image-text post', default: true }],
            },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(getContentGenerationOptions(fetcher as typeof fetch)).resolves.toMatchObject({
      option_groups: {
        platform: [{ option_id: 'xhs' }],
      },
    });
  });

  it('posts content generation planning choices through the API boundary', async () => {
    const request = {
      goal: '生成小红书图文',
      platform: 'xhs',
      artifact_type: 'image_text_post',
      cover_strategy: 'manual_references',
      image_source: 'uploaded_assets',
    };
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/content/generation/plan');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual(request);
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            capability_id: 'content_generation',
            selected_action_id: 'content.cover',
            selected_route: '/content/generation/cover',
            workflow_id: '',
            requires_workflow_id: false,
            normalized_options: {
              platform: 'xhs',
              artifact_type: 'image_text_post',
              image_source: 'uploaded_assets',
              cover_strategy: 'manual_references',
              human_gate_mode: 'skip',
              entry_mode: 'direct_action',
            },
            rationale: 'Use the cover sub-capability when choosing imagery.',
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(planContentGeneration(request, fetcher as typeof fetch)).resolves.toMatchObject({
      selected_action_id: 'content.cover',
      selected_route: '/content/generation/cover',
      normalized_options: {
        cover_strategy: 'manual_references',
      },
    });
  });

  it('can resolve content generation catalog requests to local fixtures for mock development', () => {
    expect(contentGenerationOptionsRequest({ useLocalMock: true })).toEqual({
      path: '/mock/content-generation-options.json',
      init: {},
    });
    expect(contentGenerationPlanRequest({ platform: 'xhs' }, { useLocalMock: true })).toEqual({
      path: '/mock/content-generation-plan.json',
      init: {},
    });
  });

  it('creates a backend session through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/sessions');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual({
        user_id: 'operator_1',
        profile_id: 'holly',
        metadata: {
          source: 'workbench',
        },
      });
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            session_id: 'session_1',
            user_id: 'operator_1',
            profile_id: 'holly',
            metadata: {
              source: 'workbench',
            },
          },
        }),
        {
          status: 201,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(
      createSession(
        {
          user_id: 'operator_1',
          profile_id: 'holly',
          metadata: {
            source: 'workbench',
          },
        },
        fetcher as typeof fetch,
      ),
    ).resolves.toMatchObject({
      session_id: 'session_1',
      metadata: {
        source: 'workbench',
      },
    });
  });

  it('uploads session assets as multipart files through the API boundary', async () => {
    const file = new File(['fake image'], 'dish-reference.png', { type: 'image/png' });
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/sessions/session_1/assets');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
      }));
      expect(init?.headers).not.toHaveProperty('Content-Type');
      expect(init?.body).toBeInstanceOf(FormData);
      const form = init?.body as FormData;
      expect(form.getAll('files')).toHaveLength(1);
      expect((form.getAll('files')[0] as File).name).toBe('dish-reference.png');
      expect(form.get('usage')).toBe('reference');
      expect(form.get('task_id')).toBe('task_1');
      expect(form.get('metadata_json')).toBe(JSON.stringify({ source: 'workbench_upload' }));
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            assets: [
              {
                asset_id: 'asset_1',
                filename: 'dish-reference.png',
                kind: 'image',
                usage: 'reference',
                file_url: '/sessions/session_1/assets/asset_1/file',
              },
            ],
          },
        }),
        {
          status: 201,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(
      uploadSessionAssets(
        'session_1',
        [file],
        {
          usage: 'reference',
          task_id: 'task_1',
          metadata: {
            source: 'workbench_upload',
          },
        },
        fetcher as typeof fetch,
      ),
    ).resolves.toMatchObject({
      assets: [
        {
          asset_id: 'asset_1',
          filename: 'dish-reference.png',
        },
      ],
    });
  });

  it('checks session reference image generation readiness through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/sessions/session_1/assets/reference-image-generation-check');
      expect(init?.method).toBe('POST');
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }));
      expect(JSON.parse(String(init?.body))).toEqual({
        asset_ids: ['asset_1'],
        project: 'Holly',
        backend_public_base_url: 'https://backend.nori.ai',
        prompt: 'Validate references before content generation.',
        size: '1024x1024',
        metadata: {
          source: 'workbench',
        },
      });
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            ready: true,
            reason: 'image_generation_succeeded',
            provider_fetchable_count: 1,
            provider_fetchable_reference_images: [
              'https://backend.nori.ai/sessions/session_1/assets/asset_1/file',
            ],
            generation: {
              ready: true,
              image_count: 1,
            },
            next_actions: [{ action_id: 'run_strict_preflight', label: 'Run strict preflight' }],
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(
      checkSessionReferenceImageGeneration(
        'session_1',
        {
          asset_ids: ['asset_1'],
          project: 'Holly',
          backend_public_base_url: 'https://backend.nori.ai',
          prompt: 'Validate references before content generation.',
          size: '1024x1024',
          metadata: {
            source: 'workbench',
          },
        },
        fetcher as typeof fetch,
      ),
    ).resolves.toMatchObject({
      ready: true,
      reason: 'image_generation_succeeded',
      provider_fetchable_count: 1,
      next_actions: [{ action_id: 'run_strict_preflight' }],
    });
  });

  it('can resolve reference image generation checks to the local fixture for mock development', () => {
    expect(referenceImageGenerationCheckRequest('session_1', { asset_ids: ['asset_1'] }, { useLocalMock: true })).toEqual({
      path: '/mock/reference-image-generation-check.json',
      init: {},
    });
  });

  it('loads a content-production artifact inspection through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/workflows/content-production/runs/Holly/run_ready/artifacts/inspect');
      expect(init?.method).toBeUndefined();
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
      }));
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            schema_version: 1,
            case_id: 'Holly',
            run_id: 'run_ready',
            ready_for_review: true,
            status: 'succeeded',
            artifact_counts: { total: 5, json: 3, markdown: 1, covers: 1 },
            missing_core_artifacts: [],
            acceptance: { status: 'accepted' },
            links: {
              export: '/workflows/content-production/runs/Holly/run_ready/export',
            },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(inspectRunArtifacts('Holly', 'run_ready', fetcher as typeof fetch)).resolves.toMatchObject({
      case_id: 'Holly',
      run_id: 'run_ready',
      ready_for_review: true,
      acceptance: { status: 'accepted' },
    });
  });

  it('lists content-production runs through the API boundary', async () => {
    const fetcher = async (path: string | URL | Request, init?: RequestInit) => {
      expect(path).toBe('/api/workflows/content-production/runs?case_id=Holly&status=succeeded&limit=25&offset=5');
      expect(init?.method).toBeUndefined();
      expect(init?.headers).toEqual(expect.objectContaining({
        Accept: 'application/json',
      }));
      return new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            total_count: 3,
            filtered_count: 1,
            returned_count: 1,
            runs: [
              {
                case_id: 'Holly',
                run_id: 'run_ready',
                status: 'succeeded',
                ready_for_review: true,
                artifact_count: 7,
                cover_count: 1,
                evaluation_score: 96,
                acceptance_status: 'accepted',
                links: {
                  export: '/workflows/content-production/runs/Holly/run_ready/export',
                },
              },
            ],
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      );
    };

    await expect(
      listContentProductionRuns(
        {
          case_id: 'Holly',
          status: 'succeeded',
          limit: 25,
          offset: 5,
        },
        fetcher as typeof fetch,
      ),
    ).resolves.toMatchObject({
      filtered_count: 1,
      runs: [
        {
          run_id: 'run_ready',
          artifact_count: 7,
          acceptance_status: 'accepted',
        },
      ],
    });
  });

  it('can resolve content-production run lists to the local fixture for mock development', () => {
    expect(listContentProductionRunsRequest({ case_id: 'Holly' }, { useLocalMock: true })).toEqual({
      path: '/mock/content-production-runs.json',
      init: {},
    });
  });

  it('can resolve artifact inspection requests to the local fixture for mock development', () => {
    expect(inspectRunArtifactsRequest('Holly', 'run_ready', { useLocalMock: true })).toEqual({
      path: '/mock/artifact-inspection.json',
      init: {},
    });
  });

  it('can resolve named local artifact inspection fixtures for mock run history', () => {
    expect(inspectRunArtifactsRequest('Holly', 'mock_run_needs_review', { useLocalMock: true })).toEqual({
      path: '/mock/artifact-inspection-mock_run_needs_review.json',
      init: {},
    });
  });
});
