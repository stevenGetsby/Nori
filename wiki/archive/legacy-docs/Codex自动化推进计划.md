# Codex 自动化推进计划

状态日期：2026-05-23

> Historical automation note.
>
> Current roadmap, backlog, architecture, changelog, and verification baseline
> now live in `wiki/`. Keep this document for historical context; new
> iteration status should update `wiki/85-backlog.md`, relevant stage/API docs,
> and `wiki/90-changelog.md`.

本文档用于把 Nori 从“小红书内容生成 Agent”推进为“账号代运营 SOP Agent 系统”。自动化目标不是一次性大改，而是让 Codex 每一轮都完成一个可验证的小增量。

## 1. LLM/API 调用现状

Nori 的模型调用统一从 `llms/` 进入：

```text
api_config.yaml
  -> nori.nori_config.NoriConfig
  -> llms.config / llms.mode
  -> llms.client
  -> llms.call.chat / achat / image
  -> nori agents
```

当前 `active_models` 有四类 usage：

| usage | 当前用途 | 备注 |
| --- | --- | --- |
| `llm` | 文本 chat | 主业务调用入口 |
| `vision` | Intaker 图片逐张 multimodal 打标 | 图片理解入口 |
| `image` | 封面生图 / 图生图 | `CoverDirectorAgent` 调 `llms.image` |
| `video` | 已配置 | 当前未发现业务调用点 |

主要 API 形态：

| 函数 | 职责 |
| --- | --- |
| `llms.chat(messages, usage="llm", **kwargs)` | 同步 OpenAI-compatible chat |
| `llms.chat_json(messages, usage="llm", **kwargs)` | 同步 chat 并解析 JSON object |
| `llms.achat(...)` | 异步 chat |
| `llms.image(prompt, usage="image", reference_images=...)` | 文生图 / 图生图 |
| `llms.ensure_ready(usage)` | direct 检查 key；ghc 检查本地 `/models` |
| `llms.extract_intent(...)` | P1 意图抽取工具，失败返回 error |
| `llms.select_edit_target(...)` | E2 编辑目标路由工具，失败返回 error |

关键调用点：

| 模块 | 调用 | 失败策略 |
| --- | --- | --- |
| `IntakeAgent` | 文本意图 `llms.chat_json(..., usage="llm")`；图片逐张 multimodal `llms.chat_json(..., usage="vision")` | 文本走规则兜底；单图失败不阻塞 |
| `AccountPlannerAgent` | 账号规划 `llms.chat_json` | 结构化 fallback |
| `XHSNoteAnalyzer` | 关键词、笔记标签、单篇增强，JSON 调用走 `llms.chat_json` | 会话级链路要求 LLM 成功 |
| `NoteMakerAgent` | 选 skill、整理素材、写 note，JSON 调用走 `llms.chat_json` | 失败抛 `NoteMakerLLMError` |
| `CoverDirectorAgent` | 选参考图、写 prompt，JSON 调用走 `llms.chat_json`；调 `llms.image` | 失败抛 `CoverDirectorError` |

优先改造点：

1. API key 不进入文档/日志，后续迁到环境变量或本地 ignored config。
2. Intaker 的图片打标改为 `usage="vision"`，或者删除未使用的 vision usage。（已完成）
3. 把重复的 JSON chat 解析收敛成 `llms.chat_json(...)`。（已新增 helper，`IntakeAgent` / `AccountPlannerAgent` / `XHSNoteAnalyzer` / `NoteMakerAgent` / `CoverDirectorAgent` 已接入）
4. 给模型调用补最小 telemetry：usage、model key、耗时、错误类型、artifact id。
5. 给 image reference 能力加 provider capability check。

更完整的调用地图见 `文档/codex-skills/nori-project-operator/references/llm-api-map.md`。

## 2. 项目专用 Codex Skill

已生成并安装：

```text
文档/codex-skills/nori-project-operator/
  SKILL.md
  agents/openai.yaml
  references/
    llm-api-map.md
    roadmap.md
    iteration-protocol.md
  scripts/
    nori_status.py

~/.codex/skills/nori-project-operator/
  SKILL.md
  agents/openai.yaml
  references/
    account-ops-system.md
    iteration-protocol.md
    llm-api-map.md
    roadmap.md
  scripts/
    nori_status.py
```

这个 skill 的职责：

```text
读取项目状态
-> 选择一个最小高价值任务
-> 实现
-> 测试
-> 更新 wiki/backlog
-> 交接下一轮
```

触发场景：

```text
推进下一轮 / 按计划继续 / 实现下一个 P0
梳理 Nori / 改造 LLM 调用 / 做账号代运营 SOP
设计或实现 ops_agents / ops_models / 自动化计划
```

启用建议：

1. 项目内版本继续作为仓库记录维护。
2. 已安装版本位于 `~/.codex/skills/nori-project-operator`，供 Codex 自动发现。
3. 每轮自动化 prompt 都要求优先使用这个 skill。

## 3. 自动化循环设计

建议使用一个 Codex cron automation，按固定节奏跑“单轮推进”，而不是长时间无人值守大改。

推荐节奏：

```text
每周一 / 三 / 五 09:30
每次只做一个 bounded iteration
默认不跑 live LLM、不跑 live crawler、不生真实图
```

每轮 prompt：

```text
Use the Nori Project Operator skill if available. In <NORI_REPO>, run one bounded Nori project iteration:
1. Inspect current status and read the roadmap.
2. Pick the smallest highest-impact unfinished task.
3. Implement it with focused tests, avoiding live LLM/crawler/image calls unless explicitly required.
4. Run relevant tests, preferably ending with python -m pytest tests -q if feasible.
5. Update wiki/85-backlog.md and the relevant wiki stage/API/changelog files with status, test result, and next task.
6. Summarize changes and blockers.
```

## 4. 推荐推进顺序

### Round 1：LLM 层打稳

- `usage="vision"` 路由修正。
- `chat_json` 统一 JSON 调用。
- 配置/密钥安全策略。
- mock 测试覆盖。

### Round 2：账号代运营数据模型

- 新增 `nori/ops_models/`。
- 定义 `AccountOperationProject`、`OperationPlan`、`ContentCalendar`、`ContentTask`。
- 只做模型和序列化测试。

### Round 3：规划 Agent

- 新增 `nori/ops_agents/operation_planner.py`。
- 输入 `AccountPlanResult`，输出 7 天或 30 天运营计划。
- LLM 调用先 mock，规则 fallback 可用。

### Round 4：选题与排期

- `TopicPlanner`。
- `CalendarPlanner`。
- 把账号定位转成内容任务队列。

### Round 5：内容生产桥接

- `ContentTask -> NoteMakerAgent -> CoverDirectorAgent`。
- 输出统一 `ContentPackage`。

### Round 6：审核与复盘

- `ComplianceReviewer`。
- `ReviewAnalyzer`。
- `StrategyOptimizer`。

## 5. 暂缓事项

这些等后端闭环稳定后再做：

- 真实发布；
- 自动社群互动；
- 自动数据监测；
- 多平台适配；
- 完整前端工作台。

## 6. 当前验收基线

当前全量测试通过：

```text
python -m pytest tests -q
91 passed, 3 skipped
```

后续每轮自动化至少保持这个基线，除非该轮明确记录了临时失败和修复计划。

## 7. 自动化运行记录

### 2026-05-23

```text
本轮目标:
创建并安装专业的 Nori Project Operator skill，用于把 Nori 按小步迭代推进为账号代运营 SOP Agent 系统。

改动:
- 安装 `~/.codex/skills/nori-project-operator`，补全 SKILL.md、UI 元数据、路线图、迭代协议、LLM 调用地图、账号代运营系统参考文档和红acted 状态脚本。
- 同步项目内 `文档/codex-skills/nori-project-operator`，避免项目草稿与已安装 skill 分叉。
- 状态脚本现在可接收 repo 路径参数，并报告 `ops_models` / `ops_agents` 是否已落地。

测试:
- `python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/nori-project-operator` 通过。
- `python ~/.codex/skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过。
- `python -m pytest tests -q` 通过，63 passed。

风险/阻塞:
- 本轮只建立自动化工程 skill 和推进协议，未新增业务模块。
- `nori/ops_models` 与 `nori/ops_agents` 尚未创建。

下一轮:
实现 P1 最小账号代运营数据模型：`nori/ops_models` + `AccountOperationProject`、`ClientBrief`、`OperationPlan`、`ContentCalendar`、`ContentTask` 的序列化测试。
```

### 2026-05-23 下午

```text
本轮目标:
完成 LLM 层 JSON chat 调用收敛，减少业务 Agent 自行解析 JSON 的重复逻辑。

改动:
- 确认 `llms.chat_json(...)` / `llms.parse_json_object(...)` 已作为统一 JSON chat 入口存在并导出。
- 将 Intaker 文本理解、Intaker vision 打标、XHSNoteAnalyzer 单篇增强、关键词生成、笔记标签识别统一切到 `llms.chat_json(...)`。
- 保持 NoteMaker、CoverDirector、AccountPlanner 已有 `chat_json` 路径不变；调用仍通过 `llms.chat` 注入，现有 mock 测试无需 live LLM。

测试:
- `python -m py_compile nori/gen_agents/intaker.py nori/gen_agents/note_maker.py nori/gen_agents/cover_director.py nori/gen_agents/account_planner.py nori/ana_agents/xhs_note_analyzer.py llms/call.py llms/__init__.py` 通过。
- `python -m pytest tests/test_llms_call_json.py tests/test_gen_agents_intaker.py tests/test_gen_agents_note_maker.py tests/test_gen_agents_cover_director.py tests/test_gen_agents_account_planner.py tests/test_ana_agents_xhs_note_analyzer.py -q` 通过，62 passed。
- `python -m pytest tests -q` 通过，77 passed。

风险/阻塞:
- `llms.intent_extractor` 与 `llms.target_selector` 仍保留各自带 JSON mode fallback 的解析逻辑，后续可单独评估是否纳入 `chat_json`。
- 本轮未跑 live LLM / crawler / image generation。

下一轮:
实现 P1 最小账号代运营数据模型：`nori/ops_models` + 核心 dataclass 的 `to_dict/from_dict` 序列化测试。
```

### 2026-05-23 LLM JSON helper

```text
本轮目标:
收敛一处重复 JSON chat 解析，先建立 `llms.chat_json(...)` 作为后续迁移入口。

改动:
- 在 `llms.call` 新增 `chat_json()`、`parse_json_object()` 和 `ChatJSONError`，支持普通 JSON、fenced JSON 与前后带解释文字的嵌入 JSON object。
- 在 `llms.__init__` 导出 JSON helper。
- 将 `CoverDirectorAgent` 的参考图选择和 prompt 生成 JSON 调用迁到 `llms.chat_json(...)`，保留原有 `CoverDirectorError` 语义。
- 当前代码中 `IntakeAgent`、`NoteMakerAgent` 与 `AccountPlannerAgent` 也已通过 `llms.chat_json(...)` 走统一 JSON helper。
- 新增 `tests/test_llms_call_json.py` 覆盖 usage/kwargs 透传、注入 chat 函数、fenced/embedded JSON 和非法 JSON。

测试:
- `python -m pytest tests/test_llms_call_json.py tests/test_gen_agents_cover_director.py tests/test_gen_agents_intaker.py -q` 通过，34 passed。
- `python -m pytest tests -q` 通过，76 passed。

风险/阻塞:
- `XHSNoteAnalyzer` 中仍有本地 JSON 解析；`llms.intent_extractor` / `llms.target_selector` 仍保留自己的容错解析器。

下一轮:
继续 LLM 层收敛：评估 `XHSNoteAnalyzer` 的 `_extract_json` 是否迁到 `llms.parse_json_object()`，同时保留会话级错误语义。
```

### 2026-05-23 AccountPlanner JSON fallback

```text
本轮目标:
继续 LLM 层 JSON 调用收敛，把 `AccountPlannerAgent` 的账号规划 JSON 解析接入 `llms.chat_json(...)`。

改动:
- 将 `AccountPlannerAgent._llm_plan()` 从本地 `_extract_json()` 改为调用 `llms.chat_json(..., _chat=llms.chat)`。
- 删除 `AccountPlannerAgent` 内部重复 JSON 提取函数，保留原有结构化 fallback 策略。
- 新增账号规划非法 JSON 回退测试，锁定 LLM 输出不可解析时不阻塞规划链路。

测试:
- `python -m pytest tests/test_gen_agents_account_planner.py tests/test_llms_call_json.py -q` 通过，9 passed。
- `python -m pytest tests -q` 通过，72 passed。

风险/阻塞:
- `XHSNoteAnalyzer` 中仍有本地 JSON 解析；`llms.intent_extractor` / `llms.target_selector` 暂保留独立容错解析器。

下一轮:
继续 LLM 层收敛：评估 `XHSNoteAnalyzer` 的 `_extract_json` 是否迁到 `llms.parse_json_object()`，同时保留会话级错误语义。
```

### 2026-05-23 ops models

```text
本轮目标:
实现 P1 最小账号代运营数据模型，为后续 OperationPlanner / CalendarPlanner 提供稳定数据合同。

改动:
- 新增 `nori/ops_models` 包，导出 `AccountOperationProject`、`ClientBrief`、`OperationPlan`、`ContentCalendar`、`ContentTask`。
- 每个模型提供 `to_dict()`；需要持久化和 agent 交接的模型提供 `from_dict()` round-trip。
- `AccountOperationProject` 支持嵌套 client brief、operation plan、content calendar、content task 列表、artifacts 和 metadata。
- 新增 `tests/test_ops_models.py`，覆盖默认值、嵌套序列化和最小 payload 恢复。

测试:
- `python -m pytest tests/test_ops_models.py -q` 通过，4 passed。
- `python -m pytest tests -q` 通过，77 passed。
- `python ~/.codex/skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过，`ops_models=true`。

风险/阻塞:
- 本轮只定义模型合同，尚未创建 `nori/ops_agents`，也未接入真实 LLM 或内容生成链路。
- 暂未实现 roadmap 中更完整的 KPI、资产库、竞品研究、合规审核、发布记录、指标快照和策略迭代模型。

下一轮:
新增 `nori/ops_agents/operation_planner.py`：输入 `AccountPlanResult` / `ClientBrief`，输出 7 天 `OperationPlan` + `ContentCalendar`，先用规则 fallback 和 mock 测试。
```

### 2026-05-23 Intake chat_json contract

```text
本轮目标:
锁定 `IntakeAgent` 文本解析和 vision 打标都通过 `llms.chat_json(...)`，补齐 mock 契约测试。

改动:
- 新增 Intake 文本解析直接 mock `llms.chat_json` 的测试，确认 usage=`llm`、消息结构和 `_chat=llms.chat` 透传。
- 新增 `ChatJSONError` 触发时文本 intake 回到规则兜底的测试。
- 新增 vision 打标直接 mock `llms.chat_json` 的测试，确认 usage=`vision`、timeout 透传，并锁定单图 JSON 失败不阻塞其他图片。
- 同步本计划与 LLM API map 的当前状态：`IntakeAgent` 已接入 `chat_json`，`XHSNoteAnalyzer` 仍待迁移。

测试:
- `python -m pytest tests/test_gen_agents_intaker.py tests/test_llms_call_json.py -q` 通过，20 passed。
- `python -m pytest tests -q` 通过，76 passed。

风险/阻塞:
- 本轮未改业务代码；代码已接入 `chat_json`，本轮主要补强回归测试和文档状态。
- `XHSNoteAnalyzer` 仍有本地 `_extract_json()`，尚未迁到统一 helper。

下一轮:
继续 LLM 层收敛：把 `XHSNoteAnalyzer` 的 note enhancer、关键词和标签 JSON 调用迁到 `llms.chat_json(...)` 或 `llms.parse_json_object(...)`，保留现有失败语义并补 mock 测试。
```

### 2026-05-23 XHSNoteAnalyzer chat_json migration

```text
本轮目标:
完成 LLM 层 JSON 调用收敛，把 `XHSNoteAnalyzer` 的剩余本地 JSON 解析迁到统一 helper。

改动:
- 将 `XHSNoteAnalyzer` 的单篇 note enhancer、关键词生成、批量标签三处 JSON LLM 调用改为 `llms.chat_json(..., _chat=llms.chat)`。
- 删除 analyzer 内部 `_extract_json()`，让 fenced/embedded JSON 解析统一由 `llms.parse_json_object()` 承担。
- 新增 analyzer 路由测试，确认 usage、timeout 和 `_chat=llms.chat` 透传，同时保持原有 LLM 失败兜底/会话失败语义。
- 同步 LLM API map：主业务 JSON 调用点 `IntakeAgent`、`AccountPlannerAgent`、`XHSNoteAnalyzer`、`NoteMakerAgent`、`CoverDirectorAgent` 已接入 `chat_json`。

测试:
- `python -m pytest tests/test_llms_call_json.py tests/test_gen_agents_intaker.py tests/test_ana_agents_xhs_note_analyzer.py -q` 通过，29 passed。
- `python -m pytest tests -q` 通过，77 passed。
- `python ~/.codex/skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过，`ops_models=true`、`ops_agents=false`。

风险/阻塞:
- `llms.intent_extractor` / `llms.target_selector` 仍保留自己的容错 JSON 解析器；它们是独立工具函数，本轮未改。
- `nori/ops_agents` 尚未创建。

下一轮:
进入账号代运营 P2：新增 `nori/ops_agents/operation_planner.py`，输入 `AccountPlanResult` / `ClientBrief`，输出 7 天 `OperationPlan` + `ContentCalendar`，先用规则 fallback 和 mock 测试。
```

### 2026-05-23 NoteMaker chat_json verification

```text
本轮目标:
验证并补强 `NoteMakerAgent` 的 JSON LLM 调用统一入口，避免业务层重新实现 JSON 解析。

改动:
- `nori/gen_agents/note_maker.py` 的 `_call_json()` 走 `llms.chat_json(..., _chat=llms.chat)`，保留 `NoteMakerLLMError` 失败语义。
- 新增 NoteMaker 回归测试，确认 JSON 调用委托到 `llms.chat_json`，并透传 usage、timeout 和 `_chat`。

测试:
- `python -m pytest tests/test_llms_call_json.py tests/test_gen_agents_note_maker.py -q` 通过，18 passed。
- `python -m pytest tests -q` 通过，77 passed。
- `python ~/.codex/skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过，`ops_models=true`、`ops_agents=false`。

风险/阻塞:
- 主业务 JSON 调用已基本接入 `llms.chat_json`；`llms.intent_extractor` / `llms.target_selector` 仍保留独立容错解析器。
- `nori/ops_agents` 尚未创建。

下一轮:
进入账号代运营 P2：新增 `nori/ops_agents/operation_planner.py`，输入 `AccountPlanResult` / `ClientBrief`，输出 7 天 `OperationPlan` + `ContentCalendar`，先用规则 fallback 和 mock 测试。
```

### 2026-05-23 ops models verification

```text
本轮目标:
验证并收尾 `nori/ops_models/account_ops.py`，确保账号代运营数据合同稳定可用。

改动:
- 保持 `nori/ops_models` 仅包含 `account_ops.py` 与 `__init__.py`，去掉了多余的草稿模块。
- 保持 `AccountOperationProject`、`ClientBrief`、`OperationPlan`、`ContentCalendar`、`ContentTask` 的 round-trip 序列化测试。
- 未引入 live LLM / crawler / image 调用。

测试:
- `python -m pytest tests/test_ops_models.py -q` 通过，4 passed。
- `python -m pytest tests -q` 通过，77 passed。
- `python <NORI_REPO>/文档/codex-skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过，`ops_models=true`。

风险/阻塞:
- `nori/ops_agents` 仍未创建，账号代运营链路还停留在数据合同层。
- `ContentCalendar` 与 `OperationPlan` 当前只覆盖最小可用字段，后续还需要补 KPI、资产库和策略迭代字段。

下一轮:
新增 `nori/ops_agents/operation_planner.py`：输入 `AccountPlanResult` / `ClientBrief`，输出 7 天 `OperationPlan` + `ContentCalendar`，先用规则 fallback 和 mock 测试。
```

### 2026-05-23 OperationPlanner + ops model expansion

```text
本轮目标:
把账号代运营规划层真正接到 `ops_models`，让 `OperationPlanner` 产出可落盘的项目合同，并补齐下一层核心运营模型。

改动:
- 新增 `nori/ops_agents/operation_planner.py` 与 `nori/ops_agents/__init__.py`，提供 `OperationPlannerAgent` / `plan_operation`。
- `OperationPlannerAgent` 现在可把 `ClientBrief` + `AccountPlanResult` 转成 `AccountOperationProject`，包含 7 天 `OperationPlan`、`ContentCalendar`、`ContentTask`，并在规则 fallback 下稳定返回。
- 在 `AccountOperationProject` 中补齐 `KPIPlan`、`ContentPackage`、`ComplianceReview`、`MetricsSnapshot`、`StrategyIteration` 等闭环模型，并更新 `nori/ops_models/__init__.py` 导出。
- 让 `OperationPlannerAgent` 同步填充 `kpi_plan`，为后续 KPIPlanner / Review / StrategyOptimizer 留下稳定合同。
- 新增专项测试 `tests/test_ops_agents_operation_planner.py`，并扩展 `tests/test_ops_models.py` 覆盖新增模型 round-trip 和 package exports。

测试:
- `python -m pytest tests/test_ops_agents_operation_planner.py tests/test_ops_models.py -q` 通过，8 passed。
- `python -m pytest tests -q` 通过，81 passed。
- `python -m py_compile nori/ops_models/account_ops.py nori/ops_models/__init__.py nori/ops_agents/operation_planner.py tests/test_ops_models.py tests/test_ops_agents_operation_planner.py` 通过。
- `python ~/.codex/skills/nori-project-operator/scripts/nori_status.py <NORI_REPO>` 通过，`ops_models=true`、`ops_agents=true`。

风险/阻塞:
- `KPIPlan` 目前只是由 `OperationPlan` 派生，尚未有独立 KPIPlanner。
- `ContentPackage` / `ComplianceReview` / `StrategyIteration` 只是数据合同，生产桥接和复盘 agent 还未实现。

下一轮:
实现 `KPIPlanner` 或 `CalendarPlanner` 之一，优先把 `OperationPlan -> KPIPlan` 的规则/LLM 规划补成独立 agent。
```

### 2026-05-23 KPIPlanner

```text
本轮目标:
把 `OperationPlan -> KPIPlan` 从 OperationPlanner 内部派生逻辑提升为独立规划 agent，推进账号运营 SOP 的 KPI/里程碑层。

改动:
- 新增 `nori/ops_agents/kpi_planner.py`，提供 `KPIPlannerAgent` / `plan_kpi`。
- `KPIPlannerAgent` 支持输入 `OperationPlan`、`AccountOperationProject` 或 dict，输出稳定的 `KPIPlan`。
- 规则 fallback 会生成 `content_tasks`、`review_pass_rate`、手动核验频率、周期复盘等可人工核验指标。
- LLM 增强路径统一走 `llms.chat_json(..., _chat=llms.chat)`，失败时回到规则 fallback；测试中只 mock，不跑 live LLM。
- 更新 `nori/ops_agents/__init__.py` 导出 KPI planner。
- 新增 `tests/test_ops_agents_kpi_planner.py` 覆盖 fallback、project task count、dict 输入、LLM JSON 增强与 LLM 失败兜底。

测试:
- `python -m py_compile nori/ops_agents/kpi_planner.py tests/test_ops_agents_kpi_planner.py nori/ops_models/account_ops.py nori/ops_models/__init__.py` 通过。
- `python -m pytest tests/test_ops_agents_kpi_planner.py tests/test_ops_models.py -q` 通过，9 passed。
- `python -m pytest tests -q` 通过，86 passed。
- `python <NORI_REPO>/文档/codex-skills/nori-project-operator/scripts/nori_status.py` 通过，`ops_models=true`、`ops_agents=true`。

风险/阻塞:
- KPI 仍以人工核验和平台后台读取为默认假设，未接自动 metrics ingestion。
- CalendarPlanner / TopicPlanner / ContentTask -> NoteMaker bridge 尚未实现。

下一轮:
新增 `CalendarPlanner` 或 `TopicPlanner`，优先把 `OperationPlan + KPIPlan -> ContentCalendar/ContentTask` 拆成独立 agent，再进入内容生产桥接。
```

### 2026-05-23 LLM 主线与 CalendarPlanner

```text
本轮目标:
落实“所有服务以接入 LLM 作为主线，规则只作为审查 critic / 兜底”的方向，并补齐 `OperationPlan + KPIPlan -> ContentCalendar/ContentTask` 的独立排期 agent。

改动:
- 新增 `nori/ops_agents/calendar_planner.py`，提供 `CalendarPlannerAgent` / `plan_calendar`。
- `CalendarPlannerAgent` 默认通过 `llms.chat_json(..., usage="llm", _chat=llms.chat)` 生成内容日历和任务排期；LLM 失败或显式关闭时才返回规则 fallback。
- 规则逻辑现在只作为 fallback 与 `metadata["critic"]` 审查结果存在；fallback 会标记 `planner=rule_fallback` 且 critic `status=warn`。
- 更新 `nori/ops_agents/__init__.py` 导出 `CalendarPlannerAgent` / `plan_calendar`。
- 新增 `tests/test_ops_agents_calendar_planner.py`，覆盖规则兜底、project/dict 输入、LLM JSON 主线、LLM 失败兜底和 round-trip。
- 扩展 `tests/test_ops_agents_live_ghc.py`，增加 CalendarPlanner 的 live ghc smoke；仍由 `NORI_LIVE_GHC=1` 显式启用。

测试:
- `python -m py_compile nori/ops_agents/calendar_planner.py nori/ops_agents/__init__.py tests/test_ops_agents_calendar_planner.py tests/test_ops_agents_live_ghc.py` 通过。
- `python -m pytest tests/test_ops_agents_calendar_planner.py tests/test_ops_agents_live_ghc.py -q` 通过，5 passed, 3 skipped。
- `python -m pytest tests -q` 通过，91 passed, 3 skipped。
- `NORI_LIVE_GHC=1 python -m pytest tests/test_ops_agents_live_ghc.py -q` 未通过：`ghc-api` 本地服务不可用；手动启动时刷新 Copilot token 返回 403 `Sorry. Your account was suspended`。

风险/阻塞:
- live ghc smoke 默认跳过；本地 ghc 服务和 GitHub/Copilot 账号状态修复前，不把 live LLM 作为常规自动化必跑项。
- CalendarPlanner 只生成 planned 任务，不做真实发布、自动互动或自动数据抓取。

下一轮:
新增 `TopicPlanner`，把账号定位、内容支柱和排期任务进一步转成可给 NoteMakerAgent 使用的选题池与任务 brief。
```
