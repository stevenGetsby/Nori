# Agent：XHS Note Analyzer

## 1. 职责

XHS Note Analyzer 负责从小红书冷启动笔记中抽取 seed skill 草案。

它不生成内容，只分析已有笔记。

```text
原始 note
	-> 规则 analyzer 抽结构和证据
	-> LLM 基于证据深化 skill draft
	-> 规则层校正输出格式
```

---

## 2. 输入

第一版读取：

```text
cold_start_data/xhs/{分类}/{作者ID}/posts/{笔记ID}/meta.json
```

笔记字段：

```text
title：标题
desc：正文
tag_list：话题标签
liked / collected / comment / share：互动数据
image_count：图片数量
cover.jpg / 图片：视觉证据
```

---

## 3. 输出

输出是单篇笔记的 seed skill 草案：

```text
type：xhs_note_seed_skill
status：single_note_draft
match：适用平台、分类、场景、目标
craft：标题规则、开头规则、正文结构、互动规则、视觉规则、禁忌
evidence：来源笔记和证据片段
validation：为什么还不能算稳定 skill
```

数据模型：

```text
nori/agent_models/xhs_note.py：XHSNoteSample、XHSSeedSkillDraft
```

单篇笔记只能形成候选规则。

稳定 seed skill 必须由多篇同类笔记重复验证后生成。

---

## 4. 当前实现

```text
nori/ana_agents/xhs_note_analyzer.py
```

当前支持：

```text
读取真实 cold_start_data/xhs 笔记。
随机抽取分类下的一篇 note。
规则层抽取 single_note_draft。
LLM 基于规则证据深化草案。
规则层校正 LLM 输出格式。
识别设计案例解析型 note。
输出可追溯 evidence。
LLM 不可用时回退规则草案。
```

---

## 5. 验证方式

第一版验证：

```text
能读取真实笔记。
能输出稳定字段。
能在 mock LLM 下深化规则草案。
能在 LLM 失败时回退规则草案。
能区分设计案例与普通活动招募。
输出包含证据和 draft_only 标记。
```

后续验证：

```text
多篇聚合后检查规则重复率。
用留出笔记验证 skill 可解释性。
用同一 brief 对比有 skill / 无 skill 的生成质量。
```
