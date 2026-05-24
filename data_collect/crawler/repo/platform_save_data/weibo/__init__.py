# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 21:34
# @Desc    :

import re
from typing import List

import data_collect.crawler.config as config
from data_collect.crawler.model.m_weibo import WeiboNote, WeiboComment, WeiboCreator
from data_collect.crawler.var import source_keyword_var

from .weibo_store_impl import *


class WeibostoreFactory:
    STORES = {
        "csv": WeiboCsvStoreImplement,
        "db": WeiboDbStoreImplement,
        "json": WeiboJsonStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = WeibostoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[WeibotoreFactory.create_store] Invalid save option only supported csv or db or json ..."
            )
        return store_class()


async def batch_update_weibo_notes(note_list: List[WeiboNote]):
    if not note_list:
        return
    for note_item in note_list:
        await update_weibo_note(note_item)


async def update_weibo_note(note_item: WeiboNote):
    utils.logger.info(
        f"[store.weibo.update_weibo_note] weibo note id:{note_item.note_id}, title:{note_item.content[:24]} ..."
    )

    save_content_item = note_item.model_dump()
    save_content_item["last_modify_ts"] = utils.get_current_timestamp()
    await WeibostoreFactory.create_store().store_content(content_item=save_content_item)


async def batch_update_weibo_note_comments(note_id: str, comments: List[WeiboComment]):
    if not comments:
        return
    for comment_item in comments:
        await update_weibo_note_comment(comment_item)


async def update_weibo_note_comment(comment_item: WeiboComment):
    utils.logger.info(
        f"[store.weibo.update_weibo_note_comment] Weibo note comment: {comment_item.comment_id}, content: {comment_item.content[:24]} ..."
    )

    save_comment_item = comment_item.model_dump(exclude={"sub_comments"})
    save_comment_item["last_modify_ts"] = utils.get_current_timestamp()
    await WeibostoreFactory.create_store().store_comment(comment_item=save_comment_item)


async def save_creator(creator_info: WeiboCreator):
    utils.logger.info(
        f"[store.weibo.save_creator] creator: user_id={creator_info.user_id}, nickname={creator_info.nickname}"
    )

    local_db_item = creator_info.model_dump()
    local_db_item["last_modify_ts"] = utils.get_current_timestamp()
    await WeibostoreFactory.create_store().store_creator(local_db_item)
