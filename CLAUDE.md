# Project Instructions

Follow the shared global agent instructions in `~/.agents/AGENTS.md`.

## Wiki 维护

开发过程中，以下操作需要同步更新对应 wiki 文件：

| 当你做了这件事 | 更新哪个文件 |
|--------------|------------|
| 新增/修改 Python API、Agent 合同或公开模型字段 | `wiki/30-api-reference.md` 追加或修改对应条目 |
| 完成一个 stage 的功能 | `wiki/01-project-roadmap.md` 对应行状态改为完成或更新阶段说明 |
| 遇到非显而易见的坑 | `wiki/80-known-pitfalls.md` 追加一条（现象、原因、解法） |
| 多个 bug 互相关联、暴露系统性问题 | 新建 `wiki/81-postmortem-*.md`（单点问题用 pitfalls，系统性问题用 postmortem） |
| 架构变更（新模块、新数据流） | `wiki/20-system-architecture.md` 更新对应章节 |
| 阶段全部交付 | `wiki/90-changelog.md` 补一笔（从 backlog 已完成条目整理） |
| 发现 bug / 技术债 / 改进想法 | `wiki/85-backlog.md` 追加一条 |
| 新增视觉规则、封面规则或工作台 UX 规则 | `wiki/21-design-principle.md` 追加对应条目 |
| 出现新领域术语 | `wiki/05-glossary.md` 追加定义，防止 Agent 后续用词混乱 |
| 重命名 / 移动 wiki 文件 | 同步更新所有引用该文件的链接 |

**新建文件时机：**
- 新功能复杂度超过一句话说清 -> 新建 `wiki/6X-stage-X.md`
- 小功能 / 改进点需要 spec -> 新建 `wiki/specs/spec-{name}.md`（完成后移入 `archive/specs/`）
- 外部机制调研 -> 新建 `wiki/refs/ref-{topic}.md`
- Spec / 代码 / 设计评审完成 -> 新建 `wiki/reviews/review-{date}-{subject}.md`

**归档时机：**
- Spec 完成且 review 通过 -> `git mv wiki/specs/spec-xxx.md wiki/archive/specs/`，backlog 打勾
- Review 的 action items 全部完成 -> `git mv wiki/reviews/review-xxx.md wiki/archive/reviews/`
- Stage 归档 -> `git mv wiki/6X-stage-X.md wiki/archive/stages/`，roadmap 标注 `[archived]`

**关联维护（每次修改 wiki 文件时）：**
- `grep -r "{被修改文件名}" wiki/` -> 检查引用方是否需要同步更新
- 重命名/移动文件 -> 全文搜索旧路径，更新所有引用

**定期检查（每个阶段开始时）：**
- 扫描 wiki/ 下所有文件，更新 `Last verified` 日期
- 标出内容可能已过时的章节（加 `<!-- May be outdated -->` 注释）

不需要在每次 commit 时都更新；在功能完成、API 变更、架构调整这些节点同步即可。

