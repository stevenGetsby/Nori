# -*- coding: utf-8 -*-
from data_collect.downloader.DownloadServer.apis.base_handler import PongHandler
from data_collect.downloader.DownloadServer.apis.content_detail_handler import ContentDetailHandler
from data_collect.downloader.DownloadServer.apis.creator_query_handler import (CreatorContentListHandler,
                                        CreatorQueryHandler)

all_router = [
    (r"/", PongHandler),
    (r"/ping", PongHandler),
    (r"/api/v1/creator_query", CreatorQueryHandler),
    (r"/api/v1/creator_contents", CreatorContentListHandler),
    (r"/api/v1/content_detail", ContentDetailHandler),
]
