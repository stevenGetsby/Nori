# Holly Live Case Summary

- Run dir: `/Users/geminilight/projects/product/Nori/cases/HollyBackendAPI/runs/20260608_015425_holly_backend_api_content_generation`
- LLM: `lumina::gpt-5.5`
- Image: `relay::gpt-image-2`
- XHS keywords: 怪趣文创, 反焦虑文创
- Hot notes collected: 2

## Market Evidence
- `怪趣文创` 我的冰箱新护法➕1……🐾 | liked=26000 collected=6486 comments=562
  https://www.xiaohongshu.com/explore/68a0272b000000001c00d1ed?xsec_token=AB-rb6sWOxqJimjzW85jpNxhDPWe3ij-6t_D79TEOXH5A=&xsec_source=pc_search
- `反焦虑文创` 你正在焦虑的事终会迎来好结果 | liked=1716 collected=71 comments=997
  https://www.xiaohongshu.com/explore/69e9ce140000000013030800?xsec_token=ABZE8c0WcuHSYJ6ZI4b4GIYR8-bezMy7FpmrDqkwHtf1Q=&xsec_source=pc_search

## Learned Note Skills
- 种草推荐·朋友安利: goal=planting, tone=朋友安利, evidence=1
- 观点输出·治愈: goal=opinion, tone=治愈, evidence=1

## Account Direction
做一个用屎尿屁幽默讲反焦虑哲学的文创品牌主理人账号，既分享产品背后的荒诞灵感，也输出年轻人合法松弛的情绪价值。

## Selected Task
- 第 1 天｜Holly Shit 不是低俗玩梗，是反焦虑快乐哲学
- topic: 品牌第一条认知内容：解释“Shit人生也要拉得开心”
- objective: 让用户快速理解品牌核心：用荒诞幽默回收焦虑、时间和身体自主权，同时避免被误解为低俗猎奇。

## Generated Note
- title: 4句嘴替：厕所时间神圣
- tags: HollyShit 反焦虑 打工人 文创IP 松弛感
- cover: `/Users/geminilight/projects/product/Nori/cases/HollyBackendAPI/runs/20260608_015425_holly_backend_api_content_generation/covers/cover_种草推荐_朋友安利笔记制作指南_20260608_020146.png`

上班最崩溃的时刻，可能不是被安排活，而是连喘口气的时间都要被催。

最近看到一个很怪但很会说人话的学生文创/IP：Holly Shit 开心拉屎。
它的 Slogan 是：Shit人生也要拉的开心。

先说清楚：它不是为了恶心人，也不是靠低俗猎奇博眼球。
它更像是用一种“不太体面”的语言，替我们讲一个很体面的诉求：
我需要一点不被打扰的时间，我需要一点身体自主权，我需要一点合法躺平的松弛感。

我理解它的方式是这 4 句：

1️⃣ 厕所时间神圣不可侵犯
不是偷懒，不是摸鱼，是成年人给自己按下的暂停键。

2️⃣ Shit人生，也要拉得开心
生活已经够乱了，至少允许自己用一点荒诞幽默，把焦虑回收掉。

3️⃣ 不体面的梗，讲体面的事
它讲的不是“脏”，而是：别催我、别监控我、别把每一秒都榨干。

4️⃣ GET SHIT DOWN，不等于把自己榨干
事情可以做完，但人也要保住。打工人的尊严，有时候就藏在那几分钟安静里。

这个项目来自同济大学设计创意学院的学生，一周时间仓促做了几个文创产品。很有意思的是：市集上大家能秒懂、会笑、会买单；但放到线上，可能就容易被误解成“只是便便梗”。

所以第一条想认真替它解释一下：
Holly Shit 的怪趣，不是为了让你皱眉，而是让你笑着把焦虑吐槽出去。
它卖的也不只是文创，而是一种年轻人的小小反叛：
“我可以把日子过得一地鸡毛，但我不交出自己的喘息权。”

建议收藏这几句，当你不想解释但很想发疯时的嘴替。

你最想保护哪段厕所时间？上班、上课、回家后，还是睡前？

## Review
- compliance: passed; issues=0
- consistency: blocked; issues=4
  - medium: 标题或正文没有体现任务主题
  - medium: 正文没有体现任务目标
  - medium: 封面 prompt 没有体现标题或封面标题
  - low: 客户品牌名没有出现在内容或封面 prompt 中

## Quality Notes
- 产出已经接入真实小红书搜索结果、真实 LLM、真实图片模型；market evidence 可回溯到 `xhs_top_notes_result.json` 和各 keyword 目录。
- 当前样本量适合端到端 smoke/live case，不足以作为稳定内容策略结论。
- 下一步优化应扩大关键词和 top_k，增加竞品账号维度，并对封面进行多候选 A/B 生成与人工选择。
