"""Intake taxonomy rules and label normalization helpers."""
from __future__ import annotations

from typing import Any

from nori.shared.normalization import dedupe_preserve_order


RuleSet = list[tuple[str, tuple[str, ...]]]

GOAL_RULES: RuleSet = [
    ("品牌认知", ("品宣", "品牌认知", "品牌心智", "品牌介绍", "品牌故事", "brand_awareness")),
    ("获客留资", ("获客", "线索", "留资", "私信", "咨询", "lead_generation")),
    ("产品种草", ("种草", "安利", "推荐", "好物", "产品故事", "product_seeding")),
    ("新品发布", ("上新", "新品", "发布", "上市", "首发", "product_launch")),
    ("销售转化", ("带货", "卖货", "转化", "下单", "购买", "成交", "sales_conversion")),
    ("课程销售", ("卖课", "课程", "训练营", "课", "course_sales")),
    ("涨粉", ("涨粉", "关注", "破圈", "传播", "follower_growth")),
    ("商务合作", ("接广告", "合作", "商务", "品牌合作", "ad_collaboration")),
]

FORMAT_RULES: RuleSet = [
    ("小红书图文", ("小红书", "图文", "笔记", "封面", "xhs_note")),
    ("短视频", ("短视频", "视频", "reels", "short_video")),
    ("Vlog", ("vlog", "日常记录")),
    ("直播", ("直播", "live")),
    ("直播带货", ("直播带货", "live_commerce")),
]

TONE_RULES: RuleSet = [
    ("专业", ("专业", "权威", "可信", "professional")),
    ("高级", ("高端", "高级", "质感", "premium")),
    ("亲和", ("亲和", "温柔", "轻松", "friendly")),
    ("有趣", ("搞笑", "有趣", "幽默", "怪趣", "funny")),
    ("走心", ("走心", "共鸣", "治愈", "emotional")),
    ("干货", ("干货", "方法", "教程", "攻略", "practical")),
    ("犀利", ("毒舌", "犀利", "直接", "sharp")),
]

ANTI_RULES: RuleSet = [
    ("不要硬广", ("不要硬广", "不硬广", "别太广告", "no_hard_sell")),
    ("不要低价感", ("不要低价感", "不低价", "别廉价", "no_cheap_feel")),
    ("保持人设", ("不掉人设", "保持人设", "人设一致", "keep_persona")),
    ("不要太商业", ("不要太商业", "不太商业化", "别太商业", "not_too_commercial")),
    ("不要违规", ("不要违规", "合规", "不要擦边", "不要露骨", "no_sensitive_content")),
]

CREATIVE_RULES: RuleSet = [
    ("品牌标志", ("logo", "标志", "品牌标志")),
    ("设计语言", ("设计语", "视觉语言", "设计理念", "品牌理念", "品牌风格", "design_language")),
    ("品牌色", ("品牌色", "配色", "色彩", "brand_color")),
    ("人设", ("人设", "主理人", "账号人格", "persona")),
    ("IP角色", ("ip", "IP", "角色", "吉祥物")),
    ("口号", ("口头禅", "slogan", "标语", "catchphrase")),
]

COMMERCIAL_RULES: RuleSet = [
    ("店铺链接", ("店铺", "店铺链接", "shop_link")),
    ("商品链接", ("商品链接", "购买链接", "产品链接", "product_link")),
    ("优惠", ("优惠", "折扣", "券", "福利", "discount")),
    ("课程", ("课程", "训练营", "课", "course")),
    ("合作品", ("合作品", "联名", "合作款", "collaboration")),
    ("橱窗", ("橱窗", "showcase_window")),
]

GUARDRAIL_RULES: RuleSet = [
    ("品牌规范", ("guideline", "品牌规范", "视觉规范", "brand_guideline")),
    ("禁用词", ("禁用词", "不能说", "不要出现", "forbidden_words")),
    ("人设边界", ("人设边界", "不掉人设", "persona_boundary")),
    ("品类边界", ("不接", "不碰", "不做", "category_boundary")),
]

DATA_RULES: RuleSet = [
    ("账号数据", ("账号数据", "后台数据", "数据", "account_data")),
    ("对标内容", ("竞品", "对标", "参考账号", "competitor_content")),
    ("受众画像", ("粉丝画像", "用户画像", "受众画像", "audience_profile")),
    ("同类账号", ("同类博主", "同类账号", "similar_creator")),
    ("爆款案例", ("爆款", "高赞", "爆文", "viral_examples")),
]

QUESTION_MAP = {
    "goal": "这次内容最重要的目标是什么？比如涨粉、种草、品宣、转化。",
    "topic": "这次要围绕什么主题、产品或活动来做？",
}


def dedupe(items: list[str]) -> list[str]:
    return dedupe_preserve_order(items)


def clean_unknown(value: str) -> str:
    value = value.strip()
    return "" if value in {"", "unknown", "未知", "None", "null"} else value


def allowed_label(value: Any, rules: RuleSet, fallback: str) -> str:
    text = clean_unknown(str(value or ""))
    if not text:
        return fallback
    aliases = label_aliases(rules)
    mapped = aliases.get(text, text)
    return mapped if mapped in allowed_values(rules) else fallback


def allowed_list(value: Any, allowed: set[str], fallback: list[str], aliases: dict[str, str] | None = None) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item) for item in value]
    else:
        items = []
    alias_map = aliases or {}
    cleaned = []
    for item in items:
        text = item.strip()
        mapped = alias_map.get(text, text)
        if mapped in allowed:
            cleaned.append(mapped)
    return dedupe(cleaned or list(fallback))


def allowed_values(rules: RuleSet) -> set[str]:
    return {value for value, _ in rules}


def label_aliases(rules: RuleSet) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for value, keywords in rules:
        aliases[value] = value
        aliases[value.lower()] = value
        for keyword in keywords:
            aliases[keyword] = value
            aliases[keyword.lower()] = value
    return aliases


def missing_fields(text: str, intention: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not text:
        missing.append("topic")
    if not intention.get("goal"):
        missing.append("goal")
    return missing


def normalize_missing(value: Any, *, text: str, intention: dict[str, Any]) -> list[str]:
    if isinstance(value, str):
        raw_items = [value]
    elif isinstance(value, list):
        raw_items = [str(item) for item in value]
    else:
        raw_items = []
    missing = [item for item in raw_items if item in QUESTION_MAP]
    for item in missing_fields(text.strip(), intention):
        if item not in missing:
            missing.append(item)
    return missing


def normalize_questions(value: Any, missing: list[str]) -> list[str]:
    if isinstance(value, str):
        questions = [value]
    elif isinstance(value, list):
        questions = [str(item) for item in value if str(item).strip()]
    else:
        questions = []
    if not questions:
        questions = questions_for_missing(missing)
    return questions[:2]


def questions_for_missing(missing: list[str]) -> list[str]:
    return [QUESTION_MAP[item] for item in missing]


def pick_first(text: str, rules: RuleSet) -> str:
    lowered = text.lower()
    for value, keywords in rules:
        if any(keyword.lower() in lowered for keyword in keywords):
            return value
    return ""


def pick_many(text: str, rules: RuleSet) -> list[str]:
    lowered = text.lower()
    return [value for value, keywords in rules if any(keyword.lower() in lowered for keyword in keywords)]


def creative_assets(text: str, images: list[str]) -> list[str]:
    assets = pick_many(text, CREATIVE_RULES)
    if images:
        assets.append("图片资产")
    return dedupe(assets)


def commercial_assets(text: str) -> list[str]:
    return pick_many(text, COMMERCIAL_RULES)


def guardrails(text: str) -> list[str]:
    items = pick_many(text, GUARDRAIL_RULES)
    items.extend(pick_many(text, ANTI_RULES))
    return dedupe(items)


def data_refs(text: str) -> list[str]:
    return pick_many(text, DATA_RULES)
