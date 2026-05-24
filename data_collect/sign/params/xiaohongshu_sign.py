# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
from typing import Any, Optional

from pydantic import BaseModel, Field


class XhsSignRequest(BaseModel):
    uri: str = Field(..., title="uri", description="请求的uri")
    data: Optional[Any] = Field(None, title="data", description="请求body的数据")
    cookies: str = Field(..., title="cookies", description="请求的cookies")


class XhsSignResponse(BaseModel):
    x_s: str = Field(..., title="x_s", description="x_s")
    x_t: str = Field(..., title="x_t", description="x_t")
    x_s_common: str = Field(..., title="x_s_common", description="x_s_common")
    x_b3_traceid: str = Field(..., title="x_t_common", description="x_b3_trace_id")
    # x_mns: str = Field(..., title="x_mns", description="x_mns")


class XhsUpdateCookiesRequest(BaseModel):
    cookies: str = Field(title="cookies", description="新更新的cookies")
