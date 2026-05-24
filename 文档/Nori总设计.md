# Agent 工程重构简版

## 1. 核心判断
用户输入后，系统先由 Intaker 拆成两类信息：

```text
Intention：意图
Context：用户的资产
```

后续 Agent 不重复做这一步，只消费这两类信息继续深化。

```text
Intaker = 入场整理
Account Planner = 账号策略
```

---

## 2. 输入结构

### Intention：用户意图

回答这四个问题：

```text
目标：品牌获客 / 种草 / 品宣 / 上新 / 涨粉 / 接广告 / 卖课 / 带货
形式：图文 / 短视频 / vlog / 直播 / 直播带货 （目前xhs note 图文）
调性：专业 / 高端 / 亲和 / 搞笑 / 走心 / 干货 / 毒舌
负向偏好：不要硬广 / 不要低价感 / 不掉人设 / 不太商业化
```

### Context：用户资产

回答这四个问题：

```text
创意资产：logo / 设计语 / 品牌色 / 人设 / IP / 口头禅
商业资产：店铺链接 / 商品链接 / 优惠 / 课程 / 合作品 / 橱窗
规范红线：品牌 guideline / 禁用词 / 人设边界 / 不接品类
数据参考：账号数据 / 竞品内容 / 粉丝画像 / 同类博主 / 爆款
```

---

## 3. 当前生成主链路

当前实际跑通的是三棒聊合 Agent，所有 LLM 调用集中在 `nori/gen_agents/` 下：

```text
User Input（文字 / 文字 + 图片）
  -> Intake Agent       ：拆 Intention + Context，同步给每张图走 vision 打标
  -> NoteMaker Agent    ：在选中的 skill 上，装配出 NoteDraft（标题 / body / tags / 主视觉种子）
  -> CoverDirector Agent：从 tagged_assets 选 reference，生一张 xhs 封面
  -> JSON 归档       ：封面路径回写 NoteDraft，一次性序列化到 note_draft.json
```

交接原则：

```text
Intake 是唯一看图 / 拆意图的位置
NoteMaker 只读 vision_* 标签和文本，不重新看图
CoverDirector 是唯一调生图、唯一读原图字节的位置
三棒之间单向流水，不回头、不交叉引用
```

后续 Agent（Account Planner / Skill Router / Review / Package 等）是未来拆分方向：

```text
Intake          未来拆出 AccountPlanner、底层制别还是进 Intaker
NoteMaker       未来拆出 Skill Router / Strategy / Copy / Render 、底层依然这一棒
CoverDirector   未来拆出 Art / Render / Review、底层依然这一棒
```

---

## 4. 工程目录

```text
nori/
  gen_agents/    内容生成 agents
  ana_agents/    内容分析学习 agents
  agent_models/  共享数据模型
  agent_utils/   共享工具
```

目录边界：

```text
gen_agents：服务本次生成任务。
ana_agents：分析内容，学习规律，沉淀 skill。
agent_models：放跨 Agent 传递的数据模型。
agent_utils：放日志、JSON 解析、路径工具等共享能力。
```

当前模型：

```text
nori/agent_models/intake.py：UserInput、IntakeResult。
nori/agent_models/account_planner.py：AccountPlannerInput、AccountPlanResult。
nori/agent_models/xhs_note.py：XHSNoteSample、XHSSeedSkillDraft。
nori/agent_models/base.py：Intention、Context 等共享类型别名。
nori/agent_models/__init__.py：只做公共导出，不写具体模型逻辑。
```

当前工具：

```text
nori/agent_utils/case_log.py：真实 case 输入输出日志。
nori/agent_utils/__init__.py：只做公共导出，不写具体工具逻辑。
```

交接关系：

```text
ana_agents 产出 skill / benchmark / pattern。
gen_agents 读取这些沉淀结果，完成用户本次生成。
两边共享 agent_models 和 agent_utils，不互相直接依赖。
```

---

## 5. Agent 分工

当前在跑的三棒：

| Agent | 职责 |
|---|---|
| Intake Agent | 拆 Intention + Context，并发给每张图走 vision 打标（仓库里唯一看图的位置）。 |
| NoteMaker Agent | SkillPicker + AssetCurator + NoteComposer 三道 LLM 工序，装配出 NoteDraft。 |
| CoverDirector Agent | LLM 选 reference + 写生图 prompt + 调 llms.image 出封面（唯一调生图的位置）。 |

未来拆分方向（当前未独立实现、底层在上面三棒里跑）：

| Agent | 未来职责 |
|---|---|
| Account Planner | 消费 Intention + Context，输出账号定位和 IP 画像报告。 |
| XHS Note Analyzer | 从小红书冷启动笔记中抽取 seed skill 草案。 |
| Skill Router | 自动选择最合适的 skill 和生成能力。 |
| Strategy Agent | 决定这篇内容怎么打、图和文怎么配合。 |
| Copy Agent | 负责标题、正文、标签、CTA。 |
| Art Agent | 负责视觉方向、封面结构、图片提示。 |
| Render Agent | 负责生图、排版、导出。 |
| Review Agent | 负责质检和重生建议。 |
| Package Agent | 负责最终交付。 |

---

## 6. Skill 体系

Skill 不再只是作者风格，而是系统能力库。

```text
Author Skill：某类账号/人设的表达能力
Brand Skill：品牌视觉、语气、禁忌和资产
Commercial Skill：商品、课程、店铺、转化链路
Platform Skill：小红书/抖音/视频号等平台规则
Scene Skill：图文、短视频、直播、种草、带货等场景能力
Review Skill：红线、合规、错字、低质感检查
```

生成时不让用户选 skill。系统根据 Intention + Context 自动匹配。

---

## 7. 最小可行版本

先做一个稳定闭环：

```text
用户输入 prompt + 图片
  -> Intaker 自动拆 Intention / Context
  -> Account Planner 生成 IP 画像报告
  -> 自动选 skill
  -> 生成小红书图文 + 封面
  -> 自动质检
  -> 输出最终 package
```

本阶段只追求：

```text
能理解用户要什么
能使用用户已有资产
能形成账号定位和 IP 画像
能自动选对 skill
能生成图文一致的内容
能发现明显错误并重生
```

---

## 8. 当前重构原则

```text
不让用户理解内部 skill。
不让单个 Agent 做所有事。
不把 prompt 当最终架构。
不保留无用旧链路。
先把 Agent 职责和数据交接做清楚。
```

当前边界：

```text
Intaker 不做账号策略。
Account Planner 不重新拆解用户输入。
Account Planner 以 Intention + Context 为主输入。
原始文字、图片、链接只作为证据保留。
```

新的工程目标：

```text
把 Nori 做成一个会理解意图、会使用资产、会调度 skill、会自检交付的内容生产 Agent 系统。
```

---

## 9. 测试日志

真实 case 测试后统一写入：

```text
log/
```

日志记录：

```text
agent / case / config / input / output
```

---

## 10. Agent 文档

每个 Agent 单独维护一份文档。

当前在跑的：

| Agent | 文档 |
|---|---|
| Intake Agent | [Agent-Intake.md](Agent-Intake.md) |
| NoteMaker Agent | [Agent-NoteMaker.md](Agent-NoteMaker.md) |
| CoverDirector Agent | [Agent-CoverDirector.md](Agent-CoverDirector.md) |

未来拆分方向：

| Agent | 文档 |
|---|---|
| Account Planner | [Agent-AccountPlanner.md](Agent-AccountPlanner.md) |
| XHS Note Analyzer | [Agent-XHSNoteAnalyzer.md](Agent-XHSNoteAnalyzer.md) |
