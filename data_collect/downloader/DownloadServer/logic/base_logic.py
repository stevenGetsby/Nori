# -*- coding: utf-8 -*-
from typing import Optional

from data_collect.downloader.DownloadServer.abs.abs_api_client import AbstractApiClient
from data_collect.downloader.DownloadServer.models.base_model import PlatformEnum
from data_collect.downloader.DownloadServer.pkg.media_platform_api.media_platform_api import \
    create_media_platform_client


class BaseLogic:
    def __init__(self, platform: PlatformEnum, cookies: str = ""):
        """
        base logic constructor

        Args:
            platform: platform enum
            cookies: cookies
        """
        self.platform = platform
        self.cookies = cookies
        self.api_client: Optional[AbstractApiClient] = None

    async def async_initialize(self, **kwargs):
        """
        async initialize

        Returns:

        """
        self.api_client = await create_media_platform_client(
            self.platform, self.cookies, **kwargs
        )

    async def check_cookies(self) -> bool:
        """
        check cookies is valid

        Returns:
            bool: is valid
        """
        return await self.api_client.pong()
