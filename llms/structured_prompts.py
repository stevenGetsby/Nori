"""Prompt builders for structured LLM helper modules."""
from __future__ import annotations

from typing import Any


INTENT_FIELD_DESCRIPTIONS: dict[str, str] = {
    "topic": "本次内容的核心主题（1 句话以内，不要包含'分享'/'今天'这类无信息词）。",
    "content_type": "小红书内容形态枚举，只能从 enum 里选一个。",
    "audience": "主要受众画像（如：新手宝妈、职场新人、健身入门者）。",
    "goal": "本条内容期望达成的目标（如：收藏、转发、获客、表达观点）。",
    "tone": "整体语气调性（如：清晰自然、专业克制、生活化、犀利直接、温柔陪伴）。",
    "scene_hint": "封面期望的场景倾向（如：桌面静物、人像特写、对比拼图）。",
    "style_reference": "用户提到的视觉/文案参考（作品、博主、风格关键词）。",
}


def build_intent_system_prompt(
    fields: list[str],
    enum_constraints: dict[str, list[str]],
    max_candidates: int,
) -> str:
    field_lines: list[str] = []
    for field in fields:
        desc = INTENT_FIELD_DESCRIPTIONS.get(field, "")
        if field in enum_constraints:
            allowed = "/".join(enum_constraints[field])
            field_lines.append(f"- {field}: {desc} 只能从枚举中选：[{allowed}]")
        else:
            field_lines.append(f"- {field}: {desc}")

    field_block = "\n".join(field_lines)

    return (
        "你是小红书内容意图抽取器。\n"
        "任务：从用户的需求文本中抽取下列字段，只输出 JSON 对象，不要解释、不要前后缀。\n\n"
        f"需要抽取的字段：\n{field_block}\n\n"
        "硬性规则：\n"
        "1. 抽不到、不确定、用户没明确写的字段，对应 value 必须为 null。\n"
        "2. 不要编造内容，不要把'分享'/'今天'这类无意义词当 topic。\n"
        "3. 枚举字段必须严格落在给定枚举内，不在则返回 null。\n"
        f"4. 每个字段可以额外提供至多 {max_candidates} 个候选，"
        "格式：{\"value\": <主选>, \"candidates\": [<可选>, ...]}；"
        "若只有一个候选，直接给字符串即可。\n"
        "5. 输出必须是合法 JSON，键名严格使用上面给出的英文字段名。"
    )


def build_intent_user_prompt(text: str, fields: list[str]) -> str:
    schema_keys = ", ".join(f'"{field}"' for field in fields)
    return (
        "用户需求文本：\n"
        f"<<<\n{text}\n>>>\n\n"
        f"请输出 JSON，仅包含 keys: {{{schema_keys}}}。"
    )


def build_target_system_prompt(options: list[dict[str, Any]], max_alternatives: int) -> str:
    catalog_lines: list[str] = []
    for opt in options:
        sel = opt["selector"]
        role = opt.get("role") or ""
        kind = opt.get("kind") or ""
        summary = (opt.get("summary") or "").strip()
        if summary:
            summary = summary.replace("\n", " ")
            if len(summary) > 80:
                summary = summary[:77] + "..."
        bits = [f"selector={sel}"]
        if role:
            bits.append(f"role={role}")
        if kind:
            bits.append(f"kind={kind}")
        if summary:
            bits.append(f"summary={summary}")
        catalog_lines.append("- " + " | ".join(bits))

    catalog_block = "\n".join(catalog_lines)

    return (
        "你是一个对话编辑路由器。\n"
        "任务：用户对一份已生成的小红书内容提出了一条编辑指令；"
        "请从候选资产里挑出一个最适合被这条指令改写的 target selector，"
        "并把指令改写成无歧义、面向该资产的版本。\n\n"
        "可选资产：\n"
        f"{catalog_block}\n\n"
        "硬性规则：\n"
        "1. target_selector 必须是上面列出的 selector 字符串之一，不要发明新值。\n"
        "2. 如果用户指令里明显涉及画面/封面/视觉/构图 -> 选 role=cover_image；\n"
        "   如果指令涉及标题/正文/文案/口吻/标签 -> 选 role=copy_text；\n"
        "   不要去选 role=package / role=review / role=scratch（这些不允许编辑）。\n"
        "3. refined_instruction 中不要再用'封面'/'图'/'文案'这种指代词，"
        "要写成对该资产可直接执行的祈使句；语义不能改变。\n"
        f"4. alternatives 至多 {max_alternatives} 个；只能从候选里选；不要重复主选。\n"
        "5. confidence 取 high/medium/low 之一。\n"
        "6. 输出严格 JSON：{\"target_selector\": str, \"refined_instruction\": str,"
        " \"alternatives\": [str], \"confidence\": \"high|medium|low\","
        " \"reason\": str}。不要解释，不要前后缀。"
    )


def build_target_user_prompt(instruction: str, history: list[str]) -> str:
    parts = [
        "用户编辑指令：",
        f"<<<\n{instruction}\n>>>",
    ]
    if history:
        parts.append("")
        parts.append("最近对话摘要（最旧 -> 最新）：")
        for line in history:
            parts.append(f"- {line}")
    return "\n".join(parts)
