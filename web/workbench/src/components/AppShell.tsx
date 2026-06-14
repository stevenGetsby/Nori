import { CircleDot, Eye, Menu, Play } from 'lucide-react';
import type { WorkbenchBootstrap, WorkbenchCase } from '../api/client';
import type { ViewId } from '../routes';
import type { WorkbenchAccountFrame } from '../workbenchAccount';
import { navigationItems } from '../workbenchModel';

export type BootstrapState =
  | { status: 'loading'; data?: undefined; error?: undefined }
  | { status: 'live' | 'mock'; data: WorkbenchBootstrap; error?: undefined }
  | { status: 'fallback'; data?: undefined; error: string };

export function Sidebar({
  accountFrame,
  activeView,
  cases,
  onCaseSelect,
  onNavigate,
}: {
  accountFrame: WorkbenchAccountFrame;
  activeView: ViewId;
  cases?: WorkbenchCase[];
  onCaseSelect?: (caseId: string) => void;
  onNavigate: (view: ViewId) => void;
}) {
  const caseRows = (cases || []).filter((caseRow) => text(caseRow.case_id));
  return (
    <aside className="sidebar" aria-label="Nori navigation">
      <div className="brand-lockup">
        <img src="/assets/nori-onion-logo.png" alt="" className="brand-mark" />
        <div>
          <div className="brand-name">Nori</div>
          <div className="brand-caption">creative OS</div>
        </div>
      </div>

      <nav className="nav-stack">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              className={activeView === item.id ? 'nav-item nav-item-active' : 'nav-item'}
              key={item.id}
              onClick={() => onNavigate(item.id as ViewId)}
              type="button"
            >
              <Icon size={17} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {caseRows.length > 1 && (
        <div className="case-switcher" aria-label="Case switcher">
          <div className="case-switcher-label">Cases</div>
          <div className="case-switcher-list">
            {caseRows.map((caseRow) => {
              const caseId = text(caseRow.case_id);
              const caseTitle = text(caseRow.case_title) || caseId;
              const active = accountFrame.caseId === caseId;
              return (
                <button
                  aria-pressed={active}
                  className={active ? 'case-switcher-item case-switcher-item-active' : 'case-switcher-item'}
                  key={caseId}
                  onClick={() => onCaseSelect?.(caseId)}
                  type="button"
                >
                  <span>{caseTitle}</span>
                  <small>{caseId}</small>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <div className="operator-card">
        <div className="operator-card-label">Active account</div>
        <div className="operator-card-title">{accountFrame.accountName}</div>
        <div className="operator-case-frame">
          <span>{accountFrame.caseId}</span>
          {accountFrame.latestRunId && <small>{accountFrame.latestRunId}</small>}
        </div>
        <p>Focus: {accountFrame.contextSummary}</p>
        {accountFrame.primaryActionLabel && <em>Next: {accountFrame.primaryActionLabel}</em>}
      </div>
    </aside>
  );
}

function text(value: unknown) {
  return typeof value === 'string' && value.trim() ? value.trim() : '';
}

export function TopBar({
  activeView,
  bootstrap,
  onNavigate,
}: {
  activeView: ViewId;
  bootstrap: BootstrapState;
  onNavigate: (view: ViewId) => void;
}) {
  const meta = {
    compose: ['Production frontend', 'Nori Content Workbench'],
    planning: ['Account first', 'Account Planning'],
    context: ['Account memory', 'Context Intelligence'],
    skills: ['Reusable agents', 'Skill Operating System'],
    library: ['Delivery layer', 'Artifact Store'],
  } satisfies Record<ViewId, [string, string]>;

  const focusActiveNavigationItem = () => {
    document.querySelector<HTMLButtonElement>('.mobile-nav-item-active')?.focus();
  };

  return (
    <>
      <header className="topbar">
        <button
          aria-controls="workspace-mobile-navigation"
          aria-label="Open navigation"
          className="icon-button topbar-menu"
          onClick={focusActiveNavigationItem}
          type="button"
        >
          <Menu size={18} />
        </button>
        <div>
          <p className="eyebrow">{meta[activeView][0]}</p>
          <h1>{meta[activeView][1]}</h1>
        </div>
        <div className="topbar-actions">
          <ConnectionBadge bootstrap={bootstrap} />
          <button className="ghost-button" onClick={() => onNavigate('library')} type="button">
            <Eye size={16} />
            Preview
          </button>
          <button className="primary-button" onClick={() => onNavigate('compose')} type="button">
            <Play size={16} />
            Run workflow
          </button>
        </div>
      </header>
      <nav className="mobile-nav" id="workspace-mobile-navigation" aria-label="Mobile workspace navigation">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              aria-label={`Go to ${item.label}`}
              className={activeView === item.id ? 'mobile-nav-item mobile-nav-item-active' : 'mobile-nav-item'}
              key={item.id}
              onClick={() => onNavigate(item.id as ViewId)}
              type="button"
            >
              <Icon size={16} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </>
  );
}

function ConnectionBadge({ bootstrap }: { bootstrap: BootstrapState }) {
  const label =
    bootstrap.status === 'live'
      ? 'Backend live'
      : bootstrap.status === 'mock'
        ? 'Mock bootstrap'
      : bootstrap.status === 'fallback'
        ? 'Local demo fallback'
        : 'Connecting backend';
  return (
    <span className={`connection-badge connection-${bootstrap.status}`} title={bootstrap.status === 'fallback' ? bootstrap.error : undefined}>
      <CircleDot size={13} />
      {label}
    </span>
  );
}
