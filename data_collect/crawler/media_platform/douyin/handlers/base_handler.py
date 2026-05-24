# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import DouYinApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.aweme_processor import AwemeProcessor
    from ..processors.comment_processor import CommentProcessor


class BaseHandler(ABC):
    """Base handler class for all Douyin crawler handlers"""

    def __init__(
        self,
        dy_client: "DouYinApiClient",
        checkpoint_manager: "CheckpointRepoManager",
        aweme_processor: "AwemeProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize base handler with injected dependencies

        Args:
            dy_client: Douyin API client
            checkpoint_manager: Checkpoint manager for resume functionality
            aweme_processor: Aweme processing component
            comment_processor: Comment processing component
        """
        self.dy_client = dy_client
        self.checkpoint_manager = checkpoint_manager
        self.aweme_processor = aweme_processor
        self.comment_processor = comment_processor

    @abstractmethod
    async def handle(self) -> None:
        """
        Handle the specific crawler type operation

        Returns:
            None
        """
        raise NotImplementedError("Subclasses must implement handle method")
