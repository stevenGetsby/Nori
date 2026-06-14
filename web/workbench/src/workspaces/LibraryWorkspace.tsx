import { useCallback, useEffect, useMemo, useState } from 'react';
import { ChevronRight, Download, FileSearch } from 'lucide-react';
import {
  inspectRunArtifacts,
  listContentProductionRuns,
  type ContentProductionRunList,
  type ContentProductionRunRow,
} from '../api/client';
import type { BootstrapState } from '../components/AppShell';
import { ArtifactInspectionPreview, type ArtifactInspectionState } from '../components/ArtifactInspectionPreview';
import { PageLead, PanelHeader } from '../components/common';
import type { WorkbenchAccountFrame } from '../workbenchAccount';
import { runQueueFilters, type RunQueueFilter } from '../workbenchLibraryRoute';
import type { WorkbenchReviewTarget } from '../workbenchReviewTarget';
import { artifactPreviews, demoCapabilityMap } from '../workbenchModel';

type ActiveRun = {
  caseId: string;
  runId: string;
  source: WorkbenchReviewTarget['source'];
};

type RunListState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready'; data: ContentProductionRunList }
  | { status: 'error'; message: string };

export function LibraryWorkspace({
  accountFrame,
  bootstrap,
  fetcher,
  onReviewTargetChange,
  onRunQueueFilterChange,
  reviewTarget,
  runQueueFilter,
}: {
  accountFrame: WorkbenchAccountFrame;
  bootstrap: BootstrapState;
  fetcher?: typeof fetch;
  onReviewTargetChange?: (target: WorkbenchReviewTarget) => void;
  onRunQueueFilterChange?: (filter: RunQueueFilter, target?: WorkbenchReviewTarget) => void;
  reviewTarget?: WorkbenchReviewTarget;
  runQueueFilter: RunQueueFilter;
}) {
  const initialRun = useMemo(() => resolveActiveRun(bootstrap, accountFrame, reviewTarget), [bootstrap, accountFrame, reviewTarget]);
  const [selectedRun, setSelectedRun] = useState<ActiveRun>(initialRun);
  const [runListState, setRunListState] = useState<RunListState>({ status: 'idle' });
  const [inspectionState, setInspectionState] = useState<ArtifactInspectionState>({ status: 'idle' });
  const exportHref = resolveExportHref(selectedRun, inspectionState);

  const refreshInspection = useCallback(async () => {
    setInspectionState({ status: 'loading' });
    try {
      const data = await inspectRunArtifacts(selectedRun.caseId, selectedRun.runId, fetcher);
      setInspectionState({ status: 'ready', data });
    } catch (error: unknown) {
      setInspectionState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Backend artifact inspection request failed',
      });
    }
  }, [fetcher, selectedRun.caseId, selectedRun.runId]);

  useEffect(() => {
    setSelectedRun(initialRun);
  }, [initialRun]);

  useEffect(() => {
    let cancelled = false;

    setRunListState({ status: 'loading' });
    listContentProductionRuns(
      {
        case_id: initialRun.caseId,
        acceptance_status: runQueueFilter === 'all' ? undefined : runQueueFilter,
        limit: 12,
      },
      fetcher,
    )
      .then((data) => {
        if (!cancelled) setRunListState({ status: 'ready', data });
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setRunListState({
            status: 'error',
            message: error instanceof Error ? error.message : 'Backend run history request failed',
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [initialRun.caseId, runQueueFilter, fetcher]);

  useEffect(() => {
    let cancelled = false;

    setInspectionState({ status: 'loading' });
    inspectRunArtifacts(selectedRun.caseId, selectedRun.runId, fetcher)
      .then((data) => {
        if (!cancelled) setInspectionState({ status: 'ready', data });
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setInspectionState({
            status: 'error',
            message: error instanceof Error ? error.message : 'Backend artifact inspection request failed',
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedRun, fetcher]);

  return (
    <section className="detail-workspace" aria-label="Artifact store workspace">
      <PageLead
        kicker="Artifact Store"
        title="Artifact Store"
        body="内容库不只是作品墙，而是可验收、可追溯、可导出的交付层。每个 ContentPackage 都保留 brief、spec、素材引用、封面、正文、标签和审查记录。"
      />
      <section className="panel library-review-panel">
        <PanelHeader
          kicker="Review package"
          title="Latest reviewed package"
          action={
            <div className="library-review-actions">
              <button className="tiny-button dark" disabled={inspectionState.status === 'loading'} onClick={refreshInspection} type="button">
                <FileSearch size={13} />
                Inspect
              </button>
              <a className="tiny-button" href={exportHref}>
                <Download size={13} />
                Export
              </a>
            </div>
          }
        />
        <div className="library-review-summary">
          <div>
            <span>{selectedRun.source === 'generated' ? 'generated run' : selectedRun.source === 'backend' ? 'backend run' : 'local fixture'}</span>
            <strong>{selectedRun.caseId} / {selectedRun.runId}</strong>
          </div>
          <p>产物库默认展示当前 case 的最近一次可审查 run；没有后端数据时使用本地 fixture 保持界面可验收。</p>
        </div>
        <ArtifactInspectionPreview state={inspectionState} title="Latest reviewed package" />
      </section>
      <RunHistoryPanel
        filter={runQueueFilter}
        selectedRun={selectedRun}
        state={runListState}
        onFilterChange={(filter) => onRunQueueFilterChange?.(filter, selectedRun)}
        onSelect={(run) => {
          if (!run.case_id || !run.run_id) return;
          const nextRun = {
            caseId: String(run.case_id),
            runId: String(run.run_id),
            source: 'backend',
          } satisfies ActiveRun;
          setSelectedRun(nextRun);
          onReviewTargetChange?.(nextRun);
        }}
      />
      <div className="artifact-store-grid">
        {artifactPreviews.map((artifact) => (
          <article className="store-card" key={artifact.title}>
            <img src={artifact.image} alt="" />
            <div>
              <span>{artifact.type}</span>
              <h2>{artifact.title}</h2>
              <p>{artifact.metric}</p>
              <small>{artifact.status}</small>
            </div>
          </article>
        ))}
      </div>
      <section className="panel handoff-panel">
        <PanelHeader kicker="Handoff" title="交付包结构" />
        <div className="handoff-list">
          {demoCapabilityMap.map((item) => (
            <div className="handoff-row" key={item.demoSurface}>
              <span>{item.demoSurface}</span>
              <ChevronRight size={15} />
              <strong>{item.productionSurface}</strong>
              <p>{item.improvement}</p>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}

function RunHistoryPanel({
  filter,
  selectedRun,
  state,
  onFilterChange,
  onSelect,
}: {
  filter: RunQueueFilter;
  selectedRun: ActiveRun;
  state: RunListState;
  onFilterChange: (filter: RunQueueFilter) => void;
  onSelect: (run: ContentProductionRunRow) => void;
}) {
  const action = <RunHistoryFilters activeFilter={filter} onChange={onFilterChange} />;

  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <section className="panel run-history-panel">
        <PanelHeader kicker="Review queue" title="Run history" action={action} />
        <div className="run-history-empty">Loading run history</div>
      </section>
    );
  }

  if (state.status === 'error') {
    return (
      <section className="panel run-history-panel">
        <PanelHeader kicker="Review queue" title="Run history" action={action} />
        <div className="run-history-empty">{state.message}</div>
      </section>
    );
  }

  const runs = filterRunRows(state.data.runs || [], filter);
  return (
    <section className="panel run-history-panel">
      <PanelHeader
        kicker="Review queue"
        title="Run history"
        action={
          <div className="run-history-toolbar">
            {action}
            <span className="run-history-count">{runs.length} shown</span>
          </div>
        }
      />
      {runs.length === 0 ? (
        <div className="run-history-empty">No indexed runs for this case yet.</div>
      ) : (
        <div className="run-history-list" aria-label="Content production run history">
          {runs.map((run) => {
            const active = selectedRun.caseId === run.case_id && selectedRun.runId === run.run_id;
            return (
              <button
                className={active ? 'run-history-row run-history-row-active' : 'run-history-row'}
                key={`${run.case_id || 'case'}-${run.run_id}`}
                onClick={() => onSelect(run)}
                type="button"
              >
                <div>
                  <span>{run.case_id || selectedRun.caseId}</span>
                  <strong>{run.run_id}</strong>
                  <small>{run.created_at || run.finished_at || 'indexed run'}</small>
                </div>
                <div className="run-history-metrics">
                  <small>{run.acceptance_status || 'unreviewed'}</small>
                  <small>{Number(run.artifact_count || 0)} artifacts</small>
                  {run.evaluation_score !== undefined && <small>{run.evaluation_score} score</small>}
                </div>
              </button>
            );
          })}
        </div>
      )}
    </section>
  );
}

function filterRunRows(runs: ContentProductionRunRow[], filter: RunQueueFilter) {
  if (filter === 'all') return runs;
  return runs.filter((run) => run.acceptance_status === filter);
}

function RunHistoryFilters({
  activeFilter,
  onChange,
}: {
  activeFilter: RunQueueFilter;
  onChange: (filter: RunQueueFilter) => void;
}) {
  return (
    <div className="run-history-filters" aria-label="Run history filters">
      {runQueueFilters.map((filter) => (
        <button
          aria-pressed={activeFilter === filter.id}
          className={activeFilter === filter.id ? 'run-history-filter run-history-filter-active' : 'run-history-filter'}
          key={filter.id}
          onClick={() => onChange(filter.id)}
          type="button"
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}

function resolveExportHref(selectedRun: ActiveRun, inspectionState: ArtifactInspectionState) {
  const exportLink = inspectionState.status === 'ready' ? inspectionState.data.links?.export : undefined;
  if (exportLink) return apiHref(exportLink);

  return `/api/workflows/content-production/runs/${encodeURIComponent(selectedRun.caseId)}/${encodeURIComponent(selectedRun.runId)}/export`;
}

function apiHref(href: string) {
  return href.startsWith('/api/') || !href.startsWith('/') ? href : `/api${href}`;
}

function resolveActiveRun(
  bootstrap: BootstrapState,
  accountFrame: WorkbenchAccountFrame,
  reviewTarget?: WorkbenchReviewTarget,
): ActiveRun {
  if (reviewTarget?.caseId && reviewTarget.runId) {
    return {
      caseId: reviewTarget.caseId,
      runId: reviewTarget.runId,
      source: reviewTarget.source,
    };
  }

  if (accountFrame.caseId && accountFrame.latestRunId) {
    return {
      caseId: accountFrame.caseId,
      runId: accountFrame.latestRunId,
      source: bootstrap.status === 'live' || bootstrap.status === 'mock' ? 'backend' : 'mock',
    };
  }

  if ((bootstrap.status === 'live' || bootstrap.status === 'mock') && bootstrap.data?.cases?.length) {
    const caseWithRun = bootstrap.data.cases.find((item) => item.case_id === accountFrame.caseId && item.latest_run_id) ||
      bootstrap.data.cases.find((item) => item.case_id && item.latest_run_id);
    if (caseWithRun?.case_id && caseWithRun.latest_run_id) {
      return {
        caseId: String(caseWithRun.case_id),
        runId: String(caseWithRun.latest_run_id),
        source: 'backend',
      };
    }
  }

  return {
    caseId: 'Holly',
    runId: 'mock_run_ready',
    source: 'mock',
  };
}
