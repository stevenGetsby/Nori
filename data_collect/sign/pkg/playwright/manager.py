# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import os
import shutil
from typing import Optional

from playwright.async_api import BrowserContext, Playwright

import data_collect.sign.config as config
from data_collect.sign.pkg import utils


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
        user_data_dir = os.path.join(os.getcwd(), "browser_data", self.platfrom_name)
        stealth_js_path = os.path.join(os.getcwd(), "pkg/js/stealth.min.js")
        browser_context = await self.async_playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            accept_downloads=True,
            headless=config.playwright_headless,
            viewport={"width": 1920, "height": 1080},
            user_agent=utils.get_user_agent(),
        )
        await browser_context.add_init_script(path=stealth_js_path)
        self.browser_context = browser_context

    def _remove_browser_data(self):
        """
        删除浏览器数据
        :return:
        """
        user_data_dir = os.path.join(os.getcwd(), "browser_data", self.platfrom_name)
        if os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir)

    async def reload_browser_context(self):
        """
        重新加载浏览器
        :return:
        """
        self._remove_browser_data()
        await self.init_browser_context()
