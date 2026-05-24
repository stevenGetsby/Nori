# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import logging

from tenacity import RetryError

from data_collect.sign.apis.base_handler import TornadoBaseReqHandler
from data_collect.sign.constant import DOUYIN_DEFAULT_SIGN_SERVER
from data_collect.sign.constant.error_code import ApiCode
from data_collect.sign.logic.douyin import DouyinSignLogic
from data_collect.sign.params.douyin_sign import DouyinSignRequest, DouyinSignResponse

logger = logging.getLogger(__name__)
dy_sign_logic = DouyinSignLogic(DOUYIN_DEFAULT_SIGN_SERVER)


class DouyinSignHandler(TornadoBaseReqHandler):
    request_model = DouyinSignRequest

    async def post(self):
        """
        处理douyin签名请求
        :return:
        """
        try:
            req: DouyinSignRequest = self.parse_params()
            if not req:
                return

            response: DouyinSignResponse = await dy_sign_logic.sign(req)
            self.return_ok(data=response, msg="success")

        except RetryError as e:
            logger.error("douyin sign error, error: %s", e.last_attempt.exception())
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="douyin sign error",
                                          extra={"error": repr(e.last_attempt.exception())})

        except Exception as e:
            logger.error("douyin sign unkown error, error: %s", e)
            return self.return_error_info(ApiCode.EXCEPTION, errmsg="douyin sign error", extra={"error": repr(e)})
