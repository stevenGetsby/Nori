"""Analyze Xiaohongshu notes into cold-start seed skill drafts.

旧入口 ``analyze_note`` 处理本地 cold_start_data 单篇 meta.json。
新入口 ``collect_for_session`` 根据 context 调用 data_collect 接口
搜回平台高赞笔记 → 聚类 → 给每类输出可执行 NoteSkill。
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from nori.core import AgentBase, LLMFactory
from nori.shared.case_log import write_stage_log
from nori.agents.market_analysis.models import SessionSkillReport, XHSNoteSample, XHSSeedSkillDraft
from . import loader as xhs_note_loader
from . import note_llm as xhs_note_llm
from . import rules as xhs_note_rules
from . import session_clustering as xhs_session_clustering
from . import session_llm as xhs_session_llm
from . import session_reporter as xhs_session_reporter
from . import skill_builder as xhs_skill_builder


class XHSNoteAnalyzerLLMError(xhs_session_llm.XHSSessionLLMError):
    """Raised when fail-fast session-level analyzer LLM stages fail."""


class XHSNoteAnalyzer(AgentBase):
    """Extract executable XHS note-making skill drafts from crawled note data."""

    stage_name = "xhs_note_analyzer"

    def __init__(
        self,
        data_root: str | Path = "cold_start_data/xhs",
        *,
        use_llm: bool = True,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=use_llm, llm_factory=llm_factory)
        self.data_root = Path(data_root)

    def iter_note_meta_paths(self, category: str) -> list[Path]:
        category_dir = self.data_root / category
        if not category_dir.exists():
            raise FileNotFoundError(f"XHS cold-start category not found: {category_dir}")
        return sorted(category_dir.glob("*/posts/*/meta.json"))

    def pick_random_note(self, category: str = "设计", *, seed: int | None = None) -> XHSNoteSample:
        paths = self.iter_note_meta_paths(category)
        if not paths:
            raise FileNotFoundError(f"No XHS note meta files found in {self.data_root / category}")
        rng = random.Random(seed)
        return self.load_note(rng.choice(paths))

    def load_note(self, meta_path: str | Path) -> XHSNoteSample:
        return xhs_note_loader.load_note_sample(meta_path)

    def run(self, note: XHSNoteSample, *, use_llm: bool | None = None) -> XHSSeedSkillDraft:
        """Standard AgentBase entrypoint for single-note analysis."""
        return self.analyze_note(note, use_llm=use_llm)

    def analyze_note(self, note: XHSNoteSample, *, use_llm: bool | None = None) -> XHSSeedSkillDraft:
        rule_draft = xhs_note_rules.rule_analyze_note(note)
        should_use_llm = self.use_llm if use_llm is None else use_llm
        if not should_use_llm:
            return rule_draft
        return xhs_note_llm.enhance_note(
            note,
            rule_draft,
            chat_func=self.llm_factory.chat_func,
            chat_json_func=self.llm_factory.chat_json_func,
        ) or xhs_note_llm.mark_llm_fallback(rule_draft)

    # ============ 会话级：搜索 → 聚类 → 技能 ============

    def collect_for_session(
        self,
        context: dict[str, Any],
        *,
        dc=None,
        max_keywords: int = 3,
    ) -> SessionSkillReport:
        """根据 context 出关键词 → 拉热门 → 聚类 → 每类一条 NoteSkill。

        context 字段（都可选）：
          - topic / account_position / target_audience : 描述走 LLM 出词
          - keywords : list[str]，给了就直接用，不走 LLM
          - platform : 默认 'xhs'
          - days : 默认 30
          - top_k_per_keyword : 默认 5
          - min_liked : 默认 500
          - pool_size : 默认 20，每轮最多一页候选
          - download_media : 默认 True
                    - data_dir : 默认 nori/skill_base/data/xhs_note_analyzer
        """
        from data_collect import DataCollector, TopNotesRule

        if not self.use_llm:
            raise ValueError("会话级 XHS Note 分析必须启用 LLM，不能使用纯规则模式产出 skill")

        # 1) 关键词
        keywords = [str(k).strip() for k in (context.get("keywords") or []) if str(k).strip()]
        if not keywords:
            if not self.use_llm:
                raise ValueError("context.keywords 缺失且未启用 LLM，无法生成关键词")
            keywords = xhs_session_llm.generate_keywords(
                context,
                max_n=max_keywords,
                error_type=XHSNoteAnalyzerLLMError,
                llm_factory=self.llm_factory,
            )
        keywords = keywords[:max_keywords]
        if not keywords:
            raise ValueError("无法从 context 推出搜索关键词")

        # 2) 调用 data_collect.collect_top_notes
        platform = context.get("platform", "xhs")
        rule = TopNotesRule(
            platform=platform,
            keywords=keywords,
            days=int(context.get("days", 30)),
            top_k_per_keyword=int(context.get("top_k_per_keyword", 5)),
            min_liked=int(context.get("min_liked", 500)),
            pool_size=int(context.get("pool_size", 20)),
            download_media=bool(context.get("download_media", True)),
            data_dir=str(context.get("data_dir") or "nori/skill_base/data/xhs_note_analyzer"),
        )
        owned_dc = dc is None
        dc = dc or DataCollector()
        try:
            if platform == "xhs":
                dc.start_sign_server()
            top_result = dc.collect_top_notes(rule)
        finally:
            if owned_dc:
                dc.stop_all()

        if top_result.insufficient:
            raise RuntimeError(f"高赞采集不足，停止生成 skill: {top_result.insufficient}")

        hot_notes = top_result.hot_notes

        # 3) 聚类
        clusters, leftover, llm_used = self._cluster_hot_notes(hot_notes)

        # 4) 每桶 NoteSkill
        skills = [xhs_skill_builder.build_note_skill(c, context) for c in clusters]

        # 5) 装 report + case log
        report = SessionSkillReport(
            context=dict(context),
            keywords=list(keywords),
            skills=skills,
            coverage={
                "total_notes": len(hot_notes),
                "buckets": {s.label: len(s.evidence_notes) for s in skills},
            },
            leftover_note_ids=leftover,
            source_data_dir=top_result.source_data_dir,
            source_keyword_dirs=dict(getattr(top_result, "source_keyword_dirs", {})),
            insufficient=list(top_result.insufficient),
            llm_enhanced=llm_used,
        )
        xhs_session_reporter.write_session_outputs(report)

        write_stage_log(
            stage="xhs_note_analyzer",
            case="session_skill",
            input_data={
                "context": dict(context),
                "search": {
                    "platform": platform,
                    "keywords": list(keywords),
                    "days": rule.days,
                    "top_k_per_keyword": rule.top_k_per_keyword,
                    "pool_size": rule.pool_size,
                    "download_media": rule.download_media,
                    "data_dir": rule.data_dir,
                },
            },
            output_data=report.to_dict(),
            config={"use_llm": self.use_llm},
        )
        return report

    def _cluster_hot_notes(self, hot_notes):
        """规则桶 + LLM 标签 → 收敛 1-4 桶。"""
        if not self.use_llm:
            raise ValueError("会话级 XHS Note 分析必须启用 LLM")
        return xhs_session_clustering.cluster_hot_notes(
            hot_notes,
            label_notes=lambda notes: xhs_session_llm.label_notes(
                notes,
                error_type=XHSNoteAnalyzerLLMError,
                llm_factory=self.llm_factory,
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze XHS note data into a seed skill draft.")
    parser.add_argument("--data-root", default="cold_start_data/xhs")
    parser.add_argument("--category", default="设计")
    parser.add_argument("--meta-path", default="")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    analyzer = XHSNoteAnalyzer(args.data_root, use_llm=not args.no_llm)
    note = analyzer.load_note(args.meta_path) if args.meta_path else analyzer.pick_random_note(args.category, seed=args.seed)
    skill = analyzer.analyze_note(note)
    print(json.dumps(skill.to_dict(), ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
