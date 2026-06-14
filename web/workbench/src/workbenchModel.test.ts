import { describe, expect, it } from 'vitest';
import { workbenchStages, demoCapabilityMap } from './workbenchModel';

describe('workbench product model', () => {
  it('tracks the five backend workflow stages in order', () => {
    expect(workbenchStages.map((stage) => stage.id)).toEqual([
      'intake',
      'context',
      'spec',
      'generation',
      'package',
    ]);
  });

  it('maps the demo surfaces to production workbench capabilities', () => {
    expect(demoCapabilityMap.map((item) => item.productionSurface)).toEqual([
      'AI brief composer',
      'Context and strategy room',
      'Skill-backed design spec',
      'Generation cockpit',
      'Artifact package review',
    ]);
  });
});
