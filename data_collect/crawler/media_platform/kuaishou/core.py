# -*- coding: utf-8 -*-


import asyncio
from typing import Optional

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.base.base_crawler import AbstractCrawler
from data_collect.crawler.pkg.account_pool.pool import AccountWithIpPoolManager
from data_collect.crawler.pkg.proxy.proxy_ip_pool import ProxyIpPool, create_ip_pool
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
from data_collect.crawler.repo.checkpoint import create_checkpoint_manager
from data_collect.crawler.var import crawler_type_var

from .client import KuaiShouApiClient
from .handlers import SearchHandler, DetailHandler, CreatorHandler, HomefeedHandler
from .processors import VideoProcessor, CommentProcessor


class KuaiShouCrawler(AbstractCrawler):
    def __init__(self) -> None:
        self.ks_client = KuaiShouApiClient()
        self.checkpoint_manager: CheckpointRepoManager = create_checkpoint_manager()

        # 限制并发数
        self.crawler_video_task_semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        self.crawler_comment_semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)

        # Initialize processors with dependency injection
        self.video_processor = VideoProcessor(
            self.ks_client,
            self.checkpoint_manager,
            self.crawler_video_task_semaphore
        )
        self.comment_processor = CommentProcessor(
            self.ks_client,
            self.checkpoint_manager,
            self.crawler_comment_semaphore
        )

        # Initialize handlers with dependency injection
        self.search_handler = SearchHandler(
            self.ks_client,
            self.checkpoint_manager,
            self.video_processor,
            self.comment_processor
        )
        self.detail_handler = DetailHandler(
            self.ks_client,
            self.checkpoint_manager,
            self.video_processor,
            self.comment_processor
        )
        self.creator_handler = CreatorHandler(
            self.ks_client,
            self.checkpoint_manager,
            self.video_processor,
            self.comment_processor
        )
        self.homefeed_handler = HomefeedHandler(
            self.ks_client,
            self.checkpoint_manager,
            self.video_processor,
            self.comment_processor
        )

    async def async_initialize(self):
        """
        Asynchronous Initialization
        Returns:

        """
        utils.logger.info(
            "[KuaiShouCrawler.async_initialize] Begin async initialize"
        )

        # 账号池和IP池的初始化
        proxy_ip_pool: Optional[ProxyIpPool] = None
        if config.ENABLE_IP_PROXY:
            # 快手对代理验证还行，可以选择长时长的IP，比如30分钟一个IP
            # 快代理：私密代理->按IP付费->专业版->IP有效时长为30分钟, 购买地址：https://www.kuaidaili.com/?ref=ldwkjqipvz6c
            proxy_ip_pool = await create_ip_pool(
                config.IP_PROXY_POOL_COUNT, enable_validate_ip=True
            )

        # 初始化账号池
        account_with_ip_pool = AccountWithIpPoolManager(
            platform_name=constant.KUAISHOU_PLATFORM_NAME,
            account_save_type=config.ACCOUNT_POOL_SAVE_TYPE,
            proxy_ip_pool=proxy_ip_pool,
        )
        await account_with_ip_pool.async_initialize()

        self.ks_client.account_with_ip_pool = account_with_ip_pool
        await self.ks_client.update_account_info()

        # 设置爬虫类型
        crawler_type_var.set(config.CRAWLER_TYPE)

    async def start(self) -> None:
        """
        Start crawler
        Returns:

        """
        if config.CRAWLER_TYPE == constant.CRALER_TYPE_SEARCH:
            # Search for notes and retrieve their comment information.
            await self.search_handler.handle()
        elif config.CRAWLER_TYPE == constant.CRALER_TYPE_DETAIL:
            # Get the information and comments of the specified post
            await self.detail_handler.handle()
        elif config.CRAWLER_TYPE == constant.CRALER_TYPE_CREATOR:
            # Get the information and comments of the specified creator
            await self.creator_handler.handle()
        elif config.CRAWLER_TYPE == constant.CRALER_TYPE_HOMEFEED:
            # Get the information and comments of the specified creator
            await self.homefeed_handler.handle()
        else:
            raise NotImplementedError(
                f"[KuaiShouCrawler.start] Not support crawler type: {config.CRAWLER_TYPE}"
            )
        utils.logger.info("[KuaiShouCrawler.start] Kuaishou Crawler finished ...")
