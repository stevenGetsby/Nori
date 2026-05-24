# -*- coding: utf-8 -*-


# 基础配置
import os
from typing import List

from data_collect.crawler.constant import MYSQL_ACCOUNT_SAVE, EXCEL_ACCOUNT_SAVE, COOKIE_BRIDGE_ACCOUNT_SAVE

PLATFORM = "xhs"
KEYWORDS = "AI Agent 程序员提效"

# 具体值参见media_platform.xxx.field下的枚举值，暂时只支持小红书
SORT_TYPE = "popularity_descending"

# 具体值参见media_platform.xxx.field下的枚举值，暂时只支持抖音
PUBLISH_TIME_TYPE = 0
CRAWLER_TYPE = "search"  # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据) | homefeed(首页推荐)

# 数据保存类型选项配置,支持三种类型：csv、db、json
SAVE_DATA_OPTION = "db"  # csv or db or json

# 账号池保存类型选项配置,支持3种类型：xlsx、mysql、cookie_bridge
# Nori 默认复用浏览器扩展同步的实时 cookie，避免回落到旧 Excel cookie。
ACCOUNT_POOL_SAVE_TYPE = os.getenv("ACCOUNT_POOL_SAVE_TYPE", COOKIE_BRIDGE_ACCOUNT_SAVE)

# CookieBridge 服务地址（仅当 ACCOUNT_POOL_SAVE_TYPE 为 cookie_bridge 时使用）
COOKIE_BRIDGE_URL = os.getenv("COOKIE_BRIDGE_URL", "http://localhost:8274")

# 爬取开始页数 默认从第一页开始
START_PAGE = 1

# 爬取视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = int(os.getenv("CRAWLER_MAX_NOTES_COUNT", "5"))

# 并发爬虫数量控制（请勿对平台发起大规模请求，并发控制仅限用于学习python的并发控制技术⚠️⚠️）
MAX_CONCURRENCY_NUM = 1

# 是否开启爬评论模式, 默认开启爬评论（可通过环境变量或CLI参数 --no-enable_comments 关闭）
ENABLE_GET_COMMENTS = os.getenv("ENABLE_GET_COMMENTS", "true").lower() == "true"

# 是否开启爬二级评论模式, 默认不开启爬二级评论
ENABLE_GET_SUB_COMMENTS = os.getenv("ENABLE_GET_SUB_COMMENTS", "false").lower() == "true"

# 有的帖子评论数量太大了，这个变量用于一个帖子评论的最大数量，0表示不限制
PER_NOTE_MAX_COMMENTS_COUNT = 100

# 是否开启日志打印输出到文件中
ENABLE_LOG_FILE = True

# 是否启用断点续爬功能
ENABLE_CHECKPOINT = True

# 指定断点续爬的检查点ID，如果为空，则加载最新的检查点
SPECIFIED_CHECKPOINT_ID = ""

# 检查点存储类型，支持 file 和 redis
CHECKPOINT_STORAGE_TYPE = "file"  # file or redis

# 是否开启微博爬取全文的功能，默认不开启（关键词搜索、创作者主页的返回的帖子里表，如果正文过长，则只返回部分内容）
# 如果开启的话会增加被风控的概率，相当于一个关键词搜索请求会再遍历所有帖子的时候，再请求一次帖子详情
ENABLE_WEIBO_FULL_TEXT = False

# 爬虫请求间隔时间，单位：秒，默认1秒（请勿对平台发起大规模请求， 应最大限度减少对平台的压力，仅用于学习python爬虫）
CRAWLER_TIME_SLEEP = float(os.getenv("CRAWLER_TIME_SLEEP", "3"))

# 已废弃⚠️⚠️⚠️指定小红书需要爬虫的笔记ID列表
# 已废弃⚠️⚠️⚠️ 指定笔记ID笔记列表会因为缺少xsec_token和xsec_source参数导致爬取失败
# XHS_SPECIFIED_ID_LIST = [
#     "66fad51c000000001b0224b8",
#     # ........................
# ]

# 指定小红书需要爬虫的笔记URL列表, 目前要携带xsec_token和xsec_source参数， xsec_token是有时间限制的
# xsec_token和xsec_source是有时效的，需要在web端打开一个小红书笔记，复制地址栏的url参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/68f20ba9000000000401619f?xsec_token=ABFNeBpLwvXZKTnBmYvNWXoooaC0vGY2tSBtjlNNLbYRw=&xsec_source=pc_feed"
    # ........................
]

# 已废弃⚠️⚠️⚠️指定小红书创作者ID列表
# 已废弃⚠️⚠️⚠️ 指定小红书创作者ID列表会因为缺少xsec_token和xsec_source参数导致爬取主页和主页的笔记列表失败
# 指定小红书创作者ID列表
# XHS_CREATOR_ID_LIST = [
#     "66215710000000000303097b",
#     # ........................
# ]

# 指定小红书创作者主页url列表, 需要携带xsec_token和xsec_source参数
XHS_CREATOR_URL_LIST = [
    "https://www.xiaohongshu.com/user/profile/5f58bd990000000001003753?xsec_token=ABeQXQ2ItOwgBVbCAnkaJJ_fC7PDB_Pr40MUvY9AOklUk%3D&xsec_source=pc_search"
    # ........................
]

# 指定微博平台需要爬取的帖子列表
WEIBO_SPECIFIED_ID_LIST = [
    "5180657661643376",
    # ........................
]
# 指定weibo创作者ID列表
WEIBO_CREATOR_ID_LIST = [
    "2172061270",
    "7449968177",
    # ........................
]

# 指定贴吧需要爬取的帖子列表
TIEBA_SPECIFIED_ID_LIST: List[str] = ["9815127841"]

# 指定贴吧名称列表，爬取该贴吧下的帖子
TIEBA_NAME_LIST: List[str] = [
    # "盗墓笔记"
]

TIEBA_CREATOR_URL_LIST = [
    "https://tieba.baidu.com/home/main/?id=tb.1.7f139e2e.6CyEwxu3VJruH_-QqpCi6g&fr=frs",
    # "https://tieba.baidu.com/home/main?id=tb.1.b9cd9508.4BEzoO0ZJbCkecLh-M4fKQ&fr=index"  # 主页帖子没有加载更多的case
    # ........................
]


# 指定bili创作者ID列表(这里是up主页面的ID)
BILI_CREATOR_ID_LIST = [
    "434377496",
    # ........................
]

# 指定B站平台需要爬取的视频bvid列表
BILI_SPECIFIED_ID_LIST = [
    "BV1d54y1g7db",
    "BV1Sz4y1U77N",
    "BV14Q4y1n7jz",
    # ........................
]

# 指定抖音需要爬取的ID列表
DY_SPECIFIED_ID_LIST = [
    "7566756334578830627",
    "7525538910311632128",
    # ........................
]

# 指定Dy创作者ID列表(sec_id)
DY_CREATOR_ID_LIST = [
    "MS4wLjABAAAATJPY7LAlaa5X-c8uNdWkvz0jUGgpw4eeXIwu_8BhvqE",
    # ........................
]


# 指定快手平台需要爬取的ID列表
KS_SPECIFIED_ID_LIST = ["3xf8enb8dbj6uig", "3x6zz972bchmvqe"]

# 指定快手创作者ID列表
KS_CREATOR_ID_LIST = [
    "3x4sm73aye7jq7i",
    # ........................
]


# 指定知乎创作者主页url列表
ZHIHU_CREATOR_URL_LIST = [
    "https://www.zhihu.com/people/yd1234567",
    # ........................
]

# 指定知乎需要爬取的帖子ID列表（仅支持下面这四种url链接的爬取）
ZHIHU_SPECIFIED_ID_LIST = [
    "https://www.zhihu.com/question/826896610/answer/4885821440",  # 回答
    "https://zhuanlan.zhihu.com/p/673461588",  # 文章
    "https://www.zhihu.com/zvideo/1539542068422144000",  # 视频
    # 爬取知乎指定问题下的答案列表，最大数量也由 CRAWLER_MAX_NOTES_COUNT 控制
    "https://www.zhihu.com/question/659910649",
]
