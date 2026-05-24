"""Data models for CoverDirectorAgent (NoteDraft + skill → 本地封面图)。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CoverResult:
    """CoverDirector 的产出：一张本地封面图。"""
    cover_path: str                              # 已落盘的本地文件路径
    prompt: str                                  # 生成时用的视觉 prompt
    size: str = ""                               # 实际请求的尺寸
    reference_paths: list[str] = field(default_factory=list)
    source: str = ""                             # 原始返回（url / data-uri 前 80 字）
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cover_path": self.cover_path,
            "prompt": self.prompt,
            "size": self.size,
            "reference_paths": list(self.reference_paths),
            "source": self.source,
            "extra": dict(self.extra),
        }
