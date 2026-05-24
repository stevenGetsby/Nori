# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import XiaoHongShuClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.note_processor import NoteProcessor
    from ..processors.comment_processor import CommentProcessor


class BaseHandler(ABC):
    """Base handler class for all XiaoHongShu crawler handlers"""

    def __init__(
        self,
        xhs_client: "XiaoHongShuClient",
        checkpoint_manager: "CheckpointRepoManager",
        note_processor: "NoteProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize base handler with injected dependencies

        Args:
            xhs_client: XiaoHongShu API client
            checkpoint_manager: Checkpoint manager for resume functionality
            note_processor: Note processing component
            comment_processor: Comment processing component
        """
        self.xhs_client = xhs_client
        self.checkpoint_manager = checkpoint_manager
        self.note_processor = note_processor
        self.comment_processor = comment_processor

    @abstractmethod
    async def handle(self) -> None:
        """
        Handle the specific crawler type operation

        Returns:
            None
        """
        raise NotImplementedError("Subclasses must implement handle method")
