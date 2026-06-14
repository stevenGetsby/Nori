import type { LucideIcon } from 'lucide-react';
import {
  Archive,
  BadgeCheck,
  BookOpenText,
  Bot,
  BrainCircuit,
  CalendarClock,
  ChartNoAxesCombined,
  CheckCircle2,
  ClipboardList,
  Compass,
  FileText,
  Image,
  Layers3,
  Lightbulb,
  MessagesSquare,
  PackageCheck,
  PenTool,
  Radar,
  RefreshCw,
  Search,
  Target,
  Sparkles,
  UploadCloud,
  WandSparkles,
} from 'lucide-react';

export type StageStatus = 'ready' | 'active' | 'running' | 'review';

export type WorkbenchStage = {
  id: 'intake' | 'context' | 'spec' | 'generation' | 'package';
  label: string;
  title: string;
  description: string;
  status: StageStatus;
  evidence: string;
  icon: LucideIcon;
};

export type DemoCapability = {
  demoSurface: string;
  productionSurface: string;
  improvement: string;
};

export type SkillCard = {
  name: string;
  scope: string;
  description: string;
  signal: string;
  icon: LucideIcon;
};

export type ArtifactPreview = {
  type: string;
  title: string;
  status: string;
  metric: string;
  image: string;
};

export type InsightItem = {
  title: string;
  description: string;
  value: string;
  icon: LucideIcon;
};

export const workbenchStages: WorkbenchStage[] = [
  {
    id: 'intake',
    label: '01 Intake',
    title: 'Brief intake',
    description: '接收目标、平台、素材和约束，形成可执行任务。',
    status: 'ready',
    evidence: '用户 brief、素材、平台、内容类型',
    icon: MessagesSquare,
  },
  {
    id: 'context',
    label: '02 Context',
    title: 'Context Pack',
    description: '汇总平台策略、账号定位、热点和素材证据。',
    status: 'active',
    evidence: '平台策略、市场热点、品牌基因',
    icon: BrainCircuit,
  },
  {
    id: 'spec',
    label: '03 Spec',
    title: 'Design Spec',
    description: '把策略拆成设计规格、skill 选择和验收规则。',
    status: 'running',
    evidence: 'ContentDesignSpec、media plan、review gate',
    icon: ClipboardList,
  },
  {
    id: 'generation',
    label: '04 Generation',
    title: 'Generation Cockpit',
    description: '执行图文、视频脚本或公众号文章生成。',
    status: 'running',
    evidence: 'ArtifactGenerationAgent、任务状态、引用素材',
    icon: WandSparkles,
  },
  {
    id: 'package',
    label: '05 Package',
    title: 'Artifact Package',
    description: '审查成品包、封面、正文、标签、来源与导出。',
    status: 'review',
    evidence: 'ContentPackage、acceptance、export bundle',
    icon: PackageCheck,
  },
];

export const demoCapabilityMap: DemoCapability[] = [
  {
    demoSurface: '首页大输入框',
    productionSurface: 'AI brief composer',
    improvement: '把自由输入升级为带平台、形式、素材和严格引用策略的任务入口。',
  },
  {
    demoSurface: '洞察 / 热点',
    productionSurface: 'Context and strategy room',
    improvement: '从展示型洞察升级为可进入工作流的 Context Pack。',
  },
  {
    demoSurface: '技能广场',
    productionSurface: 'Skill-backed design spec',
    improvement: '让 skill 服务于 Design Spec，而不是作为孤立卡片。',
  },
  {
    demoSurface: '生成聊天页',
    productionSurface: 'Generation cockpit',
    improvement: '把聊天动画改成可观察的阶段状态、引用素材和运行日志。',
  },
  {
    demoSurface: '作品库',
    productionSurface: 'Artifact package review',
    improvement: '把作品预览升级为可验收、可复盘、可导出的成品包。',
  },
];

export const skillCards: SkillCard[] = [
  {
    name: '热点小红书图文',
    scope: 'XHS image post',
    description: '追踪热点、账号适配、封面结构和标题钩子一体化生成。',
    signal: '适配度 92%',
    icon: Radar,
  },
  {
    name: '主理人口吻提炼',
    scope: 'brand voice',
    description: '从历史内容和访谈素材中提炼可信、稳定、可复用的表达方式。',
    signal: '7 条口吻规则',
    icon: Bot,
  },
  {
    name: '公众号长文结构',
    scope: 'WeChat article',
    description: '把选题转为大纲、证据、段落节奏和发布前检查。',
    signal: '4 层结构',
    icon: BookOpenText,
  },
];

export const insightItems: InsightItem[] = [
  {
    title: '平台策略',
    description: '小红书优先收藏型图文，首屏必须给结论和真实证据。',
    value: 'XHS',
    icon: Compass,
  },
  {
    title: '热点机会',
    description: '上海饭店推荐、第一次怎么点、附近人复吃正在升温。',
    value: '+18%',
    icon: ChartNoAxesCombined,
  },
  {
    title: '素材可用性',
    description: '门店环境、招牌菜和评论截图已满足严格引用模式。',
    value: '8 assets',
    icon: UploadCloud,
  },
  {
    title: '审查门槛',
    description: '封面、正文、标签和素材引用都需要进入人工 review gate。',
    value: 'Gate on',
    icon: BadgeCheck,
  },
];

export const artifactPreviews: ArtifactPreview[] = [
  {
    type: 'Cover',
    title: '第一次去这家上海小饭店怎么点',
    status: 'needs review',
    metric: '3 cover variants',
    image: '/assets/onion-burst-real.png',
  },
  {
    type: 'Note',
    title: '小红书正文 + 话题标签',
    status: 'draft ready',
    metric: '742 chars',
    image: '/assets/inspiration-skill-card.png',
  },
  {
    type: 'Export',
    title: 'ContentPackage handoff',
    status: 'blocked by review',
    metric: '6 artifacts',
    image: '/assets/search-card-reference.png',
  },
];

export const contentPlan = [
  {
    day: 'Mon',
    format: '小红书图文',
    topic: '第一次去怎么点：三道菜避雷清单',
    owner: 'Spec Agent',
  },
  {
    day: 'Wed',
    format: '短视频',
    topic: '午市套餐 28 元是否值得来',
    owner: 'Generation Agent',
  },
  {
    day: 'Fri',
    format: '公众号',
    topic: '一家社区小饭店为什么能复吃',
    owner: 'Review Gate',
  },
];

export const navigationItems = [
  { id: 'compose', label: '创作台', icon: PenTool },
  { id: 'planning', label: '账号规划', icon: Target },
  { id: 'context', label: '上下文', icon: Layers3 },
  { id: 'skills', label: 'Skills', icon: Sparkles },
  { id: 'library', label: '产物库', icon: Archive },
];

export const accountPlanningSections = [
  {
    title: '账号定位',
    label: 'Profile',
    body: '社区饭店账号，不做泛探店，围绕附近人真实复吃、第一次怎么点、下班吃什么建立信任。',
    evidence: ['核心人群：附近上班族', '内容承诺：不踩雷点单', '差异化：主理人可信感'],
  },
  {
    title: '运营计划',
    label: 'Operating plan',
    body: '每周三条内容：收藏型图文、午市短视频、周末公众号长文，按热点和素材状态动态调整。',
    evidence: ['小红书优先收藏', '短视频补充信任', '公众号沉淀品牌故事'],
  },
  {
    title: '内容日历',
    label: 'Calendar',
    body: '把账号定位转成可执行排期，后续每次生成都会引用同一套 Context Pack 和素材证据。',
    evidence: ['Mon 图文', 'Wed 短视频', 'Fri 公众号'],
  },
];

export const operatorChecklist = [
  { label: 'Brief 已包含目标平台和形式', done: true, icon: CheckCircle2 },
  { label: 'Context Pack 已选择热点与账号策略', done: true, icon: Search },
  { label: 'Design Spec 等待人工确认', done: false, icon: Lightbulb },
  { label: 'Generation Agent 可在确认后执行', done: false, icon: RefreshCw },
  { label: 'Package 需要最终验收导出', done: false, icon: FileText },
];

export const referencedAssets = [
  '/assets/nori-onion-logo.png',
  '/assets/nori-ip-character.png',
  '/assets/onion-burst-collage.png',
  '/assets/onion-burst-star.png',
  '/assets/icon-xiaohongshu.png',
  '/assets/icon-wechat.png',
  '/assets/icon-douyin.png',
  '/assets/icon-ins.png',
];

export const creationModes = [
  { label: '小红书图文', icon: Image },
  { label: '短视频脚本', icon: CalendarClock },
  { label: '公众号长文', icon: FileText },
];
