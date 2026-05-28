"""Run the Holly live end-to-end case with real XHS, LLM, and image APIs."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import llms
from data_collect.adapter import HotNote, TopNotesResult
from nori.content_generation.content_producer import ContentProducerAgent
from nori.context_building.calendar_planner import CalendarPlannerAgent
from nori.context_building.kpi_planner import KPIPlannerAgent
from nori.context_building.operation_planner import OperationPlannerAgent
from nori.core import ClientBrief, LLMFactory
from nori.learning_loop.review import ReviewGateAgent
from nori.market_analysis.models import SessionSkillReport
from nori.market_analysis.xhs_note_analyzer import XHSNoteAnalyzer
from nori.market_analysis.xhs_note_analyzer import session_reporter as xhs_session_reporter
from nori.market_analysis.xhs_note_analyzer import skill_builder as xhs_skill_builder
from nori.user_profiling.account_planner import AccountPlannerAgent
from nori.user_profiling.intaker import IntakeAgent
from nori.user_profiling.models import AccountPlannerInput, UserInput


CASE_DIR = ROOT / "data" / "Holly"
MATERIAL_DIR = CASE_DIR / "holly shit品牌素材"
CRAWLER_PYTHON = ROOT / "data_collect" / "crawler" / ".venv" / "bin" / "python"

KEYWORDS = ["怪趣文创", "反焦虑文创"]
TOP_K_PER_KEYWORD = 1
ASSET_NAMES = [
    "微信图片_20250617195920.jpg",
    "资源 49@2x.png",
    "资源 50@2x.png",
    "明信片 打印文件_画板 1.png",
]


def main() -> int:
    run_dir = CASE_DIR / "live_runs" / datetime.now().strftime("%Y%m%d_%H%M%S_holly_live")
    market_dir = run_dir / "market"
    covers_dir = run_dir / "covers"
    run_dir.mkdir(parents=True, exist_ok=False)
    market_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)

    _assert_active_models()
    llm_factory = _llm_factory()

    brief_text = (CASE_DIR / "设计理念.md").read_text(encoding="utf-8")
    asset_paths = _selected_assets()

    top_result = _collect_xhs_notes(market_dir)
    _write_json(run_dir / "xhs_top_notes_result.json", top_result.to_dict())

    analyzer = XHSNoteAnalyzer(use_llm=True, llm_factory=llm_factory)
    market_report = _build_market_report(analyzer, top_result, brief_text)
    _write_json(run_dir / "market_session_skill_report.json", market_report.to_dict())
    _write_json(run_dir / "note_skill_guides.json", xhs_session_reporter.skills_output(market_report))

    intake = IntakeAgent(use_llm=True, use_vision=True, llm_factory=llm_factory).run(
        UserInput(text=brief_text, images=[str(path) for path in asset_paths])
    )
    _write_json(run_dir / "intake_result.json", intake.to_dict())

    account_plan = AccountPlannerAgent(use_llm=True, llm_factory=llm_factory).run(
        AccountPlannerInput.from_intaker(
            intake,
            text=brief_text,
            images=[str(path) for path in asset_paths],
            platform="xhs",
            enable_search=False,
        )
    )
    _write_json(run_dir / "account_plan.json", account_plan.to_dict())

    client_brief = _client_brief(brief_text, account_plan, top_result)
    _write_json(run_dir / "client_brief.json", client_brief.to_dict())

    project = OperationPlannerAgent(use_llm=True, llm_factory=llm_factory).run(
        client_brief,
        account_plan,
        project_id=f"holly_live_{run_dir.name}",
        project_name="Holly Shit 小红书冷启动",
        start_date=date.today(),
        horizon_days=7,
    )
    _write_json(run_dir / "operation_project.json", project.to_dict())

    kpi_plan = KPIPlannerAgent(use_llm=True, llm_factory=llm_factory).run(project)
    _write_json(run_dir / "kpi_plan.json", kpi_plan.to_dict())

    calendar = CalendarPlannerAgent(use_llm=True, llm_factory=llm_factory).run(
        project,
        kpi_plan=kpi_plan,
        client_brief=client_brief,
        start_date=date.today(),
        horizon_days=7,
    )
    _write_json(run_dir / "content_calendar.json", calendar.to_dict())

    task = _select_task(calendar)
    _write_json(run_dir / "selected_task.json", task.to_dict())

    package = ContentProducerAgent(llm_factory=llm_factory).run(
        task,
        skills=market_report.skills,
        assets=intake.assets,
        out_dir=covers_dir,
        client_brief=client_brief,
        project=project,
        use_cover=True,
    )
    _write_json(run_dir / "content_package.json", package.to_dict())

    reviews = ReviewGateAgent().run(package, task=task, client_brief=client_brief, project=project)
    _write_json(run_dir / "reviews.json", [review.to_dict() for review in reviews])

    summary = _summary_markdown(
        run_dir=run_dir,
        top_result=top_result,
        market_report=market_report,
        account_plan=account_plan,
        task=task,
        package=package,
        reviews=reviews,
    )
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), "summary": str(run_dir / "summary.md")}, ensure_ascii=False))
    return 0


def _assert_active_models() -> None:
    active = {usage: llms.get_active(usage).key for usage in ("llm", "vision", "image")}
    expected = {
        "llm": "lumina::gpt-5.5",
        "vision": "lumina::gpt-5.5",
        "image": "relay::gpt-image-2",
    }
    if active != expected:
        raise RuntimeError(f"active model mismatch: expected={expected}, actual={active}")


def _llm_factory() -> LLMFactory:
    def chat(messages: list[dict[str, Any]], **kwargs: Any) -> str:
        kwargs.setdefault("timeout", 180)
        return llms.chat(messages, **kwargs)

    def chat_json(messages: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("timeout", 180)
        return llms.chat_json(messages, **kwargs)

    def image(prompt: str, **kwargs: Any) -> list[str]:
        kwargs.setdefault("timeout", 300)
        return llms.image(prompt, **kwargs)

    return LLMFactory(chat_func=chat, chat_json_func=chat_json, image_func=image)


def _selected_assets() -> list[Path]:
    paths = [MATERIAL_DIR / name for name in ASSET_NAMES]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing Holly assets: {missing}")
    return paths


def _collect_xhs_notes(market_dir: Path) -> TopNotesResult:
    if not CRAWLER_PYTHON.exists():
        raise FileNotFoundError(f"crawler python not found: {CRAWLER_PYTHON}")
    output_path = market_dir / "xhs_top_notes_result.json"
    child_code = f"""
import json
from pathlib import Path
from data_collect import DataCollector, TopNotesRule

root = Path({str(ROOT)!r})
out = Path({str(market_dir)!r})
dc = DataCollector(project_root=root, python_bin={str(CRAWLER_PYTHON)!r})
rule = TopNotesRule(
    platform='xhs',
    keywords={KEYWORDS!r},
    top_k_per_keyword={TOP_K_PER_KEYWORD},
    download_media=False,
    data_dir=str(out),
)
result = dc.collect_top_notes(rule)
Path({str(output_path)!r}).write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({{'count': len(result.hot_notes), 'insufficient': result.insufficient}}, ensure_ascii=False))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    proc = subprocess.run(
        [str(CRAWLER_PYTHON), "-c", child_code],
        cwd=str(ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=900,
        check=False,
    )
    (market_dir / "crawler_stdout.log").write_text(proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"XHS collection failed with code {proc.returncode}; see {market_dir / 'crawler_stdout.log'}")
    data = json.loads(output_path.read_text(encoding="utf-8"))
    notes = [HotNote(**item) for item in data.get("hot_notes", [])]
    return TopNotesResult(
        platform=str(data.get("platform") or "xhs"),
        queries=list(data.get("queries") or []),
        hot_notes=notes,
        insufficient=list(data.get("insufficient") or []),
        source_data_dir=str(data.get("source_data_dir") or ""),
        source_keyword_dirs=dict(data.get("source_keyword_dirs") or {}),
        source_db=str(data.get("source_db") or ""),
    )


def _build_market_report(
    analyzer: XHSNoteAnalyzer,
    top_result: TopNotesResult,
    brief_text: str,
) -> SessionSkillReport:
    context = {
        "platform": "xhs",
        "topic": "Holly Shit 开心拉屎反焦虑怪趣文创账号冷启动",
        "account_position": "用便便精神、反焦虑、怪趣 IP 和原创文创产品做小红书种草与人格化内容。",
        "target_audience": "高压学习和上班人群、喜欢怪趣文创和反差幽默的年轻女性、原创设计周边买家。",
        "keywords": list(top_result.queries),
        "case_brief": brief_text[:1200],
        "data_dir": top_result.source_data_dir,
        "top_k_per_keyword": TOP_K_PER_KEYWORD,
        "download_media": False,
    }
    if top_result.insufficient:
        raise RuntimeError(f"XHS hot-note collection insufficient: {top_result.insufficient}")
    clusters, leftover, llm_used = analyzer._cluster_hot_notes(top_result.hot_notes)
    skills = [xhs_skill_builder.build_note_skill(cluster, context) for cluster in clusters]
    report = SessionSkillReport(
        context=context,
        keywords=list(top_result.queries),
        skills=skills,
        coverage={"total_notes": len(top_result.hot_notes), "buckets": {s.label: len(s.evidence_notes) for s in skills}},
        leftover_note_ids=leftover,
        source_data_dir=top_result.source_data_dir,
        source_keyword_dirs=dict(top_result.source_keyword_dirs),
        source_db=top_result.source_db,
        insufficient=list(top_result.insufficient),
        llm_enhanced=llm_used,
    )
    xhs_session_reporter.write_session_outputs(report)
    return report


def _client_brief(brief_text: str, account_plan: Any, top_result: TopNotesResult) -> ClientBrief:
    source_refs = [
        {
            "type": "xhs_note",
            "keyword": note.keyword,
            "title": note.title,
            "url": note.note_url,
            "liked": note.liked,
            "collected": note.collected,
        }
        for note in top_result.hot_notes
    ]
    return ClientBrief(
        client_name="Holly",
        brand_name="Holly Shit开心拉屎",
        platform="xhs",
        goals=[
            "让小红书用户快速理解品牌：Shit人生也要拉得开心。",
            "把线下卖得好的怪趣文创转成线上可关注、可收藏、可下单的内容资产。",
            "为后续接 commission、卖杯子/包/钥匙扣/贴纸/冰箱贴等产品建立账号人设。",
        ],
        audience=list(account_plan.audience_profile),
        positioning_notes=[
            account_plan.recommended_positioning,
            "品牌核心不是低俗玩梗，而是用荒诞幽默回收焦虑和身体自主权。",
        ],
        constraints=[
            "保留 Holly Shit 的反叛、自信、搞笑、怪趣调性。",
            "内容必须能落到具体产品或 IP，不只写抽象情绪。",
            "小红书表达要有点击钩子、收藏理由和评论入口。",
        ],
        taboos=[
            "不要把便便梗写成低俗猎奇。",
            "不要虚构销量、价格、疗效或未提供的合作背书。",
            "不要照搬真实竞品笔记句子。",
        ],
        source_materials=source_refs,
        context={"case_brief": brief_text},
    )


def _select_task(calendar: Any) -> Any:
    if not calendar.tasks:
        raise RuntimeError("calendar has no content tasks")
    return sorted(calendar.tasks, key=lambda task: (task.priority, task.scheduled_date or ""))[0]


def _summary_markdown(
    *,
    run_dir: Path,
    top_result: TopNotesResult,
    market_report: SessionSkillReport,
    account_plan: Any,
    task: Any,
    package: Any,
    reviews: list[Any],
) -> str:
    review_lines = []
    for review in reviews:
        data = review.to_dict()
        issues = data.get("issues") or []
        review_lines.append(f"- {data.get('reviewer', '')}: {data.get('status', '')}; issues={len(issues)}")
        for issue in issues[:5]:
            review_lines.append(f"  - {issue.get('severity', '')}: {issue.get('message', '')}")

    note_lines: list[str] = []
    for note in top_result.hot_notes:
        note_lines.extend(
            [
                f"- `{note.keyword}` {note.title} | liked={note.liked} collected={note.collected} comments={note.comment}",
                f"  {note.note_url}",
            ]
        )

    return "\n".join(
        [
            "# Holly Live Case Summary",
            "",
            f"- Run dir: `{run_dir}`",
            "- LLM: `lumina::gpt-5.5`",
            "- Image: `relay::gpt-image-2`",
            f"- XHS keywords: {', '.join(top_result.queries)}",
            f"- Hot notes collected: {len(top_result.hot_notes)}",
            "",
            "## Market Evidence",
            *note_lines,
            "",
            "## Learned Note Skills",
            *[
                f"- {skill.label}: goal={skill.goal}, tone={skill.tone}, evidence={len(skill.evidence_notes)}"
                for skill in market_report.skills
            ],
            "",
            "## Account Direction",
            account_plan.recommended_positioning,
            "",
            "## Selected Task",
            f"- {task.title}",
            f"- topic: {task.topic}",
            f"- objective: {task.objective}",
            "",
            "## Generated Note",
            f"- title: {package.title}",
            f"- tags: {' '.join(package.tags)}",
            f"- cover: `{package.cover_path}`",
            "",
            package.body,
            "",
            "## Review",
            *review_lines,
            "",
            "## Quality Notes",
            "- 产出已经接入真实小红书搜索结果、真实 LLM、真实图片模型；market evidence 可回溯到 `xhs_top_notes_result.json` 和各 keyword 目录。",
            "- 当前样本量为每个关键词 1 篇，适合端到端 smoke/live case，不足以作为稳定内容策略结论。",
            "- 下一步优化应扩大关键词和 top_k，增加竞品账号维度，并对封面进行多候选 A/B 生成与人工选择。",
            "",
        ]
    )


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
