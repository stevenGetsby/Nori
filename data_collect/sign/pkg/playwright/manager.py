# -*- coding: utf-8 -*-
from __future__ import annotations


# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path
from typing import Optional

from playwright.async_api import BrowserContext, Playwright

import data_collect.sign.config as config
from data_collect.sign.pkg import utils


_PKG_ROOT = Path(__file__).resolve().parents[1]


def _resolve_runtime_path(env_name: str, default: Path) -> Path:
    value = os.getenv(env_name)
    path = Path(value).expanduser() if value else default
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


class PlaywrightManager:
    """
    Playwright管理类
    """

    def __init__(self, platform_name: str, async_playwright: Playwright):
        """
        初始化
        :param platform_name: 平台名 constant.XHS_PLATFORM_NAME | constant.DOUYIN_PLATFORM_NAME
        :param async_playwright:
        """
        self.platfrom_name = platform_name
        self.async_playwright = async_playwright
        self.browser_context: Optional[BrowserContext] = None


    async def init_browser_context(self):
        """
        初始化浏览器
        :return:
        """
        self._remove_browser_data()
        user_data_dir = self._browser_data_dir()
        stealth_js_path = _PKG_ROOT / "js" / "stealth.min.js"
        browser_context = await self.async_playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            accept_downloads=True,
            headless=config.playwright_headless,
            viewport={"width": 1920, "height": 1080},
            user_agent=utils.get_user_agent(),
        )
        await browser_context.add_init_script(path=str(stealth_js_path))
        self.browser_context = browser_context

    def _browser_data_dir(self) -> Path:
        root = _resolve_runtime_path("DATA_COLLECT_BROWSER_DATA_DIR", Path.cwd() / "browser_data")
        return root / self.platfrom_name

    def _remove_browser_data(self):
        """
        删除浏览器数据
        :return:
        """
        user_data_dir = self._browser_data_dir()
        if user_data_dir.exists():
            shutil.rmtree(user_data_dir)

    async def reload_browser_context(self):
        """
        重新加载浏览器
        :return:
        """
        self._remove_browser_data()
        await self.init_browser_context()
