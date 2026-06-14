import { Activity, AlertTriangle, ArrowUpRight, CheckCircle2, Database } from 'lucide-react';
import type { BootstrapState } from './AppShell';
import { buildWorkbenchSnapshot, type SnapshotMetricKind, type SnapshotAction as SnapshotActionView } from '../workbenchSnapshot';

export function WorkbenchSnapshot({ bootstrap }: { bootstrap: BootstrapState }) {
  if (bootstrap.status === 'loading' || bootstrap.status === 'fallback') return null;

  const snapshot = buildWorkbenchSnapshot(bootstrap.data);
  if (!snapshot) return null;

  return (
    <section className="snapshot-strip" aria-label="Backend workbench snapshot">
      <div className="snapshot-status">
        <span className={snapshot.ready ? 'snapshot-dot' : 'snapshot-dot blocked'} />
        <div>
          <p>Backend snapshot</p>
          <strong>{snapshot.status}</strong>
        </div>
      </div>
      <div className="snapshot-metrics" aria-label="Workbench health metrics">
        {snapshot.metrics.map((metric) => (
          <SnapshotMetric kind={metric.kind} key={metric.kind} label={metric.label} />
        ))}
      </div>
      {snapshot.action && <SnapshotAction action={snapshot.action} />}
    </section>
  );
}

const metricIcons = {
  runs: Activity,
  cases: Database,
  blocked: AlertTriangle,
  ready: CheckCircle2,
} satisfies Record<SnapshotMetricKind, typeof Activity>;

function SnapshotMetric({ kind, label }: { kind: SnapshotMetricKind; label: string }) {
  const Icon = metricIcons[kind];
  return (
    <span className="snapshot-metric">
      <Icon size={15} />
      {label}
    </span>
  );
}

function SnapshotAction({ action }: { action: SnapshotActionView }) {
  return (
    <div className={`snapshot-action severity-${action.severity}`}>
      <div>
        <span>{action.caseId}</span>
        <strong>{action.label}</strong>
      </div>
      {action.href ? (
        <a href={action.href} aria-label={action.label}>
          <ArrowUpRight size={15} />
        </a>
      ) : (
        <ArrowUpRight size={15} />
      )}
    </div>
  );
}
