# -*- coding: utf-8 -*-
import asyncio
import json
import os
import sys
from typing import Dict, Optional, Type

import data_collect.crawler.cmd_arg as cmd_arg
import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
import data_collect.crawler.db as db
from data_collect.crawler.base.base_crawler import AbstractCrawler
from data_collect.crawler.media_platform.douyin import DouYinCrawler
from data_collect.crawler.media_platform.kuaishou import KuaiShouCrawler
from data_collect.crawler.media_platform.weibo import WeiboCrawler
from data_collect.crawler.media_platform.xhs import XiaoHongShuCrawler
from data_collect.crawler.constant import MYSQL_ACCOUNT_SAVE
from data_collect.crawler.pkg.tools.utils import init_logging_config


class CrawlerFactory:
    CRAWLERS: Dict[str, AbstractCrawler] = {
        constant.XHS_PLATFORM_NAME: XiaoHongShuCrawler,
        constant.WEIBO_PLATFORM_NAME: WeiboCrawler,
        constant.DOUYIN_PLATFORM_NAME: DouYinCrawler,
        constant.KUAISHOU_PLATFORM_NAME: KuaiShouCrawler,
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class: Optional[Type[AbstractCrawler]] = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError(
                f"Invalid platform '{platform}'. Supported: xhs / dy / ks / wb"
            )
        return crawler_class()


async def main():
    cmd_arg.parse_cmd()
    init_logging_config()

    if config.SAVE_DATA_OPTION == "db" or config.ACCOUNT_POOL_SAVE_TYPE in [MYSQL_ACCOUNT_SAVE]:
        await db.init_db()

    crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
    await crawler.async_initialize()

    summary = {
        "platform": config.PLATFORM,
        "crawler_type": config.CRAWLER_TYPE,
    }
    if config.SAVE_DATA_OPTION == "db":
        db_path = getattr(config, "SQLITE_DB_PATH", "./media_crawler.db")
        summary["db_path"] = os.path.abspath(db_path)
    try:
        await crawler.start()
        summary["status"] = "completed"
    except Exception as e:
        summary["status"] = "failed"
        summary["error"] = str(e)
    print(f"---CRAWL_SUMMARY: {json.dumps(summary, ensure_ascii=False)}---")

    if config.SAVE_DATA_OPTION == "db" or config.ACCOUNT_POOL_SAVE_TYPE in [MYSQL_ACCOUNT_SAVE]:
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
