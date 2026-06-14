"""Run the Holly live end-to-end case with real XHS, LLM, and image APIs."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import nori.core.llms as llms
from data_collect.adapter import TopNotesResult
from nori.core import CaseWorkspace, LLMFactory
from nori.workflows import RuntimeRunRecorder
from nori.workflows.content_production import (
    ContentProductionConfig,
    ContentProductionWorkflow,
    record_content_production_artifacts,
    top_notes_result_from_dict,
)


CASE = CaseWorkspace(ROOT, case_id="Holly", title="Holly Shit开心拉屎").ensure()
CASE_DIR = CASE.case_dir
BRIEF_PATH = CASE.brief_dir / "original.md"
MATERIAL_DIR = CASE.raw_assets_dir / "brand_materials"
CRAWLER_PYTHON = ROOT / "data_collect" / "crawler" / ".venv" / "bin" / "python"

KEYWORDS = ["怪趣文创", "反焦虑文创"]
TOP_K_PER_KEYWORD = 3
ASSET_NAMES = [
    "微信图片_20250617195920.jpg",
    "资源 49@2x.png",
    "资源 50@2x.png",
    "明信片 打印文件_画板 1.png",
]

WORKFLOW_NAME = "holly_live_content_generation"
GOAL = "用 Holly 真实素材和小红书市场证据生成一篇图文内容，并生成封面图片。"


def main() -> int:
    _assert_active_models()
    llm_factory = _llm_factory()
    brief_text = BRIEF_PATH.read_text(encoding="utf-8")
    asset_paths = _selected_assets()

    run_dir = CASE.create_run_dir("holly_live", at=datetime.now(), metadata={"workflow_name": WORKFLOW_NAME})
    market_dir = run_dir / "market"
    covers_dir = run_dir / "covers"
    market_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)

    CASE.record_artifact(
        run_id=run_dir.name,
        artifact_type="original_brief",
        path=BRIEF_PATH,
        created_by="user",
        status="source",
    )
    runtime_recorder = RuntimeRunRecorder(
        user_id="holly",
        profile_id="holly",
        workflow_name=WORKFLOW_NAME,
        goal=GOAL,
    )
    runtime = runtime_recorder.start(
        user_input={"brief_text": brief_text, "case_id": CASE.case_id, "case_dir": str(CASE_DIR)},
        run_dir=run_dir,
        source="brief/original.md",
        acceptance=[
            "生成 content_design_spec.json",
            "生成 content_package.json",
            "生成 cover png",
            "生成 summary.md",
        ],
        metadata={"case_id": CASE.case_id, "case_dir": str(CASE_DIR), "case_manifest": str(CASE.case_manifest_path)},
    )
    runtime_recorder.write_snapshot(runtime, run_dir)

    workflow = ContentProductionWorkflow(config=_holly_config())
    state = workflow.initial_state(
        run_dir=run_dir,
        market_dir=market_dir,
        covers_dir=covers_dir,
        llm_factory=llm_factory,
        brief_text=brief_text,
        asset_paths=asset_paths,
        top_notes_collector=_collect_xhs_notes,
    )
    try:
        _final_state, workflow_run = workflow.run(
            state,
            session_id=runtime.session.session_id,
            task_id=runtime.task_goal.task_id,
            human_gate_mode=os.getenv("NORI_HUMAN_GATE_MODE", "skip"),
        )
    except Exception as exc:
        failed_run = getattr(exc, "workflow_run", None)
        if failed_run is not None:
            runtime_recorder.write_snapshot(replace(runtime, workflow_run=failed_run), run_dir)
        CASE.record_run(
            run_dir,
            workflow=WORKFLOW_NAME,
            status="failed",
            metadata={"error_type": type(exc).__name__},
        )
        record_content_production_artifacts(CASE, run_dir, status="failed")
        raise
    runtime = replace(runtime, workflow_run=workflow_run)
    runtime_recorder.write_snapshot(runtime, run_dir)
    CASE.record_run(run_dir, workflow=WORKFLOW_NAME, status="completed")
    record_content_production_artifacts(CASE, run_dir)
    print(json.dumps({"run_dir": str(run_dir), "summary": str(run_dir / "summary.md")}, ensure_ascii=False))
    return 0


def _holly_config() -> ContentProductionConfig:
    return ContentProductionConfig(
        workflow_name=WORKFLOW_NAME,
        client_name="Holly",
        brand_name="Holly Shit开心拉屎",
        platform="xhs",
        project_id_prefix="holly_live",
        project_name="Holly Shit 小红书冷启动",
        topic="Holly Shit 开心拉屎反焦虑怪趣文创账号冷启动",
        account_position="用便便精神、反焦虑、怪趣 IP 和原创文创产品做小红书种草与人格化内容。",
        target_audience="高压学习和上班人群、喜欢怪趣文创和反差幽默的年轻女性、原创设计周边买家。",
        goals=[
            "让小红书用户快速理解品牌：Shit人生也要拉得开心。",
            "把线下卖得好的怪趣文创转成线上可关注、可收藏、可下单的内容资产。",
            "为后续接 commission、卖杯子/包/钥匙扣/贴纸/冰箱贴等产品建立账号人设。",
        ],
        positioning_notes=[
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
        platform_rules=[
            {"rule": "小红书图文首屏必须一眼看出情绪利益点和收藏理由。"},
            {"rule": "标题、封面和正文开头要围绕同一个点击钩子。"},
        ],
        top_k_per_keyword=TOP_K_PER_KEYWORD,
        download_media=False,
        horizon_days=7,
        llm_label="lumina::gpt-5.5",
        image_label="relay::gpt-image-2",
    )


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


def _collect_xhs_notes(market_dir: Path, search_context: dict[str, Any] | None = None) -> TopNotesResult:
    if not CRAWLER_PYTHON.exists():
        raise FileNotFoundError(f"crawler python not found: {CRAWLER_PYTHON}")
    output_path = market_dir / "xhs_top_notes_result.json"
    planned_keywords = [
        str(item).strip()
        for item in ((search_context or {}).get("keywords") or KEYWORDS)
        if str(item).strip()
    ]
    planned_top_k = int((search_context or {}).get("top_k_per_keyword") or TOP_K_PER_KEYWORD)
    child_code = f"""
import json
from pathlib import Path
from data_collect import DataCollector, TopNotesRule

root = Path({str(ROOT)!r})
out = Path({str(market_dir)!r})
dc = DataCollector(project_root=root, python_bin={str(CRAWLER_PYTHON)!r})
rule = TopNotesRule(
    platform='xhs',
    keywords={planned_keywords!r},
    top_k_per_keyword={planned_top_k!r},
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
        cached = _cached_top_notes_result()
        if os.getenv("NORI_HOLLY_ALLOW_CACHED_XHS") == "1" and cached is not None:
            _write_json(market_dir / "xhs_top_notes_result.json", cached.to_dict())
            (market_dir / "crawler_stdout.log").write_text(
                f"{proc.stdout}\n\n[Nori] XHS live collection failed; reused cached top notes because "
                "NORI_HOLLY_ALLOW_CACHED_XHS=1.\n",
                encoding="utf-8",
            )
            return cached
        raise RuntimeError(f"XHS collection failed with code {proc.returncode}; see {market_dir / 'crawler_stdout.log'}")
    data = json.loads(output_path.read_text(encoding="utf-8"))
    return top_notes_result_from_dict(data)


def _cached_top_notes_result() -> TopNotesResult | None:
    candidates = []
    for path in sorted(CASE.runs_dir.glob("*_holly_live/xhs_top_notes_result.json"), reverse=True):
        try:
            result = top_notes_result_from_dict(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
        if result.hot_notes and not result.insufficient:
            candidates.append(result)
    return candidates[0] if candidates else None


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
