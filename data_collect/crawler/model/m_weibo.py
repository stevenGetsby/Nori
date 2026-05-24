# -*- coding: utf-8 -*-

from typing import Optional, List

from pydantic import BaseModel, Field


class WeiboNote(BaseModel):
    """微博笔记模型"""

    # 笔记基本信息
    note_id: str = Field(default="", description="笔记ID")
    content: str = Field(default="", description="笔记内容")
    create_time: str = Field(default="", description="创建时间戳")
    create_date_time: str = Field(default="", description="创建日期时间")
    liked_count: str = Field(default="", description="点赞数")
    comments_count: str = Field(default="", description="评论数")
    shared_count: str = Field(default="", description="转发数")
    note_url: str = Field(default="", description="笔记URL")
    ip_location: str = Field(default="", description="IP地理位置")

    # 媒体信息
    image_list: str = Field(default="", description="图片列表")
    video_url: str = Field(default="", description="视频URL")

    # 用户信息
    user_id: str = Field(default="", description="用户ID")
    nickname: str = Field(default="", description="用户昵称")
    gender: str = Field(default="", description="用户性别")
    profile_url: str = Field(default="", description="用户主页URL")
    avatar: str = Field(default="", description="用户头像")

    # 其他信息
    source_keyword: str = Field(default="", description="搜索来源关键字")

    # 时间戳字段（仅在写入数据库时使用）
    add_ts: Optional[int] = Field(default=None, description="记录添加时间戳")
    last_modify_ts: Optional[int] = Field(default=None, description="记录最后修改时间戳")


class WeiboComment(BaseModel):
    """微博评论模型"""

    # 评论基本信息
    comment_id: str = Field(default="", description="评论ID")
    note_id: str = Field(default="", description="笔记ID")
    content: str = Field(default="", description="评论内容")
    create_time: str = Field(default="", description="创建时间戳")
    create_date_time: str = Field(default="", description="创建日期时间")
    sub_comment_count: str = Field(default="", description="子评论数")
    like_count: str = Field(default="0", description="点赞数")
    ip_location: str = Field(default="", description="IP地理位置")
    parent_comment_id: str = Field(default="", description="父评论ID")

    # 用户信息
    user_id: str = Field(default="", description="用户ID")
    nickname: str = Field(default="", description="用户昵称")
    gender: str = Field(default="", description="用户性别")
    profile_url: str = Field(default="", description="用户主页URL")
    avatar: str = Field(default="", description="用户头像")

    # 子评论列表（仅用于内存中传递，不写入数据库）
    sub_comments: Optional[List['WeiboComment']] = Field(default=None, description="子评论列表")

    # 时间戳字段（仅在写入数据库时使用）
    add_ts: Optional[int] = Field(default=None, description="记录添加时间戳")
    last_modify_ts: Optional[int] = Field(default=None, description="记录最后修改时间戳")


class WeiboCreator(BaseModel):
    """微博创作者模型"""

    # 创作者基本信息
    user_id: str = Field(default="", description="用户ID")
    nickname: str = Field(default="", description="用户昵称")
    gender: str = Field(default="", description="性别")
    avatar: str = Field(default="", description="头像")
    desc: str = Field(default="", description="用户描述")
    ip_location: str = Field(default="", description="IP地理位置")

    # 统计信息
    follows: str = Field(default="", description="关注数")
    fans: str = Field(default="", description="粉丝数")
    tag_list: str = Field(default="", description="标签列表")

    # 时间戳字段（仅在写入数据库时使用）
    add_ts: Optional[int] = Field(default=None, description="记录添加时间戳")
    last_modify_ts: Optional[int] = Field(default=None, description="记录最后修改时间戳")
