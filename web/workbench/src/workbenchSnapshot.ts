import type { WorkbenchAction, WorkbenchBootstrap } from './api/client';

export type SnapshotMetricKind = 'runs' | 'cases' | 'blocked' | 'ready';

export type SnapshotMetric = {
  kind: SnapshotMetricKind;
  label: string;
};

export type SnapshotAction = {
  caseId: string;
  label: string;
  severity: string;
  href?: string;
};

export type WorkbenchSnapshotView = {
  ready: boolean;
  status: string;
  metrics: SnapshotMetric[];
  action?: SnapshotAction;
};

export function buildWorkbenchSnapshot(data: WorkbenchBootstrap): WorkbenchSnapshotView | null {
  const overview = data.overview;
  const summary = overview?.summary;
  const metrics = [
    numberMetric(overview?.run_count, 'runs'),
    numberMetric(overview?.case_count, 'cases'),
    numberMetric(summary?.blocked_count, 'blocked'),
    numberMetric(summary?.ready_count, 'ready'),
  ].filter((metric): metric is SnapshotMetric => Boolean(metric));
  const actionSource = data.primary_actions?.[0]
    ? { action: data.primary_actions[0], fallbackCaseId: '' }
    : firstCaseAction(data);
  const action = actionSource ? normalizeAction(actionSource.action, actionSource.fallbackCaseId) : undefined;
  const status = data.status || (data.ready === false ? 'needs_attention' : 'ready');

  if (!data.status && metrics.length === 0 && !action) return null;

  return {
    ready: data.ready !== false,
    status,
    metrics,
    action,
  };
}

function numberMetric(value: number | undefined, kind: SnapshotMetricKind): SnapshotMetric | null {
  return typeof value === 'number' ? { kind, label: `${value} ${kind}` } : null;
}

function firstCaseAction(data: WorkbenchBootstrap) {
  const row = data.cases?.find((caseRow) => caseRow.primary_action);
  return row?.primary_action ? { action: row.primary_action, fallbackCaseId: row.case_id || '' } : undefined;
}

function normalizeAction(action: WorkbenchAction, fallbackCaseId: string): SnapshotAction {
  return {
    caseId: action.case_id || fallbackCaseId || 'all cases',
    label: action.label || action.action_id || 'Next action',
    severity: action.severity || 'next_step',
    href: action.href ? apiHref(action.href) : undefined,
  };
}

function apiHref(href: string) {
  return href.startsWith('/api/') || !href.startsWith('/') ? href : `/api${href}`;
}
