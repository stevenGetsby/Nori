# -*- coding: utf-8 -*-

import asyncio
import json
from typing import Dict, List, TYPE_CHECKING

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.model.m_checkpoint import Checkpoint
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.platform_save_data import douyin as douyin_store
from ..field import HomeFeedTagIdType
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import DouYinApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.aweme_processor import AwemeProcessor
    from ..processors.comment_processor import CommentProcessor


class HomefeedHandler(BaseHandler):
    """Handles homefeed-based crawling operations"""

    def __init__(
            self,
            dy_client: "DouYinApiClient",
            checkpoint_manager: "CheckpointRepoManager",
            aweme_processor: "AwemeProcessor",
            comment_processor: "CommentProcessor"
    ):
        """
        Initialize homefeed handler

        Args:
            dy_client: Douyin API client
            checkpoint_manager: Checkpoint manager for resume functionality
            aweme_processor: Aweme processing component
            comment_processor: Comment processing component
        """
        super().__init__(dy_client, checkpoint_manager, aweme_processor, comment_processor)

    async def handle(self) -> None:
        """
        Handle homefeed-based crawling

        Returns:
            None
        """
        await self.get_homefeed_awemes()

    async def get_homefeed_awemes(self):
        """
        Get homefeed awemes and comments
        Returns:
            None
        """
        utils.logger.info(
            "[HomefeedHandler.get_homefeed_awemes] Begin get douyin homefeed awemes"
        )

        # 初始化检查点
        checkpoint = Checkpoint(
            platform=constant.DOUYIN_PLATFORM_NAME,
            mode=constant.CRALER_TYPE_HOMEFEED,
            current_homefeed_cursor="",
            current_homefeed_note_index=0
        )

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.DOUYIN_PLATFORM_NAME,
                mode=constant.CRALER_TYPE_HOMEFEED,
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[HomefeedHandler.get_homefeed_awemes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        current_refresh_index = checkpoint.current_homefeed_note_index or 0
        per_page_count = 20
        saved_aweme_count = 0
        while saved_aweme_count <= config.CRAWLER_MAX_NOTES_COUNT:
            try:
                utils.logger.info(
                    f"[HomefeedHandler.get_homefeed_awemes] Get homefeed awemes, current_refresh_index: {current_refresh_index}, per_page_count: {per_page_count}"
                )

                homefeed_aweme_res = await self.dy_client.get_homefeed_aweme_list(
                    tag_id=HomeFeedTagIdType.ALL,
                    refresh_index=current_refresh_index,
                    count=per_page_count,
                )
                if not homefeed_aweme_res or homefeed_aweme_res.get("StatusCode") != 0:
                    utils.logger.info(
                        f"[HomefeedHandler.get_homefeed_awemes] No more content!"
                    )
                    break

                # extract aweme list from homefeed_aweme_res
                aweme_ids = []
                cards: List[Dict] = homefeed_aweme_res.get("cards", [])
                filtered_cards = [card for card in cards if card.get("type") == 1]

                for card in filtered_cards:
                    # 限制爬取数量，避免超过 CRAWLER_MAX_NOTES_COUNT
                    if saved_aweme_count >= config.CRAWLER_MAX_NOTES_COUNT:
                        utils.logger.info(
                            f"[HomefeedHandler.get_homefeed_awemes] Reached max awemes count: {config.CRAWLER_MAX_NOTES_COUNT}"
                        )
                        break

                    aweme_json_str: str = card.get("aweme")
                    if not aweme_json_str:
                        continue

                    aweme_info: Dict = json.loads(aweme_json_str)
                    if not aweme_info.get("aweme_id"):
                        continue
                    aweme_id = aweme_info.get("aweme_id")
                    aweme_ids.append(aweme_id)

                    # 检查是否已经爬取过
                    if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                            checkpoint_id=checkpoint.id, note_id=aweme_id
                    ):
                        utils.logger.info(
                            f"[HomefeedHandler.get_homefeed_videos] Aweme {aweme_id} is already crawled, skip"
                        )
                        saved_aweme_count += 1
                        continue

                    await self.checkpoint_manager.add_note_to_checkpoint(
                        checkpoint_id=checkpoint.id,
                        note_id=aweme_id,
                        extra_params_info={},
                        is_success_crawled=True,
                    )

                    from data_collect.crawler.media_platform.douyin.extractor import DouyinExtractor
                    extractor = DouyinExtractor()
                    aweme = extractor.extract_aweme_from_dict(aweme_info)
                    if aweme:
                        await douyin_store.update_douyin_aweme(aweme_item=aweme)
                    saved_aweme_count += 1

                await self.comment_processor.batch_get_aweme_comments(
                    aweme_ids, checkpoint_id=checkpoint.id
                )
                current_refresh_index += per_page_count

                # 爬虫请求间隔时间
                await asyncio.sleep(config.CRAWLER_TIME_SLEEP)

            except Exception as ex:
                utils.logger.error(
                    f"[HomefeedHandler.get_homefeed_awemes] Get homefeed awemes error: {ex}"
                )
                # 发生异常了，则打印当前爬取的索引，用于后续继续爬取
                utils.logger.info(
                    "------------------------------------------记录当前爬取的索引------------------------------------------"
                )
                for i in range(3):
                    utils.logger.error(
                        f"[HomefeedHandler.get_homefeed_awemes] Current refresh_index: {current_refresh_index}"
                    )
                utils.logger.info(
                    "------------------------------------------记录当前爬取的索引---------------------------------------------------"
                )

                utils.logger.info(
                    f"[HomefeedHandler.get_homefeed_awemes] 可以在配置文件中开启断点续爬功能，继续爬取当前位置的信息"
                )
                return

            finally:
                # 更新检查点状态
                lastest_checkpoint = (
                    await self.checkpoint_manager.load_checkpoint_by_id(checkpoint.id)
                )
                lastest_checkpoint.current_homefeed_note_index = current_refresh_index
                await self.checkpoint_manager.update_checkpoint(lastest_checkpoint)

        utils.logger.info(
            "[HomefeedHandler.get_homefeed_awemes] Douyin homefeed awemes crawler finished ..."
        )
