# Nori 文档入口

状态日期：2026-05-24

Nori 的当前权威项目文档在 `wiki/`。根 README 只做导航，避免和 wiki、历史 `文档/` 分册重复维护。

## 必读入口

| 文件 | 用途 |
| --- | --- |
| [wiki/00-product-proposal.md](wiki/00-product-proposal.md) | 产品定位、目标用户、当前做什么/不做什么 |
| [wiki/01-project-roadmap.md](wiki/01-project-roadmap.md) | 阶段总览、功能索引、里程碑 |
| [wiki/20-system-architecture.md](wiki/20-system-architecture.md) | 技术栈、目录结构、数据流、核心模块 |
| [wiki/85-backlog.md](wiki/85-backlog.md) | 当前待办、验证基线、下一步任务 |
| [CLAUDE.md](CLAUDE.md) | 项目级 Agent 指令和 wiki 维护规则 |

## 按任务加载

| 任务 | 先读 |
| --- | --- |
| 改生成链路 | [wiki/60-stage-generation-core.md](wiki/60-stage-generation-core.md) |
| 改账号代运营后端 | [wiki/61-stage-account-ops-backend.md](wiki/61-stage-account-ops-backend.md) |
| 改采集或 skill 学习 | [wiki/62-stage-data-collection-and-skill-learning.md](wiki/62-stage-data-collection-and-skill-learning.md) |
| 查 API/Agent 合同 | [wiki/30-api-reference.md](wiki/30-api-reference.md) |
| 查坑和环境问题 | [wiki/80-known-pitfalls.md](wiki/80-known-pitfalls.md) |

## 历史参考

`文档/` 下保留旧的设计记录、Agent 分册和项目专用 Codex skill。后续新增或更新的项目级事实应写入 `wiki/`，只在需要追溯历史决策时读取 `文档/`。
