"""运行模式开关。

职能：
  - 读取/写入 NORI_MODE
  - direct ↔ ghc 切换后刷新 config
  - ghc 模式启动前校验本地代理 http://localhost:8313 是否可达

交接：
  - 上游调用方：main.py、skills/evolution/*、writer
  - 下游：llms.config.reload()
"""
from __future__ import annotations

import os
from typing import Literal

import httpx

from nori.config_normalization import mode_key

from . import config as _config
from .client import validate_client_config

Mode = Literal["direct", "ghc"]


def current_mode() -> str:
    """返回当前生效模式（环境变量优先，否则看 yaml）。"""
    return mode_key(os.getenv("NORI_MODE")) or mode_key(_config.get_config().mode)


def set_mode(mode: Mode | str) -> str:
    """切换运行模式，触发配置重载。"""
    mode = mode_key(mode)
    if mode not in ("direct", "ghc"):
        raise ValueError(f"非法 mode: {mode}")
    os.environ["NORI_MODE"] = mode
    _config.reload()
    return current_mode()


def ensure_ready(usage: str = "llm", timeout: float = 3.0) -> None:
    """在真正调用前做一次预检。

    - ghc 模式：GET {base_url}/models，失败直接抛异常，避免深层 500
    - direct 模式：检查 api_key / base_url 非空
    """
    model = _config.get_active(usage)
    client_options = validate_client_config(model, usage)
    if current_mode() == "ghc":
        url = f"{client_options['base_url'].rstrip('/')}/models"
        try:
            r = httpx.get(
                url,
                headers={"Authorization": f"Bearer {client_options['api_key']}"},
                timeout=timeout,
            )
            r.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"ghc 代理不可用: {url} ({exc}). "
                f"请先启动 ghc-api: "
                f"source ~/.venvs/ghc-api/bin/activate && "
                f"ghc-api -p 8313 -a 127.0.0.1"
            ) from exc
