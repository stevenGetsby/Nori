# Nori 数据采集模块

`data_collect/` 是 Nori 的统一数据采集层，封装多平台爬虫、签名服务、媒体下载。

## 支持平台

| 平台 | 代码 | 搜索 | 详情 | 创作者 | 推荐流 | 签名服务 |
|------|------|------|------|--------|--------|----------|
| 小红书 | `xhs` | ✓ | ✓ | ✓ | – | 需启动 |
| 抖音   | `dy`  | ✓ | ✓ | ✓ | ✓ | 需启动 |
| 快手   | `ks`  | ✓ | ✓ | ✓ | ✓ | 内置   |
| 微博   | `wb`  | ✓ | ✓ | ✓ | – | 内置   |

## 目录结构

```
data_collect/
├── adapter.py        # 统一入口（Nori 调用此处）
├── __init__.py
├── crawler/          # 主爬虫程序（搜索/详情/创作者/推荐）
├── sign/             # 签名服务（xhs/dy 需要，默认端口 8989）
└── downloader/       # 媒体下载服务（默认端口 8990）
```

## 快速使用

```python
from data_collect import DataCollector, SearchRule, DetailRule, DownloadRule

dc = DataCollector()

# 1. 启动签名服务（xhs/dy 必需，ks/wb 可跳过）
dc.start_sign_server()

# 2. 关键词搜索
summary = dc.search(SearchRule(
    platform="xhs",
    keywords=["AI Agent", "小红书运营"],
    max_notes=50,
    enable_comments=False,
))
print(summary)
# {'platform': 'xhs', 'crawler_type': 'search', 'status': 'completed', 'db_path': '...'}

# 3. 详情抓取
dc.fetch_detail(DetailRule(
    platform="xhs",
    urls=["https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"],
))

# 4. 媒体下载
paths = dc.download(DownloadRule(
    platform="xhs",
    targets=["https://www.xiaohongshu.com/explore/xxx"],
    save_dir="./downloads",
))

dc.stop_all()
```

## 高赞素材采集接口

`DataCollector.collect_top_notes` 是给 Nori 上层调用的高层接口。

它在内部组合：

```text
搜索 popular 两页（约 40 条） → JSON 落到 skill data → 合并去重按点赞降序取 top_k → 可选下载封面/图片/视频 → 输出本地路径
```

不写爬虫，不生成内容，统一调用 `search` / `fetch_detail` / `download`。

规则：

```python
@dataclass
class TopNotesRule:
    platform: Platform                  # xhs / dy / ks / wb
    keywords: Sequence[str]             # 搜索关键词
    days: int = 30                      # 已废弃；XHS 实现忽略
    top_k_per_keyword: int = 5          # 每个关键词保留数量
    min_liked: int = 500                # 已废弃；XHS 实现忽略
    pool_size: int = 20                 # 已废弃；XHS 固定抓两页
    download_media: bool = False        # 是否下载封面/图片/视频
    save_dir: str = ""                  # 空值时落到当次 data_dir/media
    data_dir: str = "nori/skill_base/data/xhs_note_analyzer"
```

返回：

```python
@dataclass
class HotNote:
    note_id: str
    title: str
    author_id: str
    author_name: str
    liked: int
    collected: int
    comment: int
    share: int
    cover_path: Optional[str]
    image_paths: list[str]
    video_path: Optional[str]
    note_url: str

@dataclass
class TopNotesResult:
    platform: str
    queries: list[str]
    hot_notes: list[HotNote]
    insufficient: list[dict]
    source_data_dir: str
```

调用示例：

```python
from data_collect import DataCollector, TopNotesRule

dc = DataCollector()
dc.start_sign_server()
result = dc.collect_top_notes(TopNotesRule(
    platform="xhs",
    keywords=["AI Agent", "Agent 工程"],
    top_k_per_keyword=5,
    min_liked=500,
    pool_size=20,
    download_media=True,
))
for n in result.hot_notes:
    print(n.title, n.liked, n.cover_path)
dc.stop_all()
```

接口职能：

```text
把创作目标转成搜索关键词的执行入口。
统一调度搜索、详情、下载三步。
每个关键词抓 popular 两页（约 40 条），合并去重后按点赞降序取 top_k；不做时间窗 / min_liked 过滤。
insufficient 仅在去重后总候选数 < top_k 时上报。
保留 note_url、本地素材路径、source_data_dir。
失败时返回明确错误，不阻塞上层流程。

skill 链路默认使用 JSON，不创建 SQLite。每个关键词单独建目录，目录名为 `日期_关键词`：

```text
nori/skill_base/data/xhs_note_analyzer/holly/
├── <run_id>_session_skill_report.json
├── <run_id>_文创/
│   ├── search_contents_<date>.json   # 缩进后的原始搜索 JSON
│   └── selected_notes.json           # 本关键词入选笔记，可能为空数组
└── <run_id>_怪趣文创_文创品牌/
    ├── search_contents_<date>.json
    ├── selected_notes.json
    └── <note_id>/
        ├── note.json                 # 单篇笔记文本、标签、指标和本地素材路径
        ├── video.mp4                 # 如为视频笔记，视频放在 poster 根目录
        └── images/
            ├── cover.webp            # 封面，给多模态 LLM 直接读取
            ├── image_0.webp
            └── image_1.webp
```
```

不在接口内做：

```text
不判断爆款概率。
不生成正文或图片。
不在 data_collect 内写 LLM 逻辑。
```

## 配置入口

| 文件 | 用途 |
|------|------|
| `crawler/config/base_config.py` | 平台、关键词、爬取数量、评论开关等 |
| `crawler/config/db_config.py`   | SQLite/MySQL/Redis 连接 |
| `crawler/config/proxy_config.py`| IP 代理池 |
| `crawler/config/sign_srv_config.py` | 签名服务地址 |
| `sign/config.py`                | 签名服务监听端口、playwright 模式 |

`DataCollector` 会在每次任务运行前写入运行期配置：

```text
ACCOUNT_POOL_SAVE_TYPE=cookie_bridge
COOKIE_BRIDGE_URL=http://localhost:8274
SIGN_SRV_HOST / SIGN_SRV_PORT 按 DataCollector.sign_url 设置
save_option=db 时才写 DB_TYPE=sqlite / 独立 SQLITE_DB_PATH
save_option=json 时只落 JSON 文件，不打开 SQLite
```

直接用原生 crawler CLI 时仍可用环境变量覆盖；通过 `DataCollector` 调用时，以适配层运行期配置为准。

## 账号 Cookie

默认走 CookieBridge，从浏览器扩展拿当前 cookie。运行前必须满足：

```text
SignSrv 可访问：/signsrv/pong
CookieBridge 可访问：/api/accounts
CookieBridge 中存在目标平台 cookie，例如 xhs
```

如果 CookieBridge 扩展账号列表为空，`DataCollector` 会尝试从本机 Chrome 最近活跃的目标平台 profile 读取 cookie，并写入 CookieBridge 本地缓存；不会打印 cookie 值。旧的 `crawler/config/accounts_cookies.xlsx` 只作为显式设置 `ACCOUNT_POOL_SAVE_TYPE=xlsx` 时的兜底来源。

## CLI 调试

```bash
# 直接运行爬虫
python -m data_collect.crawler.main --platform xhs --type search --keywords "AI Agent"

# 启动签名服务
python -m data_collect.sign.app

# 启动下载服务
python -m data_collect.downloader.DownloadServer.app
```
