"""项目级 LLM 调用入口。

岗位分工：
  - config.py   : 读取 api_config.yaml，提供 mode/激活模型解析
  - mode.py     : 切换 direct / ghc，校验本地代理可用
  - client.py   : OpenAI SDK 客户端工厂
  - call.py     : 同步/异步 chat、JSON chat、image 高层调用

对外只暴露本文件的符号，内部实现可替换。
"""
from __future__ import annotations

from .config import get_config, get_active, resolve
from .mode import current_mode, set_mode, ensure_ready
from .client import get_client, get_async_client
from .call import ChatJSONError, achat, chat, chat_json, image, parse_json_object
from .intent_extractor import IntentLLMResult, extract_intent
from .target_selector import TargetSelectionResult, select_edit_target

__all__ = [
    "get_config",
    "get_active",
    "resolve",
    "current_mode",
    "set_mode",
    "ensure_ready",
    "get_client",
    "get_async_client",
    "chat",
    "chat_json",
    "parse_json_object",
    "ChatJSONError",
    "achat",
    "image",
    "IntentLLMResult",
    "extract_intent",
    "TargetSelectionResult",
    "select_edit_target",
]
