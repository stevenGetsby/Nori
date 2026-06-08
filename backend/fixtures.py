"""Backend-owned local experiment fixtures."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .experiments import PROJECT_ROOT


HOLLY_ASSET_NAMES = [
    "微信图片_20250617195920.jpg",
    "资源 49@2x.png",
    "资源 50@2x.png",
    "明信片 打印文件_画板 1.png",
]


def holly_content_production_fixture(
    *,
    project_root: str | Path = PROJECT_ROOT,
    max_assets: int = 4,
) -> dict[str, Any]:
    """Build a backend content-production request from the local Holly case."""

    root = Path(project_root)
    case_dir = root / "cases" / "Holly"
    brief_path = case_dir / "brief" / "original.md"
    assets_dir = case_dir / "assets" / "raw" / "brand_materials"
    if not brief_path.is_file():
        raise FileNotFoundError(f"Holly brief not found: {brief_path}")

    selected_names = HOLLY_ASSET_NAMES[: max(0, int(max_assets or 0))]
    asset_paths = [assets_dir / name for name in selected_names]
    missing_assets = [str(path) for path in asset_paths if not path.is_file()]
    if missing_assets:
        raise FileNotFoundError(f"missing Holly fixture assets: {missing_assets}")

    market_evidence = _latest_holly_market_evidence(case_dir)
    return {
        "case_id": "Holly",
        "case_title": "Holly Shit开心拉屎",
        "goal": "用 Holly 真实素材和小红书市场证据生成一篇图文内容，并生成封面图片。",
        "brief_text": brief_path.read_text(encoding="utf-8"),
        "platform": "xhs",
        "asset_paths": [str(path) for path in asset_paths],
        "market_evidence": market_evidence,
        "human_gate_mode": "skip",
        "config": {
            "client_name": "Holly",
            "brand_name": "Holly Shit开心拉屎",
            "project_id_prefix": "holly_backend_smoke",
            "project_name": "Holly Shit Backend Smoke",
            "topic": "Holly Shit 开心拉屎反焦虑怪趣文创账号冷启动",
            "account_position": "用便便精神、反焦虑、怪趣 IP 和原创文创产品做小红书种草与人格化内容。",
            "target_audience": "高压学习和上班人群、喜欢怪趣文创和反差幽默的年轻女性、原创设计周边买家。",
            "goals": [
                "让小红书用户快速理解品牌：Shit人生也要拉得开心。",
                "把线下卖得好的怪趣文创转成线上可关注、可收藏、可下单的内容资产。",
            ],
            "positioning_notes": [
                "品牌核心不是低俗玩梗，而是用荒诞幽默回收焦虑和身体自主权。",
            ],
            "constraints": [
                "保留 Holly Shit 的反叛、自信、搞笑、怪趣调性。",
                "内容必须能落到具体产品或 IP，不只写抽象情绪。",
            ],
            "taboos": [
                "不要把便便梗写成低俗猎奇。",
                "不要虚构销量、价格、疗效或未提供的合作背书。",
            ],
            "platform_rules": [
                {"rule": "小红书图文首屏必须一眼看出情绪利益点和收藏理由。"},
                {"rule": "标题、封面和正文开头要围绕同一个点击钩子。"},
            ],
            "top_k_per_keyword": 1,
            "download_media": False,
            "horizon_days": 7,
        },
        "metadata": {
            "source": "backend.fixture.holly_content_production",
            "brief_path": str(brief_path),
            "asset_names": selected_names,
            "market_evidence_source": str(market_evidence.get("_source_path") or ""),
        },
    }


def _latest_holly_market_evidence(case_dir: Path) -> dict[str, Any]:
    candidates = [
        *(case_dir / "runs").glob("*/market/xhs_top_notes_result.json"),
        *(case_dir / "runs").glob("*/xhs_top_notes_result.json"),
    ]
    for path in sorted(candidates, reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and (data.get("hot_notes") or data.get("queries")):
            return {**data, "_source_path": str(path)}
    raise FileNotFoundError(f"no cached Holly market evidence found under {case_dir / 'runs'}")


__all__ = ["HOLLY_ASSET_NAMES", "holly_content_production_fixture"]
