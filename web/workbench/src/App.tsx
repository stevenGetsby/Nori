import { useEffect, useMemo, useState } from 'react';
import { getWorkbenchBootstrap } from './api/client';
import { Sidebar, TopBar, type BootstrapState } from './components/AppShell';
import { WorkbenchSnapshot } from './components/WorkbenchSnapshot';
import {
  activeCaseFromHash,
  hashForReviewTarget,
  libraryFilterFromHash,
  reviewTargetFromHash,
  viewFromHash,
  type ViewId,
} from './routes';
import { buildWorkbenchAccountFrame } from './workbenchAccount';
import type { RunQueueFilter } from './workbenchLibraryRoute';
import type { WorkbenchReviewTarget } from './workbenchReviewTarget';
import { ComposeWorkspace } from './workspaces/ComposeWorkspace';
import { ContextWorkspace } from './workspaces/ContextWorkspace';
import { LibraryWorkspace } from './workspaces/LibraryWorkspace';
import { PlanningWorkspace } from './workspaces/PlanningWorkspace';
import { SkillsWorkspace } from './workspaces/SkillsWorkspace';

export function App({ fetcher, bootstrapPath }: { fetcher?: typeof fetch; bootstrapPath?: string }) {
  const [activeView, setActiveView] = useState<ViewId>(() => viewFromHash(window.location.hash));
  const [bootstrap, setBootstrap] = useState<BootstrapState>({ status: 'loading' });
  const [reviewTarget, setReviewTarget] = useState<WorkbenchReviewTarget | undefined>(() => reviewTargetFromHash(window.location.hash));
  const [libraryFilter, setLibraryFilter] = useState<RunQueueFilter>(() => libraryFilterFromHash(window.location.hash));
  const [activeCaseId, setActiveCaseId] = useState<string | undefined>(() => activeCaseFromHash(window.location.hash));
  const accountFrame = useMemo(
    () => buildWorkbenchAccountFrame(bootstrap.status === 'live' || bootstrap.status === 'mock' ? bootstrap.data : undefined, activeCaseId),
    [bootstrap, activeCaseId],
  );
  const cases = bootstrap.status === 'live' || bootstrap.status === 'mock' ? bootstrap.data.cases || [] : [];

  const libraryHash = (target: WorkbenchReviewTarget | undefined = reviewTarget, filter: RunQueueFilter = libraryFilter) => {
    if (target) return hashForReviewTarget(target, filter);
    const params = new URLSearchParams();
    if (activeCaseId) params.set('case_id', activeCaseId);
    if (filter !== 'all') params.set('filter', filter);
    const query = params.toString();
    return query ? `#library?${query}` : '#library';
  };

  const workspaceHash = (view: ViewId, caseId = activeCaseId) => {
    if (view === 'library') return libraryHash();
    if (!caseId) return `#${view}`;
    return `#${view}?case_id=${encodeURIComponent(caseId)}`;
  };

  const setActiveReviewTarget = (target: WorkbenchReviewTarget) => {
    setReviewTarget(target);
    if (activeView === 'library') {
      const nextHash = hashForReviewTarget(target, libraryFilter);
      if (window.location.hash !== nextHash) {
        window.history.pushState(null, '', nextHash);
      }
    }
  };

  const setActiveLibraryFilter = (filter: RunQueueFilter, target?: WorkbenchReviewTarget) => {
    const nextTarget = target || reviewTarget;
    setLibraryFilter(filter);
    if (target) {
      setReviewTarget(target);
    }
    if (activeView === 'library') {
      const nextHash = libraryHash(nextTarget, filter);
      if (window.location.hash !== nextHash) {
        window.history.pushState(null, '', nextHash);
      }
    }
  };

  const navigate = (view: ViewId) => {
    setActiveView(view);
    const nextHash = workspaceHash(view);
    if (window.location.hash !== nextHash) {
      window.history.pushState(null, '', nextHash);
    }
  };

  const selectCase = (caseId: string) => {
    setActiveCaseId(caseId);
    setReviewTarget(undefined);
    const nextHash = activeView === 'library'
      ? `#library?case_id=${encodeURIComponent(caseId)}${libraryFilter === 'all' ? '' : `&filter=${encodeURIComponent(libraryFilter)}`}`
      : workspaceHash(activeView, caseId);
    if (window.location.hash !== nextHash) {
      window.history.pushState(null, '', nextHash);
    }
  };

  useEffect(() => {
    const syncFromHash = () => {
      setActiveView(viewFromHash(window.location.hash));
      setActiveCaseId(activeCaseFromHash(window.location.hash));
      const nextReviewTarget = reviewTargetFromHash(window.location.hash);
      if (nextReviewTarget) setReviewTarget(nextReviewTarget);
      setLibraryFilter(libraryFilterFromHash(window.location.hash));
    };
    window.addEventListener('hashchange', syncFromHash);
    return () => window.removeEventListener('hashchange', syncFromHash);
  }, []);

  useEffect(() => {
    let cancelled = false;
    getWorkbenchBootstrap(fetcher, bootstrapPath)
      .then((data) => {
        if (!cancelled) setBootstrap({ status: data.source === 'mock' ? 'mock' : 'live', data });
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setBootstrap({
            status: 'fallback',
            error: error instanceof Error ? error.message : 'Backend bootstrap failed',
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [fetcher, bootstrapPath]);

  return (
    <div className="app-shell">
      <Sidebar accountFrame={accountFrame} activeView={activeView} cases={cases} onCaseSelect={selectCase} onNavigate={navigate} />
      <main className="workbench">
        <TopBar activeView={activeView} bootstrap={bootstrap} onNavigate={navigate} />
        <WorkbenchSnapshot bootstrap={bootstrap} />
        {activeView === 'compose' && (
          <ComposeWorkspace
            accountFrame={accountFrame}
            fetcher={fetcher}
            onOpenLibrary={() => navigate('library')}
            onReviewTargetReady={setActiveReviewTarget}
          />
        )}
        {activeView === 'planning' && <PlanningWorkspace accountFrame={accountFrame} bootstrap={bootstrap} />}
        {activeView === 'context' && <ContextWorkspace accountFrame={accountFrame} bootstrap={bootstrap} />}
        {activeView === 'skills' && <SkillsWorkspace fetcher={fetcher} />}
        {activeView === 'library' && (
          <LibraryWorkspace
            accountFrame={accountFrame}
            bootstrap={bootstrap}
            fetcher={fetcher}
            reviewTarget={reviewTarget}
            runQueueFilter={libraryFilter}
            onRunQueueFilterChange={setActiveLibraryFilter}
            onReviewTargetChange={setActiveReviewTarget}
          />
        )}
      </main>
    </div>
  );
}
