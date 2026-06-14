# Holly Live Flow Review

## 本次真实生成流程

1. 读取用户输入
   - 输入文件：`cases/Holly/brief/original.md`
   - 输入素材：`cases/Holly/assets/raw/brand_materials/` 中选取 4 张代表性图片
   - 用户目标：小红书账号定位、涨粉、后续接单、同时能卖文创产品

2. 真实小红书调研
   - 使用 `data_collect` 真实搜索小红书
   - 搜索关键词：`怪趣文创`、`反焦虑文创`
   - 每个关键词取 1 条 hot note，写入 `xhs_top_notes_result.json`
   - 本次市场样本用于抽取内容结构，不用于照搬文案

3. 市场 skill 提取
   - 使用 `lumina::gpt-5.5` 对真实 note 做聚类和标签
   - 产出两个 note skill：
     - `情绪吐槽·吐槽`
     - `经验复盘·个人经验`

4. Intake 和素材理解
   - 使用 `lumina::gpt-5.5` 做文本 intake
   - 使用 vision 对素材做标签
   - 4 张图中 2 张成功识别出产品/IP/品牌信号，2 张 vision 超时，只保留为普通图片

5. 账号定位与内容任务
   - 账号定位结果：`一个用屎尿屁幽默替年轻人反焦虑发声的同济设计生文创主理人账号。`
   - 选中的内容任务：围绕厕所时间、带薪拉屎、合法躺平做一篇反焦虑观点/经验帖

6. Note 生成
   - NoteMaker 选择了 `经验复盘·个人经验` skill
   - 生成标题：`别再为休息羞耻了`
   - 生成正文使用了用户原始信息：
     - 同济设计学生
     - 市集卖得好，线上卖不动
     - Holly Shit 开心拉屎
     - Shit 人生也要拉得开心
     - 厕所时间、带薪拉屎、休息权、身体自主权

7. 封面生成
   - CoverDirector 选中了 1 张 Holly 原始素材作为 reference path
   - 生成了 cover prompt，并在 prompt 中要求保留 Holly Shit 的 IP/品牌元素
   - `relay::gpt-image-2` 真实生成了封面图

8. Review
   - Compliance review：passed
   - Consistency review：passed

## 是否真的参考了用户意图

结论：正文较好地参考了用户意图，封面参考还不够硬。

已满足的部分：
- 保留了 Holly Shit 的反焦虑、厕所快乐、屎尿屁幽默方向。
- 没有把品牌写成低俗猎奇，而是转成休息权和身体自主权。
- 用了用户提供的真实背景：同济设计学生、市集卖得好、线上卖不动。
- 内容形式适合小红书首发人设帖，不是直接硬广。

不足：
- 产品转化弱，杯子、包、挂件、贴纸、冰箱贴、手机支架没有自然进入正文。
- 市场样本只有 2 条，只能验证链路，不能支撑稳定策略。
- 选中的 skill 偏“经验复盘”，安全但不够“不羁/冲击/怪趣”。
- Review 是规则型 review，还没有高级“是否真的适合 Holly 涨粉卖货”的判断。

## 图片参考问题

本次封面不是严格意义上的 image-to-image。

实际发生的是：
- CoverDirector 选择了用户素材：`微信图片_20250617195920.jpg`
- prompt 中明确写入了参考图的语义：Holly Shit、工作女孩 IP、小狗、厕所快乐、反焦虑
- 但 `relay::gpt-image-2` 在接收本地图片转成 base64/data-uri 时返回错误：`不支持base64参数，请使用图片url传参`
- 为了跑通端到端流程，代码当时降级成了同一 prompt 的文生图

因此本次封面“参考了用户素材语义”，但没有真正把用户图片作为模型输入。

## 下一步需要解决

必须验证并修复参考图链路：

1. 验证 `relay::gpt-image-2` 是否支持 OpenAI multipart `images.edit`
2. 验证 `relay::gpt-image-2` 是否只支持公网 image URL
3. 如果支持公网 URL，则改造 `llms.image` 让 relay 能保留 URL reference，不再只接收 bytes/base64
4. 如果本地图片无法被 relay 直接消费，则需要增加一个上传/托管步骤，把用户素材变成可访问图片 URL
5. 只有当真实图片作为 reference 输入成功，才算“真的参考用户图片”

## 后续验证结果

已完成 API 验证：

- `relay::gpt-image-2` 的 OpenAI multipart `images.edit` 不可用。
  - 返回：`当前接口暂不支持，请使用 /v1/images/generations`
- `relay::gpt-image-2` 的 `/v1/images/generations` 支持 `extra_body.image_urls`。
  - 使用公网图片 URL 作为 reference 可以成功生成图片。
  - 验证产物：`reference_url_probe/result.json`
  - 验证图片：`reference_url_probe/cover_relay_url_reference_probe_20260529_031741.png`
- 本地 Holly 图片直接传入仍不可用。
  - 原因：relay 拒绝 base64/data-uri reference。
  - 当前代码已改为显式失败：`relay image reference generation requires public HTTPS image URLs`

代码层修复：

- `llms.image` 现在会保留 `https://...` reference image，不再把所有 reference 都压成 bytes。
- relay 分支会优先传 `image_urls` 给 `/v1/images/generations`。
- relay 分支遇到本地文件/bytes/base64 reference 时不再静默降级为文生图，而是直接报错。
- `CoverDirector` 现在能把 URL reference 原样传给 `llms.image`。

当前结论：

- API 不是完全不支持参考图，它支持“公网 URL 参考图”。
- API 不支持直接参考本地用户图片。
- 要让 Holly 本地素材真正进入 reference，需要增加一个可信上传/托管步骤，将本地素材变成可被 relay 访问的 HTTPS URL。
- 在没有上传/托管步骤前，不能声称本地 Holly 图片已经作为模型 reference 输入成功。
