import { describe, expect, it } from 'vitest';
import { activeCaseFromHash, hashForReviewTarget, libraryFilterFromHash, reviewTargetFromHash, viewFromHash } from './routes';

describe('workbench hash routes', () => {
  it('reads the workspace id before query parameters', () => {
    expect(viewFromHash('#library?case_id=Holly&run_id=run_deep')).toBe('library');
  });

  it('extracts the active case from any workspace route', () => {
    expect(activeCaseFromHash('#planning?case_id=BeanLab')).toBe('BeanLab');
    expect(activeCaseFromHash('#compose?case=Holly')).toBe('Holly');
  });

  it('extracts a review target from an Artifact Store deep link', () => {
    expect(reviewTargetFromHash('#library?case_id=Holly&run_id=run_deep')).toEqual({
      caseId: 'Holly',
      runId: 'run_deep',
      source: 'backend',
    });
  });

  it('extracts the Artifact Store queue filter from a deep link', () => {
    expect(libraryFilterFromHash('#library?case_id=Holly&run_id=run_deep&filter=needs_review')).toBe('needs_review');
  });

  it('falls back to all when an Artifact Store queue filter is unknown', () => {
    expect(libraryFilterFromHash('#library?case_id=Holly&run_id=run_deep&filter=archived')).toBe('all');
  });

  it('keeps the Artifact Store queue filter when building a review target hash', () => {
    expect(hashForReviewTarget({ caseId: 'Holly', runId: 'run_deep', source: 'backend' }, 'blocked')).toBe(
      '#library?case_id=Holly&run_id=run_deep&filter=blocked',
    );
  });
});
