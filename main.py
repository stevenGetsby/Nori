#!/usr/bin/env python3
"""Nori — AI 内容创作引擎 主入口

用法：
    python main.py                # 启动 Nori 服务
    python main.py --mode ghc     # 使用 ghc-api 模式启动
    python main.py --mode direct  # 使用直连模式启动
    python main.py --show-config  # 显示当前配置概览
"""
import argparse
import sys
import os
from typing import Optional

# 确保项目根目录在 sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


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


def main():
    parser = argparse.ArgumentParser(description="Nori — AI 内容创作引擎")
    parser.add_argument("--mode", choices=["direct", "ghc"],
                        help="运行模式: direct=直连服务商, ghc=GitHub Copilot 代理")
    parser.add_argument("--show-config", action="store_true",
                        help="显示当前配置概览后退出")
    args = parser.parse_args()

    if args.mode:
        os.environ["NORI_MODE"] = args.mode

    if args.show_config:
        show_config(args.mode)
        return

    # 启动 Nori 服务
    from nori.nori_config import NoriConfig
    cfg = NoriConfig()
    print(f"Nori 启动中... (模式: {cfg.mode})")

    try:
        from nori.nori.server import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("Nori 服务模块未安装，请先: cd nori && pip install -e .")
        print("\n当前配置概览:")
        show_config(args.mode)


if __name__ == "__main__":
    main()
