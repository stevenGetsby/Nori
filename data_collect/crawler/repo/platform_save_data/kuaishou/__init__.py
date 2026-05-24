# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 20:03
# @Desc    :
from typing import List

import data_collect.crawler.config as config
from data_collect.crawler.base.base_crawler import AbstractStore
from data_collect.crawler.model.m_kuaishou import KuaishouVideo, KuaishouVideoComment, KuaishouCreator
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.var import source_keyword_var

from .kuaishou_store_impl import (
    KuaishouCsvStoreImplement,
    KuaishouDbStoreImplement,
    KuaishouJsonStoreImplement,
)


class KuaishouStoreFactory:
    STORES = {
        "csv": KuaishouCsvStoreImplement,
        "db": KuaishouDbStoreImplement,
        "json": KuaishouJsonStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = KuaishouStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[KuaishouStoreFactory.create_store] Invalid save option only supported csv or db or json ..."
            )
        return store_class()


async def batch_update_kuaishou_videos(videos: List[KuaishouVideo]):
    """批量更新快手视频

    Args:
        videos: 视频列表
    """
    if not videos:
        return

    for video_item in videos:
        await update_kuaishou_video(video_item)


async def update_kuaishou_video(video_item: KuaishouVideo):
    """更新快手视频

    Args:
        video_item: 视频对象
    """
    video_item.source_keyword = source_keyword_var.get()
    local_db_item = video_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    print_title = video_item.title[:30] if video_item.title else video_item.desc[:30]
    utils.logger.info(
        f"[store.kuaishou.update_kuaishou_video] kuaishou video, id: {video_item.video_id}, title: {print_title}"
    )
    await KuaishouStoreFactory.create_store().store_content(local_db_item)


async def batch_update_ks_video_comments(comments: List[KuaishouVideoComment]):
    """批量更新快手视频评论

    Args:
        comments: 评论列表
    """
    if not comments:
        return

    for comment_item in comments:
        await update_ks_video_comment(comment_item)


async def update_ks_video_comment(comment_item: KuaishouVideoComment):
    """更新快手视频评论

    Args:
        comment_item: 评论对象
    """
    local_db_item = comment_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.kuaishou.update_ks_video_comment] kuaishou video comment, video_id: {comment_item.video_id}, comment_id: {comment_item.comment_id}"
    )
    await KuaishouStoreFactory.create_store().store_comment(local_db_item)


async def save_creator(user_id: str, creator: KuaishouCreator):
    """保存快手创作者信息

    Args:
        user_id: 用户ID
        creator: 创作者对象
    """
    if not creator:
        return

    local_db_item = creator.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.kuaishou.save_creator] kuaishou creator, id: {creator.user_id}, nickname: {creator.nickname}"
    )
    await KuaishouStoreFactory.create_store().store_creator(local_db_item)
