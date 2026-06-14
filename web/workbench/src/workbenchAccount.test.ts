import { describe, expect, it } from 'vitest';
import { buildWorkbenchAccountFrame } from './workbenchAccount';

describe('workbench account frame', () => {
  it('uses an explicit active case over the backend default case', () => {
    expect(
      buildWorkbenchAccountFrame(
        {
          overview: {
            active_account: 'Portfolio',
          },
          context_layer: {
            active_case_id: 'Holly',
            active_run_id: 'run_holly_latest',
            summary: 'Backend default case memory.',
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
        },
        'BeanLab',
      ),
    ).toEqual({
      accountName: 'Bean Lab Studio',
      caseId: 'BeanLab',
      caseTitle: 'Bean Lab Studio',
      latestRunId: 'run_bean_latest',
      contextSummary: 'BeanLab active content is ready for review.',
      primaryActionLabel: 'Publish espresso launch',
    });
  });

  it('ignores an explicit active case that is not present in backend cases', () => {
    expect(
      buildWorkbenchAccountFrame(
        {
          context_layer: {
            active_case_id: 'Holly',
            active_run_id: 'run_holly_latest',
            summary: 'Holly context is ready.',
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
          ],
        },
        'GhostCase',
      ),
    ).toMatchObject({
      accountName: 'Holly Cafe',
      caseId: 'Holly',
      latestRunId: 'run_holly_latest',
      contextSummary: 'Holly context is ready.',
    });
  });
});
