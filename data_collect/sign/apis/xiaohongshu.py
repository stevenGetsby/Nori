# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import logging

from tenacity import RetryError

from data_collect.sign.apis.base_handler import TornadoBaseReqHandler
from data_collect.sign.constant import XHS_DEFAULT_SIGN_SERVER
from data_collect.sign.constant.error_code import ApiCode
from data_collect.sign.context_vars import xhs_manager_ctx_var
from data_collect.sign.logic.xhs import XhsSignLogic
from data_collect.sign.params.xiaohongshu_sign import (XhsSignRequest, XhsSignResponse,
                                     XhsUpdateCookiesRequest)
from data_collect.sign.pkg.custom_exceptions import BusinessLogicError

logger = logging.getLogger(__name__)
xhs_sign_logic = XhsSignLogic(XHS_DEFAULT_SIGN_SERVER)


class XhsSignHandler(TornadoBaseReqHandler):
    request_model = XhsSignRequest

    async def post(self):
        """
        处理xhs签名请求
        :return:
        """
        try:
            req: XhsSignRequest = self.parse_params()
            if not req:
                return

            response: XhsSignResponse = await xhs_sign_logic.sign(req)
            self.return_ok(data=response, msg="success")

        except RetryError as e:
            logger.error("xhs sign error, error: %s", e.last_attempt.exception())
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="xhs sign error",
                                          extra={"error": repr(e.last_attempt.exception())})

        except Exception as e:
            logger.error("xhs sign unkown error, error: %s", e)
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="xhs sign error", extra={"error": repr(e)})


class XhsUpdateSignBrowserCookies(TornadoBaseReqHandler):
    request_model = XhsUpdateCookiesRequest

    async def post(self):
        """
        更新xhs浏览器cookies,会调用xhs_browser_manager中的一系列方法来完成cookies更新
        :return:
        """
        req: XhsUpdateCookiesRequest = self.parse_params()
        if not req:
            return

        xhs_browser_manager = xhs_manager_ctx_var.get()
        if not xhs_browser_manager:
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="xhs browser manager object not found...")
        try:
            await xhs_browser_manager.update_fixed_cookies(req.cookies)
            self.return_ok(msg="update xhs sign server browser cookies success")
        except BusinessLogicError as e:
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="update xhs browser cookies logic error",
                                          extra={"error": repr(e)})
        except Exception as e:
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="update xhs browser cookies unkown error",
                                          extra={"error": repr(e)})
