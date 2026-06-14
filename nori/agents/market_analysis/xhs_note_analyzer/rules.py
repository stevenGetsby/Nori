"""Rule-based single-note analysis helpers for Xiaohongshu notes."""
from __future__ import annotations

import re
from typing import Any

from nori.agents.market_analysis.schemas import XHSNoteSample, XHSSeedSkillDraft


def rule_analyze_note(note: XHSNoteSample) -> XHSSeedSkillDraft:
    lines = content_lines(note.desc)
    title_rule_rows = title_rules(note.title)
    opening_rule_rows = opening_rules(lines)
    body_step_rows = body_steps(note, lines)
    interaction_rule_rows = interaction_rules(note, lines)
    visual_rule_rows = visual_rules(note)
    avoid_rule_rows = avoid_rules(note, lines)
    scene = scene_for_note(note, lines)
    goals = goals_for_note(note, lines)
    confidence = confidence_for_note(note, title_rule_rows, body_step_rows)
    return XHSSeedSkillDraft(
        skill_id=f"seed.xhs.{slug(note.category)}.note.single.{note.note_id}",
        category=note.category,
        match={
            "platform": ["小红书"],
            "category": [note.category],
            "scene": scene,
            "goals": goals,
            "note_type": note.note_type or "图文",
        },
        craft={
            "creative_goal": creative_goal(scene),
            "title_rules": title_rule_rows,
            "opening_rules": opening_rule_rows,
            "body_structure": body_step_rows,
            "interaction_rules": interaction_rule_rows,
            "visual_rules": visual_rule_rows,
            "avoid_rules": avoid_rule_rows,
        },
        evidence={
            "note_count": 1,
            "confidence": confidence,
            "source_note": {
                "note_id": note.note_id,
                "title": note.title,
                "author": note.author_name,
                "metrics": note.metrics,
                "image_count": note.image_count,
                "tags": note.tags,
                "meta_path": str(note.meta_path),
                "note_url": note.note_url,
            },
            "text_evidence": {
                "opening": lines[:2],
                "section_markers": section_markers(lines),
                "cta_lines": cta_lines(lines),
            },
        },
        validation={
            "result": "draft_only",
            "llm_enhanced": False,
            "pipeline": ["rule_analyzer"],
            "reason": "单篇笔记只能形成候选规则，不能证明稳定 seed skill。",
            "next_check": [
                "同类笔记中重复出现的规则才可升为 seed skill。",
                "需要用留出笔记验证结构可解释性。",
                "需要与无 skill 生成结果做对照评估。",
            ],
        },
    )


def content_lines(desc: str) -> list[str]:
    return [line.strip() for line in re.split(r"[\r\n]+", desc or "") if line.strip()]


def title_rules(title: str) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    if "｜" in title or "|" in title:
        rules.append({"name": "栏目式标题", "rule": "用栏目名加项目名，让用户先知道内容类型。", "evidence": title})
    if "？" in title or "?" in title:
        rules.append({"name": "提问式标题", "rule": "用一个具体问题制造点击理由。", "evidence": title})
    if "！" in title or "!" in title:
        rules.append({"name": "口播感标题", "rule": "用强语气让标题像一句现场发言。", "evidence": title})
    if re.search(r"\d", title):
        rules.append({"name": "数字钩子", "rule": "标题里放数字，暗示清单、步骤或结果。", "evidence": title})
    if len(title) <= 18:
        rules.append({"name": "短标题", "rule": "标题控制在短句内，先给情绪或悬念。", "evidence": title})
    if not rules:
        rules.append({"name": "观点标题", "rule": "用一句明确观点承载整篇 note 的角度。", "evidence": title})
    return rules


def opening_rules(lines: list[str]) -> list[dict[str, str]]:
    if not lines:
        return []
    first = lines[0]
    rules = [{"name": "首句定场", "rule": "第一句先给场景、情绪或判断，不急着解释信息。", "evidence": first}]
    if len(first) <= 18:
        rules.append({"name": "短句开场", "rule": "用短句开场，让用户快速进入语境。", "evidence": first})
    if "？" in first or "?" in first:
        rules.append({"name": "问题开场", "rule": "开头抛问题，后文负责回答。", "evidence": first})
    return rules


def body_steps(note: XHSNoteSample, lines: list[str]) -> list[dict[str, str]]:
    if is_design_case(note, lines):
        return design_case_body_steps(lines)
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "开场", "rule": "先给情绪、场景或核心判断。", "evidence": lines[0]})
    question_lines = [line for line in lines if "？" in line or "?" in line]
    if question_lines:
        steps.append({"name": "连续追问", "rule": "用问题串推动阅读，让用户带着疑问往下看。", "evidence": question_lines[0]})
    section_lines = section_markers(lines)
    if section_lines:
        steps.append({"name": "模块分段", "rule": "用明确小标题承载规则、方向、奖励或清单信息。", "evidence": section_lines[0]})
    action_lines = cta_lines(lines)
    if action_lines:
        steps.append({"name": "行动收口", "rule": "结尾给发布、搜索、参与、收藏或购买动作。", "evidence": action_lines[0]})
    tag_lines = [line for line in lines if "#" in line]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用话题标签承接平台分发和活动入口。", "evidence": tag_lines[-1]})
    if len(steps) == 1 and len(lines) > 2:
        steps.append({"name": "叙事展开", "rule": "用多段短句逐步补充原因、细节和结果。", "evidence": lines[min(1, len(lines) - 1)]})
    return steps


def interaction_rules(note: XHSNoteSample, lines: list[str]) -> list[dict[str, str]]:
    rules = []
    if note.tags:
        rules.append({"name": "话题入口", "rule": "保留核心话题标签，方便平台识别主题。", "evidence": " ".join(note.tags[:3])})
    action_lines = cta_lines(lines)
    if action_lines:
        rules.append({"name": "明确动作", "rule": "给用户一个低成本动作，如搜索、发布、参与、收藏。", "evidence": action_lines[0]})
    if note.metrics.get("commented", 0) > 0:
        rules.append({"name": "评论触发", "rule": "标题或正文要留下可回答的问题。", "evidence": f"comment_count={note.metrics['commented']}"})
    return rules


def visual_rules(note: XHSNoteSample) -> list[dict[str, str]]:
    rules = [{"name": "封面先承担点击", "rule": "封面必须先表达主题、情绪或问题，不只是放素材。", "evidence": "cover.jpg"}]
    if note.image_count >= 3:
        rules.append({"name": "多图递进", "rule": "图集应承担信息递进：封面吸引，后续图补充细节。", "evidence": f"image_count={note.image_count}"})
    else:
        rules.append({"name": "少图集中", "rule": "少图笔记要让单张图完成主题表达。", "evidence": f"image_count={note.image_count}"})
    return rules


def avoid_rules(note: XHSNoteSample, lines: list[str]) -> list[str]:
    rules = ["不要照搬原笔记句子，只抽结构和方法。", "不要把单篇个例直接当稳定规律。"]
    text = f"{note.title}\n" + "\n".join(lines)
    if "活动" in text or "奖励" in text:
        rules.append("活动型 note 不要只堆规则，要先给用户参与理由。")
    if "搜索" in text:
        rules.append("搜索引导要自然出现，不要像硬插入口令。")
    return rules


def scene_for_note(note: XHSNoteSample, lines: list[str]) -> str:
    text = f"{note.title}\n" + "\n".join(lines)
    if is_design_case(note, lines):
        return "设计案例解析型 note"
    if any(word in text for word in ("参与方式", "活动奖励", "发起", "活动页")):
        return "活动招募型 note"
    if any(word in text for word in ("教程", "步骤", "攻略", "怎么")):
        return "教程攻略型 note"
    if any(word in text for word in ("好物", "种草", "值得买", "推荐")):
        return "种草推荐型 note"
    if "？" in note.title or "?" in note.title:
        return "问题悬念型 note"
    return "观点叙事型 note"


def goals_for_note(note: XHSNoteSample, lines: list[str]) -> list[str]:
    text = f"{note.title}\n" + "\n".join(lines)
    if is_design_case(note, lines):
        return ["作品展示", "设计灵感", "品牌表达"]
    goals = []
    if any(word in text for word in ("参与", "发布", "活动", "奖励")):
        goals.append("活动参与")
    if any(word in text for word in ("搜索", "活动页", "话题")):
        goals.append("平台搜索")
    if any(word in text for word in ("收藏", "攻略", "清单")):
        goals.append("收藏")
    if any(word in text for word in ("评论", "你觉得", "谁说了算")):
        goals.append("互动")
    return goals or ["阅读完成"]


def creative_goal(scene: str) -> str:
    if scene == "设计案例解析型 note":
        return "把一个设计项目讲成有背景、有方法、有审美判断的作品案例。"
    if scene == "活动招募型 note":
        return "先让用户理解参与理由，再交代参与方式和奖励。"
    if scene == "教程攻略型 note":
        return "把复杂信息拆成可收藏、可执行的步骤。"
    if scene == "种草推荐型 note":
        return "把产品或对象包装成具体生活场景里的解决方案。"
    if scene == "问题悬念型 note":
        return "用问题带动点击和评论，再在正文里逐步给答案。"
    return "用一个清晰观点组织内容，让用户愿意继续读完。"


def section_markers(lines: list[str]) -> list[str]:
    return [line for line in lines if re.search(r"^【.+】", line) or line.endswith("：")][:5]


def cta_lines(lines: list[str]) -> list[str]:
    keywords = ("搜索", "发布", "收藏", "评论", "私信", "下单", "购买", "进入", "参与方式", "参与活动")
    return [line for line in lines if any(keyword in line for keyword in keywords)][:5]


def is_design_case(note: XHSNoteSample, lines: list[str]) -> bool:
    text = f"{note.title}\n" + "\n".join(lines)
    design_signals = ("视觉", "设计", "海报", "平面", "创作团队", "项目时间", "原创设计", "设计灵感")
    return note.category == "设计" and sum(1 for signal in design_signals if signal in text) >= 2


def design_case_body_steps(lines: list[str]) -> list[dict[str, str]]:
    steps: list[dict[str, str]] = []
    if lines:
        steps.append({"name": "项目缘起", "rule": "先交代项目来源、主题或活动背景。", "evidence": lines[0]})
    context_line = first_line_with(lines, ("通过", "在", "邀请", "起点"), start=1)
    if context_line:
        steps.append({"name": "场景展开", "rule": "用地点、对象或行动把设计项目放进真实语境。", "evidence": context_line})
    visual_line = first_line_with(lines, ("视觉", "海报", "结构", "色", "图形", "字体"), start=1)
    if visual_line:
        steps.append({"name": "视觉方法", "rule": "说明设计系统、色彩、图形或版式如何服务主题。", "evidence": visual_line})
    meaning_line = first_line_with(lines, ("不只是", "不只", "牵动", "意义", "联结"), start=1)
    if meaning_line:
        steps.append({"name": "概念升华", "rule": "从视觉方法上升到情绪、文化或品牌意义。", "evidence": meaning_line})
    credit_line = first_line_with(lines, ("项目时间", "创作团队", "版权所有"), start=1)
    if credit_line:
        steps.append({"name": "项目信息", "rule": "保留项目时间、团队和版权信息，建立作品可信度。", "evidence": credit_line})
    tag_lines = [line for line in lines if "#" in line]
    if tag_lines:
        steps.append({"name": "话题归档", "rule": "用设计相关话题承接搜索、收藏和同好分发。", "evidence": tag_lines[-1]})
    return steps


def first_line_with(lines: list[str], keywords: tuple[str, ...], *, start: int = 0) -> str:
    for line in lines[start:]:
        if any(keyword in line for keyword in keywords):
            return line
    return ""


def confidence_for_note(
    note: XHSNoteSample,
    title_rule_rows: list[dict[str, str]],
    body_step_rows: list[dict[str, str]],
) -> float:
    score = 0.35
    if note.title:
        score += 0.1
    if note.desc:
        score += 0.1
    if note.tags:
        score += 0.08
    if note.image_count:
        score += 0.07
    if len(title_rule_rows) >= 2:
        score += 0.1
    if len(body_step_rows) >= 3:
        score += 0.1
    if sum(note.metrics.values()) > 0:
        score += 0.1
    return round(min(score, 0.9), 2)


def slug(value: str) -> str:
    text = str(value or "skill").strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", text)
    return text.strip("_") or "skill"


__all__ = [
    "avoid_rules",
    "body_steps",
    "confidence_for_note",
    "content_lines",
    "creative_goal",
    "cta_lines",
    "design_case_body_steps",
    "first_line_with",
    "goals_for_note",
    "interaction_rules",
    "is_design_case",
    "opening_rules",
    "rule_analyze_note",
    "scene_for_note",
    "section_markers",
    "slug",
    "title_rules",
    "visual_rules",
]
