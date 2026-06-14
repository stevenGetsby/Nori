import type { WorkbenchReviewTarget } from './workbenchReviewTarget';
import { normalizeRunQueueFilter, type RunQueueFilter } from './workbenchLibraryRoute';

export type ViewId = 'compose' | 'planning' | 'context' | 'skills' | 'library';

export const viewIds: ViewId[] = ['compose', 'planning', 'context', 'skills', 'library'];

export function viewFromHash(hash: string): ViewId {
  const candidate = hash.replace(/^#/, '').split('?')[0];
  return viewIds.includes(candidate as ViewId) ? (candidate as ViewId) : 'compose';
}

export function activeCaseFromHash(hash: string): string | undefined {
  const query = hash.replace(/^#/, '').split('?')[1] || '';
  const params = new URLSearchParams(query);
  return params.get('case_id') || params.get('case') || undefined;
}

export function reviewTargetFromHash(hash: string): WorkbenchReviewTarget | undefined {
  if (viewFromHash(hash) !== 'library') return undefined;

  const query = hash.replace(/^#/, '').split('?')[1] || '';
  const params = new URLSearchParams(query);
  const caseId = activeCaseFromHash(hash);
  const runId = params.get('run_id') || params.get('run');
  if (!caseId || !runId) return undefined;

  return {
    caseId,
    runId,
    source: 'backend',
  };
}

export function libraryFilterFromHash(hash: string): RunQueueFilter {
  if (viewFromHash(hash) !== 'library') return 'all';

  const query = hash.replace(/^#/, '').split('?')[1] || '';
  const params = new URLSearchParams(query);
  return normalizeRunQueueFilter(params.get('filter'));
}

export function hashForReviewTarget(target: WorkbenchReviewTarget, filter: RunQueueFilter = 'all') {
  const params = new URLSearchParams({
    case_id: target.caseId,
    run_id: target.runId,
  });
  if (filter !== 'all') {
    params.set('filter', filter);
  }
  return `#library?${params.toString()}`;
}
