"""Prompt templates owned by XHSNoteAnalyzer."""
from __future__ import annotations


NOTE_SYSTEM_PROMPT = "你是 Nori 的 XHS Note Skill Analyzer。只输出 JSON。"

NOTE_USER_PROMPT = """\
基于规则 analyzer 已抽取的结构和证据，深化小红书 note 的 seed skill draft。

原始 note：
{note}

规则草案：
{rule_draft}

你要做的事：
1. 只基于原始 note 和规则草案，不编造没有证据的事实。
2. 把规则写得更像可执行创作技能，而不是复述原文内容。
3. 保留单篇草案定位，不要声称这是稳定 skill。
4. evidence 字段只能引用给定 note 或规则草案中的证据。

输出 JSON，字段固定：
{{
    "match": {{
        "scene": "具体 note 场景",
        "goals": ["目标，3个以内"],
        "note_type": "图文/视频"
    }},
    "craft": {{
        "creative_goal": "一句话说明这类 note 的创作目标",
        "title_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "opening_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "body_structure": [{{"name": "结构步骤", "rule": "可执行规则", "evidence": "证据片段"}}],
        "interaction_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "visual_rules": [{{"name": "规则名", "rule": "可执行规则", "evidence": "证据片段"}}],
        "avoid_rules": ["禁忌，必须可执行"]
    }},
    "evidence": {{
        "llm_observations": ["LLM 基于证据提炼出的观察，5条以内"]
    }},
    "validation": {{
        "llm_notes": ["这份草案仍需如何验证，3条以内"]
    }}
}}
"""

KEYWORD_SYSTEM_PROMPT = "你是 Nori 的小红书选词助手，只输出 JSON。"

KEYWORD_USER_PROMPT = """\
根据本次创作 context，给出 1-{max_n} 个小红书搜索关键词。

context:
{context}

要求：
1. 每个关键词长度 2-12 个汉字，能让小红书搜索召回到相关内容。
2. 关键词要覆盖 context 里描述的话题或场景，不要发散。
3. 不要返回品牌名或带 #/【】 等特殊符号。
4. 输出 JSON: {{"keywords": ["...", "..."]}}
"""

LABEL_SYSTEM_PROMPT = "你是 Nori 的小红书笔记目标识别助手，只输出 JSON。"

LABEL_USER_PROMPT = """\
给下面这批小红书笔记每篇打 goal 和 tone 标签。

候选 goal: tutorial / planting / debrief / opinion / news / rant / general
候选 tone（不限于）: 科普 / 吐槽 / 朋友安利 / 专业测评 / 干货 / 个人经验

笔记列表:
{notes}

输出 JSON: {{"labels": [{{"note_id": "...", "goal": "...", "tone": "..."}}, ...]}}
"""


__all__ = [
    "KEYWORD_SYSTEM_PROMPT",
    "KEYWORD_USER_PROMPT",
    "LABEL_SYSTEM_PROMPT",
    "LABEL_USER_PROMPT",
    "NOTE_SYSTEM_PROMPT",
    "NOTE_USER_PROMPT",
]
