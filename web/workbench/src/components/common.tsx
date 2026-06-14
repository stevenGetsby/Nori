import type { ReactNode } from 'react';

export function PageLead({ kicker, title, body }: { kicker: string; title: string; body: string }) {
  return (
    <header className="page-lead">
      <span>{kicker}</span>
      <h2>{title}</h2>
      <p>{body}</p>
    </header>
  );
}

export function PanelHeader({
  kicker,
  title,
  action,
}: {
  kicker: string;
  title: string;
  action?: ReactNode;
}) {
  return (
    <div className="panel-header">
      <div>
        <p>{kicker}</p>
        <h2>{title}</h2>
      </div>
      {action}
    </div>
  );
}
