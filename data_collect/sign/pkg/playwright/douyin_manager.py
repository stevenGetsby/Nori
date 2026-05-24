# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import asyncio
import logging
from typing import Optional

from playwright.async_api import Page, Playwright
from tenacity import (RetryError, retry, retry_if_result, stop_after_attempt,
                      wait_fixed)

import data_collect.sign.config as config
import data_collect.sign.constant as constant
from data_collect.sign.pkg import utils
from data_collect.sign.pkg.playwright.manager import PlaywrightManager

logger = logging.getLogger(__name__)


class DouYinPlaywrightManager(PlaywrightManager):
    def __init__(self, _async_playwright: Playwright):
        """
        Initialize
        :param _async_playwright:
        """
        super().__init__(constant.DOUYIN_PLATFORM_NAME, _async_playwright)
        self.context_page: Optional[Page] = None

    @retry(stop=stop_after_attempt(120), wait=wait_fixed(1), retry=retry_if_result(lambda value: value is False))
    async def check_slider_captcha_exist(self) -> bool:
        """
        Check if the slider captcha exists
        :return:
        """
        current_page_content = await self.context_page.content()
        if "验证码中间页" in current_page_content:
            logger.info("[DouYinPlaywrightManager.check_slider_captcha_exist] 启动DY浏览器启动时出现验证码，请手动验证")
            return False
        return True

    async def load_page(self):
        """
        Initialize the page
        :return:
        """
        await self.init_browser_context()
        await self.add_fixed_cookies()
        self.context_page = await self.browser_context.new_page()
        await self.context_page.goto(constant.DOUYIN_INDEX_URL)
        await asyncio.sleep(constant.PLAYWRIGHT_INDEX_LOAD_TIME)
        try:
            await self.check_slider_captcha_exist()
            logger.info("[DouYinPlaywrightManager.load_page] Douyin浏览器启动成功，等待APP启动即可提供服务...")
        except RetryError:
            logger.info("[DouYinPlaywrightManager.load_page] Check slider captcha exist failed ...")
            raise RetryError

    async def add_fixed_cookies(self):
        """
        Add fixed cookies
        :return:
        """
        for key, value in utils.convert_str_cookie_to_dict(config.dy_fixed_cookie).items():
            await self.browser_context.add_cookies([{
                'name': key,
                'value': value,
                'domain': ".douyin.com",
                'path': "/"
            }])

    async def reload_page(self):
        """
        Reload the page
        :return:
        """
        await self.reload_browser_context()
        await self.load_page()
