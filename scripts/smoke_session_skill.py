"""Session-level XHS skill smoke test using the real Holly chain case.

端到端真实测试:
  Holly intaker/account_planner 日志 -> 搜索词 -> DataCollector.collect_top_notes
  -> XHSNoteAnalyzer.collect_for_session 聚类 -> NoteSkill + case log

用法:
    python scripts/smoke_session_skill.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nori.agents.market_analysis import XHSNoteAnalyzer


DEFAULT_DATA_DIR = "nori/skill_base/data/xhs_note_analyzer/holly"


def main() -> int:
    parser = argparse.ArgumentParser(description="Session-level XHS skill smoke test for Holly.")
    parser.add_argument("--case-log", default="", help="Holly intaker -> account_planner 链路日志")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--min-liked", type=int, default=500)
    parser.add_argument("--pool", type=int, default=20)
    parser.add_argument("--max-keywords", type=int, default=3)
    parser.add_argument("--download", dest="download", action="store_true", default=True)
    parser.add_argument("--no-download", dest="download", action="store_false")
    args = parser.parse_args()

    case_log = Path(args.case_log) if args.case_log else _latest_holly_chain_log()
    try:
        context = _context_from_holly_chain_log(
            case_log,
            days=args.days,
            top_k=args.top_k,
            pool=args.pool,
            min_liked=args.min_liked,
            max_keywords=args.max_keywords,
            download_media=args.download,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[error] failed to load Holly context: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    analyzer = XHSNoteAnalyzer(use_llm=True)
    try:
        report = analyzer.collect_for_session(context)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] collect_for_session failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))

    print(file=sys.stderr)
    print("=== Summary ===", file=sys.stderr)
    print(f"case_log       : {case_log}", file=sys.stderr)
    print(f"keywords       : {report.keywords}", file=sys.stderr)
    print(f"total_notes    : {report.coverage.get('total_notes', 0)}", file=sys.stderr)
    print(f"llm_enhanced   : {report.llm_enhanced}", file=sys.stderr)
    print(f"source_data_dir: {report.source_data_dir}", file=sys.stderr)
    skill_output_path = _skill_output_path(report)
    if skill_output_path:
        print(f"skill_json     : {skill_output_path}", file=sys.stderr)
    for skill in report.skills:
        metrics = skill.metrics_summary
        print(
            f"  - {skill.label} (goal={skill.goal}, type={skill.note_type})"
            f" sample={metrics.get('sample')} liked_p50={metrics.get('liked_p50')}"
            f" collected_p50={metrics.get('collected_p50')}",
            file=sys.stderr,
        )
    if report.insufficient:
        print(f"insufficient   : {report.insufficient}", file=sys.stderr)
    if report.leftover_note_ids:
        print(f"leftover       : {len(report.leftover_note_ids)} notes", file=sys.stderr)
    return 0


def _skill_output_path(report) -> str:
    if not report.source_data_dir:
        return ""
    for path_text in report.source_keyword_dirs.values():
        match = re.match(r"(\d{8}_\d{6})_", Path(path_text).name)
        if match:
            return str(Path(report.source_data_dir) / f"{match.group(1)}_note_skill_guides.json")
    return str(Path(report.source_data_dir) / "session_note_skill_guides.json")


def _latest_holly_chain_log() -> Path:
    candidates = sorted(Path("log").glob("agent_chain_holly_intaker_to_account_planner_*.json"))
    if not candidates:
        raise FileNotFoundError("未找到 log/agent_chain_holly_intaker_to_account_planner_*.json")
    return candidates[-1]


def _context_from_holly_chain_log(
    path: Path,
    *,
    days: int,
    top_k: int,
    pool: int,
    min_liked: int,
    max_keywords: int,
    download_media: bool,
) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    output = data.get("output") if isinstance(data.get("output"), dict) else {}
    intaker = output.get("intaker") if isinstance(output.get("intaker"), dict) else {}
    planner = output.get("account_planner") if isinstance(output.get("account_planner"), dict) else {}

    keywords = _search_keywords(planner, max_keywords=max_keywords)
    if not keywords:
        raise ValueError("Holly account_planner 输出里没有 benchmark search_keywords")

    tags = planner.get("tags") if isinstance(planner.get("tags"), dict) else {}
    ip_report = planner.get("ip_portrait_report") if isinstance(planner.get("ip_portrait_report"), dict) else {}
    return {
        "case": data.get("case") or "holly_intaker_to_account_planner",
        "source_case_log": str(path),
        "platform": "xhs",
        "topic": "Holly Shit 怪趣文创",
        "account_position": planner.get("recommended_positioning") or tags.get("positioning") or "怪趣文创",
        "target_audience": planner.get("audience_profile") or [],
        "intention": intaker.get("intention") or {},
        "planner_tags": tags,
        "content_directions": planner.get("content_directions") or [],
        "account_keywords": ip_report.get("account_keywords") or [],
        "unique_selling_points": planner.get("unique_selling_points") or [],
        "keywords": keywords,
        "days": days,
        "top_k_per_keyword": top_k,
        "min_liked": min_liked,
        "pool_size": pool,
        "download_media": download_media,
        "data_dir": DEFAULT_DATA_DIR,
    }


def _search_keywords(planner: dict[str, Any], *, max_keywords: int) -> list[str]:
    benchmarks = planner.get("benchmark_accounts") if isinstance(planner.get("benchmark_accounts"), dict) else {}
    level_rows = benchmarks.get("keyword_levels") if isinstance(benchmarks.get("keyword_levels"), list) else []
    level_keywords: list[str] = []
    for item in sorted((row for row in level_rows if isinstance(row, dict)), key=lambda row: int(row.get("level") or 0)):
        keyword = str(item.get("keyword") or "").strip()
        if keyword and keyword not in level_keywords:
            level_keywords.append(keyword)
        if len(level_keywords) >= max_keywords:
            return level_keywords
    raw = benchmarks.get("search_keywords") if isinstance(benchmarks.get("search_keywords"), list) else []
    keywords: list[str] = []
    for item in raw:
        keyword = str(item or "").strip()
        if keyword and keyword not in keywords:
            keywords.append(keyword)
        if len(keywords) >= max_keywords:
            break
    return keywords


if __name__ == "__main__":
    sys.exit(main())
