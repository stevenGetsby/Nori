import { describe, expect, it } from 'vitest';
import { buildWorkbenchSnapshot } from './workbenchSnapshot';

describe('workbench snapshot view model', () => {
  it('builds status, metrics, and next action from backend bootstrap data', () => {
    const snapshot = buildWorkbenchSnapshot({
      ready: false,
      status: 'needs_attention',
      overview: {
        run_count: 3,
        case_count: 2,
        summary: {
          blocked_count: 2,
          ready_count: 1,
        },
      },
      primary_actions: [
        {
          case_id: 'Holly',
          label: 'Fix references',
          severity: 'blocking',
          href: '/experiments/content-production/cases/Holly/next-actions',
        },
      ],
    });

    expect(snapshot).toEqual({
      ready: false,
      status: 'needs_attention',
      metrics: [
        { kind: 'runs', label: '3 runs' },
        { kind: 'cases', label: '2 cases' },
        { kind: 'blocked', label: '2 blocked' },
        { kind: 'ready', label: '1 ready' },
      ],
      action: {
        caseId: 'Holly',
        label: 'Fix references',
        severity: 'blocking',
        href: '/api/experiments/content-production/cases/Holly/next-actions',
      },
    });
  });

  it('returns null when bootstrap has no workbench health data', () => {
    expect(buildWorkbenchSnapshot({ source: 'mock', cases: [], links: {} })).toBeNull();
  });

  it('falls back to the first case primary action when primary_actions is absent', () => {
    const snapshot = buildWorkbenchSnapshot({
      cases: [
        {
          case_id: 'CaseA',
          primary_action: {
            action_id: 'draft_evaluation',
            severity: 'review',
          },
        },
      ],
    });

    expect(snapshot?.action).toEqual({
      caseId: 'CaseA',
      label: 'draft_evaluation',
      severity: 'review',
      href: undefined,
    });
  });
});
