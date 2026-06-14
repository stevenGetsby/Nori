import { useEffect, useRef, useState, type ChangeEvent } from 'react';
import {
  ArrowUpRight,
  Check,
  ChevronRight,
  CircleDot,
  Compass,
  Download,
  FileSearch,
  Play,
  Plus,
  Send,
  Sparkle,
} from 'lucide-react';
import {
  buildRunTemplate,
  checkSessionReferenceImageGeneration,
  createSession,
  getContentGenerationOptions,
  inspectRunArtifacts,
  planContentGeneration,
  runContentProduction,
  runPreflight,
  uploadSessionAssets,
  type ContentDesignSpecDraft,
  type ContentGenerationOptions,
  type ContentGenerationPlan,
  type ContentRunResult,
  type PreflightResponse,
  type ReferenceImageGenerationCheckResult,
  type RunTemplateResponse,
  type SessionAsset,
} from '../api/client';
import { ArtifactInspectionPreview, type ArtifactInspectionState } from '../components/ArtifactInspectionPreview';
import { PanelHeader } from '../components/common';
import type { WorkbenchAccountFrame } from '../workbenchAccount';
import type { WorkbenchReviewTarget } from '../workbenchReviewTarget';
import {
  artifactPreviews,
  contentPlan,
  creationModes,
  demoCapabilityMap,
  insightItems,
  operatorChecklist,
  referencedAssets,
  skillCards,
  workbenchStages,
} from '../workbenchModel';

const defaultBrief =
  '给巷口暖胃小馆生成一篇小红书图文：主题是第一次去怎么点，语气真实，封面要有明确结论，必须引用门店和菜品素材。';

type TemplateState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready' | 'needs_input'; data: RunTemplateResponse }
  | { status: 'error'; message: string };

type PreflightState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready' | 'blocked'; data: PreflightResponse }
  | { status: 'error'; message: string };

type RunState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'succeeded' | 'queued' | 'failed'; data: ContentRunResult }
  | { status: 'error'; message: string };

type GenerationControlsState =
  | { status: 'loading' }
  | { status: 'ready'; data: ContentGenerationOptions }
  | { status: 'error'; message: string };

type GenerationPlanState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready'; data: ContentGenerationPlan }
  | { status: 'error'; message: string };

type AssetIntakeState =
  | { status: 'idle' }
  | { status: 'uploading' }
  | { status: 'ready' }
  | { status: 'error'; message: string };

type ReferenceCheckState =
  | { status: 'idle' }
  | { status: 'checking' }
  | { status: 'ready' | 'blocked'; data: ReferenceImageGenerationCheckResult }
  | { status: 'error'; message: string };

type GenerationSelections = {
  platform: string;
  artifact_type: string;
  image_source: string;
  cover_strategy: string;
  human_gate_mode: string;
  entry_mode: string;
};

const defaultGenerationSelections: GenerationSelections = {
  platform: 'xhs',
  artifact_type: 'image_text_post',
  image_source: 'uploaded_assets',
  cover_strategy: 'auto',
  human_gate_mode: 'skip',
  entry_mode: 'workflow',
};

function defaultsFromOptions(options: ContentGenerationOptions, fallback: GenerationSelections): GenerationSelections {
  return {
    platform: defaultOptionId(options, 'platform', fallback.platform),
    artifact_type: defaultOptionId(options, 'artifact_type', fallback.artifact_type),
    image_source: defaultOptionId(options, 'image_source', fallback.image_source),
    cover_strategy: defaultOptionId(options, 'cover_strategy', fallback.cover_strategy),
    human_gate_mode: defaultOptionId(options, 'human_gate_mode', fallback.human_gate_mode),
    entry_mode: defaultOptionId(options, 'entry_mode', fallback.entry_mode),
  };
}

function defaultOptionId(options: ContentGenerationOptions, groupId: keyof GenerationSelections, fallback: string) {
  const group = options.option_groups?.[groupId] || [];
  return group.find((option) => option.default)?.option_id || group[0]?.option_id || fallback;
}

export function ComposeWorkspace({
  accountFrame,
  fetcher,
  onOpenLibrary,
  onReviewTargetReady,
}: {
  accountFrame: WorkbenchAccountFrame;
  fetcher?: typeof fetch;
  onOpenLibrary?: () => void;
  onReviewTargetReady?: (target: WorkbenchReviewTarget) => void;
}) {
  return (
    <>
      <HeroWorkspace accountFrame={accountFrame} />
      <WorkflowStrip />
      <section className="workspace-grid" aria-label="Nori production workbench">
        <BriefComposer
          accountFrame={accountFrame}
          fetcher={fetcher}
          onOpenLibrary={onOpenLibrary}
          onReviewTargetReady={onReviewTargetReady}
        />
        <ContextRoom />
        <SpecPanel />
        <GenerationCockpit />
        <PackageReview />
      </section>
    </>
  );
}

function HeroWorkspace({ accountFrame }: { accountFrame: WorkbenchAccountFrame }) {
  return (
    <section className="hero-workspace">
      <div className="hero-copy">
        <div className="status-pill">
          <CircleDot size={14} />
          content-production workflow
        </div>
        <h2>从一句创作意图，到可验收的内容成品包。</h2>
        <p>
          正式版把 demo 的大输入框、洞察、skill、生成聊天和作品库合并成一条可观察的生产链路：
          先为 {accountFrame.caseId} 生成设计规格，再交给执行 Agent 产出图文、视频脚本或公众号文章。
        </p>
      </div>
      <div className="hero-visual" aria-hidden="true">
        <div className="hero-orbit hero-orbit-one" />
        <div className="hero-orbit hero-orbit-two" />
        <img src="/assets/nori-ip-character.png" alt="" />
        <div className="hero-badge hero-badge-left">Context aware</div>
        <div className="hero-badge hero-badge-right">Skill backed</div>
      </div>
    </section>
  );
}

function WorkflowStrip() {
  return (
    <section className="workflow-strip" aria-label="Workflow stages">
      {workbenchStages.map((stage) => {
        const Icon = stage.icon;
        return (
          <article className={`stage-card stage-${stage.status}`} key={stage.id}>
            <div className="stage-icon">
              <Icon size={18} />
            </div>
            <div>
              <div className="stage-label">{stage.label}</div>
              <h3>{stage.title}</h3>
              <p>{stage.description}</p>
              <span>{stage.evidence}</span>
            </div>
          </article>
        );
      })}
    </section>
  );
}

function BriefComposer({
  accountFrame,
  fetcher,
  onOpenLibrary,
  onReviewTargetReady,
}: {
  accountFrame: WorkbenchAccountFrame;
  fetcher?: typeof fetch;
  onOpenLibrary?: () => void;
  onReviewTargetReady?: (target: WorkbenchReviewTarget) => void;
}) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [brief, setBrief] = useState(defaultBrief);
  const [controlsState, setControlsState] = useState<GenerationControlsState>({ status: 'loading' });
  const [planState, setPlanState] = useState<GenerationPlanState>({ status: 'idle' });
  const [generationSelections, setGenerationSelections] = useState<GenerationSelections>(defaultGenerationSelections);
  const [sessionId, setSessionId] = useState('');
  const [uploadedAssets, setUploadedAssets] = useState<SessionAsset[]>([]);
  const [assetIntakeState, setAssetIntakeState] = useState<AssetIntakeState>({ status: 'idle' });
  const [referenceCheckState, setReferenceCheckState] = useState<ReferenceCheckState>({ status: 'idle' });
  const [templateState, setTemplateState] = useState<TemplateState>({ status: 'idle' });
  const [preflightState, setPreflightState] = useState<PreflightState>({ status: 'idle' });
  const [runState, setRunState] = useState<RunState>({ status: 'idle' });
  const [artifactInspectionState, setArtifactInspectionState] = useState<ArtifactInspectionState>({ status: 'idle' });

  useEffect(() => {
    let cancelled = false;
    getContentGenerationOptions(fetcher)
      .then((data) => {
        if (cancelled) return;
        setControlsState({ status: 'ready', data });
        setGenerationSelections((current) => defaultsFromOptions(data, current));
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setControlsState({
            status: 'error',
            message: error instanceof Error ? error.message : 'Content generation catalog request failed',
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [fetcher]);

  const updateGenerationSelection = (groupId: keyof GenerationSelections, optionId: string) => {
    const nextSelections = { ...generationSelections, [groupId]: optionId };
    setGenerationSelections(nextSelections);
    setPlanState({ status: 'loading' });
    planContentGeneration(
      {
        goal: brief,
        ...nextSelections,
      },
      fetcher,
    )
      .then((data) => setPlanState({ status: 'ready', data }))
      .catch((error: unknown) => {
        setPlanState({
          status: 'error',
          message: error instanceof Error ? error.message : 'Content generation planning request failed',
        });
      });
  };

  const uploadReferenceAssets = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.currentTarget.files || []);
    event.currentTarget.value = '';
    if (files.length === 0) return;

    setAssetIntakeState({ status: 'uploading' });
    setTemplateState({ status: 'idle' });
    setPreflightState({ status: 'idle' });
    setRunState({ status: 'idle' });
    setArtifactInspectionState({ status: 'idle' });
    setReferenceCheckState({ status: 'idle' });
    try {
      let activeSessionId = sessionId;
      if (!activeSessionId) {
        const session = await createSession(
          {
            profile_id: accountFrame.caseId,
            metadata: {
              source: 'workbench',
              brief_preview: brief.slice(0, 120),
            },
          },
          fetcher,
        );
        activeSessionId = session.session_id;
        setSessionId(activeSessionId);
      }

      const data = await uploadSessionAssets(
        activeSessionId,
        files,
        {
          usage: 'reference',
          metadata: {
            source: 'workbench_upload',
            platform: generationSelections.platform,
            artifact_type: generationSelections.artifact_type,
          },
        },
        fetcher,
      );
      setUploadedAssets((current) => [...current, ...(data.assets || [])]);
      setAssetIntakeState({ status: 'ready' });
    } catch (error) {
      setAssetIntakeState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Reference asset upload failed',
      });
    }
  };

  const verifyReferenceImages = async () => {
    const assetIds = uploadedAssets.map((asset) => asset.asset_id).filter(Boolean);
    if (!sessionId || assetIds.length === 0) return;

    setReferenceCheckState({ status: 'checking' });
    setTemplateState({ status: 'idle' });
    setPreflightState({ status: 'idle' });
    setRunState({ status: 'idle' });
    setArtifactInspectionState({ status: 'idle' });
    try {
      const data = await checkSessionReferenceImageGeneration(
        sessionId,
        {
          asset_ids: assetIds,
          project: accountFrame.caseId,
          prompt: 'Validate references before content generation.',
          size: '1024x1024',
          metadata: {
            source: 'workbench',
            platform: generationSelections.platform,
            artifact_type: generationSelections.artifact_type,
          },
        },
        fetcher,
      );
      setReferenceCheckState({ status: data.ready ? 'ready' : 'blocked', data });
    } catch (error) {
      setReferenceCheckState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Reference image generation check failed',
      });
    }
  };

  const prepareTemplate = async () => {
    setTemplateState({ status: 'loading' });
    setPreflightState({ status: 'idle' });
    setRunState({ status: 'idle' });
    setArtifactInspectionState({ status: 'idle' });
    try {
      const assetIds = uploadedAssets.map((asset) => asset.asset_id).filter(Boolean);
      const data = await buildRunTemplate(
        {
          case_id: accountFrame.caseId,
          case_title: accountFrame.caseTitle,
          brief_text: brief,
          platform: generationSelections.platform,
          ...(sessionId ? { session_id: sessionId } : {}),
          ...(assetIds.length > 0 ? { asset_ids: assetIds } : {}),
          ...(referenceCheckState.status === 'ready' ? { require_reference_image_generation_check: true } : {}),
          require_image_references: true,
          human_gate_mode: generationSelections.human_gate_mode,
          config: {
            artifact_type: generationSelections.artifact_type,
            image_source: generationSelections.image_source,
            cover_strategy: generationSelections.cover_strategy,
            entry_mode: generationSelections.entry_mode,
          },
        },
        fetcher,
      );
      setTemplateState({ status: data.ready_for_preflight ? 'ready' : 'needs_input', data });
    } catch (error) {
      setTemplateState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Backend run template request failed',
      });
    }
  };

  const preparePreflight = async () => {
    if (templateState.status !== 'ready') return;
    setPreflightState({ status: 'loading' });
    setRunState({ status: 'idle' });
    setArtifactInspectionState({ status: 'idle' });
    try {
      const payload = {
        ...templateState.data.request,
        case_id: String(templateState.data.request?.case_id || accountFrame.caseId),
        brief_text: String(templateState.data.request?.brief_text || brief),
      };
      const data = await runPreflight(payload, fetcher);
      setPreflightState({ status: data.ready ? 'ready' : 'blocked', data });
    } catch (error) {
      setPreflightState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Backend preflight request failed',
      });
    }
  };

  const runWorkflow = async () => {
    if (templateState.status !== 'ready' || preflightState.status !== 'ready') return;
    setRunState({ status: 'loading' });
    setArtifactInspectionState({ status: 'idle' });
    try {
      const payload = {
        ...templateState.data.request,
        case_id: String(templateState.data.request?.case_id || accountFrame.caseId),
        brief_text: String(templateState.data.request?.brief_text || brief),
      };
      const data = await runContentProduction(payload, fetcher);
      const status = data.status === 'succeeded' ? 'succeeded' : data.job_id ? 'queued' : 'failed';
      setRunState({ status, data });
      if (status === 'succeeded' && data.run_id) {
        onReviewTargetReady?.({
          caseId: String(payload.case_id || accountFrame.caseId),
          runId: data.run_id,
          source: 'generated',
        });
      }
    } catch (error) {
      setRunState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Backend content run request failed',
      });
    }
  };

  const inspectArtifacts = async () => {
    if (runState.status !== 'succeeded') return;
    const runId = runState.data.run_id;
    const caseId = String(templateState.status === 'ready' ? templateState.data.request?.case_id || accountFrame.caseId : accountFrame.caseId);
    if (!runId) return;

    setArtifactInspectionState({ status: 'loading' });
    try {
      const data = await inspectRunArtifacts(caseId, runId, fetcher);
      setArtifactInspectionState({ status: 'ready', data });
    } catch (error) {
      setArtifactInspectionState({
        status: 'error',
        message: error instanceof Error ? error.message : 'Backend artifact inspection request failed',
      });
    }
  };

  return (
    <section className="panel composer-panel">
      <PanelHeader
        kicker="Intake"
        title="AI brief composer"
        action={
          <button
            className="tiny-button"
            disabled={assetIntakeState.status === 'uploading'}
            onClick={() => fileInputRef.current?.click()}
            type="button"
          >
            <Plus size={14} />
            {assetIntakeState.status === 'uploading' ? 'Uploading' : 'Add asset'}
          </button>
        }
      />
      <input
        ref={fileInputRef}
        aria-label="Upload reference assets"
        className="file-input-hidden"
        multiple
        accept="image/*"
        onChange={uploadReferenceAssets}
        type="file"
      />

      <div className="composer-account-frame" aria-label="Active compose account">
        <span>Active case</span>
        <strong>{accountFrame.caseId}</strong>
        {accountFrame.latestRunId && <small>{accountFrame.latestRunId}</small>}
      </div>

      <label className="brief-label" htmlFor="brief">
        创作 brief
      </label>
      <textarea
        id="brief"
        aria-label="创作 brief"
        value={brief}
        onChange={(event) => setBrief(event.target.value)}
      />

      <div className="mode-grid" aria-label="Content modes">
        {creationModes.map((mode, index) => {
          const Icon = mode.icon;
          return (
            <button className={index === 0 ? 'mode-chip mode-chip-active' : 'mode-chip'} key={mode.label}>
              <Icon size={16} />
              {mode.label}
            </button>
          );
        })}
      </div>

      <AssetIntake
        assets={uploadedAssets}
        onVerifyReferences={verifyReferenceImages}
        referenceCheckState={referenceCheckState}
        sessionId={sessionId}
        state={assetIntakeState}
      />

      <GenerationControls
        onSelect={updateGenerationSelection}
        planState={planState}
        selections={generationSelections}
        state={controlsState}
      />

      <button
        aria-label="Prepare backend run template"
        className="send-button"
        disabled={templateState.status === 'loading'}
        onClick={prepareTemplate}
        type="button"
      >
        <Send size={16} />
        {templateState.status === 'loading' ? 'Preparing template' : 'Prepare backend run template'}
      </button>
      <TemplatePreview
        onPreflight={preparePreflight}
        onInspectArtifacts={inspectArtifacts}
        onOpenLibrary={onOpenLibrary}
        onRunWorkflow={runWorkflow}
        artifactInspectionState={artifactInspectionState}
        preflightState={preflightState}
        runState={runState}
        state={templateState}
      />
    </section>
  );
}

function AssetIntake({
  assets,
  onVerifyReferences,
  referenceCheckState,
  sessionId,
  state,
}: {
  assets: SessionAsset[];
  onVerifyReferences: () => void;
  referenceCheckState: ReferenceCheckState;
  sessionId: string;
  state: AssetIntakeState;
}) {
  const canVerify = assets.length > 0 && Boolean(sessionId);
  const nextActions =
    referenceCheckState.status === 'ready' || referenceCheckState.status === 'blocked'
      ? referenceCheckState.data.next_actions || []
      : [];
  const providerFetchableCount =
    referenceCheckState.status === 'ready' || referenceCheckState.status === 'blocked'
      ? Number(referenceCheckState.data.provider_fetchable_count || 0)
      : 0;
  const referenceReason =
    referenceCheckState.status === 'ready' || referenceCheckState.status === 'blocked'
      ? formatReferenceReason(referenceCheckState.data.reason)
      : '';

  return (
    <div className="asset-intake">
      <div className="asset-intake-header">
        <div>
          <span>Reference assets</span>
          <strong>{assets.length > 0 ? `${assets.length} uploaded` : 'Demo references ready'}</strong>
        </div>
        {sessionId && <small>{sessionId}</small>}
      </div>

      <div className="asset-ribbon" aria-label="Demo reference assets">
        {referencedAssets.map((asset) => (
          <img src={asset} alt="" key={asset} />
        ))}
      </div>

      {state.status === 'uploading' && (
        <div className="asset-intake-status">
          <Sparkle size={14} />
          <span>Uploading reference assets</span>
        </div>
      )}
      {state.status === 'error' && (
        <div className="asset-intake-status asset-intake-error">
          <span>{state.message}</span>
        </div>
      )}
      {assets.length > 0 && (
        <>
          <div className="uploaded-asset-list" aria-label="Uploaded reference assets">
            {assets.map((asset) => (
              <div className="uploaded-asset" key={asset.asset_id}>
                {asset.file_url ? <img src={asset.file_url} alt="" /> : <div className="uploaded-asset-fallback" />}
                <div>
                  <strong>{asset.filename || asset.asset_id}</strong>
                  <small>{asset.asset_id}</small>
                </div>
              </div>
            ))}
          </div>
          <button
            className="reference-check-button"
            disabled={!canVerify || referenceCheckState.status === 'checking'}
            onClick={onVerifyReferences}
            type="button"
          >
            <Check size={14} />
            {referenceCheckState.status === 'checking' ? 'Checking references' : 'Verify references'}
          </button>
        </>
      )}
      {referenceCheckState.status === 'ready' || referenceCheckState.status === 'blocked' ? (
        <div
          className={
            referenceCheckState.status === 'ready'
              ? 'reference-check-card reference-check-ready'
              : 'reference-check-card reference-check-blocked'
          }
        >
          <span>{referenceCheckState.status === 'ready' ? 'Reference check ready' : 'Reference check blocked'}</span>
          {referenceReason && <strong>{referenceReason}</strong>}
          <small>{providerFetchableCount} fetchable reference{providerFetchableCount === 1 ? '' : 's'}</small>
          {nextActions.length > 0 && (
            <div className="reference-action-list" aria-label="Reference check next actions">
              {nextActions.slice(0, 2).map((action) => (
                <em key={action.action_id}>{action.label || action.action_id}</em>
              ))}
            </div>
          )}
        </div>
      ) : null}
      {referenceCheckState.status === 'error' && (
        <div className="reference-check-card reference-check-blocked">
          <span>Reference check failed</span>
          <strong>{referenceCheckState.message}</strong>
        </div>
      )}
    </div>
  );
}

function formatReferenceReason(reason: unknown) {
  return String(reason || '').replaceAll('_', ' ');
}

function GenerationControls({
  state,
  planState,
  selections,
  onSelect,
}: {
  state: GenerationControlsState;
  planState: GenerationPlanState;
  selections: GenerationSelections;
  onSelect: (groupId: keyof GenerationSelections, optionId: string) => void;
}) {
  if (state.status === 'loading') {
    return (
      <div className="generation-controls-panel">
        <span>Generation controls</span>
        <strong>Loading backend catalog</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="generation-controls-panel generation-controls-error">
        <span>Generation controls</span>
        <strong>Catalog unavailable</strong>
        <p>{state.message}</p>
      </div>
    );
  }

  return (
    <div className="generation-controls-panel">
      <span>Generation controls</span>
      <strong>Backend capability catalog</strong>
      <ControlGroup
        groupId="platform"
        label="Platform"
        options={state.data.option_groups?.platform || []}
        selected={selections.platform}
        onSelect={onSelect}
      />
      <ControlGroup
        groupId="artifact_type"
        label="Artifact"
        options={state.data.option_groups?.artifact_type || []}
        selected={selections.artifact_type}
        onSelect={onSelect}
      />
      <ControlGroup
        groupId="cover_strategy"
        label="Cover"
        options={state.data.option_groups?.cover_strategy || []}
        selected={selections.cover_strategy}
        onSelect={onSelect}
      />
      <PlanPreview state={planState} />
    </div>
  );
}

function ControlGroup({
  groupId,
  label,
  options,
  selected,
  onSelect,
}: {
  groupId: keyof GenerationSelections;
  label: string;
  options: { option_id: string; label: string; description?: string }[];
  selected: string;
  onSelect: (groupId: keyof GenerationSelections, optionId: string) => void;
}) {
  if (options.length === 0) return null;
  return (
    <div className="generation-control-group">
      <small>{label}</small>
      <div>
        {options.map((option) => (
          <button
            className={option.option_id === selected ? 'catalog-chip catalog-chip-active' : 'catalog-chip'}
            key={option.option_id}
            onClick={() => onSelect(groupId, option.option_id)}
            title={option.description}
            type="button"
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
}

function PlanPreview({ state }: { state: GenerationPlanState }) {
  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <div className="generation-plan-preview">
        <Compass size={14} />
        <span>Planning entrypoint</span>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="generation-plan-preview generation-plan-error">
        <Compass size={14} />
        <span>{state.message}</span>
      </div>
    );
  }

  return (
    <div className="generation-plan-card">
      <span>Recommended action</span>
      <strong>{state.data.selected_action_id || 'content.plan'}</strong>
      {state.data.selected_route && <p>{state.data.selected_route}</p>}
      {state.data.rationale && <small>{state.data.rationale}</small>}
    </div>
  );
}

function TemplatePreview({
  state,
  preflightState,
  runState,
  artifactInspectionState,
  onPreflight,
  onRunWorkflow,
  onInspectArtifacts,
  onOpenLibrary,
}: {
  state: TemplateState;
  preflightState: PreflightState;
  runState: RunState;
  artifactInspectionState: ArtifactInspectionState;
  onPreflight: () => void;
  onRunWorkflow: () => void;
  onInspectArtifacts: () => void;
  onOpenLibrary?: () => void;
}) {
  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <div className="template-preview">
        <span>Run Template</span>
        <strong>Preparing backend template</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="template-preview template-preview-error">
        <span>Run Template</span>
        <strong>Template request failed</strong>
        <p>{state.message}</p>
      </div>
    );
  }

  const missingFields = state.data.missing_fields || [];
  const actions = state.data.actions || [];
  return (
    <div className={state.status === 'ready' ? 'template-preview template-preview-ready' : 'template-preview'}>
      <span>Run Template</span>
      <strong>{state.status === 'ready' ? 'Template ready for preflight' : 'Template needs input'}</strong>
      {missingFields.length > 0 && (
        <div className="template-chip-list" aria-label="Missing run template fields">
          {missingFields.map((field) => (
            <small key={field}>{field}</small>
          ))}
        </div>
      )}
      {actions.length > 0 && (
        <div className="template-action-list" aria-label="Run template next actions">
          {actions.slice(0, 3).map((action) => (
            <div key={action.action_id}>
              <ChevronRight size={13} />
              <span>{action.label || action.action_id}</span>
            </div>
          ))}
        </div>
      )}
      <DesignSpecPreview spec={state.data.content_design_spec} />
      {state.status === 'ready' && (
        <button
          className="template-preflight-button"
          disabled={preflightState.status === 'loading'}
          onClick={onPreflight}
          type="button"
        >
          <Play size={14} />
          {preflightState.status === 'loading' ? 'Running preflight' : 'Run preflight'}
        </button>
      )}
      <PreflightPreview
        artifactInspectionState={artifactInspectionState}
        onInspectArtifacts={onInspectArtifacts}
        onOpenLibrary={onOpenLibrary}
        onRunWorkflow={onRunWorkflow}
        runState={runState}
        state={preflightState}
      />
    </div>
  );
}

function DesignSpecPreview({ spec }: { spec?: ContentDesignSpecDraft }) {
  if (!spec) {
    return (
      <div className="design-spec-preview">
        <span>Design Spec Gate</span>
        <strong>Spec gate waiting for workflow stage</strong>
        <p>后端当前 run-template 已准备运行请求；正式 ContentDesignSpec 会在 workflow 的 content_design_spec stage 生成。</p>
      </div>
    );
  }

  const skillRefs = spec.selected_skill_refs || [];
  const structure = spec.structure || [];
  const acceptanceChecks = spec.acceptance_checks || [];
  return (
    <div className="design-spec-preview design-spec-ready">
      <span>Design Spec Gate</span>
      <strong>Spec draft ready</strong>
      <div className="design-spec-meta" aria-label="Design spec metadata">
        {spec.spec_id && <small>{spec.spec_id}</small>}
        {spec.platform && <small>{spec.platform}</small>}
        {spec.artifact_type && <small>{spec.artifact_type}</small>}
      </div>
      {spec.creative_angle && <p>{spec.creative_angle}</p>}
      {skillRefs.length > 0 && (
        <div className="design-spec-section" aria-label="Selected spec skills">
          <span>Skills</span>
          {skillRefs.slice(0, 3).map((skill) => (
            <small key={String(skill.skill_id || skill.label)}>{String(skill.label || skill.skill_id || 'skill')}</small>
          ))}
        </div>
      )}
      {structure.length > 0 && (
        <div className="design-spec-section" aria-label="Design spec structure">
          <span>Structure</span>
          {structure.slice(0, 3).map((item) => (
            <small key={String(item.slot || item.purpose)}>{String(item.slot || 'slot')}: {String(item.purpose || '')}</small>
          ))}
        </div>
      )}
      {acceptanceChecks.length > 0 && (
        <div className="design-spec-checks" aria-label="Design spec acceptance checks">
          {acceptanceChecks.slice(0, 4).map((check) => (
            <small key={check}>{check}</small>
          ))}
        </div>
      )}
    </div>
  );
}

function PreflightPreview({
  state,
  runState,
  artifactInspectionState,
  onRunWorkflow,
  onInspectArtifacts,
  onOpenLibrary,
}: {
  state: PreflightState;
  runState: RunState;
  artifactInspectionState: ArtifactInspectionState;
  onRunWorkflow: () => void;
  onInspectArtifacts: () => void;
  onOpenLibrary?: () => void;
}) {
  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <div className="preflight-preview">
        <span>Preflight</span>
        <strong>Checking run readiness</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="preflight-preview preflight-preview-error">
        <span>Preflight</span>
        <strong>Preflight request failed</strong>
        <p>{state.message}</p>
      </div>
    );
  }

  const checks = state.data.checks || [];
  const actions = state.data.actions || [];
  return (
    <div className={state.status === 'ready' ? 'preflight-preview preflight-preview-ready' : 'preflight-preview'}>
      <span>Preflight</span>
      <strong>{state.status === 'ready' ? 'Preflight ready' : 'Preflight blocked'}</strong>
      {checks.length > 0 && (
        <div className="preflight-check-list" aria-label="Preflight checks">
          {checks.slice(0, 4).map((check) => (
            <div className={`preflight-check check-${check.status}`} key={check.name}>
              <span>{check.name}</span>
              <small>{check.status}</small>
            </div>
          ))}
        </div>
      )}
      {actions.length > 0 && (
        <div className="template-action-list" aria-label="Preflight next actions">
          {actions.slice(0, 3).map((action) => (
            <div key={action.action_id}>
              <ChevronRight size={13} />
              <span>{action.label || action.action_id}</span>
            </div>
          ))}
        </div>
      )}
      {state.status === 'ready' && (
        <button
          className="template-preflight-button run-button"
          disabled={runState.status === 'loading'}
          onClick={onRunWorkflow}
          type="button"
        >
          <Play size={14} />
          {runState.status === 'loading' ? 'Running workflow' : 'Run content workflow'}
        </button>
      )}
      <RunResultPreview
        artifactInspectionState={artifactInspectionState}
        onInspectArtifacts={onInspectArtifacts}
        onOpenLibrary={onOpenLibrary}
        state={runState}
      />
    </div>
  );
}

function RunResultPreview({
  state,
  artifactInspectionState,
  onInspectArtifacts,
  onOpenLibrary,
}: {
  state: RunState;
  artifactInspectionState: ArtifactInspectionState;
  onInspectArtifacts: () => void;
  onOpenLibrary?: () => void;
}) {
  if (state.status === 'idle') return null;

  if (state.status === 'loading') {
    return (
      <div className="run-result-preview">
        <span>Content Run</span>
        <strong>Running workflow</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="run-result-preview run-result-error">
        <span>Content Run</span>
        <strong>Run request failed</strong>
        <p>{state.message}</p>
      </div>
    );
  }

  const actions = state.data.actions || [];
  const artifactNames = Object.keys(state.data.artifact_paths || {});
  return (
    <div className={state.status === 'succeeded' ? 'run-result-preview run-result-ready' : 'run-result-preview'}>
      <span>Content Run</span>
      <strong>{state.status === 'succeeded' ? 'Run succeeded' : state.status === 'queued' ? 'Run queued' : 'Run failed'}</strong>
      {state.data.run_id && <p>{state.data.run_id}</p>}
      {artifactNames.length > 0 && (
        <div className="run-artifact-list" aria-label="Generated artifacts">
          {artifactNames.slice(0, 4).map((artifact) => (
            <small key={artifact}>{artifact}</small>
          ))}
        </div>
      )}
      {actions.length > 0 && (
        <div className="template-action-list" aria-label="Run result actions">
          {actions.slice(0, 3).map((action) => (
            <div key={action.action_id}>
              <ChevronRight size={13} />
              <span>{action.label || action.action_id}</span>
            </div>
          ))}
        </div>
      )}
      {state.status === 'succeeded' && (
        <div className="run-result-actions">
          <button className="template-preflight-button review-store-button" onClick={onOpenLibrary} type="button">
            <ArrowUpRight size={14} />
            Review in Artifact Store
          </button>
          <button
            className="template-preflight-button inspect-button"
            disabled={artifactInspectionState.status === 'loading'}
            onClick={onInspectArtifacts}
            type="button"
          >
            <FileSearch size={14} />
            {artifactInspectionState.status === 'loading' ? 'Inspecting artifacts' : 'Inspect artifacts'}
          </button>
        </div>
      )}
      <ArtifactInspectionPreview state={artifactInspectionState} />
    </div>
  );
}

function ContextRoom() {
  return (
    <section className="panel context-panel">
      <PanelHeader kicker="Context" title="Context Pack" />
      <div className="insight-grid">
        {insightItems.map((item) => {
          const Icon = item.icon;
          return (
            <article className="insight-card" key={item.title}>
              <div className="insight-icon">
                <Icon size={16} />
              </div>
              <div className="insight-value">{item.value}</div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          );
        })}
      </div>
      <div className="calendar-list">
        {contentPlan.map((item) => (
          <div className="calendar-row" key={item.day}>
            <span>{item.day}</span>
            <div>
              <strong>{item.topic}</strong>
              <small>{item.format} · {item.owner}</small>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function SpecPanel() {
  return (
    <section className="panel spec-panel">
      <PanelHeader kicker="Spec Agent" title="Design Spec" />
      <div className="spec-card">
        <div className="spec-card-top">
          <Sparkle size={18} />
          <span>selected skill</span>
        </div>
        <h3>热点小红书图文生成</h3>
        <p>以热点适配、真实素材、封面结论和收藏理由为核心，生成可审查的图文规格。</p>
      </div>
      <div className="skill-list">
        {skillCards.map((skill) => {
          const Icon = skill.icon;
          return (
            <article className="skill-row" key={skill.name}>
              <div className="skill-row-icon">
                <Icon size={17} />
              </div>
              <div>
                <strong>{skill.name}</strong>
                <span>{skill.scope}</span>
                <p>{skill.description}</p>
              </div>
              <em>{skill.signal}</em>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function GenerationCockpit() {
  return (
    <section className="panel generation-panel">
      <PanelHeader
        kicker="Generation Agent"
        title="Generation cockpit"
        action={
          <button className="tiny-button dark">
            <Play size={13} />
            Start
          </button>
        }
      />
      <div className="terminal-card">
        <div className="terminal-line">
          <span />
          reading ContextPack.platform_strategy
        </div>
        <div className="terminal-line">
          <span />
          material refs: storefront, signature dish, menu, comments
        </div>
        <div className="terminal-line active">
          <span />
          drafting cover variants with strict reference policy
        </div>
      </div>
      <div className="checklist">
        {operatorChecklist.map((item) => {
          const Icon = item.icon;
          return (
            <div className={item.done ? 'check-row done' : 'check-row'} key={item.label}>
              <Icon size={16} />
              <span>{item.label}</span>
              {item.done && <Check size={15} />}
            </div>
          );
        })}
      </div>
    </section>
  );
}

function PackageReview() {
  return (
    <section className="panel package-panel">
      <PanelHeader
        kicker="Review"
        title="Artifact Package"
        action={
          <button className="tiny-button">
            <Download size={14} />
            Export
          </button>
        }
      />
      <div className="artifact-grid">
        {artifactPreviews.map((artifact) => (
          <article className="artifact-card" key={artifact.title}>
            <img src={artifact.image} alt="" />
            <div>
              <span>{artifact.type}</span>
              <h3>{artifact.title}</h3>
              <p>{artifact.metric}</p>
              <small>{artifact.status}</small>
            </div>
          </article>
        ))}
      </div>
      <div className="capability-map">
        {demoCapabilityMap.map((item) => (
          <div className="map-row" key={item.demoSurface}>
            <span>{item.demoSurface}</span>
            <ChevronRight size={14} />
            <strong>{item.productionSurface}</strong>
            <button aria-label={item.improvement}>
              <ArrowUpRight size={14} />
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
