export type RunQueueFilter = 'all' | 'needs_review' | 'accepted' | 'blocked';

export const runQueueFilters: Array<{ id: RunQueueFilter; label: string }> = [
  { id: 'all', label: 'All' },
  { id: 'needs_review', label: 'Needs review' },
  { id: 'accepted', label: 'Accepted' },
  { id: 'blocked', label: 'Blocked' },
];

export function normalizeRunQueueFilter(value: string | null | undefined): RunQueueFilter {
  return runQueueFilters.some((filter) => filter.id === value) ? (value as RunQueueFilter) : 'all';
}
