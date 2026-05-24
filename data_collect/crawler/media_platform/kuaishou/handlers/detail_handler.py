# -*- coding: utf-8 -*-

import asyncio
from typing import TYPE_CHECKING

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.model.m_checkpoint import Checkpoint
from data_collect.crawler.pkg.tools import utils
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import KuaiShouApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.video_processor import VideoProcessor
    from ..processors.comment_processor import CommentProcessor


class DetailHandler(BaseHandler):
    """Handles detail-based crawling operations for specified videos"""

    def __init__(
        self,
        ks_client: "KuaiShouApiClient",
        checkpoint_manager: "CheckpointRepoManager",
        video_processor: "VideoProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize detail handler

        Args:
            ks_client: Kuaishou API client
            checkpoint_manager: Checkpoint manager for resume functionality
            video_processor: Video processing component
            comment_processor: Comment processing component
        """
        super().__init__(ks_client, checkpoint_manager, video_processor, comment_processor)

    async def handle(self) -> None:
        """
        Handle detail-based crawling

        Returns:
            None
        """
        await self.get_specified_videos()

    async def get_specified_videos(self) -> None:
        """
        Get the information and comments of the specified videos with checkpoint support
        Returns:
            None
        """
        utils.logger.info("[DetailHandler.get_specified_videos] Begin get specified videos")
        checkpoint = Checkpoint(platform=constant.KUAISHOU_PLATFORM_NAME, mode=constant.CRALER_TYPE_DETAIL)

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.KUAISHOU_PLATFORM_NAME,
                mode=constant.CRALER_TYPE_DETAIL,
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[DetailHandler.get_specified_videos] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        # 使用video processor批量处理指定的视频
        processed_video_ids = await self.video_processor.batch_get_video_list(
            config.KS_SPECIFIED_ID_LIST, checkpoint.id
        )

        # 批量获取视频评论
        await self.comment_processor.batch_get_video_comments(processed_video_ids, checkpoint.id)

        # 爬虫请求间隔时间
        await asyncio.sleep(config.CRAWLER_TIME_SLEEP)

        utils.logger.info("[DetailHandler.get_specified_videos] Completed processing specified videos")
