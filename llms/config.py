"""配置桥接层。

职能：
  - 复用 nori.nori_config.NoriConfig，不重复解析
  - 按 usage 返回当前激活模型
  - 按 model_key 解析任意模型

交接：
  - 上游：api_config.yaml（根目录）
  - 下游：llms.client、llms.call
"""
from __future__ import annotations

from nori.core.contracts import ResolvedModel
from nori.nori_config import NoriConfig, cfg as _default_cfg

_cfg: NoriConfig = _default_cfg


def get_config() -> NoriConfig:
    """获取当前 NoriConfig 单例。"""
    return _cfg


def reload() -> NoriConfig:
    """重新读取 api_config.yaml（切换 mode 后用）。"""
    global _cfg
    _cfg = NoriConfig()
    return _cfg


def get_active(usage: str = "llm") -> ResolvedModel:
    """返回当前 mode 下 usage 对应的激活模型。"""
    return _cfg.get_active(usage)


def resolve(model_key: str) -> ResolvedModel:
    """将 provider::model_id 解析为完整模型配置。"""
    return _cfg.resolve(model_key)
