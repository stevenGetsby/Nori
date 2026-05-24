# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 18:46
# @Desc    :
from typing import List

import data_collect.crawler.config as config
from data_collect.crawler.base.base_crawler import AbstractStore
from data_collect.crawler.model.m_douyin import DouyinAweme, DouyinAwemeComment, DouyinCreator
from data_collect.crawler.pkg.tools import utils
from data_collect.crawler.var import source_keyword_var

from .douyin_store_impl import (
    DouyinCsvStoreImplement,
    DouyinDbStoreImplement,
    DouyinJsonStoreImplement,
)


class DouyinStoreFactory:
    STORES = {
        "csv": DouyinCsvStoreImplement,
        "db": DouyinDbStoreImplement,
        "json": DouyinJsonStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = DouyinStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[DouyinStoreFactory.create_store] Invalid save option only supported csv or db or json ..."
            )
        return store_class()


async def batch_update_douyin_awemes(awemes: List[DouyinAweme]):
    """
    批量更新抖音视频
    Args:
        awemes: 视频列表
    """
    if not awemes:
        return

    for aweme_item in awemes:
        await update_douyin_aweme(aweme_item)


async def update_douyin_aweme(aweme_item: DouyinAweme):
    """
    更新抖音视频
    Args:
        aweme_item: 视频对象
    """
    aweme_item.source_keyword = source_keyword_var.get()
    local_db_item = aweme_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    print_title = aweme_item.title[:30] if aweme_item.title else aweme_item.desc[:30]
    utils.logger.info(
        f"[store.douyin.update_douyin_aweme] douyin aweme, id: {aweme_item.aweme_id}, title: {print_title}"
    )
    await DouyinStoreFactory.create_store().store_content(local_db_item)


async def batch_update_dy_aweme_comments(aweme_id: str, comments: List[DouyinAwemeComment]):
    """
    批量更新抖音视频评论
    Args:
        aweme_id: 视频ID
        comments: 评论列表
    """
    if not comments:
        return

    for comment_item in comments:
        await update_dy_aweme_comment(comment_item)


async def update_dy_aweme_comment(comment_item: DouyinAwemeComment):
    """
    更新抖音视频评论
    Args:
        comment_item: 评论对象
    """
    local_db_item = comment_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.douyin.update_dy_aweme_comment] douyin aweme comment, aweme_id: {comment_item.aweme_id}, comment_id: {comment_item.comment_id}"
    )
    await DouyinStoreFactory.create_store().store_comment(local_db_item)


async def save_creator(user_id: str, creator: DouyinCreator):
    """
    保存抖音创作者信息
    Args:
        user_id: 用户ID
        creator: 创作者对象
    """
    if not creator:
        return

    local_db_item = creator.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.douyin.save_creator] douyin creator, id: {creator.user_id}, nickname: {creator.nickname}"
    )
    await DouyinStoreFactory.create_store().store_creator(local_db_item)
