# -*- coding: utf-8 -*-

import asyncio
from typing import List, TYPE_CHECKING, Optional

import data_collect.crawler.config as config
import data_collect.crawler.constant as constant
from data_collect.crawler.model.m_checkpoint import Checkpoint
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.repo.platform_save_data import weibo as weibo_store
from data_collect.crawler.model.m_weibo import WeiboCreator, WeiboNote
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import WeiboClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.note_processor import NoteProcessor
    from ..processors.comment_processor import CommentProcessor


class CreatorHandler(BaseHandler):
    """Handles creator-based crawling operations"""

    def __init__(
        self,
        wb_client: "WeiboClient",
        checkpoint_manager: "CheckpointRepoManager",
        note_processor: "NoteProcessor",
        comment_processor: "CommentProcessor",
    ):
        """
        Initialize creator handler

        Args:
            wb_client: Weibo API client
            checkpoint_manager: Checkpoint manager for resume functionality
            note_processor: Note processing component
            comment_processor: Comment processing component
        """
        super().__init__(
            wb_client, checkpoint_manager, note_processor, comment_processor
        )

    async def handle(self) -> None:
        """
        Handle creator-based crawling

        Returns:
            None
        """
        await self.get_creators_and_notes()

    @staticmethod
    def _find_creator_index_in_creator_list(creator_id: str) -> int:
        """
        Find creator index in creator list

        Args:
            creator_id: creator id

        Returns:
            int: creator index
        """
        creator_list = config.WEIBO_CREATOR_ID_LIST
        for index, creator_item in enumerate(creator_list):
            if creator_item == creator_id:
                return index
        return -1

    async def get_creators_and_notes(self) -> None:
        """
        Get creator's information and their notes and comments
        Returns:
            None
        """
        utils.logger.info(
            "[CreatorHandler.get_creators_and_notes] Begin get weibo creators"
        )
        checkpoint = Checkpoint(
            platform=constant.WEIBO_PLATFORM_NAME, mode=constant.CRALER_TYPE_CREATOR
        )
        creator_list = config.WEIBO_CREATOR_ID_LIST
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.WEIBO_PLATFORM_NAME,
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

        for user_id in creator_list:
            checkpoint.current_creator_id = user_id
            await self.checkpoint_manager.save_checkpoint(checkpoint)

            creator_info: Optional[WeiboCreator] = (
                await self.wb_client.get_creator_info_by_id(creator_id=user_id)
            )
            if creator_info:
                utils.logger.info(
                    f"[CreatorHandler.get_creators_and_notes] creator info: {creator_info}"
                )
                await weibo_store.save_creator(creator_info)

                # Get container info for fetching notes
                container_info = await self.wb_client.get_creator_container_info(
                    user_id
                )

                # Get all note information of the creator
                all_notes_list = await self.get_all_notes_by_creator(
                    creator_id=user_id,
                    container_id=container_info.get("lfid_container_id"),
                    checkpoint_id=checkpoint.id,
                )

                note_ids = [note.note_id for note in all_notes_list if note.note_id]
                await self.comment_processor.batch_get_note_comments(
                    note_ids, checkpoint_id=checkpoint.id
                )

            else:
                utils.logger.error(
                    f"[CreatorHandler.get_creators_and_notes] get creator info error, creator_id:{user_id}"
                )

    async def get_all_notes_by_creator(
        self,
        creator_id: str,
        container_id: str,
        checkpoint_id: str = "",
    ) -> List[WeiboNote]:
        """
        获取指定用户下的所有发过的帖子，该方法会一直查找一个用户下的所有帖子信息
        Args:
            creator_id: 用户ID
            container_id: 容器ID
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
        since_id = checkpoint.current_creator_page or "0"
        crawler_total_count = 0
        while notes_has_more and crawler_total_count <= config.CRAWLER_MAX_NOTES_COUNT:
            notes_res = await self.wb_client.get_notes_by_creator(
                creator_id, container_id, since_id
            )
            if not notes_res:
                utils.logger.error(
                    f"[CreatorHandler.get_all_notes_by_creator] The current creator may have been banned by weibo, so they cannot access the data."
                )
                break

            since_id = str(notes_res.get("cardlistInfo", {}).get("since_id", "0"))
            if "cards" not in notes_res:
                utils.logger.info(
                    f"[CreatorHandler.get_all_notes_by_creator] No 'cards' key found in response: {notes_res}"
                )
                break

            cards = notes_res["cards"]
            utils.logger.info(
                f"[CreatorHandler.get_all_notes_by_creator] got user_id:{creator_id} cards len : {len(cards)}"
            )

            # Extract notes from cards
            notes = []
            for card in cards:
                if card.get("card_type") == 9:
                    note = self.wb_client._extractor.extract_note_from_dict(card)
                    if note:
                        notes.append(note)

            # Process notes through note processor
            note_ids = await self.note_processor.batch_get_note_list(
                notes, checkpoint_id=checkpoint_id
            )
            await self.comment_processor.batch_get_note_comments(
                note_ids, checkpoint_id=checkpoint.id
            )

            result.extend(notes)
            crawler_total_count += 10
            notes_has_more = (
                notes_res.get("cardlistInfo", {}).get("total", 0) > crawler_total_count
            )

            # Update checkpoint with current page
            checkpoint = await self.checkpoint_manager.load_checkpoint_by_id(
                checkpoint_id
            )
            checkpoint.current_creator_page = since_id
            await self.checkpoint_manager.update_checkpoint(checkpoint)

            # 爬虫请求间隔时间
            await asyncio.sleep(config.CRAWLER_TIME_SLEEP)

        return result
