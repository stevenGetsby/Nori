import { useEffect, useState } from 'react';
import { Compass } from 'lucide-react';
import {
  getContentGenerationOptions,
  planContentGeneration,
  type ContentGenerationOption,
  type ContentGenerationOptions,
  type ContentGenerationPlan,
} from '../api/client';
import { PageLead, PanelHeader } from '../components/common';
import { skillCards } from '../workbenchModel';

type SkillCatalogState =
  | { status: 'loading' }
  | { status: 'ready'; data: ContentGenerationOptions }
  | { status: 'error'; message: string };

type SkillPlanState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready'; data: ContentGenerationPlan }
  | { status: 'error'; message: string };

type SkillSelections = {
  platform: string;
  artifact_type: string;
  image_source: string;
  cover_strategy: string;
  human_gate_mode: string;
  entry_mode: string;
};

const defaultSkillSelections: SkillSelections = {
  platform: 'xhs',
  artifact_type: 'image_text_post',
  image_source: 'uploaded_assets',
  cover_strategy: 'auto',
  human_gate_mode: 'skip',
  entry_mode: 'workflow',
};

const skillPlanningGoal =
  '将热点小红书图文 skill 转换为可复用 ContentDesignSpec，再交给执行 Agent 生成图文、视频脚本或公众号文章。';

export function SkillsWorkspace({ fetcher }: { fetcher?: typeof fetch }) {
  const [catalogState, setCatalogState] = useState<SkillCatalogState>({ status: 'loading' });
  const [planState, setPlanState] = useState<SkillPlanState>({ status: 'idle' });
  const [selections, setSelections] = useState<SkillSelections>(defaultSkillSelections);

  useEffect(() => {
    let cancelled = false;
    getContentGenerationOptions(fetcher)
      .then((data) => {
        if (cancelled) return;
        const nextSelections = defaultsFromOptions(data, defaultSkillSelections);
        setCatalogState({ status: 'ready', data });
        setSelections(nextSelections);
        requestSkillPlan(nextSelections, fetcher, cancelled, setPlanState);
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setCatalogState({
            status: 'error',
            message: error instanceof Error ? error.message : 'Content generation catalog request failed',
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [fetcher]);

  const updateSelection = (groupId: keyof SkillSelections, optionId: string) => {
    const nextSelections = { ...selections, [groupId]: optionId };
    setSelections(nextSelections);
    requestSkillPlan(nextSelections, fetcher, false, setPlanState);
  };

  return (
    <section className="detail-workspace" aria-label="Skill operating system">
      <PageLead
        kicker="Spec before generation"
        title="Skill Operating System"
        body="Skill 不直接变成一张孤立卡片，而是服务于 Design Spec：它定义平台策略、视觉规则、素材约束、验收门槛和执行 Agent 的输入。"
      />
      <SkillCatalogPanel
        onSelect={updateSelection}
        planState={planState}
        selections={selections}
        state={catalogState}
      />
      <div className="skill-os-grid">
        {skillCards.map((skill, index) => {
          const Icon = skill.icon;
          return (
            <article className={index === 0 ? 'skill-os-card featured' : 'skill-os-card'} key={skill.name}>
              <div className="skill-os-icon">
                <Icon size={22} />
              </div>
              <span>{skill.scope}</span>
              <h2>{skill.name}</h2>
              <p>{skill.description}</p>
              <div className="skill-contract">
                <strong>{skill.signal}</strong>
                <small>feeds ContentDesignSpec</small>
              </div>
            </article>
          );
        })}
      </div>
      <section className="panel skill-contract-panel">
        <PanelHeader kicker="Reusable Contract" title="Design Spec contract" />
        <div className="contract-columns">
          {[
            ['Strategy', '平台规则、目标人群、热点适配和账号定位。'],
            ['Media plan', '封面结构、参考素材、图片数量和视频脚本节奏。'],
            ['Acceptance', '引用完整性、标题风险、语气一致性和人工 review gate。'],
          ].map(([title, body]) => (
            <article key={title}>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}

function requestSkillPlan(
  selections: SkillSelections,
  fetcher: typeof fetch | undefined,
  cancelled: boolean,
  setPlanState: (state: SkillPlanState) => void,
) {
  if (cancelled) return;
  setPlanState({ status: 'loading' });
  planContentGeneration(
    {
      goal: skillPlanningGoal,
      ...selections,
      metadata: {
        source: 'skill_operating_system',
        target_contract: 'ContentDesignSpec',
      },
    },
    fetcher,
  )
    .then((data) => {
      if (!cancelled) setPlanState({ status: 'ready', data });
    })
    .catch((error: unknown) => {
      if (!cancelled) {
        setPlanState({
          status: 'error',
          message: error instanceof Error ? error.message : 'Content generation planning request failed',
        });
      }
    });
}

function defaultsFromOptions(options: ContentGenerationOptions, fallback: SkillSelections): SkillSelections {
  return {
    platform: defaultOptionId(options, 'platform', fallback.platform),
    artifact_type: defaultOptionId(options, 'artifact_type', fallback.artifact_type),
    image_source: defaultOptionId(options, 'image_source', fallback.image_source),
    cover_strategy: defaultOptionId(options, 'cover_strategy', fallback.cover_strategy),
    human_gate_mode: defaultOptionId(options, 'human_gate_mode', fallback.human_gate_mode),
    entry_mode: defaultOptionId(options, 'entry_mode', fallback.entry_mode),
  };
}

function defaultOptionId(options: ContentGenerationOptions, groupId: keyof SkillSelections, fallback: string) {
  const group = options.option_groups?.[groupId] || [];
  return (
    group.find((option) => option.option_id === fallback)?.option_id ||
    group.find((option) => option.default)?.option_id ||
    group[0]?.option_id ||
    fallback
  );
}

function SkillCatalogPanel({
  state,
  planState,
  selections,
  onSelect,
}: {
  state: SkillCatalogState;
  planState: SkillPlanState;
  selections: SkillSelections;
  onSelect: (groupId: keyof SkillSelections, optionId: string) => void;
}) {
  if (state.status === 'loading') {
    return (
      <section className="panel skill-catalog-panel">
        <PanelHeader kicker="Backend contract" title="Backend skill catalog" />
        <div className="skill-catalog-loading">Loading generation capabilities</div>
      </section>
    );
  }

  if (state.status === 'error') {
    return (
      <section className="panel skill-catalog-panel skill-catalog-error">
        <PanelHeader kicker="Backend contract" title="Backend skill catalog" />
        <div className="skill-catalog-loading">{state.message}</div>
      </section>
    );
  }

  return (
    <section className="panel skill-catalog-panel">
      <PanelHeader
        kicker="Backend contract"
        title="Backend skill catalog"
        action={<span className="skill-catalog-count">{Object.keys(state.data.option_groups || {}).length} option groups</span>}
      />
      <div className="skill-catalog-layout">
        <div className="skill-catalog-controls" aria-label="Skill catalog controls">
          <SkillOptionGroup
            groupId="platform"
            label="Platform"
            options={state.data.option_groups?.platform || []}
            selected={selections.platform}
            onSelect={onSelect}
          />
          <SkillOptionGroup
            groupId="artifact_type"
            label="Artifact"
            options={state.data.option_groups?.artifact_type || []}
            selected={selections.artifact_type}
            onSelect={onSelect}
          />
          <SkillOptionGroup
            groupId="cover_strategy"
            label="Cover strategy"
            options={state.data.option_groups?.cover_strategy || []}
            selected={selections.cover_strategy}
            onSelect={onSelect}
          />
          <SkillOptionGroup
            groupId="entry_mode"
            label="Entrypoint"
            options={state.data.option_groups?.entry_mode || []}
            selected={selections.entry_mode}
            onSelect={onSelect}
          />
        </div>
        <SkillPlanPreview state={planState} />
      </div>
    </section>
  );
}

function SkillOptionGroup({
  groupId,
  label,
  options,
  selected,
  onSelect,
}: {
  groupId: keyof SkillSelections;
  label: string;
  options: ContentGenerationOption[];
  selected: string;
  onSelect: (groupId: keyof SkillSelections, optionId: string) => void;
}) {
  if (options.length === 0) return null;

  return (
    <div className="skill-option-group">
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

function SkillPlanPreview({ state }: { state: SkillPlanState }) {
  if (state.status === 'idle' || state.status === 'loading') {
    return (
      <div className="skill-plan-card">
        <Compass size={16} />
        <span>Design Spec handoff</span>
        <strong>{state.status === 'loading' ? 'Planning execution contract' : 'Waiting for catalog'}</strong>
      </div>
    );
  }

  if (state.status === 'error') {
    return (
      <div className="skill-plan-card skill-plan-error">
        <Compass size={16} />
        <span>Design Spec handoff</span>
        <strong>{state.message}</strong>
      </div>
    );
  }

  const normalizedOptions = state.data.normalized_options || {};
  return (
    <div className="skill-plan-card">
      <Compass size={16} />
      <span>Design Spec handoff</span>
      <strong>{state.data.selected_action_id || 'content.plan'}</strong>
      {state.data.selected_route && <p>{state.data.selected_route}</p>}
      {state.data.rationale && <small>{state.data.rationale}</small>}
      <div className="skill-plan-options" aria-label="Normalized generation options">
        {Object.entries(normalizedOptions).slice(0, 6).map(([key, value]) => (
          <em key={key}>
            {key}: {value}
          </em>
        ))}
      </div>
    </div>
  );
}
