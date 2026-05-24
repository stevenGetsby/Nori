# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.model.m_checkpoint import Checkpoint
from data_collect.crawler.pkg.tools import utils
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import DouYinApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.aweme_processor import AwemeProcessor
    from ..processors.comment_processor import CommentProcessor


class DetailHandler(BaseHandler):
    """Handles detail-based crawling operations for specified awemes"""

    def __init__(
        self,
        dy_client: "DouYinApiClient",
        checkpoint_manager: "CheckpointRepoManager",
        aweme_processor: "AwemeProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize detail handler

        Args:
            dy_client: Douyin API client
            checkpoint_manager: Checkpoint manager for resume functionality
            aweme_processor: Aweme processing component
            comment_processor: Comment processing component
        """
        super().__init__(dy_client, checkpoint_manager, aweme_processor, comment_processor)

    async def handle(self) -> None:
        """
        Handle detail-based crawling

        Returns:
            None
        """
        await self.get_specified_awemes()

    async def get_specified_awemes(self):
        """
        Get the information and comments of the specified post
        Returns:
            None
        """
        utils.logger.info(
            "[DetailHandler.get_specified_awemes] Begin get douyin specified awemes"
        )

        checkpoint = Checkpoint(platform=constant.DOUYIN_PLATFORM_NAME, mode=constant.CRALER_TYPE_DETAIL)

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.DOUYIN_PLATFORM_NAME,
                mode=constant.CRALER_TYPE_DETAIL,
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[DetailHandler.get_specified_awemes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        processed_aweme_ids = await self.aweme_processor.batch_get_aweme_list_from_ids(
            config.DY_SPECIFIED_ID_LIST, checkpoint_id=checkpoint.id
        )
        await self.comment_processor.batch_get_aweme_comments(
            processed_aweme_ids, checkpoint_id=checkpoint.id
        )
