export type WorkbenchReviewTarget = {
  caseId: string;
  runId: string;
  source: 'generated' | 'backend' | 'mock';
};
