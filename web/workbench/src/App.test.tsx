import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { App } from './App';

describe('App', () => {
  it('opens a workspace from the URL hash and updates the hash when navigating', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#planning');

    render(<App />);

    expect(screen.getAllByRole('heading', { name: 'Account Planning' }).length).toBeGreaterThanOrEqual(1);

    await user.click(screen.getByRole('button', { name: '产物库' }));

    expect(window.location.hash).toBe('#library');
    expect(screen.getAllByRole('heading', { name: 'Artifact Store' }).length).toBeGreaterThanOrEqual(1);
  });

  it('requests the backend workbench bootstrap on startup', async () => {
    const fetcher = vi.fn(async () =>
      new Response(JSON.stringify({ code: 0, message: 'ok', data: { cases: [], links: {} } }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );

    render(<App bootstrapPath="/api/experiments/content-production/workbench" fetcher={fetcher as typeof fetch} />);

    expect(fetcher).toHaveBeenCalledWith(
      '/api/experiments/content-production/workbench',
      expect.objectContaining({ headers: expect.objectContaining({ Accept: 'application/json' }) }),
    );
    expect(await screen.findByText('Backend live')).toBeInTheDocument();
  });

  it('renders backend workbench snapshot health when bootstrap data is available', async () => {
    const fetcher = vi.fn(async () =>
      new Response(
        JSON.stringify({
          code: 0,
          message: 'ok',
          data: {
            status: 'needs_attention',
            ready: false,
            overview: {
              run_count: 3,
              case_count: 2,
              summary: {
                blocked_count: 2,
                ready_count: 1,
              },
            },
            cases: [
              {
                case_id: 'Holly',
                action_status: 'blocked',
                primary_action: {
                  label: 'Fix references',
                  severity: 'blocking',
                  message: 'Selected uploads must be provider-fetchable before image generation.',
                },
              },
            ],
            primary_actions: [
              {
                case_id: 'Holly',
                label: 'Fix references',
                severity: 'blocking',
                message: 'Selected uploads must be provider-fetchable before image generation.',
              },
            ],
            links: {
              run_template: '/experiments/content-production/run-template',
            },
          },
        }),
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        },
      ),
    );

    render(<App bootstrapPath="/api/experiments/content-production/workbench" fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('needs_attention')).toBeInTheDocument();
    expect(screen.getByText('3 runs')).toBeInTheDocument();
    expect(screen.getByText('2 cases')).toBeInTheDocument();
    expect(screen.getByText('2 blocked')).toBeInTheDocument();
    expect(screen.getByText('Fix references')).toBeInTheDocument();
    expect(screen.getAllByText('Holly').length).toBeGreaterThanOrEqual(1);
  });

  it('shows a local fallback state when backend bootstrap fails', async () => {
    const fetcher = vi.fn(async () =>
      new Response(JSON.stringify({ code: 503, message: 'backend unavailable', data: {} }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' },
      }),
    );

    render(<App bootstrapPath="/api/experiments/content-production/workbench" fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Local demo fallback')).toBeInTheDocument();
  });

  it('renders a production workbench around the content workflow', () => {
    render(<App />);

    expect(screen.getByRole('heading', { name: /Nori Content Workbench/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: '创作 brief' })).toBeInTheDocument();
    expect(screen.getAllByText('Context Pack').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Design Spec').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Artifact Package').length).toBeGreaterThanOrEqual(1);
  });

  it('loads generation controls from the backend catalog and renders a plan recommendation', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/content/generation/options') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              option_groups: {
                platform: [
                  { option_id: 'xhs', label: 'Xiaohongshu', description: 'XHS image-text note.', default: true },
                  { option_id: 'wechat', label: 'WeChat Official Account', description: 'Long-form article.' },
                ],
                artifact_type: [
                  { option_id: 'image_text_post', label: 'Image-text post', description: 'Spec-driven post.', default: true },
                  { option_id: 'article', label: 'Article', description: 'Long-form article.' },
                ],
                cover_strategy: [
                  { option_id: 'auto', label: 'Auto', description: 'Let Nori choose references.', default: true },
                  { option_id: 'manual_references', label: 'Manual references', description: 'User selected refs.' },
                ],
                image_source: [
                  { option_id: 'uploaded_assets', label: 'Uploaded assets', description: 'Use uploaded materials.', default: true },
                ],
                human_gate_mode: [
                  { option_id: 'skip', label: 'Skip', description: 'Record gate as skipped.', default: true },
                ],
                entry_mode: [
                  { option_id: 'direct_action', label: 'Direct action', description: 'Call a concrete capability.', default: true },
                  { option_id: 'workflow', label: 'Workflow', description: 'Run orchestrated workflow.' },
                ],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/content/generation/plan') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body.platform).toBe('xhs');
        expect(body.artifact_type).toBe('image_text_post');
        expect(body.cover_strategy).toBe('manual_references');
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
              rationale: 'Use the cover sub-capability when the product is choosing or generating imagery without rerunning the whole workflow.',
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Generation controls')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Xiaohongshu' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'WeChat Official Account' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Image-text post' })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Manual references' }));

    expect(await screen.findByText('Recommended action')).toBeInTheDocument();
    expect(screen.getByText('content.cover')).toBeInTheDocument();
    expect(screen.getByText('/content/generation/cover')).toBeInTheDocument();
  });

  it('prepares a backend run template from the compose brief before generation', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/experiments/content-production/run-template') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body.brief_text).toContain('给巷口暖胃小馆生成一篇小红书图文');
        expect(body.case_id).toBe('Holly');
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: false,
              missing_fields: ['session', 'market_evidence'],
              actions: [
                {
                  action_id: 'create_session',
                  label: 'Create session',
                  href: '/sessions',
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));

    expect(await screen.findByText('Template needs input')).toBeInTheDocument();
    expect(screen.getByText('session')).toBeInTheDocument();
    expect(screen.getByText('market_evidence')).toBeInTheDocument();
    expect(screen.getByText('Create session')).toBeInTheDocument();
    expect(screen.getByText('Spec gate waiting for workflow stage')).toBeInTheDocument();
  });

  it('uses the backend active account and case when preparing a compose run template', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#compose');

    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              case_id: 'BeanLab',
              overview: {
                active_account: 'Bean Lab Studio',
              },
              context_layer: {
                active_case_id: 'BeanLab',
                summary: 'Launch a coffee account with neighborhood credibility.',
              },
              cases: [
                {
                  case_id: 'BeanLab',
                  case_title: 'Bean Lab Studio',
                  latest_run_id: 'run_bean_latest',
                  primary_action: {
                    label: 'Review launch content',
                    message: 'Coffee launch content is ready for a production run.',
                  },
                },
              ],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/content/generation/options') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              option_groups: {
                platform: [{ option_id: 'xhs', label: 'Xiaohongshu', default: true }],
                artifact_type: [{ option_id: 'image_text_post', label: 'Image-text post', default: true }],
                image_source: [{ option_id: 'uploaded_assets', label: 'Uploaded assets', default: true }],
                cover_strategy: [{ option_id: 'auto', label: 'Auto', default: true }],
                human_gate_mode: [{ option_id: 'skip', label: 'Skip', default: true }],
                entry_mode: [{ option_id: 'workflow', label: 'Workflow', default: true }],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/experiments/content-production/run-template') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body.case_id).toBe('BeanLab');
        expect(body.case_title).toBe('Bean Lab Studio');
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: false,
              missing_fields: ['session'],
              actions: [],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Bean Lab Studio')).toBeInTheDocument();
    expect(screen.getAllByText('BeanLab').length).toBeGreaterThanOrEqual(1);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));

    expect(await screen.findByText('Template needs input')).toBeInTheDocument();
  });

  it('uploads reference assets into a session and sends them into the run template draft', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/content/generation/options') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              option_groups: {
                platform: [{ option_id: 'xhs', label: 'Xiaohongshu', default: true }],
                artifact_type: [{ option_id: 'image_text_post', label: 'Image-text post', default: true }],
                image_source: [{ option_id: 'uploaded_assets', label: 'Uploaded assets', default: true }],
                cover_strategy: [{ option_id: 'auto', label: 'Auto', default: true }],
                human_gate_mode: [{ option_id: 'skip', label: 'Skip', default: true }],
                entry_mode: [{ option_id: 'workflow', label: 'Workflow', default: true }],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/sessions') {
        expect(init?.method).toBe('POST');
        expect(JSON.parse(String(init?.body))).toMatchObject({
          profile_id: 'Holly',
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
              profile_id: 'Holly',
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
      }
      if (path === '/api/sessions/session_1/assets') {
        expect(init?.method).toBe('POST');
        expect(init?.body).toBeInstanceOf(FormData);
        const form = init?.body as FormData;
        expect((form.getAll('files')[0] as File).name).toBe('dish-reference.png');
        expect(form.get('usage')).toBe('reference');
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
      }
      if (path === '/api/experiments/content-production/run-template') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body.session_id).toBe('session_1');
        expect(body.asset_ids).toEqual(['asset_1']);
        expect(body.config.image_source).toBe('uploaded_assets');
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              request: body,
              assets: {
                selected_count: 1,
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    const file = new File(['fake image'], 'dish-reference.png', { type: 'image/png' });
    await user.upload(await screen.findByLabelText('Upload reference assets'), file);

    expect(await screen.findByText('dish-reference.png')).toBeInTheDocument();
    expect(screen.getByText('asset_1')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));

    expect(await screen.findByText('Template ready for preflight')).toBeInTheDocument();
  });

  it('checks uploaded reference assets before preparing a strict image-generation run template', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/content/generation/options') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              option_groups: {
                platform: [{ option_id: 'xhs', label: 'Xiaohongshu', default: true }],
                artifact_type: [{ option_id: 'image_text_post', label: 'Image-text post', default: true }],
                image_source: [{ option_id: 'uploaded_assets', label: 'Uploaded assets', default: true }],
                cover_strategy: [{ option_id: 'auto', label: 'Auto', default: true }],
                human_gate_mode: [{ option_id: 'skip', label: 'Skip', default: true }],
                entry_mode: [{ option_id: 'workflow', label: 'Workflow', default: true }],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/sessions') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              session_id: 'session_1',
              profile_id: 'Holly',
            },
          }),
          {
            status: 201,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/sessions/session_1/assets') {
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
      }
      if (path === '/api/sessions/session_1/assets/reference-image-generation-check') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body.asset_ids).toEqual(['asset_1']);
        expect(body.project).toBe('Holly');
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
      }
      if (path === '/api/experiments/content-production/run-template') {
        const body = JSON.parse(String(init?.body));
        expect(body.session_id).toBe('session_1');
        expect(body.asset_ids).toEqual(['asset_1']);
        expect(body.require_reference_image_generation_check).toBe(true);
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              request: body,
              reference_images: {
                latest_check: {
                  ready: true,
                  reason: 'image_generation_succeeded',
                },
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.upload(
      await screen.findByLabelText('Upload reference assets'),
      new File(['fake image'], 'dish-reference.png', { type: 'image/png' }),
    );
    await user.click(await screen.findByRole('button', { name: 'Verify references' }));

    expect(await screen.findByText('Reference check ready')).toBeInTheDocument();
    expect(screen.getByText('image generation succeeded')).toBeInTheDocument();
    expect(screen.getByText('1 fetchable reference')).toBeInTheDocument();
    expect(screen.getByText('Run strict preflight')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));

    expect(await screen.findByText('Template ready for preflight')).toBeInTheDocument();
  });

  it('renders a design spec draft when the run template provides one', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/experiments/content-production/run-template') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              request: {
                session_id: 'session_1',
                case_id: 'Holly',
                brief_text: '生成一篇小红书图文',
              },
              content_design_spec: {
                spec_id: 'spec_holly_xhs_001',
                platform: 'xhs',
                artifact_type: 'image_text_post',
                creative_angle: '第一次到店点单避坑，用真实菜单和招牌菜建立收藏理由。',
                selected_skill_refs: [
                  {
                    skill_id: 'xhs_hotspot_image_post',
                    label: '热点小红书图文生成',
                  },
                ],
                structure: [
                  { slot: 'cover', purpose: '首图给出明确点单结论' },
                  { slot: 'body', purpose: '三段式解释适合谁和为什么' },
                ],
                media_plan: {
                  cover: { required: true, reference_policy: 'uploaded_assets' },
                },
                acceptance_checks: ['封面必须有结论', '正文必须引用门店素材'],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));

    expect(await screen.findByText('Spec draft ready')).toBeInTheDocument();
    expect(screen.getByText('spec_holly_xhs_001')).toBeInTheDocument();
    expect(screen.getAllByText('热点小红书图文生成').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('第一次到店点单避坑，用真实菜单和招牌菜建立收藏理由。')).toBeInTheDocument();
    expect(screen.getByText('封面必须有结论')).toBeInTheDocument();
    expect(screen.getByText('正文必须引用门店素材')).toBeInTheDocument();
  });

  it('runs preflight from a ready run template and renders checks/actions', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/experiments/content-production/run-template') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              missing_fields: [],
              request: {
                session_id: 'session_1',
                case_id: 'Holly',
                brief_text: '生成一篇小红书图文',
              },
              actions: [
                {
                  action_id: 'run_preflight',
                  label: 'Run preflight',
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/preflight') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready: false,
              checks: [
                {
                  name: 'reference_transfer',
                  status: 'failed',
                  message: 'Reference assets need public URLs.',
                },
              ],
              actions: [
                {
                  action_id: 'publish_reference_assets',
                  label: 'Publish references',
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));
    expect(await screen.findByText('Template ready for preflight')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Run preflight' }));

    expect(await screen.findByText('Preflight blocked')).toBeInTheDocument();
    expect(screen.getByText('reference_transfer')).toBeInTheDocument();
    expect(screen.getByText('Publish references')).toBeInTheDocument();
  });

  it('runs the content workflow from a ready preflight and renders delivery links', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/experiments/content-production/run-template') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              request: {
                session_id: 'session_1',
                case_id: 'Holly',
                brief_text: '生成一篇小红书图文',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/preflight') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready: true,
              checks: [{ name: 'reference_transfer', status: 'passed' }],
              actions: [{ action_id: 'run_experiment', label: 'Run experiment' }],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              workflow_name: 'content_production',
              run_id: 'run_ready',
              status: 'succeeded',
              artifact_paths: {
                'content_package.json': 'cases/Holly/runs/run_ready/content_package.json',
              },
              actions: [
                {
                  action_id: 'inspect_run',
                  label: 'Inspect run',
                  href: '/workflows/content-production/runs/Holly/run_ready/artifacts/inspect',
                },
                {
                  action_id: 'export_run',
                  label: 'Export run',
                  href: '/workflows/content-production/runs/Holly/run_ready/export',
                },
              ],
            },
          }),
          {
            status: 201,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 1,
              filtered_count: 1,
              returned_count: 1,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_ready',
                  status: 'succeeded',
                  created_at: '2026-06-08T10:00:00',
                  acceptance_status: 'accepted',
                  evaluation_score: 96,
                  artifact_count: 7,
                  cover_count: 1,
                  candidate: { ready_for_review: true },
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
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_ready/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              schema_version: 1,
              case_id: 'Holly',
              run_id: 'run_ready',
              status: 'succeeded',
              workflow_name: 'content_production',
              ready_for_review: true,
              artifact_counts: {
                total: 5,
                json: 3,
                markdown: 1,
                covers: 1,
              },
              missing_core_artifacts: [],
              proof: {
                status: 'ready',
              },
              acceptance: {
                status: 'accepted',
              },
              evaluations: {
                summary: {
                  count: 1,
                  score: 95,
                },
              },
              content_package: {
                available: true,
                json_summary: {
                  keys: ['cover', 'posts', 'publish_checklist'],
                  field_count: 3,
                },
              },
              covers: [
                {
                  available: true,
                  artifact_name: 'covers/cover.png',
                  url: '/workflows/content-production/runs/Holly/run_ready/artifacts/covers/cover.png',
                },
              ],
              links: {
                export: '/workflows/content-production/runs/Holly/run_ready/export',
                replay: '/workflows/content-production/runs/Holly/run_ready/replay',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));
    await user.click(await screen.findByRole('button', { name: 'Run preflight' }));
    expect(await screen.findByText('Preflight ready')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Run content workflow' }));

    expect(await screen.findByText('Run succeeded')).toBeInTheDocument();
    expect(screen.getByText('run_ready')).toBeInTheDocument();
    expect(screen.getByText('content_package.json')).toBeInTheDocument();
    expect(screen.getByText('Inspect run')).toBeInTheDocument();
    expect(screen.getByText('Export run')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Inspect artifacts' }));

    expect(await screen.findByText('Artifact inspection ready')).toBeInTheDocument();
    expect(screen.getByText('accepted')).toBeInTheDocument();
    expect(screen.getByText('5 artifacts')).toBeInTheDocument();
    expect(screen.getByText('No missing core artifacts')).toBeInTheDocument();
    expect(screen.getByText('95 review score')).toBeInTheDocument();
    expect(screen.getByText('/workflows/content-production/runs/Holly/run_ready/export')).toBeInTheDocument();
  });

  it('carries a successful compose run into the Artifact Store review target', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#compose');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_old' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/experiments/content-production/run-template') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready_for_preflight: true,
              request: {
                case_id: 'Holly',
                brief_text: '生成一篇小红书图文',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/preflight') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              ready: true,
              checks: [{ name: 'reference_transfer', status: 'passed' }],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              workflow_name: 'content_production',
              run_id: 'run_new',
              status: 'succeeded',
              artifact_paths: {
                'content_package.json': 'cases/Holly/runs/run_new/content_package.json',
              },
            },
          }),
          {
            status: 201,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 2,
              returned_count: 2,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_new',
                  status: 'succeeded',
                  acceptance_status: 'accepted',
                  artifact_count: 7,
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_new/export',
                  },
                },
                {
                  case_id: 'Holly',
                  run_id: 'run_old',
                  status: 'succeeded',
                  acceptance_status: 'accepted',
                  artifact_count: 4,
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_old/export',
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
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_new/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_new',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 7, json: 4, markdown: 2, covers: 1 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              links: {
                export: '/workflows/content-production/runs/Holly/run_new/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_old/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_old',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 4, json: 2, markdown: 1, covers: 1 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              links: {
                export: '/workflows/content-production/runs/Holly/run_old/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: 'Prepare backend run template' }));
    await user.click(await screen.findByRole('button', { name: 'Run preflight' }));
    await user.click(screen.getByRole('button', { name: 'Run content workflow' }));
    expect(await screen.findByText('Run succeeded')).toBeInTheDocument();
    expect(screen.getByText('run_new')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Review in Artifact Store' }));

    expect(window.location.hash).toBe('#library?case_id=Holly&run_id=run_new');
    expect(await screen.findByText('Holly / run_new')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Export' })).toHaveAttribute(
      'href',
      '/api/workflows/content-production/runs/Holly/run_new/export',
    );
  });

  it('switches between the production workspaces from navigation', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole('button', { name: '上下文' }));
    expect(screen.getByRole('heading', { name: 'Context Intelligence' })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Skills' }));
    expect(screen.getAllByRole('heading', { name: 'Skill Operating System' }).length).toBeGreaterThanOrEqual(1);

    await user.click(screen.getByRole('button', { name: '产物库' }));
    expect(screen.getAllByRole('heading', { name: 'Artifact Store' }).length).toBeGreaterThanOrEqual(1);

    await user.click(screen.getByRole('button', { name: '创作台' }));
    expect(screen.getByRole('heading', { name: /Nori Content Workbench/i })).toBeInTheDocument();
  });

  it('uses topbar actions as real workspace shortcuts', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#context');

    render(<App />);

    await user.click(screen.getByRole('button', { name: 'Preview' }));
    expect(window.location.hash).toBe('#library');
    expect(screen.getAllByRole('heading', { name: 'Artifact Store' }).length).toBeGreaterThanOrEqual(1);

    await user.click(screen.getByRole('button', { name: 'Run workflow' }));
    expect(window.location.hash).toBe('#compose');
    expect(screen.getByRole('heading', { name: /Nori Content Workbench/i })).toBeInTheDocument();
  });

  it('moves focus to the active mobile navigation item when opening navigation', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#planning');

    render(<App />);

    await user.click(screen.getByRole('button', { name: 'Open navigation' }));

    expect(screen.getByRole('button', { name: 'Go to 账号规划' })).toHaveFocus();
  });

  it('connects the Skill Operating System to backend generation catalog and spec handoff planning', async () => {
    window.history.replaceState(null, '', '#skills');
    const fetcher = vi.fn(async (path: string | URL | Request, init?: RequestInit) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(JSON.stringify({ code: 0, message: 'ok', data: { source: 'mock', cases: [], links: {} } }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      if (path === '/api/content/generation/options') {
        expect(init?.method).toBeUndefined();
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              option_groups: {
                platform: [
                  { option_id: 'xhs', label: 'Xiaohongshu', description: 'XHS image-text note.', default: true },
                  { option_id: 'wechat', label: 'WeChat Official Account', description: 'Long-form article.' },
                ],
                artifact_type: [
                  { option_id: 'image_text_post', label: 'Image-text post', description: 'Spec-driven post.', default: true },
                  { option_id: 'article', label: 'Article', description: 'Long-form article.' },
                ],
                cover_strategy: [
                  { option_id: 'auto', label: 'Auto', description: 'Let Nori choose references.', default: true },
                  { option_id: 'manual_references', label: 'Manual references', description: 'Use selected references.' },
                ],
                image_source: [
                  { option_id: 'uploaded_assets', label: 'Uploaded assets', description: 'Use session assets.', default: true },
                ],
                human_gate_mode: [
                  { option_id: 'skip', label: 'Skip', description: 'Record skipped gate.', default: true },
                ],
                entry_mode: [
                  { option_id: 'direct_action', label: 'Direct action', description: 'Call a single route.', default: true },
                  { option_id: 'workflow', label: 'Workflow', description: 'Run orchestrated workflow.' },
                ],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/content/generation/plan') {
        expect(init?.method).toBe('POST');
        const body = JSON.parse(String(init?.body));
        expect(body).toMatchObject({
          platform: 'xhs',
          artifact_type: 'image_text_post',
          cover_strategy: 'auto',
          image_source: 'uploaded_assets',
          human_gate_mode: 'skip',
          entry_mode: 'workflow',
        });
        expect(body.metadata.source).toBe('skill_operating_system');
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              capability_id: 'content_generation',
              selected_action_id: 'workflow.content_production',
              selected_route: '/workflows/content-production/runs',
              workflow_id: 'content-production',
              requires_workflow_id: true,
              normalized_options: {
                platform: 'xhs',
                artifact_type: 'image_text_post',
                image_source: 'uploaded_assets',
                cover_strategy: 'auto',
                human_gate_mode: 'skip',
                entry_mode: 'workflow',
              },
              rationale: 'Use the workflow when skills must become a reusable Design Spec before generation.',
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Backend skill catalog')).toBeInTheDocument();
    expect(screen.getByText('Xiaohongshu')).toBeInTheDocument();
    expect(screen.getByText('WeChat Official Account')).toBeInTheDocument();
    expect(screen.getByText('Image-text post')).toBeInTheDocument();
    expect(await screen.findByText('Design Spec handoff')).toBeInTheDocument();
    expect(screen.getByText('workflow.content_production')).toBeInTheDocument();
    expect(screen.getByText('/workflows/content-production/runs')).toBeInTheDocument();
  });

  it('loads artifact inspection data in the Artifact Store workspace', async () => {
    const user = userEvent.setup();
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_ready' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_ready/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_ready',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 7, json: 4, markdown: 2, covers: 1 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              evaluations: { summary: { score: 96 } },
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
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: '产物库' }));

    expect(await screen.findByRole('heading', { name: 'Latest reviewed package' })).toBeInTheDocument();
    expect(screen.getByText('Holly / run_ready')).toBeInTheDocument();
    expect(screen.getByText('accepted')).toBeInTheDocument();
    expect(screen.getByText('7 artifacts')).toBeInTheDocument();
    expect(screen.getByText('96 review score')).toBeInTheDocument();
    expect(screen.getByText('/workflows/content-production/runs/Holly/run_ready/export')).toBeInTheDocument();
  });

  it('wires Artifact Store inspect and export actions to the selected backend run', async () => {
    const user = userEvent.setup();
    let inspectCalls = 0;
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_ready' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 1,
              filtered_count: 1,
              returned_count: 1,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_ready',
                  status: 'succeeded',
                  artifact_count: 7,
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
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_ready/artifacts/inspect') {
        inspectCalls += 1;
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_ready',
              ready_for_review: true,
              artifact_counts: { total: 7, json: 4, markdown: 2, covers: 1 },
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
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: '产物库' }));

    expect(await screen.findByText('Artifact inspection ready')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Export' })).toHaveAttribute(
      'href',
      '/api/workflows/content-production/runs/Holly/run_ready/export',
    );

    await user.click(screen.getByRole('button', { name: 'Inspect' }));

    expect(inspectCalls).toBeGreaterThanOrEqual(2);
  });

  it('opens the Artifact Store directly from a case and run deep link', async () => {
    window.history.replaceState(null, '', '#library?case_id=Holly&run_id=run_deep');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_old' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 2,
              returned_count: 2,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_deep',
                  status: 'succeeded',
                  artifact_count: 9,
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_deep/export',
                  },
                },
                {
                  case_id: 'Holly',
                  run_id: 'run_old',
                  status: 'succeeded',
                  artifact_count: 3,
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_old/export',
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
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_deep/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_deep',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 9, json: 5, markdown: 3, covers: 1 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              links: {
                export: '/workflows/content-production/runs/Holly/run_deep/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Holly / run_deep')).toBeInTheDocument();
    expect(screen.getAllByText('9 artifacts').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole('link', { name: 'Export' })).toHaveAttribute(
      'href',
      '/api/workflows/content-production/runs/Holly/run_deep/export',
    );
  });

  it('lets the Artifact Store browse run history and inspect a selected run', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#compose');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_latest' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 2,
              returned_count: 2,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_latest',
                  status: 'succeeded',
                  created_at: '2026-06-08T11:00:00',
                  acceptance_status: 'accepted',
                  evaluation_score: 97,
                  artifact_count: 8,
                  cover_count: 2,
                  candidate: { ready_for_review: true },
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_latest/export',
                  },
                },
                {
                  case_id: 'Holly',
                  run_id: 'run_previous',
                  status: 'succeeded',
                  created_at: '2026-06-07T20:00:00',
                  acceptance_status: 'needs_review',
                  evaluation_score: 82,
                  artifact_count: 6,
                  cover_count: 1,
                  candidate: { ready_for_review: false },
                  links: {
                    export: '/workflows/content-production/runs/Holly/run_previous/export',
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
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_latest/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_latest',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 8, json: 4, markdown: 2, covers: 2 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              evaluations: { summary: { score: 97 } },
              links: {
                export: '/workflows/content-production/runs/Holly/run_latest/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_previous/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_previous',
              ready_for_review: false,
              status: 'succeeded',
              artifact_counts: { total: 6, json: 3, markdown: 2, covers: 1 },
              missing_core_artifacts: ['visual_reference_review'],
              acceptance: { status: 'needs_review' },
              evaluations: { summary: { score: 82 } },
              links: {
                export: '/workflows/content-production/runs/Holly/run_previous/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    await user.click(screen.getByRole('button', { name: '产物库' }));

    expect(await screen.findByText('Run history')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run_latest/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run_previous/ })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /run_previous/ }));

    expect(window.location.hash).toBe('#library?case_id=Holly&run_id=run_previous');
    expect(await screen.findByText('Holly / run_previous')).toBeInTheDocument();
    expect(screen.getAllByText('needs_review').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('6 artifacts').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('82 review score')).toBeInTheDocument();
    expect(screen.getByText('Missing core artifacts: visual_reference_review')).toBeInTheDocument();
  });

  it('filters the Artifact Store run history without replacing the active review target', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#library?case_id=Holly&run_id=run_latest');
    const requestedPaths: string[] = [];
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      requestedPaths.push(path.toString());

      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_latest' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 2,
              returned_count: 2,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_latest',
                  status: 'succeeded',
                  acceptance_status: 'accepted',
                  artifact_count: 8,
                },
                {
                  case_id: 'Holly',
                  run_id: 'run_previous',
                  status: 'succeeded',
                  acceptance_status: 'needs_review',
                  artifact_count: 6,
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&acceptance_status=needs_review&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 1,
              returned_count: 1,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_previous',
                  status: 'succeeded',
                  acceptance_status: 'needs_review',
                  artifact_count: 6,
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_latest/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_latest',
              ready_for_review: true,
              artifact_counts: { total: 8, json: 4, markdown: 2, covers: 2 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              links: {
                export: '/workflows/content-production/runs/Holly/run_latest/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Holly / run_latest')).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: /run_previous/ })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Needs review' }));

    expect(await screen.findByText('1 shown')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run_previous/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /run_latest/ })).not.toBeInTheDocument();
    expect(screen.getByText('Holly / run_latest')).toBeInTheDocument();
    expect(window.location.hash).toBe('#library?case_id=Holly&run_id=run_latest&filter=needs_review');
    expect(requestedPaths).toContain('/api/workflows/content-production/runs?case_id=Holly&acceptance_status=needs_review&limit=12');
  });

  it('restores the Artifact Store run history filter from a deep link', async () => {
    window.history.replaceState(null, '', '#library?case_id=Holly&run_id=run_latest&filter=needs_review');
    const requestedPaths: string[] = [];
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      requestedPaths.push(path.toString());

      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_latest' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=Holly&acceptance_status=needs_review&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 1,
              returned_count: 1,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_previous',
                  status: 'succeeded',
                  acceptance_status: 'needs_review',
                  artifact_count: 6,
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_latest/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_latest',
              ready_for_review: true,
              artifact_counts: { total: 8, json: 4, markdown: 2, covers: 2 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Holly / run_latest')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Needs review' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: /run_previous/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /run_latest/ })).not.toBeInTheDocument();
    expect(requestedPaths).toContain('/api/workflows/content-production/runs?case_id=Holly&acceptance_status=needs_review&limit=12');
  });

  it('applies the active run history filter to returned rows when the data source is unfiltered', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#library?case_id=Holly&run_id=run_latest');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              cases: [{ case_id: 'Holly', latest_run_id: 'run_latest' }],
              links: {},
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path.toString().startsWith('/api/workflows/content-production/runs?case_id=Holly')) {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 2,
              filtered_count: 2,
              returned_count: 2,
              runs: [
                {
                  case_id: 'Holly',
                  run_id: 'run_latest',
                  status: 'succeeded',
                  acceptance_status: 'accepted',
                  artifact_count: 8,
                },
                {
                  case_id: 'Holly',
                  run_id: 'run_previous',
                  status: 'succeeded',
                  acceptance_status: 'needs_review',
                  artifact_count: 6,
                },
              ],
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs/Holly/run_latest/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'Holly',
              run_id: 'run_latest',
              ready_for_review: true,
              artifact_counts: { total: 8, json: 4, markdown: 2, covers: 2 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByRole('button', { name: /run_latest/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run_previous/ })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Needs review' }));

    expect(await screen.findByText('1 shown')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /run_latest/ })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /run_previous/ })).toBeInTheDocument();
  });

  it('keeps account planning as the first-class workflow before generation', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole('button', { name: '账号规划' }));

    expect(screen.getAllByRole('heading', { name: 'Account Planning' }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('账号定位')).toBeInTheDocument();
    expect(screen.getByText('运营计划')).toBeInTheDocument();
    expect(screen.getByText('内容日历')).toBeInTheDocument();
  });

  it('renders backend account planning state from the workbench bootstrap', async () => {
    window.history.replaceState(null, '', '#planning');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              status: 'needs_attention',
              ready: false,
              overview: {
                active_account: '巷口暖胃小馆',
                run_count: 8,
                case_count: 2,
                summary: {
                  ready_count: 6,
                  blocked_count: 1,
                },
              },
              cases: [
                {
                  case_id: 'Holly',
                  run_count: 5,
                  latest_run_id: 'run_ready',
                  action_status: 'blocked',
                  primary_action: {
                    label: 'Fix references',
                    severity: 'blocking',
                    message: 'Selected uploads must be provider-fetchable before image generation.',
                  },
                },
                {
                  case_id: 'HollyBackendAPI',
                  run_count: 3,
                  latest_run_id: 'run_review',
                  action_status: 'needs_review',
                  primary_action: {
                    label: 'Draft evaluation',
                    severity: 'review',
                    message: 'Create deterministic evaluation draft.',
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
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Backend account plan')).toBeInTheDocument();
    expect(screen.getAllByText('巷口暖胃小馆').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('8 runs').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('2 cases').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('1 blocked').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Holly / run_ready')).toBeInTheDocument();
    expect(screen.getAllByText('Fix references').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('HollyBackendAPI / run_review')).toBeInTheDocument();
    expect(screen.getByText('Draft evaluation')).toBeInTheDocument();
  });

  it('renders backend context layer data from the workbench bootstrap in the Context workspace', async () => {
    window.history.replaceState(null, '', '#context');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              status: 'ready',
              ready: true,
              overview: {
                active_account: '巷口暖胃小馆',
                run_count: 8,
                case_count: 2,
                summary: {
                  ready_count: 6,
                  blocked_count: 1,
                },
              },
              cases: [
                {
                  case_id: 'Holly',
                  latest_run_id: 'run_context',
                  action_status: 'ready',
                },
              ],
              context_layer: {
                context_pack_id: 'ctx_holly_xhs_live',
                status: 'ready',
                active_case_id: 'Holly',
                active_run_id: 'run_context',
                summary: 'Design Spec input ready',
                slices: [
                  {
                    kind: 'platform_strategy',
                    title: 'Platform strategy',
                    summary: 'XHS first-screen conclusion with evidence-backed copy.',
                    signal: 'XHS',
                  },
                  {
                    kind: 'market_hotspots',
                    title: 'Market hotspots',
                    summary: '第一次怎么点 and 社区饭店复吃 are rising.',
                    signal: '2 hot notes',
                  },
                ],
                source_refs: ['market/xhs_top_notes_result.json', 'content_context_pack.json'],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Backend context layer')).toBeInTheDocument();
    expect(screen.getByText('ctx_holly_xhs_live')).toBeInTheDocument();
    expect(screen.getByText('Design Spec input ready')).toBeInTheDocument();
    expect(screen.getByText('Holly / run_context')).toBeInTheDocument();
    expect(screen.getByText('platform_strategy')).toBeInTheDocument();
    expect(screen.getByText('market_hotspots')).toBeInTheDocument();
    expect(screen.getByText('2 hot notes')).toBeInTheDocument();
    expect(screen.getByText('market/xhs_top_notes_result.json')).toBeInTheDocument();
  });

  it('uses one backend active account frame across Planning, Context, and Library workspaces', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#planning');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              status: 'ready',
              ready: true,
              overview: {
                run_count: 4,
                case_count: 2,
                summary: {
                  ready_count: 2,
                  blocked_count: 0,
                },
              },
              cases: [
                {
                  case_id: 'Holly',
                  case_title: 'Holly Cafe',
                  latest_run_id: 'run_holly_latest',
                  run_count: 2,
                  action_status: 'ready',
                },
                {
                  case_id: 'BeanLab',
                  case_title: 'Bean Lab Studio',
                  latest_run_id: 'run_bean_latest',
                  run_count: 2,
                  action_status: 'ready',
                  primary_action: {
                    label: 'Publish espresso launch',
                    message: 'BeanLab active content is ready for review.',
                  },
                },
              ],
              context_layer: {
                context_pack_id: 'ctx_bean_launch',
                status: 'ready',
                active_case_id: 'BeanLab',
                active_run_id: 'run_bean_latest',
                summary: 'BeanLab launch memory is ready for design spec generation.',
                source_refs: ['bean/context_pack.json'],
                slices: [
                  {
                    kind: 'brand_positioning',
                    title: 'Brand positioning',
                    summary: 'Neighborhood coffee account with credible launch content.',
                    signal: 'BeanLab',
                  },
                ],
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      if (path === '/api/workflows/content-production/runs?case_id=BeanLab&limit=12') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              total_count: 1,
              filtered_count: 1,
              returned_count: 1,
              runs: [
                {
                  case_id: 'BeanLab',
                  run_id: 'run_bean_latest',
                  status: 'succeeded',
                  acceptance_status: 'accepted',
                  artifact_count: 5,
                  links: {
                    export: '/workflows/content-production/runs/BeanLab/run_bean_latest/export',
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
      }
      if (path === '/api/workflows/content-production/runs/BeanLab/run_bean_latest/artifacts/inspect') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              case_id: 'BeanLab',
              run_id: 'run_bean_latest',
              ready_for_review: true,
              status: 'succeeded',
              artifact_counts: { total: 5, json: 3, markdown: 1, covers: 1 },
              missing_core_artifacts: [],
              acceptance: { status: 'accepted' },
              links: {
                export: '/workflows/content-production/runs/BeanLab/run_bean_latest/export',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('Backend account plan')).toBeInTheDocument();
    expect(screen.getByText('输入账号资料：Bean Lab Studio')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: '上下文' }));
    expect(await screen.findByText('Backend context layer')).toBeInTheDocument();
    expect(screen.getByText('ctx_bean_launch')).toBeInTheDocument();
    expect(screen.getByText('BeanLab / run_bean_latest')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: '产物库' }));
    expect(await screen.findByText('BeanLab / run_bean_latest')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Export' })).toHaveAttribute(
      'href',
      '/api/workflows/content-production/runs/BeanLab/run_bean_latest/export',
    );
  });

  it('restores and changes the active case from workspace routes', async () => {
    const user = userEvent.setup();
    window.history.replaceState(null, '', '#planning?case_id=BeanLab');
    const fetcher = vi.fn(async (path: string | URL | Request) => {
      if (path === '/mock/workbench-bootstrap.json') {
        return new Response(
          JSON.stringify({
            code: 0,
            message: 'ok',
            data: {
              source: 'mock',
              status: 'ready',
              ready: true,
              overview: {
                active_account: 'Portfolio',
              },
              cases: [
                {
                  case_id: 'Holly',
                  case_title: 'Holly Cafe',
                  latest_run_id: 'run_holly_latest',
                  primary_action: {
                    label: 'Review Holly',
                    message: 'Holly message.',
                  },
                },
                {
                  case_id: 'BeanLab',
                  case_title: 'Bean Lab Studio',
                  latest_run_id: 'run_bean_latest',
                  primary_action: {
                    label: 'Publish espresso launch',
                    message: 'BeanLab active content is ready for review.',
                  },
                },
              ],
              context_layer: {
                active_case_id: 'Holly',
                active_run_id: 'run_holly_latest',
                summary: 'Backend default context.',
              },
            },
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          },
        );
      }
      throw new Error(`unexpected request: ${path.toString()}`);
    });

    render(<App fetcher={fetcher as typeof fetch} />);

    expect(await screen.findByText('输入账号资料：Bean Lab Studio')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /BeanLab/ })).toHaveAttribute('aria-pressed', 'true');
    expect(window.location.hash).toBe('#planning?case_id=BeanLab');

    await user.click(screen.getByRole('button', { name: /Holly Cafe/ }));

    expect(await screen.findByText('输入账号资料：Holly Cafe')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Holly Cafe/ })).toHaveAttribute('aria-pressed', 'true');
    expect(window.location.hash).toBe('#planning?case_id=Holly');
  });
});
