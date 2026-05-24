# -*- coding: utf-8 -*-


from contextvars import ContextVar
from typing import Any, Optional

from data_collect.crawler.async_db import AbstractAsyncDB

request_keyword_var: ContextVar[str] = ContextVar("request_keyword", default="")
crawler_type_var: ContextVar[str] = ContextVar("crawler_type", default="")
media_crawler_db_var: ContextVar[AbstractAsyncDB] = ContextVar("media_crawler_db_var")
db_conn_pool_var: ContextVar[Optional[Any]] = ContextVar("db_conn_pool_var", default=None)
source_keyword_var: ContextVar[str] = ContextVar("source_keyword", default="")
