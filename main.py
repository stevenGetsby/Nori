#!/usr/bin/env python3
"""Nori — AI 内容创作引擎主入口

用法：
    python main.py                # 显示当前可用入口
    python main.py --mode ghc     # 使用 ghc-api 模式启动
    python main.py --mode direct  # 使用直连模式启动
    python main.py --show-config  # 显示当前配置概览
    python main.py --run-holly-live
"""
import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# 确保项目根目录在 sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def show_config(mode: Optional[str] = None):
    """显示当前配置概览。"""
    if mode:
        os.environ["NORI_MODE"] = mode

    from nori.nori_config import NoriConfig
    cfg = NoriConfig()

    print(f"运行模式: {cfg.mode}")
    print(f"激活模型:")
    for usage, model_key in cfg.active_summary.items():
        try:
            m = cfg.resolve(model_key)
            print(f"  {usage:8s} → {model_key}  ({m.base_url})")
        except KeyError as e:
            print(f"  {usage:8s} → {model_key}  (⚠️ {e})")


def show_entrypoints() -> None:
    """Print the supported runtime entrypoints for this repository."""

    print("Nori 当前没有内置 web server 入口。可用入口：")
    print("  python main.py --show-config")
    print("  python main.py --run-holly-live")
    print("  python scripts/backend_holly_smoke.py --help")
    print("  python scripts/run_holly_live_case.py")
    print("  python scripts/continue_holly_live_case.py")
    print("  python scripts/smoke_note_maker.py --help")
    print("  python scripts/smoke_session_skill.py --help")
    print()
    print("默认测试：python -m pytest tests -q")


def run_holly_live() -> int:
    """Run the canonical live Holly workflow."""

    from scripts.run_holly_live_case import main as run_main

    return int(run_main() or 0)


def main():
    parser = argparse.ArgumentParser(description="Nori — AI 内容创作引擎")
    parser.add_argument("--mode", choices=["direct", "ghc"],
                        help="运行模式: direct=直连服务商, ghc=GitHub Copilot 代理")
    parser.add_argument("--show-config", action="store_true",
                        help="显示当前配置概览后退出")
    parser.add_argument("--run-holly-live", action="store_true",
                        help="运行 Holly 真实端到端内容生成 workflow")
    args = parser.parse_args()

    if args.mode:
        os.environ["NORI_MODE"] = args.mode

    if args.show_config:
        show_config(args.mode)
        return

    if args.run_holly_live:
        return run_holly_live()

    show_entrypoints()
    return None


if __name__ == "__main__":
    sys.exit(main())
