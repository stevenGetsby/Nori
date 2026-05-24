# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

from typing import Any, Optional

from pydantic import BaseModel


class OkResponseModel(BaseModel):
    biz_code: int = 0
    msg: str = "OK!"
    isok: bool = True
    data: Optional[Any] = None


class ErrorResponseModel(BaseModel):
    biz_code: int
    msg: str
    isok: bool = False
    extra: Optional[Any] = None
