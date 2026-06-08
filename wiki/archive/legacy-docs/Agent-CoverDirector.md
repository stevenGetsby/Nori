# Agent：CoverDirector

## 1. 职责

CoverDirector 是生成链路的第三棒。

它只做一件事：

```text
拿到 NoteDraft + 用户 assets（已打标），生成一张可用的 xhs 封面。
```

不写正文，不挑 skill，不重新看图。

---

## 2. 输入

```text
note_draft     ：NoteMaker 产出的草稿（取 title / skill_id / cover_path 种子）
tagged_assets  ：UserAsset 列表，每张图带 vision_* 标签
intent         ：Intaker 的 Intention
context        ：Intaker 的 Context
```

`tagged_assets` 是 LLM 选 reference 的素材池来源；空池时退回旧的 `_collect_reference_paths` 规则。

---

## 3. 输出

一个 `CoverResult`：

```text
cover_path       ：落盘的封面 PNG 路径
prompt           ：本次喂给生图模型的最终 prompt
size             ：生图尺寸（默认 1072x1440，小红书 3:4）
reference_paths  ：实际用作 reference 的图片路径列表
source           ：生图服务返回的源 URL
extra            ：其他元信息
```

---

## 4. 工序

```text
工序 1  ReferencePicker  ：LLM 从 tagged_assets 里挑 0~MAX_REFERENCES 张
工序 2  PromptComposer   ：LLM 把 NoteDraft + 品牌信号写成生图 prompt
工序 3  ImageRender      ：调 llms.image，把 reference 图字节一起喂进去
```

任一工序失败抛 `CoverDirectorError`。

---

## 5. 工序 1：ReferencePicker

```text
常量
  MAX_REFERENCES         = 8     # 给生图模型最多塞 8 张 reference
  MAX_PROMPT_REFERENCES  = 3     # prompt 里最多写 3 张参考要点
```

LLM 看到的素材池字段：

```text
index / path / subject / vision_roles / brand_signals / usable_for / quality
```

软规则（写进 system prompt）：

```text
优先 usable_for 含 cover
优先 brand_signals 与本篇主题对得上
排除 usable_for=not_usable 或 quality=low
不重复选同一张
数量 0~MAX_REFERENCES
```

硬过滤（代码层）：

```text
LLM 返回的 index 必须能解析成 int
对 path 做 Path.exists 校验，不存在直接丢
去重
裁到 MAX_REFERENCES
```

---

## 6. 工序 2：PromptComposer

输入：

```text
NoteDraft.title / skill_id
intent.goal / tone / anti
被选中的 reference 列表（subject + brand_signals）
小红书 3:4 封面排版要求
```

产出一段长 prompt，关键约束：

```text
封面是产品/IP 主导，占 65~70% 画面
保留 reference 里的 IP、品牌色、产品形态
主标题用 NoteDraft.title，副标题一行不超过 12 字
不出现 logo / app UI / 假认证 / 多余水印
```

---

## 7. 工序 3：ImageRender

```text
reference_paths -> image_to_bytes(...) -> 压缩到 < 1.5MB
调 llms.image(prompt, usage="image", size=DEFAULT_SIZE, reference_images=ref_bytes)
返回的 PNG 写到 out_dir / cover_<skill_id>_<timestamp>.png
```

压缩工具复用 `nori/gen_agents/_image_io.py`，避免 relay::gpt-image-2 的 413 错。

---

## 8. 当前实现

```text
nori/gen_agents/cover_director.py
nori/gen_agents/_image_io.py
```

外部入口：

```text
CoverDirectorAgent().run(note_draft, tagged_assets, intent=..., context=..., out_dir=...)
```

已验证：

```text
Holly 真实素材 28 张：通过
LLM 选出 3 张 reference（IP 角色海报 + 产品摆拍 + 生活方式实拍）
封面落盘：SHOWCASE/Holly/generation_test/covers/cover_*.png（约 1.9MB）
封面延续品牌 IP 与品牌色，主副标题正确读取自 NoteDraft.title
relay::gpt-image-2 不再 413
```

---

## 9. 交接关系

```text
上游：IntakeAgent       → 提供 tagged_assets（vision_* 已打好）
上游：NoteMakerAgent    → 提供 NoteDraft（title + cover_path 种子）
本身：CoverDirectorAgent → 产 CoverResult（cover_path）
下游：归档层            → 把 cover_path 写回 NoteDraft.cover_path，序列化到 note_draft.json
```

CoverDirector 是整条链路里**唯一**调用生图模型的位置，也是**唯一**会读原始图字节的下游 Agent。
