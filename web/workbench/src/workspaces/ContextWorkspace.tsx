import { Activity, BadgeCheck, FileSearch, Layers3 } from 'lucide-react';
import type { WorkbenchBootstrap, WorkbenchContextSlice } from '../api/client';
import type { BootstrapState } from '../components/AppShell';
import { PageLead, PanelHeader } from '../components/common';
import type { WorkbenchAccountFrame } from '../workbenchAccount';
import { contentPlan, insightItems } from '../workbenchModel';

type ContextViewModel = {
  activeAccount: string;
  status: string;
  contextPackId: string;
  activeCaseId: string;
  activeRunId: string;
  summary: string;
  sourceRefs: string[];
  slices: WorkbenchContextSlice[];
  metricLabels: string[];
};

export function ContextWorkspace({
  accountFrame,
  bootstrap,
}: {
  accountFrame: WorkbenchAccountFrame;
  bootstrap: BootstrapState;
}) {
  const contextView = buildContextView(bootstrap, accountFrame);
  return (
    <section className="detail-workspace context-detail" aria-label="Context intelligence workspace">
      <PageLead
        kicker="Account planning first"
        title="先理解账号，再生成内容。"
        body="正式版把 demo 里的 IP 模式、账号定位、内容日历和热点洞察合并成 Context layer。它不是装饰信息，而是每一次 Design Spec 和 Generation Agent 的输入。"
      />
      <BackendContextPanel contextView={contextView} />
      <div className="detail-grid">
        <section className="panel memory-panel">
          <PanelHeader kicker="Account Memory" title={contextView.activeAccount} />
          <div className="memory-hero">
            <img src="/assets/insight-avatar-reference.png" alt="" />
            <div>
              <span>IP mode unlocked</span>
              <h3>附近人真实复吃的社区饭店账号</h3>
              <p>定位不追泛流量，优先解释第一次怎么点、什么时候来舒服、哪道菜适合谁。</p>
            </div>
          </div>
          <div className="memory-tags">
            {['真实到店', '菜单不踩雷', '下班晚饭', '附近人', '先结论后理由'].map((tag) => (
              <span key={tag}>{tag}</span>
            ))}
          </div>
        </section>

        <section className="panel signal-panel">
          <PanelHeader kicker="Strategy Inputs" title="Context sources" />
          <div className="source-list">
            {insightItems.map((item) => {
              const Icon = item.icon;
              return (
                <article className="source-row" key={item.title}>
                  <Icon size={18} />
                  <div>
                    <strong>{item.title}</strong>
                    <p>{item.description}</p>
                  </div>
                  <span>{item.value}</span>
                </article>
              );
            })}
          </div>
        </section>

        <section className="panel calendar-panel-wide">
          <PanelHeader kicker="Operating Calendar" title="持续运营日历" />
          <div className="calendar-board">
            {contentPlan.map((item) => (
              <article className="calendar-ticket" key={item.day}>
                <span>{item.day}</span>
                <strong>{item.topic}</strong>
                <p>{item.format}</p>
                <small>{item.owner}</small>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

function BackendContextPanel({ contextView }: { contextView: ContextViewModel }) {
  return (
    <section className="panel context-runtime-panel">
      <PanelHeader
        kicker="Runtime context"
        title="Backend context layer"
        action={<span className="context-status-pill">{contextView.status}</span>}
      />
      <div className="context-runtime-layout">
        <article className="context-pack-card">
          <div className="context-pack-icon">
            <Layers3 size={18} />
          </div>
          <span>Context Pack</span>
          <h2>{contextView.contextPackId}</h2>
          <p>{contextView.summary}</p>
          <div className="context-pack-meta">
            <strong>{contextView.activeCaseId}{contextView.activeRunId ? ` / ${contextView.activeRunId}` : ''}</strong>
            {contextView.metricLabels.map((label) => (
              <small key={label}>{label}</small>
            ))}
          </div>
        </article>

        <div className="context-slice-list" aria-label="Backend context slices">
          {contextView.slices.map((slice) => (
            <article className="context-slice-card" key={slice.kind || slice.title}>
              <span>{slice.kind || 'context_slice'}</span>
              <strong>{slice.title || slice.kind || 'Context slice'}</strong>
              {slice.summary && <p>{slice.summary}</p>}
              {slice.signal && <em>{slice.signal}</em>}
            </article>
          ))}
        </div>

        <div className="context-source-card" aria-label="Context source references">
          <FileSearch size={17} />
          <span>Source refs</span>
          <div>
            {contextView.sourceRefs.map((ref) => (
              <code key={ref}>{ref}</code>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function buildContextView(bootstrap: BootstrapState, accountFrame: WorkbenchAccountFrame): ContextViewModel {
  if (bootstrap.status === 'live' || bootstrap.status === 'mock') {
    return contextViewFromBootstrap(bootstrap.data, accountFrame);
  }

  return {
    activeAccount: accountFrame.accountName,
    status: bootstrap.status === 'fallback' ? 'local_fallback' : 'loading',
    contextPackId: bootstrap.status === 'fallback' ? 'ctx_local_fallback' : 'ctx_loading',
    activeCaseId: accountFrame.caseId,
    activeRunId: accountFrame.latestRunId || '',
    summary: bootstrap.status === 'fallback' ? bootstrap.error : accountFrame.contextSummary,
    sourceRefs: ['local workbench model'],
    slices: fallbackSlices(),
    metricLabels: ['static memory'],
  };
}

function contextViewFromBootstrap(data: WorkbenchBootstrap, accountFrame: WorkbenchAccountFrame): ContextViewModel {
  const layer = data.context_layer || {};
  const overview = data.overview || {};
  const summary = overview.summary || {};
  const activeAccount = accountFrame.accountName;
  const activeCaseId = accountFrame.caseId;
  const activeRunId = accountFrame.latestRunId || '';
  const metricLabels = [
    metricLabel(overview.run_count, 'runs'),
    metricLabel(overview.case_count, 'cases'),
    metricLabel(summary.ready_count, 'ready'),
    metricLabel(summary.blocked_count, 'blocked'),
  ].filter((label): label is string => Boolean(label));

  return {
    activeAccount,
    status: String(layer.status || data.status || (data.ready === false ? 'needs_attention' : 'ready')),
    contextPackId: String(layer.context_pack_id || `ctx_${activeCaseId || 'workspace'}`),
    activeCaseId,
    activeRunId,
    summary: String(layer.summary || accountFrame.contextSummary || 'Backend snapshot is shaping the context used by Design Spec and generation.'),
    sourceRefs: sourceRefsFromBootstrap(data),
    slices: layer.slices?.length ? layer.slices : fallbackSlices(),
    metricLabels,
  };
}

function sourceRefsFromBootstrap(data: WorkbenchBootstrap) {
  const layerRefs = data.context_layer?.source_refs || [];
  if (layerRefs.length > 0) return layerRefs;

  const links = data.links || {};
  return [
    links.overview || '/experiments/content-production/overview',
    links.run_template || '/experiments/content-production/run-template',
    links.runs || '/workflows/content-production/runs',
  ].filter(Boolean);
}

function fallbackSlices(): WorkbenchContextSlice[] {
  return insightItems.map((item) => ({
    kind: item.title === '平台策略' ? 'platform_strategy' : item.title === '热点机会' ? 'market_hotspots' : item.title === '素材可用性' ? 'asset_context' : 'acceptance',
    title: item.title,
    summary: item.description,
    signal: item.value,
  }));
}

function metricLabel(value: unknown, label: string) {
  return typeof value === 'number' ? `${value} ${label}` : '';
}
