# Agent：Account Planner

## 1. 职责

Account Planner 负责做账号规划。

它接收 Intaker 输出的 Intention + Context，生成账号定位和 IP 画像报告。

```text
把 Intention + Context 深化成账号策略。
```

---

## 2. 输入

主输入：

```text
Intention：用户要什么、不要什么
Context：用户有什么资产
```

辅助证据：

```text
文字：品牌理念、产品说明、目标诉求
图片：品牌素材、产品图、风格图、IP 图
链接：店铺、账号、产品、参考内容
搜索：可选开启
```

Account Planner 不重新拆解用户输入。

原始文字、图片和链接只用来补充细节。

链接暂时先作为 Context 保存，不在第一版里抓取网页内容。

---

## 3. 五个小标签

Account Planner 先形成五个简短标签：

```text
赛道：属于什么内容/商业赛道
目标：账号优先服务什么结果
平台：主要经营哪个平台
产品：卖什么或承接什么
定位：账号一句话身份
```

标签要短，方便后续 Agent 使用。

---

## 4. 输出

基础输出五块：

```text
recommended_positioning：推荐账号定位
audience_profile：目标受众画像
content_directions：内容方向建议
benchmark_accounts：对标账号推荐
unique_selling_points：差异化卖点
```

对标账号包含两层：

```text
search_keywords：LLM 根据输入生成的搜索关键词
accounts：搜索或 LLM 推荐出来的参考账号
```

最终形成一份 IP 画像报告：

```text
ip_portrait_report
```

报告包含五块：

```text
account_name_suggestions：账号名建议
account_keywords：账号关键词
content_pillars：账号内容主要支柱
benchmark_creators：对标博主
cover_design_formats：推荐封面图片设计格式
```

这份报告给后续内容策略、封面设计和账号搭建 Agent 使用。

---

## 5. 搜索交接

第一版搜索做成可插拔接口。

```text
不开启搜索：LLM 只给搜索关键词和推荐理由。
开启搜索：用关键词去社交平台搜索，再把结果交给 LLM 总结。
```

后续可接 MediaCrawler：

```text
平台：xhs / dy / bili / zhihu
模式：search
输入：keywords
输出：标题、作者、互动数据、链接、摘要
```

MediaCrawler 参考路径：

```text
文档/reference/MediaCrawler/Crawler/.claude/skills/media-crawler-pro/references/text-crawler.md
```

---

## 6. 当前实现

```text
nori/gen_agents/account_planner.py
```

模型定义：

```text
nori/agent_models/account_planner.py：AccountPlannerInput、AccountPlanResult
```

第一版策略：

```text
LLM 先规划
规则再兜底
搜索接口先预留
输出结构保持稳定
```

已验证：

```text
Holly 真实素材规则规划：通过
Intaker -> Account Planner 链路：通过
IP 画像报告：通过
LLM 调用：通过 mock 验证
搜索 Provider：通过
真实测试日志：写入 log/
```

---

## 7. 日志规则

每次真实 case 测试后，都要把输入和输出写入 `log/`。

日志至少包含：

```text
agent
case
config
input
output
```

公共写入函数：

```text
nori/agent_utils/case_log.py
```

`nori/agent_utils/__init__.py` 只做公共导出。
