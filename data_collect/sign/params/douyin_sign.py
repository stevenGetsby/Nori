# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class DouyinSignRequest(BaseModel):
    uri: str = Field(..., title="request_uri", description="请求的uri")
    query_params: str = Field(..., title="query_params", description="请求的query_params(urlencode之后的参数)")
    user_agent: str = Field(..., title="user_agent", description="请求的user_agent")
    cookies: str = Field(..., title="cookies", description="请求的cookies")


class DouyinSignResponse(BaseModel):
    a_bogus: str = Field(..., title="a_bogus", description="a_bogus")
