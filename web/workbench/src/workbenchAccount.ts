import type { WorkbenchBootstrap, WorkbenchCase } from './api/client';

export type WorkbenchAccountFrame = {
  accountName: string;
  caseId: string;
  caseTitle: string;
  latestRunId?: string;
  contextSummary: string;
  primaryActionLabel?: string;
};

const fallbackFrame: WorkbenchAccountFrame = {
  accountName: '巷口暖胃小馆',
  caseId: 'Holly',
  caseTitle: '巷口暖胃小馆',
  latestRunId: 'mock_run_ready',
  contextSummary: '社区饭店账号，主打真实复吃、第一次点单和下班晚饭场景。',
};

export function buildWorkbenchAccountFrame(data?: WorkbenchBootstrap, activeCaseOverride?: string): WorkbenchAccountFrame {
  if (!data) return fallbackFrame;

  const firstCaseWithRun = data.cases?.find((caseRow) => text(caseRow.case_id) && text(caseRow.latest_run_id));
  const firstCase = data.cases?.find((caseRow) => text(caseRow.case_id));
  const requestedOverrideCaseId = text(activeCaseOverride);
  const overrideCaseId = requestedOverrideCaseId && findCase(data.cases, requestedOverrideCaseId) ? requestedOverrideCaseId : '';
  const activeCaseId =
    overrideCaseId ||
    text(data.context_layer?.active_case_id) ||
    text(data.case_id) ||
    text(firstCaseWithRun?.case_id) ||
    text(firstCase?.case_id) ||
    fallbackFrame.caseId;
  const activeCase = findCase(data.cases, activeCaseId) || firstCaseWithRun || firstCase;
  const caseTitle = text(activeCase?.case_title) || (overrideCaseId ? activeCaseId : text(data.overview?.active_account)) || activeCaseId;
  const accountName = overrideCaseId ? caseTitle : text(data.overview?.active_account) || caseTitle || fallbackFrame.accountName;
  const latestRunId =
    (overrideCaseId ? '' : text(data.context_layer?.active_run_id)) ||
    text(data.active_run_id) ||
    text(activeCase?.latest_run_id) ||
    undefined;
  const primaryActionLabel = text(activeCase?.primary_action?.label) || text(data.primary_actions?.[0]?.label) || undefined;
  const contextSummary =
    (overrideCaseId ? '' : text(data.context_layer?.summary)) ||
    text(activeCase?.primary_action?.message) ||
    text(data.primary_actions?.[0]?.message) ||
    fallbackFrame.contextSummary;

  return {
    accountName,
    caseId: activeCaseId,
    caseTitle,
    latestRunId,
    contextSummary,
    primaryActionLabel,
  };
}

function findCase(cases: WorkbenchCase[] | undefined, caseId: string) {
  return cases?.find((caseRow) => text(caseRow.case_id) === caseId);
}

function text(value: unknown) {
  return typeof value === 'string' && value.trim() ? value.trim() : '';
}
