# -*- coding: utf-8 -*-

import asyncio
from typing import List, Optional, TYPE_CHECKING

from data_collect.crawler.model.m_douyin import DouyinAweme
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.platform_save_data import douyin as douyin_store
from ..exception import DataFetchError

if TYPE_CHECKING:
    from ..client import DouYinApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager


class AwemeProcessor:
    """Handles aweme processing operations including detail extraction and batch processing"""

    def __init__(
        self,
        dy_client: "DouYinApiClient",
        checkpoint_manager: "CheckpointRepoManager",
        crawler_aweme_task_semaphore: asyncio.Semaphore,
    ):
        """
        Initialize aweme processor

        Args:
            dy_client: Douyin API client
            checkpoint_manager: Checkpoint manager for resume functionality
            crawler_aweme_task_semaphore: Semaphore to limit concurrent aweme tasks
        """
        self.dy_client = dy_client
        self.checkpoint_manager = checkpoint_manager
        self.crawler_aweme_task_semaphore = crawler_aweme_task_semaphore

    async def get_aweme_detail_async_task(
        self,
        aweme_id: str,
        checkpoint_id: str = "",
    ) -> Optional[DouyinAweme]:
        """
        Get aweme detail from API

        Args:
            aweme_id: aweme id
            checkpoint_id: checkpoint id
        Returns:
            aweme model
        """
        aweme = None
        async with self.crawler_aweme_task_semaphore:
            try:
                aweme = await self.dy_client.get_video_by_id(aweme_id)
                if aweme:
                    await douyin_store.update_douyin_aweme(aweme)
                    return aweme
                else:
                    utils.logger.warning(
                        f"[AwemeProcessor.get_aweme_detail_async_task] have not fund aweme detail aweme_id:{aweme_id}"
                    )

            except DataFetchError as ex:
                utils.logger.error(
                    f"[AwemeProcessor.get_aweme_detail_async_task] Get aweme detail error: {ex}"
                )
                return None

            except KeyError as ex:
                utils.logger.error(
                    f"[AwemeProcessor.get_aweme_detail_async_task] have not fund aweme detail aweme_id:{aweme_id}, err: {ex}"
                )
                return None

            finally:
                if checkpoint_id:
                    is_success_crawled = aweme is not None
                    await self.checkpoint_manager.update_note_to_checkpoint(
                        checkpoint_id=checkpoint_id,
                        note_id=aweme_id,
                        is_success_crawled=is_success_crawled,
                        is_success_crawled_comments=False,
                        current_note_comment_cursor=None,
                    )

    async def batch_get_aweme_list_from_ids(
        self, aweme_ids: List[str], checkpoint_id: str
    ) -> List[str]:
        """
        Concurrently obtain the specified aweme list by IDs and save the data
        Args:
            aweme_ids: List of aweme IDs
            checkpoint_id: Checkpoint ID

        Returns:
            List of successfully processed aweme IDs
        """
        task_list, processed_aweme_ids = [], []
        for aweme_id in aweme_ids:
            if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                checkpoint_id=checkpoint_id, note_id=aweme_id
            ):
                utils.logger.info(
                    f"[AwemeProcessor.batch_get_aweme_list_from_ids] Aweme {aweme_id} is already crawled, skip"
                )
                processed_aweme_ids.append(aweme_id)
                continue

            await self.checkpoint_manager.add_note_to_checkpoint(
                checkpoint_id=checkpoint_id,
                note_id=aweme_id,
                extra_params_info={},
            )

            task = self.get_aweme_detail_async_task(
                aweme_id=aweme_id,
                checkpoint_id=checkpoint_id,
            )
            task_list.append(task)

        aweme_details = await asyncio.gather(*task_list)
        for aweme in aweme_details:
            if aweme:
                processed_aweme_ids.append(aweme.aweme_id)

        return processed_aweme_ids
