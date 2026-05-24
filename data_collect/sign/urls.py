# -*- coding: utf-8 -*-
from data_collect.sign.apis.base_handler import PongHandler
from data_collect.sign.apis.douyin import DouyinSignHandler
from data_collect.sign.apis.xiaohongshu import XhsSignHandler, XhsUpdateSignBrowserCookies

url_handlers = [
    # pong api
    (r"/signsrv/pong", PongHandler),

    # xhs sign server api
    (r"/signsrv/v1/xhs/sign", XhsSignHandler),
    (r"/signsrv/v1/xhs/update_browser_cookies", XhsUpdateSignBrowserCookies),

    # douyin sign server api
    (r"/signsrv/v1/douyin/sign", DouyinSignHandler),
]
