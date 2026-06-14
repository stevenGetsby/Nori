import { Activity, AlertTriangle, CheckCircle2, Database, Target } from 'lucide-react';
import type { WorkbenchBootstrap, WorkbenchCase } from '../api/client';
import type { BootstrapState } from '../components/AppShell';
import { PageLead, PanelHeader } from '../components/common';
import type { WorkbenchAccountFrame } from '../workbenchAccount';
import { accountPlanningSections } from '../workbenchModel';

type PlanningRuntimeView = {
  activeAccount: string;
  status: string;
  metrics: string[];
  cases: PlanningCaseView[];
};

type PlanningCaseView = {
  caseId: string;
  runId: string;
  status: string;
  runCount: number;
  actionLabel: string;
  actionMessage: string;
  severity: string;
};

export function PlanningWorkspace({
  accountFrame,
  bootstrap,
}: {
  accountFrame: WorkbenchAccountFrame;
  bootstrap: BootstrapState;
}) {
  const runtime = buildPlanningRuntime(bootstrap, accountFrame);
  return (
    <section className="detail-workspace planning-workspace" aria-label="Account planning workspace">
      <PageLead
        kicker="Before content generation"
        title="Account Planning"
        body="Nori 正式版保留 demo 最关键的产品判断：先把账号定位、运营计划和内容日历生成出来，再进入具体内容制作。这样每一次生成都继承账号记忆，而不是从一条 prompt 重新开始。"
      />
      <PlanningRuntimePanel runtime={runtime} />
      <div className="planning-grid">
        <section className="panel planning-intake-panel">
          <PanelHeader kicker="Planning Intake" title={`输入账号资料：${runtime.activeAccount}`} />
          <div className="planning-dropzone">
            <img src="/assets/nori-pixel-companion.png" alt="" />
            <div>
              <strong>上传门店素材、菜单、评论和过往内容</strong>
              <p>正式版会把这些资料沉淀成 Context Pack，并在后续 brief/spec/generation 中持续引用。</p>
            </div>
          </div>
          <div className="planning-input-grid">
            {['目标平台：小红书 / 公众号', '账号目标：附近人复吃', '约束：真实、不夸张、不泛流量'].map((item) => (
              <span key={item}>{item}</span>
            ))}
          </div>
        </section>

        <section className="panel planning-output-panel">
          <PanelHeader kicker="Generated Plan" title="规划结果" />
          <div className="planning-section-list">
            {accountPlanningSections.map((section) => (
              <article className="planning-section-card" key={section.title}>
                <span>{section.label}</span>
                <h2>{section.title}</h2>
                <p>{section.body}</p>
                <div>
                  {section.evidence.map((item) => (
                    <small key={item}>{item}</small>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

function PlanningRuntimePanel({ runtime }: { runtime: PlanningRuntimeView }) {
  return (
    <section className="panel planning-runtime-panel">
      <PanelHeader
        kicker="Account runtime"
        title="Backend account plan"
        action={<span className="planning-status-pill">{runtime.status}</span>}
      />
      <div className="planning-runtime-layout">
        <article className="planning-account-card">
          <div className="planning-account-icon">
            <Target size={18} />
          </div>
          <span>Active account</span>
          <h2>{runtime.activeAccount}</h2>
          <p>账号规划不是一次性文档，而是所有 case、context pack、spec 和 artifact run 的共同约束。</p>
          <div className="planning-runtime-metrics" aria-label="Planning runtime metrics">
            {runtime.metrics.map((metric, index) => {
              const Icon = index === 0 ? Activity : index === 1 ? Database : index === 2 ? AlertTriangle : CheckCircle2;
              return (
                <small key={metric}>
                  <Icon size={13} />
                  {metric}
                </small>
              );
            })}
          </div>
        </article>

        <div className="planning-case-list" aria-label="Account planning case queue">
          {runtime.cases.map((caseRow) => (
            <article className={`planning-case-card severity-${caseRow.severity}`} key={caseRow.caseId}>
              <div>
                <span>{caseRow.status}</span>
                <strong>{caseRow.caseId}{caseRow.runId ? ` / ${caseRow.runId}` : ''}</strong>
                <small>{caseRow.runCount} runs</small>
              </div>
              <div>
                <em>{caseRow.actionLabel}</em>
                {caseRow.actionMessage && <p>{caseRow.actionMessage}</p>}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function buildPlanningRuntime(bootstrap: BootstrapState, accountFrame: WorkbenchAccountFrame): PlanningRuntimeView {
  if (bootstrap.status === 'live' || bootstrap.status === 'mock') {
    return planningRuntimeFromBootstrap(bootstrap.data, accountFrame);
  }

  return {
    activeAccount: accountFrame.accountName,
    status: bootstrap.status === 'fallback' ? 'local_fallback' : 'loading',
    metrics: bootstrap.status === 'fallback' ? ['local model'] : ['loading snapshot'],
    cases: [
      {
        caseId: accountFrame.caseId,
        runId: accountFrame.latestRunId || '',
        status: bootstrap.status,
        runCount: 0,
        actionLabel: bootstrap.status === 'fallback' ? bootstrap.error : 'Loading backend plan',
        actionMessage: '',
        severity: 'next_step',
      },
    ],
  };
}

function planningRuntimeFromBootstrap(data: WorkbenchBootstrap, accountFrame: WorkbenchAccountFrame): PlanningRuntimeView {
  const overview = data.overview || {};
  const summary = overview.summary || {};
  const metrics = [
    metricLabel(overview.run_count, 'runs'),
    metricLabel(overview.case_count, 'cases'),
    metricLabel(summary.blocked_count, 'blocked'),
    metricLabel(summary.ready_count, 'ready'),
  ].filter((metric): metric is string => Boolean(metric));

  return {
    activeAccount: accountFrame.accountName,
    status: String(data.status || (data.ready === false ? 'needs_attention' : 'ready')),
    metrics,
    cases: data.cases?.length ? data.cases.map(planningCaseFromBootstrap) : [
      {
        caseId: accountFrame.caseId,
        runId: accountFrame.latestRunId || '',
        status: 'needs_first_run',
        runCount: 0,
        actionLabel: 'Create first run',
        actionMessage: 'Start by preparing a run template from this account plan.',
        severity: 'next_step',
      },
    ],
  };
}

function planningCaseFromBootstrap(caseRow: WorkbenchCase): PlanningCaseView {
  const action = caseRow.primary_action || {};
  return {
    caseId: String(caseRow.case_id || 'Case'),
    runId: String(caseRow.latest_run_id || caseRow.target_run_id || ''),
    status: String(caseRow.action_status || caseRow.latest_status || 'ready'),
    runCount: Number(caseRow.run_count || 0),
    actionLabel: String(action.label || action.action_id || 'Next action'),
    actionMessage: String(action.message || ''),
    severity: String(action.severity || 'next_step'),
  };
}

function metricLabel(value: unknown, label: string) {
  return typeof value === 'number' ? `${value} ${label}` : '';
}
