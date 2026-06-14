# Agent：Intaker

## 1. 职责

Intaker 是用户输入后的第一层。

它只做一件事：

```text
把「文字」或「文字 + 图片」整理成可执行输入。
```

输出给后续 Agent 使用。

当前策略：

```text
LLM 先理解
规则再兜底
输出结构保持稳定
```

---

## 2. 输入

当前只支持两种：

```text
文字
文字 + 图片
```

图片在 Intaker 层做语义打标，结果挂在每张 `UserAsset` 上，不在这一层做任何生成。

---

## 3. 输出

Intaker 输出四块：

```text
intention：用户要什么、不要什么
context：用户有什么资产（含每张图片的视觉打标）
ready：信息是否够用
questions：还需要问用户什么
```

下游 NoteMaker、CoverDirector 只看 `intention` + `context.assets`，不再重复 OCR / 看图。

---

## 4. Intention

Intention 先拆四类：

```text
goal：目标
format：形式
tone：调性
anti：负向偏好
```

例子：

```text
goal = 种草 / 品宣 / 涨粉 / 带货
format = 小红书图文
tone = 高级 / 亲和 / 搞笑 / 干货
anti = 不要硬广 / 不要低价感 / 不掉人设
```

标签值统一使用中文，不向后续 Agent 输出英文枚举。

---

## 5. Context

Context 先拆四类：

```text
creative_assets：创意资产
commercial_assets：商业资产
guardrails：规范红线
data_refs：数据参考
```

图片统一进入 `images`，后续再判断是产品图、风格图、人物图还是参考图。

---

## 6. 判断规则

```text
信息够用：ready = true，进入后续 Agent。
信息不够：ready = false，只问必要问题。
```

LLM 负责理解自然语言里的隐含目标和资产。

规则层负责两件事：

```text
LLM 不可用时兜底。
LLM 输出不稳定时校正结构。
```

第一版只问最关键的问题：

```text
缺目标：问这次内容最重要的目标是什么。
缺主题：问这次围绕什么主题、产品或活动。
```

---

## 7. 图片视觉打标

Intaker 内部工序：

```text
_normalize_input：去重、规范化路径、剔除非法 asset
_extract_intention_llm：纯文本理解意图
_build_tagged_assets：并发打标每张图片
_check_ready：判断 ready / questions
```

打标工序细节：

```text
并发：concurrent.futures.ThreadPoolExecutor(max_workers=6)
粒度：每张图独立调一次 vision LLM，附带用户原文 user_text
输入：单图 data-uri（统一压缩长边 1280、JPEG q=85、<1.5MB） + 用户文本
返回：vision_roles / subject / brand_signals / usable_for / quality
校验：白名单过滤非法枚举，失败抛 stderr warn，不抛异常
```

图片预处理在 `nori/gen_agents/_image_io.py`：

```text
image_to_data_uri(path) -> str   # 给 vision 打标用
image_to_bytes(path)    -> bytes # 给 CoverDirector 喂 reference 用
压缩规则：alpha 通道 flatten 成白底，再 JPEG 压缩，目标 < 1.5MB
用途：解决 relay::gpt-image-2 413 Request Entity Too Large
```

UserAsset 的视觉打标字段：

```text
vision_roles   ：product_shot / lifestyle / scene_photo / ip_character /
                 brand_logo / portrait / reference_style / background_only
subject        ：一句话主体描述
brand_signals  ：识别到的品牌字标 / slogan / IP
usable_for     ：cover / body / background_only / not_usable
quality        ：high / medium / low
```

不再保留的字段：`role`、`tags`（被 `vision_roles` + `subject` + `brand_signals` 覆盖）。

---

## 8. 当前实现

```text
nori/gen_agents/intaker.py
nori/gen_agents/_image_io.py
```

模型定义：

```text
nori/agent_models/intake.py        ：UserInput、IntakeResult
nori/agent_models/note_draft.py    ：UserAsset（含 vision_* 字段）
```

已验证：

```text
文字输入：通过
文字 + 图片输入：通过
缺目标追问：通过
LLM 调用：通过 mock 验证
LLM 失败兜底：通过
Holly 真实素材（29 张、169MB）：通过，tagged_images = 28/28
中文标签输出：通过
```

---

## 9. 交接关系

```text
上游：用户（文字 / 文字+图片）
下游：NoteMaker（消费 intention + assets 装配草稿）
     CoverDirector（消费 assets 选 reference 生封面）
```

Intaker 是整条生成链路里**唯一**做图片理解的位置。下游 Agent 只读 vision_* 字段。
