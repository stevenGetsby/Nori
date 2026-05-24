# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import KuaiShouApiClient
    from data_collect.crawler.repo.checkpoint.checkpoint_store import CheckpointRepoManager
    from ..processors.video_processor import VideoProcessor
    from ..processors.comment_processor import CommentProcessor


class BaseHandler(ABC):
    """Base handler class for all Kuaishou crawler handlers"""

    def __init__(
        self,
        ks_client: "KuaiShouApiClient",
        checkpoint_manager: "CheckpointRepoManager",
        video_processor: "VideoProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize base handler with injected dependencies

        Args:
            ks_client: Kuaishou API client
            checkpoint_manager: Checkpoint manager for resume functionality
            video_processor: Video processing component
            comment_processor: Comment processing component
        """
        self.ks_client = ks_client
        self.checkpoint_manager = checkpoint_manager
        self.video_processor = video_processor
        self.comment_processor = comment_processor

    @abstractmethod
    async def handle(self) -> None:
        """
        Handle the specific crawler operation

        Returns:
            None
        """
        pass
