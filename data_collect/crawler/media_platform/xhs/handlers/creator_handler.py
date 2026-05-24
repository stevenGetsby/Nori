# -*- coding: utf-8 -*-

import asyncio
from typing import Dict, List, TYPE_CHECKING

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.model.m_checkpoint import Checkpoint
from data_collect.crawler.model.m_xhs import CreatorUrlInfo
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.platform_save_data import xhs as xhs_store
from ..extractor import XiaoHongShuExtractor
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import XiaoHongShuClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.note_processor import NoteProcessor
    from ..processors.comment_processor import CommentProcessor


class CreatorHandler(BaseHandler):
    """Handles creator-based crawling operations"""

    def __init__(
        self,
        xhs_client: "XiaoHongShuClient",
        checkpoint_manager: "CheckpointRepoManager",
        note_processor: "NoteProcessor",
        comment_processor: "CommentProcessor",
    ):
        """
        Initialize creator handler

        Args:
            xhs_client: XiaoHongShu API client
            checkpoint_manager: Checkpoint manager for resume functionality
            note_processor: Note processing component
            comment_processor: Comment processing component
        """
        super().__init__(
            xhs_client, checkpoint_manager, note_processor, comment_processor
        )
        self.extractor = XiaoHongShuExtractor()

    async def handle(self) -> None:
        """
        Handle creator-based crawling

        Returns:
            None
        """
        await self.get_creators_and_notes()

    def _find_creator_index_in_creator_list(self, creator_id: str) -> int:
        """
        Find creator index in creator list

        Args:
            creator_id: creator id

        Returns:
            int: creator index
        """
        creator_list = config.XHS_CREATOR_URL_LIST
        for index, creator_item in enumerate(creator_list):
            creator_url_info: CreatorUrlInfo = self.extractor.parse_creator_info_from_creator_url(
                creator_item
            )
            if creator_url_info.creator_id == creator_id:
                return index
        return -1

    async def get_creators_and_notes(self) -> None:
        """
        Get creator's information and their notes and comments
        Returns:
            None
        """
        utils.logger.info(
            "[CreatorHandler.get_creators_and_notes] Begin get xiaohongshu creators"
        )
        checkpoint = Checkpoint(
            platform=constant.XHS_PLATFORM_NAME, mode=constant.CRALER_TYPE_CREATOR
        )
        creator_list = config.XHS_CREATOR_URL_LIST
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.XHS_PLATFORM_NAME,
                mode=constant.CRALER_TYPE_CREATOR,
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[CreatorHandler.get_creators_and_notes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
                creator_index = self._find_creator_index_in_creator_list(
                    lastest_checkpoint.current_creator_id
                )
                if creator_index == -1:
                    utils.logger.error(
                        f"[CreatorHandler.get_creators_and_notes] Creator {lastest_checkpoint.current_creator_id} not found in creator list"
                    )
                    creator_index = 0

                creator_list = creator_list[creator_index:]

        for creator_url in creator_list:
            creator_url_info: CreatorUrlInfo = self.extractor.parse_creator_info_from_creator_url(
                creator_url
            )
            checkpoint.current_creator_id = creator_url_info.creator_id
            await self.checkpoint_manager.save_checkpoint(checkpoint)

            creator_info = await self.xhs_client.get_creator_info(
                user_id=creator_url_info.creator_id,
                xsec_token=creator_url_info.xsec_token,
                xsec_source=creator_url_info.xsec_source,
            )
            if not creator_info:
                raise Exception(
                    f"[CreatorHandler.get_creators_and_notes] Get creator info error, user_id: {creator_url_info.creator_id}"
                )

            await xhs_store.save_creator(creator_info)

            # Get all note information of the creator
            await self.get_all_notes_by_creator(
                user_id=creator_url_info.creator_id,
                xsec_token=creator_url_info.xsec_token,
                xsec_source=creator_url_info.xsec_source,
                checkpoint_id=checkpoint.id,
            )

    async def get_all_notes_by_creator(
        self,
        user_id: str,
        xsec_token: str = "",
        xsec_source: str = "",
        checkpoint_id: str = "",
    ) -> List[Dict]:
        """
        获取指定用户下的所有发过的帖子，该方法会一直查找一个用户下的所有帖子信息
        Args:
            user_id: 用户ID
            xsec_token: 验证token
            xsec_source: 渠道来源
            checkpoint_id: 检查点ID

        Returns:
            List of notes
        """
        checkpoint = await self.checkpoint_manager.load_checkpoint_by_id(checkpoint_id)
        if not checkpoint:
            raise Exception(
                f"[CreatorHandler.get_all_notes_by_creator] Get checkpoint error, checkpoint_id: {checkpoint_id}"
            )

        result = []
        notes_has_more = True
        notes_cursor = checkpoint.current_creator_page or ""
        saved_creator_count = 0
        max_notes_count = config.CRAWLER_MAX_NOTES_COUNT
        while notes_has_more and saved_creator_count < max_notes_count:
            remaining_notes_count = max_notes_count - saved_creator_count
            notes_res = await self.xhs_client.get_notes_by_creator(
                user_id,
                notes_cursor,
                page_size=min(30, remaining_notes_count),
                xsec_token=xsec_token,
                xsec_source=xsec_source,
            )

            if not notes_res:
                utils.logger.error(
                    f"[CreatorHandler.get_notes_by_creator] The current creator may have been banned by xhs, so they cannot access the data."
                )
                break

            notes_has_more = notes_res.get("has_more", False)
            notes_cursor = notes_res.get("cursor", "")

            if "notes" not in notes_res:
                utils.logger.info(
                    f"[CreatorHandler.get_all_notes_by_creator] No 'notes' key found in response: {notes_res}"
                )
                break

            notes = notes_res["notes"][:remaining_notes_count]
            utils.logger.info(
                f"[CreatorHandler.get_all_notes_by_creator] got user_id:{user_id} notes len : {len(notes)}, notes_cursor: {notes_cursor}"
            )
            note_ids, xsec_tokens = await self.note_processor.batch_get_note_list(
                notes, checkpoint_id=checkpoint_id
            )
            await self.comment_processor.batch_get_note_comments(
                note_ids, xsec_tokens, checkpoint_id=checkpoint_id
            )

            result.extend(notes)
            saved_creator_count += len(notes)

            # 需要加载最新的检查点，因为在fetch_creator_notes_detail方法中，有对检查点左边
            checkpoint = await self.checkpoint_manager.load_checkpoint_by_id(
                checkpoint_id
            )
            checkpoint.current_creator_page = notes_cursor
            await self.checkpoint_manager.update_checkpoint(checkpoint)

            # 爬虫请求间隔时间
            await asyncio.sleep(config.CRAWLER_TIME_SLEEP)
        return result
