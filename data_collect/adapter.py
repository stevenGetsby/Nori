"""Nori 数据采集统一适配层

封装 crawler / sign / downloader 三个子服务，供 Nori 主程序按规则调用。

入口类: ``DataCollector``
规则数据类: ``SearchRule`` / ``DetailRule`` / ``CreatorRule`` / ``DownloadRule``
"""
from __future__ import annotations

import asyncio
import os
import signal
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Literal, Optional, Sequence
from urllib.parse import urlparse

import httpx

# --- 类型定义 ---
Platform = Literal["xhs", "dy", "ks", "wb"]
CrawlType = Literal["search", "detail", "creator", "homefeed"]
SaveOption = Literal["db", "csv", "json"]

_ROOT = Path(__file__).resolve().parent
_CRAWLER_DIR = _ROOT / "crawler"
_SIGN_DIR = _ROOT / "sign"
_DOWNLOADER_DIR = _ROOT / "downloader" / "DownloadServer"


# --- 规则定义 ---

SearchSort = Literal["general", "popular", "latest"]

@dataclass
class SearchRule:
    """关键词搜索规则"""
    platform: Platform
    keywords: Sequence[str]
    max_notes: int = 50
    sort: SearchSort = "general"          # 平台搜索排序：综合 / 最热 / 最新
    enable_comments: bool = False
    enable_sub_comments: bool = False
    save_option: SaveOption = "db"
    data_dir: str = ""
    sqlite_path: str = ""


@dataclass
class TopNotesRule:
    """高赞素材采集规则（上层接口）

    XHS 行为：每关键词抓 popular 两页（约 40 条），合并去重后按点赞数降序取 top_k。
    不做时间窗 / min_liked 过滤；下列 days / min_liked / pool_size 字段保留向后兼容但被 XHS 实现忽略。
    insufficient 仅在去重后总候选数 < top_k 时上报。
    """
    platform: Platform
    keywords: Sequence[str]
    days: int = 30                          # 已废弃；XHS 实现忽略
    top_k_per_keyword: int = 5              # 每关键词保留多少篇
    min_liked: int = 500                    # 已废弃；XHS 实现忽略
    pool_size: int = 20                     # 已废弃；XHS 固定抓两页（约 40 条）
    download_media: bool = False            # 是否下载封面/图集/视频
    save_dir: str = ""                      # 默认落到当次 data_dir/media
    data_dir: str = "nori/skill_base/data/xhs_note_analyzer"


@dataclass
class HotNote:
    """单篇高赞笔记结构"""
    note_id: str
    keyword: str
    title: str
    desc: str
    author_id: str
    author_name: str
    liked: int
    collected: int
    comment: int
    share: int
    tags: List[str]
    image_count: int
    note_type: str
    note_url: str
    time_ms: int
    cover_path: Optional[str] = None
    image_paths: List[str] = field(default_factory=list)
    video_path: Optional[str] = None
    visual_style: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "note_id": self.note_id,
            "keyword": self.keyword,
            "title": self.title,
            "desc": self.desc,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "liked": self.liked,
            "collected": self.collected,
            "comment": self.comment,
            "share": self.share,
            "tags": list(self.tags),
            "image_count": self.image_count,
            "note_type": self.note_type,
            "note_url": self.note_url,
            "time_ms": self.time_ms,
            "cover_path": self.cover_path,
            "image_paths": list(self.image_paths),
            "video_path": self.video_path,
            "visual_style": dict(self.visual_style),
        }


@dataclass
class TopNotesResult:
    """高赞采集结果"""
    platform: str
    queries: List[str]
    hot_notes: List[HotNote]
    insufficient: List[dict] = field(default_factory=list)
    source_data_dir: str = ""
    source_keyword_dirs: dict[str, str] = field(default_factory=dict)
    source_db: str = ""

    def to_dict(self) -> dict:
        data = {
            "platform": self.platform,
            "queries": list(self.queries),
            "hot_notes": [n.to_dict() for n in self.hot_notes],
            "insufficient": list(self.insufficient),
            "source_data_dir": self.source_data_dir,
            "source_keyword_dirs": dict(self.source_keyword_dirs),
        }
        if self.source_db:
            data["source_db"] = self.source_db
        return data

@dataclass
class DetailRule:
    """笔记/视频详情抓取规则"""
    platform: Platform
    urls: Sequence[str]
    enable_comments: bool = True
    save_option: SaveOption = "db"
    sqlite_path: str = ""

@dataclass
class CreatorRule:
    """创作者主页抓取规则"""
    platform: Platform
    creator_urls: Sequence[str]
    include_posts: bool = True
    include_comments: bool = False
    save_option: SaveOption = "db"
    sqlite_path: str = ""

@dataclass
class HomefeedRule:
    """首页推荐流抓取规则（仅 dy/ks 完整支持）"""
    platform: Platform
    max_notes: int = 50
    save_option: SaveOption = "db"
    sqlite_path: str = ""

@dataclass
class DownloadRule:
    """媒体文件下载规则"""
    platform: Platform
    targets: Sequence[str]            # 笔记/视频 ID 或 URL
    save_dir: str = "./downloads"
    include_video: bool = True
    include_images: bool = True
    include_cover: bool = True


# --- 主入口 ---

class _ServiceHandle:
    """轻量子进程句柄"""
    def __init__(self, name: str, proc: subprocess.Popen):
        self.name = name
        self.proc = proc

    def stop(self) -> None:
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGTERM)
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class DataCollector:
    """Nori 数据采集统一入口

    使用：

        from data_collect import DataCollector, SearchRule
        dc = DataCollector()
        dc.start_sign_server()                       # 启动签名服务（xhs/dy 需要）
        results = dc.search(SearchRule(
            platform="xhs",
            keywords=["AI Agent"],
            max_notes=50,
        ))
        dc.stop_all()
    """

    SIGN_PORT = 8989
    DOWNLOAD_PORT = 8990

    def __init__(
        self,
        sign_url: str = "http://127.0.0.1:8989",
        downloader_url: str = "http://127.0.0.1:8990",
        cookie_bridge_url: str | None = None,
        account_pool_save_type: str | None = None,
        auto_seed_cookie_bridge: bool | None = None,
        runtime_dir: str | Path = "data_collect/runtime",
        python_bin: str = sys.executable,
        project_root: Optional[Path] = None,
    ):
        self.sign_url = sign_url.rstrip("/")
        self.downloader_url = downloader_url.rstrip("/")
        self.sign_host, self.sign_port = _host_port(self.sign_url, self.SIGN_PORT)
        self.downloader_host, self.downloader_port = _host_port(self.downloader_url, self.DOWNLOAD_PORT)
        self.cookie_bridge_url = (cookie_bridge_url or os.getenv("COOKIE_BRIDGE_URL", "http://localhost:8274")).rstrip("/")
        self.account_pool_save_type = account_pool_save_type or os.getenv("ACCOUNT_POOL_SAVE_TYPE", "cookie_bridge")
        if auto_seed_cookie_bridge is None:
            auto_seed_cookie_bridge = os.getenv("DATA_COLLECT_AUTO_BROWSER_COOKIE", "1").lower() not in {"0", "false", "no"}
        self.auto_seed_cookie_bridge = auto_seed_cookie_bridge
        self.python_bin = python_bin
        self.project_root = project_root or _ROOT.parent
        runtime_path = Path(runtime_dir).expanduser()
        if not runtime_path.is_absolute():
            runtime_path = self.project_root / runtime_path
        self.runtime_dir = runtime_path
        self._services: dict[str, _ServiceHandle] = {}

    # ============ 服务管理 ============

    def start_sign_server(self, port: int | None = None, wait_ready: bool = True) -> None:
        """启动签名服务（端口默认 8989）。已运行则跳过。

        注意 cwd 设为 ``data_collect/sign``：上游 sign 库里
        ``DouyinJavascriptSign`` 用 ``Path('pkg/js/douyin.js')``
        相对路径加载 JS，需要在该目录下运行。
        """
        if self.is_sign_alive():
            return
        port = port or self.sign_port
        env = self._child_env()
        env["APP_PORT"] = str(port)
        sign_cwd = self.project_root / "data_collect" / "sign"
        proc = subprocess.Popen(
            [self.python_bin, "-m", "data_collect.sign.app"],
            cwd=str(sign_cwd),
            env=env,
        )
        self._services["sign"] = _ServiceHandle("sign", proc)
        if wait_ready:
            self._wait_http(f"{self.sign_url}/signsrv/pong", timeout=30)

    def start_downloader(self, port: int | None = None, wait_ready: bool = True) -> None:
        """启动下载服务（端口默认 8990）。已运行则跳过。"""
        if self.is_downloader_alive():
            return
        port = port or self.downloader_port
        env = self._child_env()
        env["APP_PORT"] = str(port)
        proc = subprocess.Popen(
            [self.python_bin, "-m", "data_collect.downloader.DownloadServer.app"],
            cwd=str(self.project_root),
            env=env,
        )
        self._services["downloader"] = _ServiceHandle("downloader", proc)
        if wait_ready:
            self._wait_http(f"{self.downloader_url}/ping", timeout=30)

    def stop_all(self) -> None:
        """停止所有由本实例启动的子服务"""
        for h in list(self._services.values()):
            h.stop()
        self._services.clear()

    def health_check(self, platform: Platform = "xhs") -> dict:
        return {
            "sign": self.is_sign_alive(),
            "downloader": self.is_downloader_alive(),
            "cookie_bridge": self._cookie_bridge_status(platform),
        }

    def is_sign_alive(self) -> bool:
        return self._http_ok(f"{self.sign_url}/signsrv/pong")

    def is_downloader_alive(self) -> bool:
        return self._http_ok(f"{self.downloader_url}/ping")

    # ============ 爬取接口 ============

    def search(self, rule: SearchRule) -> dict:
        """关键词搜索抓取"""
        platform_adapter = self._platform_adapter(rule.platform)
        if platform_adapter is not None:
            return platform_adapter.search(rule)
        return self._run_crawler(
            platform=rule.platform,
            crawler_type="search",
            keywords=",".join(rule.keywords),
            sort=rule.sort,
            enable_comments=rule.enable_comments,
            enable_sub_comments=rule.enable_sub_comments,
            save_option=rule.save_option,
            data_dir=rule.data_dir,
            sqlite_path=rule.sqlite_path,
            max_notes=rule.max_notes,
        )

    def fetch_detail(self, rule: DetailRule) -> dict:
        """详情页抓取（多个 URL/ID）"""
        return self._run_crawler(
            platform=rule.platform,
            crawler_type="detail",
            urls=",".join(rule.urls),
            enable_comments=rule.enable_comments,
            save_option=rule.save_option,
            sqlite_path=rule.sqlite_path,
        )

    def fetch_creator(self, rule: CreatorRule) -> dict:
        """创作者主页抓取"""
        return self._run_crawler(
            platform=rule.platform,
            crawler_type="creator",
            urls=",".join(rule.creator_urls),
            enable_comments=rule.include_comments,
            save_option=rule.save_option,
            sqlite_path=rule.sqlite_path,
        )

    def fetch_homefeed(self, rule: HomefeedRule) -> dict:
        """首页推荐流抓取（仅部分平台支持）"""
        return self._run_crawler(
            platform=rule.platform,
            crawler_type="homefeed",
            save_option=rule.save_option,
            sqlite_path=rule.sqlite_path,
            max_notes=rule.max_notes,
        )

    # ============ 下载接口 ============

    def download(self, rule: DownloadRule) -> List[str]:
        """同步下载多个目标的媒体文件，返回保存路径列表"""
        platform_adapter = self._platform_adapter(rule.platform)
        if platform_adapter is None:
            raise NotImplementedError(f"download 暂未支持平台: {rule.platform}")
        return platform_adapter.download(rule)

    def batch_download(self, rules: Iterable[DownloadRule]) -> dict:
        """批量下载，返回 {target: [paths]}"""
        out = {}
        for rule in rules:
            out[",".join(rule.targets)] = self.download(rule)
        return out

    # ============ 高层接口 ============

    def collect_top_notes(self, rule: TopNotesRule) -> TopNotesResult:
        """按平台收集高赞素材；平台细节由 data_collect/platforms/*.py 实现。"""
        platform_adapter = self._platform_adapter(rule.platform)
        if platform_adapter is None:
            raise NotImplementedError(f"collect_top_notes 暂未支持平台: {rule.platform}")
        return platform_adapter.collect_top_notes(rule)

    def _platform_adapter(self, platform: Platform):
        if platform == "xhs":
            from data_collect.platforms.xhs import XHSPlatformAdapter

            return XHSPlatformAdapter(self)
        return None

    # ============ 内部辅助 ============

    def _run_crawler(
        self,
        platform: Platform,
        crawler_type: CrawlType,
        keywords: str = "",
        urls: str = "",
        sort: Optional[str] = None,
        enable_comments: bool = False,
        enable_sub_comments: bool = False,
        save_option: SaveOption = "db",
        data_dir: str | Path | None = None,
        sqlite_path: str | Path | None = None,
        max_notes: Optional[int] = None,
    ) -> dict:
        """直接调用 crawler 子模块（同进程 in-process 调用）。"""
        from data_collect.crawler import config as _config
        from data_collect.crawler.config import db_config as _db_config
        from data_collect.crawler.config import sign_srv_config as _sign_srv_config

        sqlite_file = self._resolve_sqlite_path(platform, crawler_type, sqlite_path) if save_option == "db" else None
        self._apply_runtime_config(_config, _db_config, _sign_srv_config, sqlite_file)
        self._ensure_runtime_ready(platform)

        _config.PLATFORM = platform
        _config.CRAWLER_TYPE = crawler_type
        _config.SAVE_DATA_OPTION = save_option
        _config.ENABLE_GET_COMMENTS = enable_comments
        _config.ENABLE_GET_SUB_COMMENTS = enable_sub_comments
        if keywords:
            _config.KEYWORDS = keywords
        if max_notes is not None:
            _config.CRAWLER_MAX_NOTES_COUNT = max_notes
        if sort is not None:
            _config.SORT_TYPE = sort
        if urls:
            self._apply_url_override(platform, crawler_type, [u.strip() for u in urls.split(",") if u.strip()])
        if save_option == "json" and data_dir:
            self._apply_json_store_path(platform, Path(data_dir))

        summary: dict = {
            "platform": platform,
            "crawler_type": crawler_type,
            "status": "pending",
            "account_pool_save_type": _config.ACCOUNT_POOL_SAVE_TYPE,
            "cookie_bridge_url": _config.COOKIE_BRIDGE_URL,
            "sign_server": f"http://{_config.SIGN_SRV_HOST}:{_config.SIGN_SRV_PORT}",
        }
        if sqlite_file is not None:
            summary["sqlite_path"] = str(sqlite_file)

        from data_collect.crawler import db as _db
        from data_collect.crawler.main import CrawlerFactory

        async def _run():
            need_db = save_option == "db"
            if need_db:
                await _db.init_db()
            crawler = CrawlerFactory.create_crawler(platform=platform)
            await crawler.async_initialize()
            try:
                await crawler.start()
                summary["status"] = "completed"
            except Exception as e:
                summary["status"] = "failed"
                summary["error"] = str(e)
            finally:
                if need_db:
                    await _db.close()

        try:
            asyncio.run(_run())
        except RuntimeError:
            # 已有 event loop（如 Jupyter）
            loop = asyncio.get_event_loop()
            loop.run_until_complete(_run())

        if save_option == "db":
            summary["db_path"] = os.path.abspath(_db_config.SQLITE_DB_PATH)
        if save_option == "json" and data_dir:
            summary["data_dir"] = str(Path(data_dir).expanduser().resolve())
        return summary

    def _resolve_sqlite_path(self, platform: Platform, crawler_type: CrawlType, sqlite_path: str | Path | None) -> Path:
        if sqlite_path:
            path = Path(sqlite_path).expanduser()
            if not path.is_absolute():
                path = self.project_root / path
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = self.runtime_dir / "sqlite" / platform / f"{crawler_type}_{stamp}.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _apply_runtime_config(self, config_module, db_config_module, sign_config_module, sqlite_path: Path | None) -> None:
        config_module.ACCOUNT_POOL_SAVE_TYPE = self.account_pool_save_type
        config_module.COOKIE_BRIDGE_URL = self.cookie_bridge_url
        config_module.SIGN_SRV_HOST = self.sign_host
        config_module.SIGN_SRV_PORT = str(self.sign_port)
        config_module.ENABLE_CHECKPOINT = False

        if sqlite_path is not None:
            config_module.DB_TYPE = "sqlite"
            config_module.SQLITE_DB_PATH = str(sqlite_path)
            db_config_module.DB_TYPE = "sqlite"
            db_config_module.SQLITE_DB_PATH = str(sqlite_path)

        sign_config_module.SIGN_SRV_HOST = self.sign_host
        sign_config_module.SIGN_SRV_PORT = str(self.sign_port)

        self._refresh_sign_client_endpoint(config_module)

    def _ensure_runtime_ready(self, platform: Platform) -> None:
        if self._platform_uses_sign(platform):
            self.start_sign_server()
            if not self.is_sign_alive():
                raise RuntimeError(f"SignSrv 未就绪: {self.sign_url}/signsrv/pong")
        if self.account_pool_save_type == "cookie_bridge":
            self._ensure_cookie_bridge_ready(platform)

    @staticmethod
    def _platform_uses_sign(platform: Platform) -> bool:
        return platform in {"xhs", "dy", "ks"}

    def _cookie_bridge_status(self, platform: Platform) -> dict:
        if self.account_pool_save_type != "cookie_bridge":
            return {"required": False, "available": None, "url": self.cookie_bridge_url}
        try:
            resp = httpx.get(f"{self.cookie_bridge_url}/api/accounts", timeout=3)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            return {
                "required": True,
                "alive": False,
                "available": False,
                "url": self.cookie_bridge_url,
                "error": str(exc),
            }
        accounts = data.get("data", {}).get("accounts", []) if isinstance(data, dict) else []
        available_accounts = [
            item for item in accounts
            if isinstance(item, dict)
            and isinstance(item.get("platforms"), dict)
            and item["platforms"].get(platform, {}).get("has_cookies")
        ]
        cookie_status = self._cookie_bridge_cookie_status(platform)
        return {
            "required": True,
            "alive": bool(data.get("isok")) if isinstance(data, dict) else False,
            "available": bool(available_accounts) or bool(cookie_status.get("available")),
            "url": self.cookie_bridge_url,
            "platform": platform,
            "account_count": len(available_accounts),
            "cookie_endpoint": cookie_status,
        }

    def _ensure_cookie_bridge_ready(self, platform: Platform) -> None:
        status = self._cookie_bridge_status(platform)
        if not status.get("alive"):
            raise RuntimeError(
                f"CookieBridge 未就绪: {self.cookie_bridge_url}/api/accounts; "
                f"请先启动 CookieBridge，并确认浏览器扩展已连接。error={status.get('error', '')}"
            )
        should_seed = not status.get("available") or self._should_refresh_cookie_bridge_seed(status)
        if self.auto_seed_cookie_bridge and should_seed:
            if self._seed_cookie_bridge_from_browser(platform):
                status = self._cookie_bridge_status(platform)
                if status.get("available"):
                    return
        if not status.get("available"):
            raise RuntimeError(
                f"CookieBridge 中没有可用 {platform} cookie: {self.cookie_bridge_url}; "
                "请确认浏览器已登录目标平台，且扩展已同步 cookie，或允许 browser-cookie3 读取本机浏览器 cookie。"
            )

    @staticmethod
    def _should_refresh_cookie_bridge_seed(status: dict) -> bool:
        endpoint = status.get("cookie_endpoint") if isinstance(status, dict) else {}
        if not isinstance(endpoint, dict):
            return False
        return (
            status.get("account_count") == 0
            and endpoint.get("available")
            and endpoint.get("client_id") == "local_browser"
        )

    def _cookie_bridge_cookie_status(self, platform: Platform) -> dict:
        try:
            resp = httpx.get(f"{self.cookie_bridge_url}/api/cookies/{platform}", timeout=5)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            return {"available": False, "error": str(exc)}
        payload = data.get("data", {}) if isinstance(data, dict) else {}
        return {
            "available": bool(data.get("isok")) and bool(payload.get("cookies")),
            "source": payload.get("source"),
            "client_id": payload.get("client_id"),
            "msg": data.get("msg") if isinstance(data, dict) else "",
        }

    def _seed_cookie_bridge_from_browser(self, platform: Platform) -> bool:
        cookie_string, cookie_count = self._browser_cookie_string(platform)
        if not cookie_string:
            return False
        try:
            resp = httpx.post(
                f"{self.cookie_bridge_url}/api/cookies/{platform}/set",
                json={"cookies": cookie_string, "client_id": "local_browser"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return False
        return bool(data.get("isok")) and cookie_count > 0

    def _platform_cookie_string(self, platform: Platform) -> str:
        if self.account_pool_save_type == "cookie_bridge":
            status = self._cookie_bridge_status(platform)
            if not status.get("available") or self._should_refresh_cookie_bridge_seed(status):
                self._seed_cookie_bridge_from_browser(platform)
            try:
                resp = httpx.get(f"{self.cookie_bridge_url}/api/cookies/{platform}", timeout=5)
                resp.raise_for_status()
                data = resp.json()
                payload = data.get("data", {}) if isinstance(data, dict) else {}
                cookies = payload.get("cookies") or ""
                if cookies:
                    return str(cookies)
            except Exception:
                pass
        cookie_string, _ = self._browser_cookie_string(platform)
        return cookie_string

    @staticmethod
    def _browser_cookie_string(platform: Platform) -> tuple[str, int]:
        domain_map = {
            "xhs": ".xiaohongshu.com",
            "dy": ".douyin.com",
            "ks": ".kuaishou.com",
            "wb": ".weibo.com",
        }
        domain = domain_map.get(platform)
        if not domain:
            return "", 0
        required_names = {"xhs": {"web_session", "a1"}}.get(platform, set())
        candidates = DataCollector._chrome_cookie_candidates(domain, required_names)

        try:
            import browser_cookie3
        except Exception:
            return "", 0

        for cookie_file, key_file in candidates:
            try:
                cookie_jar = browser_cookie3.chrome(
                    cookie_file=str(cookie_file) if cookie_file else None,
                    key_file=str(key_file) if key_file else None,
                    domain_name=domain,
                )
            except Exception:
                continue
            cookies = [(cookie.name, cookie.value) for cookie in cookie_jar if cookie.name and cookie.value]
            if required_names and not required_names.issubset({name for name, _ in cookies}):
                continue
            cookie_string = "; ".join(f"{name}={value}" for name, value in cookies)
            if cookie_string:
                return cookie_string, len(cookies)
        return "", 0

    @staticmethod
    def _chrome_cookie_candidates(domain: str, required_names: set[str]) -> list[tuple[Path | None, Path | None]]:
        explicit_file = os.getenv("DATA_COLLECT_CHROME_COOKIE_FILE")
        explicit_profile = os.getenv("DATA_COLLECT_CHROME_PROFILE")

        chrome_root = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
        key_file = chrome_root / "Local State"
        candidates: list[tuple[int, int, int, Path | None, Path | None]] = []

        if explicit_file:
            cookie_file = Path(explicit_file).expanduser()
            candidates.append((1, 0, 0, cookie_file, key_file if key_file.exists() else None))
        if explicit_profile:
            cookie_file = DataCollector._profile_cookie_file(chrome_root / explicit_profile)
            if cookie_file:
                candidates.append((1, 0, 0, cookie_file, key_file if key_file.exists() else None))

        if chrome_root.exists():
            for profile_dir in chrome_root.iterdir():
                cookie_file = DataCollector._profile_cookie_file(profile_dir)
                if not cookie_file:
                    continue
                has_required, last_access, count = DataCollector._chrome_cookie_metadata(
                    cookie_file,
                    domain,
                    required_names,
                )
                if count:
                    candidates.append((has_required, last_access, count, cookie_file, key_file if key_file.exists() else None))

        candidates.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
        result = [(cookie_file, key_file) for _, _, _, cookie_file, key_file in candidates]
        result.append((None, None))
        return result

    @staticmethod
    def _profile_cookie_file(profile_dir: Path) -> Path | None:
        for relative in ("Network/Cookies", "Cookies"):
            cookie_file = profile_dir / relative
            if cookie_file.exists():
                return cookie_file
        return None

    @staticmethod
    def _chrome_cookie_metadata(cookie_file: Path, domain: str, required_names: set[str]) -> tuple[int, int, int]:
        try:
            import sqlite3

            con = sqlite3.connect(f"file:{cookie_file}?mode=ro", uri=True)
            rows = con.execute(
                """
                select name, last_access_utc
                from cookies
                where host_key like ?
                """,
                (f"%{domain.lstrip('.')}",),
            ).fetchall()
            con.close()
        except Exception:
            return 0, 0, 0
        names = {name for name, _ in rows}
        has_required = int(not required_names or required_names.issubset(names))
        last_access = max((int(last_access or 0) for _, last_access in rows), default=0)
        return has_required, last_access, len(rows)

    def _refresh_sign_client_endpoint(self, config_module) -> None:
        module = sys.modules.get("data_collect.crawler.pkg.rpc.sign_srv_client.sign_client")
        if not module:
            return
        endpoint = f"http://{config_module.SIGN_SRV_HOST}:{config_module.SIGN_SRV_PORT}"
        setattr(module, "SIGN_SERVER_URL", endpoint)

    @staticmethod
    def _apply_json_store_path(platform: Platform, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        if platform == "xhs":
            from data_collect.crawler.repo.platform_save_data.xhs.xhs_store_impl import (
                XhsJsonStoreImplement,
                calculate_number_of_files,
            )

            path = str(data_dir)
            XhsJsonStoreImplement.json_store_path = path
            XhsJsonStoreImplement.file_count = calculate_number_of_files(path)

    @staticmethod
    def _apply_url_override(platform: Platform, crawler_type: str, urls: List[str]) -> None:
        from data_collect.crawler import config as _config
        detail_map = {
            "xhs": "XHS_SPECIFIED_NOTE_URL_LIST",
            "dy": "DY_SPECIFIED_ID_LIST",
            "ks": "KS_SPECIFIED_ID_LIST",
            "wb": "WEIBO_SPECIFIED_ID_LIST",
        }
        creator_map = {
            "xhs": "XHS_CREATOR_URL_LIST",
            "dy": "DY_CREATOR_ID_LIST",
            "ks": "KS_CREATOR_ID_LIST",
            "wb": "WEIBO_CREATOR_ID_LIST",
        }
        if crawler_type == "detail":
            attr = detail_map.get(platform)
        elif crawler_type == "creator":
            attr = creator_map.get(platform)
        else:
            return
        if attr and hasattr(_config, attr):
            setattr(_config, attr, urls)

    def _child_env(self) -> dict:
        env = os.environ.copy()
        existing = env.get("PYTHONPATH", "")
        root = str(self.project_root)
        env["PYTHONPATH"] = root if not existing else f"{root}{os.pathsep}{existing}"
        env["ACCOUNT_POOL_SAVE_TYPE"] = self.account_pool_save_type
        env["COOKIE_BRIDGE_URL"] = self.cookie_bridge_url
        env["SIGN_SRV_HOST"] = self.sign_host
        env["SIGN_SRV_PORT"] = str(self.sign_port)
        return env

    def _http_ok(self, url: str) -> bool:
        try:
            r = httpx.get(url, timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def _wait_http(self, url: str, timeout: int = 30) -> None:
        import time
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._http_ok(url):
                return
            time.sleep(0.5)
        raise TimeoutError(f"service not ready: {url}")


__all__ = [
    "DataCollector",
    "SearchRule",
    "DetailRule",
    "CreatorRule",
    "HomefeedRule",
    "DownloadRule",
    "TopNotesRule",
    "HotNote",
    "TopNotesResult",
    "Platform",
    "CrawlType",
    "SearchSort",
]


def _host_port(url: str, default_port: int) -> tuple[str, int]:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or default_port
    return host, port
