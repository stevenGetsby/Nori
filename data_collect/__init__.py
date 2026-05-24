"""Nori 数据采集模块

提供四个平台（xhs / dy / ks / wb）的搜索、详情、创作者、首页推荐抓取
以及媒体下载能力。统一入口为 :class:`DataCollector`。
"""
from .adapter import (
    CreatorRule,
    DataCollector,
    DetailRule,
    DownloadRule,
    HomefeedRule,
    HotNote,
    SearchRule,
    SearchSort,
    TopNotesResult,
    TopNotesRule,
)

__all__ = [
    "DataCollector",
    "SearchRule",
    "SearchSort",
    "DetailRule",
    "CreatorRule",
    "HomefeedRule",
    "DownloadRule",
    "TopNotesRule",
    "HotNote",
    "TopNotesResult",
]
