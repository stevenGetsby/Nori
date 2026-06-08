"""Uvicorn entrypoint for the Nori FastAPI backend."""
from __future__ import annotations

import argparse

import uvicorn


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Nori FastAPI backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()
    uvicorn.run("backend.app:app", host=args.host, port=args.port, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
