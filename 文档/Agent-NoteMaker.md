# Agent：NoteMaker

## 1. 职责

NoteMaker 是生成链路的第二棒。

它只做一件事：

```text
拿到 skill 列表 + 用户 assets（已打标），装配一篇 xhs note 草稿。
```

不重新理解意图，不重新看图，不写封面。

---

## 2. 输入

```text
skills   ：可用的 NoteSkill 列表（来自 skill_base / 现阶段从测试 fixture 注入）
assets   ：UserAsset 列表（Intaker 已打好 vision_* 标签）
intent   ：Intaker 的 Intention（goal / format / tone / anti）
context  ：Intaker 的 Context（品牌资产、规范红线、数据参考）
```

---

## 3. 输出

一个 `NoteDraft`：

```text
skill_id          ：本次用的 skill
title             ：主标题
candidate_titles  ：候选标题列表（规则名 + 选用理由）
body              ：正文
tags              ：标签
comment_hook      ：评论钩子
cover_path        ：主视觉路径（给 CoverDirector 当种子）
image_paths       ：正文配图路径列表
asset_bundle      ：装配后的 AssetBundle 快照
metrics_target    ：目标互动量
validation        ：内部自检结论
llm_enhanced      ：始终 true
```

---

## 4. 工序

3 道 LLM 工序，纯 LLM，不走规则兜底，任一失败抛 `NoteMakerLLMError`：

```text
工序 1  SkillPicker   ：skill 列表里挑 1 条最贴的
工序 2  AssetCurator  ：图片/文本分门别类成 AssetBundle
工序 3  NoteComposer  ：一次性出标题 + 候选 + 正文 + tags + 钩子 + 自检
```

工序之间是单向流水：上一步的产物喂给下一步，不回头。

---

## 5. 工序 1：SkillPicker

```text
输入：skills 概要（skill_id / label / goal / tone / note_type / metrics_summary）+ intent + context
输出：被选中的那条 skill 完整对象
跳过条件：skills 只有 1 条时直接用，不调 LLM
```

---

## 6. 工序 2：AssetCurator

把扁平的 `assets` 装配成 `AssetBundle`，分类清楚哪张当主视觉、哪张做配图、文字怎么用：

```text
输入打包给 LLM 的素材包：
  images       ：{index, path, vision_roles, subject, brand_signals, usable_for, quality}
  text_input   ：{index, text}
```

注意：素材包只塞**视觉标签字段**，不再塞 `role` / `tags`（已废弃）。

LLM 产出：

```text
main_images   ：主视觉候选（封面种子从这里取第一张）
aux_images    ：辅助配图
text_points   ：可直接复用的文案片段
brand_facts   ：品牌事实
data_points   ：数据/案例
```

---

## 7. 工序 3：NoteComposer

一次性出齐全部文案。封面种子从 `bundle.main_images[0].path` 直接取。

```text
title             ：最终标题
candidate_titles  ：候选 + rule_name + rationale
body              ：正文
tags              ：tag 列表
comment_hook      ：评论引导
validation        ：{status, issues}
```

---

## 8. 当前实现

```text
nori/gen_agents/note_maker.py
nori/agent_models/note_draft.py：NoteDraft / AssetBundle / UserAsset
```

外部入口：

```text
make_note = NoteMakerAgent().run
```

已验证：

```text
skill 列表 = 1：跳 SkillPicker，直通后续工序
skill 列表 > 1：SkillPicker 选中合理 skill
assets 全为字符串路径：通过 _normalize_asset 兜底接收
Holly 真实素材 28 张：通过，输出标题 / body / 8 张正文配图 / 主视觉路径
```

---

## 9. 交接关系

```text
上游：IntakeAgent  → 提供 intent + assets（含 vision_* 标签）
本身：NoteMakerAgent → 产 NoteDraft（含 cover_path 种子）
下游：CoverDirectorAgent → 用 NoteDraft.cover_path 当种子，再选 reference 生封面
```

NoteMaker 只读 `vision_*` 字段，不会回头去读原图字节，也不调 vision LLM。
