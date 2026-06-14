import type { ArtifactInspectionResult } from '../api/client';

export type ArtifactInspectionState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready'; data: ArtifactInspectionResult }
  | { status: 'error'; message: string };

export function ArtifactInspectionPreview({
  state,
  title = 'Artifact Inspection',
}: {
  state: ArtifactInspectionState;
  title?: string;
}) {
  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <div className="artifact-inspection-preview">
        <span>{title}</span>
        <strong>Loading review package</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="artifact-inspection-preview artifact-inspection-error">
        <span>{title}</span>
        <strong>Inspection request failed</strong>
        <p>{state.message}</p>
      </div>
    );
  }

  const counts = state.data.artifact_counts || {};
  const totalArtifacts = Number(counts.total || 0);
  const missingCore = state.data.missing_core_artifacts || [];
  const acceptanceStatus = String(state.data.acceptance?.status || 'unreviewed');
  const evaluationSummary = (state.data.evaluations?.summary || {}) as Record<string, unknown>;
  const reviewScore = evaluationSummary.score;
  const contentPackageKeys = state.data.content_package?.json_summary?.keys || [];
  const exportLink = state.data.links?.export;

  return (
    <div className="artifact-inspection-preview artifact-inspection-ready">
      <span>{title}</span>
      <strong>{state.data.ready_for_review ? 'Artifact inspection ready' : 'Artifact inspection needs review'}</strong>
      <div className="artifact-inspection-metrics" aria-label="Artifact inspection metrics">
        <small>{acceptanceStatus}</small>
        <small>{totalArtifacts} artifacts</small>
        <small>{Number(counts.covers || 0)} covers</small>
        {reviewScore !== undefined && <small>{String(reviewScore)} review score</small>}
      </div>
      <p>{missingCore.length > 0 ? `Missing core artifacts: ${missingCore.join(', ')}` : 'No missing core artifacts'}</p>
      {contentPackageKeys.length > 0 && (
        <div className="run-artifact-list" aria-label="Content package fields">
          {contentPackageKeys.slice(0, 5).map((key) => (
            <small key={key}>{key}</small>
          ))}
        </div>
      )}
      {exportLink && <p className="artifact-inspection-link">{exportLink}</p>}
    </div>
  );
}
