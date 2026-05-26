"""Prompt registry for NoteMakerAgent LLM substages."""
from __future__ import annotations

ASSET_CURATOR_SYSTEM_PROMPT = "你是 Nori 的素材整理工序，只输出 JSON。"
NOTE_COMPOSER_SYSTEM_PROMPT = "你是 Nori 的小红书 note 写手，只输出 JSON。"

__all__ = ["ASSET_CURATOR_SYSTEM_PROMPT", "NOTE_COMPOSER_SYSTEM_PROMPT"]
