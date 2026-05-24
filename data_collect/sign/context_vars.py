# -*- coding: utf-8 -*-
from contextvars import ContextVar

from data_collect.sign.pkg.playwright.douyin_manager import DouYinPlaywrightManager
from data_collect.sign.pkg.playwright.xhs_manager import XhsPlaywrightManager

request_id_var: ContextVar = ContextVar("request_id")
xhs_manager_ctx_var: ContextVar[XhsPlaywrightManager] = ContextVar("xhs_manager_ctx_var")
dy_manager_ctx_var: ContextVar[DouYinPlaywrightManager] = ContextVar("dy_manager_ctx_var")
