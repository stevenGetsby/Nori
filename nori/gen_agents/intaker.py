"""Intaker Agent: normalize text/image user input into Intention + Context.

图片处理两道工序：
  - _rule_intake / _llm_intake : 走文本理解，拿 intention + context（旧）
  - _tag_images_llm            : vision LLM “单图 + 用户文本”并发调用，给每张图打
                                  语义标签，写进 IntakeResult.assets 供下游 Agent 选图
"""
from __future__ import annotations

import concurrent.futures
import json
import sys
from pathlib import Path
from typing import Any

import llms
from nori.agent_models import IntakeResult, UserAsset, UserInput

from ._image_io import image_to_data_uri


# vision 打标的并发度（每张图 = 1 次 LLM）
VISION_PARALLELISM = 6

# 允许的视觉角色字典；超出此集合的 LLM 输出会被丢弃
ALLOWED_VISION_ROLES = {
    "brand_logo", "ip_character", "product_shot", "scene_photo",
    "lifestyle", "data_chart", "reference_style", "raw_material",
    "portrait", "unknown",
}
ALLOWED_USABLE_FOR = {"cover", "body", "background_only", "not_usable"}
ALLOWED_QUALITY = {"high", "medium", "low"}


class IntakeAgent:
    """First-step agent for the new Nori flow."""

    def __init__(self, *, use_llm: bool = True, use_vision: bool = True) -> None:
        self.use_llm = use_llm
        self.use_vision = use_vision

    def run(
        self,
        user_input: UserInput | str,
        images: list[str] | None = None,
        *,
        use_llm: bool | None = None,
        use_vision: bool | None = None,
    ) -> IntakeResult:
        normalized = _normalize_input(user_input, images)
        fallback = _rule_intake(normalized)
        should_use_llm = self.use_llm if use_llm is None else use_llm
        result = fallback if not should_use_llm else (_llm_intake(normalized, fallback) or fallback)

        # use_llm=False 时整体关闭所有 LLM 调用（包括 vision 打标）
        if use_vision is None:
            should_use_vision = self.use_vision and should_use_llm
        else:
            should_use_vision = use_vision
        result.assets = _build_tagged_assets(normalized, use_vision=should_use_vision)
        return result


intake = IntakeAgent().run


SYSTEM_PROMPT = "你是 Nori 的 Intaker Agent。只输出 JSON。"

USER_PROMPT = """\
把用户输入整理成 Nori 后续 Agent 可用的 Intention + Context。

用户文字：
{text}

用户图片：
{images}

输出 JSON，字段固定：
{{
  "intention": {{
        "goal": "品牌认知 | 获客留资 | 产品种草 | 新品发布 | 销售转化 | 课程销售 | 涨粉 | 商务合作 | 未知",
        "format": "小红书图文 | 短视频 | Vlog | 直播 | 直播带货 | 未知",
        "tone": ["专业 | 高级 | 亲和 | 有趣 | 走心 | 干货 | 犀利"],
        "anti": ["不要硬广 | 不要低价感 | 保持人设 | 不要太商业 | 不要违规"]
  }},
  "context": {{
        "creative_assets": ["品牌标志 | 设计语言 | 品牌色 | 人设 | IP角色 | 口号 | 图片资产"],
        "commercial_assets": ["店铺链接 | 商品链接 | 优惠 | 课程 | 合作品 | 橱窗"],
        "guardrails": ["品牌规范 | 禁用词 | 人设边界 | 品类边界 | 不要硬广 | 不要低价感 | 保持人设 | 不要太商业 | 不要违规"],
        "data_refs": ["账号数据 | 对标内容 | 受众画像 | 同类账号 | 爆款案例"]
  }},
  "missing": ["goal | topic"],
  "questions": ["必要澄清问题"]
}}

要求：
- 不要编造用户没有表达的资产。
- 图片存在时 creative_assets 必须包含 image_assets。
- 如果目标不明确，missing 包含 goal。
- 如果用户文字为空，missing 包含 topic。
- 只问必要问题，最多 2 个。
"""


GOAL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("品牌认知", ("品宣", "品牌认知", "品牌心智", "品牌介绍", "品牌故事", "brand_awareness")),
    ("获客留资", ("获客", "线索", "留资", "私信", "咨询", "lead_generation")),
    ("产品种草", ("种草", "安利", "推荐", "好物", "产品故事", "product_seeding")),
    ("新品发布", ("上新", "新品", "发布", "上市", "首发", "product_launch")),
    ("销售转化", ("带货", "卖货", "转化", "下单", "购买", "成交", "sales_conversion")),
    ("课程销售", ("卖课", "课程", "训练营", "课", "course_sales")),
    ("涨粉", ("涨粉", "关注", "破圈", "传播", "follower_growth")),
    ("商务合作", ("接广告", "合作", "商务", "品牌合作", "ad_collaboration")),
]

FORMAT_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("小红书图文", ("小红书", "图文", "笔记", "封面", "xhs_note")),
    ("短视频", ("短视频", "视频", "reels", "short_video")),
    ("Vlog", ("vlog", "日常记录")),
    ("直播", ("直播", "live")),
    ("直播带货", ("直播带货", "live_commerce")),
]

TONE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("专业", ("专业", "权威", "可信", "professional")),
    ("高级", ("高端", "高级", "质感", "premium")),
    ("亲和", ("亲和", "温柔", "轻松", "friendly")),
    ("有趣", ("搞笑", "有趣", "幽默", "怪趣", "funny")),
    ("走心", ("走心", "共鸣", "治愈", "emotional")),
    ("干货", ("干货", "方法", "教程", "攻略", "practical")),
    ("犀利", ("毒舌", "犀利", "直接", "sharp")),
]

ANTI_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("不要硬广", ("不要硬广", "不硬广", "别太广告", "no_hard_sell")),
    ("不要低价感", ("不要低价感", "不低价", "别廉价", "no_cheap_feel")),
    ("保持人设", ("不掉人设", "保持人设", "人设一致", "keep_persona")),
    ("不要太商业", ("不要太商业", "不太商业化", "别太商业", "not_too_commercial")),
    ("不要违规", ("不要违规", "合规", "不要擦边", "不要露骨", "no_sensitive_content")),
]

CREATIVE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("品牌标志", ("logo", "标志", "品牌标志")),
    ("设计语言", ("设计语", "视觉语言", "设计理念", "品牌理念", "品牌风格", "design_language")),
    ("品牌色", ("品牌色", "配色", "色彩", "brand_color")),
    ("人设", ("人设", "主理人", "账号人格", "persona")),
    ("IP角色", ("ip", "IP", "角色", "吉祥物")),
    ("口号", ("口头禅", "slogan", "标语", "catchphrase")),
]

COMMERCIAL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("店铺链接", ("店铺", "店铺链接", "shop_link")),
    ("商品链接", ("商品链接", "购买链接", "产品链接", "product_link")),
    ("优惠", ("优惠", "折扣", "券", "福利", "discount")),
    ("课程", ("课程", "训练营", "课", "course")),
    ("合作品", ("合作品", "联名", "合作款", "collaboration")),
    ("橱窗", ("橱窗", "showcase_window")),
]

GUARDRAIL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("品牌规范", ("guideline", "品牌规范", "视觉规范", "brand_guideline")),
    ("禁用词", ("禁用词", "不能说", "不要出现", "forbidden_words")),
    ("人设边界", ("人设边界", "不掉人设", "persona_boundary")),
    ("品类边界", ("不接", "不碰", "不做", "category_boundary")),
]

DATA_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("账号数据", ("账号数据", "后台数据", "数据", "account_data")),
    ("对标内容", ("竞品", "对标", "参考账号", "competitor_content")),
    ("受众画像", ("粉丝画像", "用户画像", "受众画像", "audience_profile")),
    ("同类账号", ("同类博主", "同类账号", "similar_creator")),
    ("爆款案例", ("爆款", "高赞", "爆文", "viral_examples")),
]

_QUESTION_MAP = {
    "goal": "这次内容最重要的目标是什么？比如涨粉、种草、品宣、转化。",
    "topic": "这次要围绕什么主题、产品或活动来做？",
}


def _rule_intake(normalized: UserInput) -> IntakeResult:
    text = normalized.text.strip()
    intention = {
        "goal": _pick_first(text, GOAL_RULES),
        "format": _pick_first(text, FORMAT_RULES) or "小红书图文",
        "tone": _pick_many(text, TONE_RULES),
        "anti": _pick_many(text, ANTI_RULES),
    }
    context = {
        "creative_assets": _creative_assets(text, normalized.images),
        "commercial_assets": _commercial_assets(text),
        "guardrails": _guardrails(text),
        "data_refs": _data_refs(text),
        "images": [_image_context(path) for path in normalized.images],
    }
    missing = _missing_fields(text, intention)
    questions = [_QUESTION_MAP[item] for item in missing]
    return IntakeResult(intention=intention, context=context, missing=missing, questions=questions)


def _llm_intake(normalized: UserInput, fallback: IntakeResult) -> IntakeResult | None:
    try:
        data = llms.chat_json(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        text=normalized.text.strip() or "无",
                        images=json.dumps(normalized.images, ensure_ascii=False),
                    ),
                },
            ],
            usage="llm",
            _chat=llms.chat,
        )
        return _normalize_llm_result(data, normalized, fallback)
    except Exception:  # noqa: BLE001 - Intake must work even if LLM is down.
        return None


def _normalize_llm_result(data: dict[str, Any], normalized: UserInput, fallback: IntakeResult) -> IntakeResult:
    intention_data = data.get("intention") if isinstance(data.get("intention"), dict) else {}
    context_data = data.get("context") if isinstance(data.get("context"), dict) else {}
    intention = {
        "goal": _allowed_label(intention_data.get("goal"), GOAL_RULES, fallback.intention.get("goal", "")),
        "format": _allowed_label(intention_data.get("format"), FORMAT_RULES, fallback.intention.get("format", "小红书图文")),
        "tone": _allowed_list(intention_data.get("tone"), _allowed_values(TONE_RULES), fallback.intention.get("tone", []), _label_aliases(TONE_RULES)),
        "anti": _allowed_list(intention_data.get("anti"), _allowed_values(ANTI_RULES), fallback.intention.get("anti", []), _label_aliases(ANTI_RULES)),
    }
    context = {
        "creative_assets": _allowed_list(
            context_data.get("creative_assets"),
            _allowed_values(CREATIVE_RULES) | {"图片资产"},
            fallback.context.get("creative_assets", []),
            _label_aliases(CREATIVE_RULES) | {"image_assets": "图片资产"},
        ),
        "commercial_assets": _allowed_list(
            context_data.get("commercial_assets"),
            _allowed_values(COMMERCIAL_RULES),
            fallback.context.get("commercial_assets", []),
            _label_aliases(COMMERCIAL_RULES),
        ),
        "guardrails": _allowed_list(
            context_data.get("guardrails"),
            _allowed_values(GUARDRAIL_RULES) | _allowed_values(ANTI_RULES),
            fallback.context.get("guardrails", []),
            _label_aliases(GUARDRAIL_RULES) | _label_aliases(ANTI_RULES),
        ),
        "data_refs": _allowed_list(
            context_data.get("data_refs"),
            _allowed_values(DATA_RULES),
            fallback.context.get("data_refs", []),
            _label_aliases(DATA_RULES),
        ),
        "images": [_image_context(path) for path in normalized.images],
    }
    if normalized.images and "图片资产" not in context["creative_assets"]:
        context["creative_assets"].append("图片资产")
    missing = _normalize_missing(data.get("missing"), normalized, intention)
    questions = _normalize_questions(data.get("questions"), missing)
    return IntakeResult(intention=intention, context=context, missing=missing, questions=questions)


def _normalize_input(user_input: UserInput | str, images: list[str] | None) -> UserInput:
    if isinstance(user_input, UserInput):
        extra_images = list(images or [])
        return UserInput(text=user_input.text, images=[*user_input.images, *extra_images])
    return UserInput(text=str(user_input or ""), images=list(images or []))


def _clean_unknown(value: str) -> str:
    value = value.strip()
    return "" if value in {"", "unknown", "未知", "None", "null"} else value


def _allowed_label(value: Any, rules: list[tuple[str, tuple[str, ...]]], fallback: str) -> str:
    text = _clean_unknown(str(value or ""))
    if not text:
        return fallback
    aliases = _label_aliases(rules)
    mapped = aliases.get(text, text)
    return mapped if mapped in _allowed_values(rules) else fallback


def _allowed_list(value: Any, allowed: set[str], fallback: list[str], aliases: dict[str, str] | None = None) -> list[str]:
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
    return _dedupe(cleaned or list(fallback))


def _allowed_values(rules: list[tuple[str, tuple[str, ...]]]) -> set[str]:
    return {value for value, _ in rules}


def _label_aliases(rules: list[tuple[str, tuple[str, ...]]]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for value, keywords in rules:
        aliases[value] = value
        aliases[value.lower()] = value
        for keyword in keywords:
            aliases[keyword] = value
            aliases[keyword.lower()] = value
    return aliases


def _normalize_missing(value: Any, normalized: UserInput, intention: dict[str, Any]) -> list[str]:
    if isinstance(value, str):
        raw_items = [value]
    elif isinstance(value, list):
        raw_items = [str(item) for item in value]
    else:
        raw_items = []
    missing = [item for item in raw_items if item in _QUESTION_MAP]
    for item in _missing_fields(normalized.text.strip(), intention):
        if item not in missing:
            missing.append(item)
    return missing


def _normalize_questions(value: Any, missing: list[str]) -> list[str]:
    if isinstance(value, str):
        questions = [value]
    elif isinstance(value, list):
        questions = [str(item) for item in value if str(item).strip()]
    else:
        questions = []
    if not questions:
        questions = [_QUESTION_MAP[item] for item in missing]
    return questions[:2]


def _pick_first(text: str, rules: list[tuple[str, tuple[str, ...]]]) -> str:
    lowered = text.lower()
    for value, keywords in rules:
        if any(keyword.lower() in lowered for keyword in keywords):
            return value
    return ""


def _pick_many(text: str, rules: list[tuple[str, tuple[str, ...]]]) -> list[str]:
    lowered = text.lower()
    return [value for value, keywords in rules if any(keyword.lower() in lowered for keyword in keywords)]


def _creative_assets(text: str, images: list[str]) -> list[str]:
    assets = _pick_many(text, CREATIVE_RULES)
    if images:
        assets.append("图片资产")
    return _dedupe(assets)


def _commercial_assets(text: str) -> list[str]:
    return _pick_many(text, COMMERCIAL_RULES)


def _guardrails(text: str) -> list[str]:
    guardrails = _pick_many(text, GUARDRAIL_RULES)
    guardrails.extend(_pick_many(text, ANTI_RULES))
    return _dedupe(guardrails)


def _data_refs(text: str) -> list[str]:
    return _pick_many(text, DATA_RULES)


def _image_context(path: str) -> dict[str, Any]:
    suffix = Path(path).suffix.lower().lstrip(".")
    return {"path": path, "kind": suffix or "image", "usage": "context"}


# ============ 视觉打标工序 ============

VISION_SYSTEM_PROMPT = (
    "你是 Nori Intaker 的视觉打标工序，只输出 JSON。"
    "你收到一段用户需求 + 一张候选素材图，"
    "请结合需求理解图片内容、用途，为这张图填一份语义标签。"
)

VISION_USER_TEMPLATE = (
    "用户的内容创作需求：\n{user_text}\n\n"
    "下面是一张候选素材图。请结合上面的需求理解这张图，填一份标签：\n"
    "{{\n"
    '  "vision_roles": [<1-3 个>],   // brand_logo / ip_character / product_shot / '
    'scene_photo / lifestyle / data_chart / reference_style / raw_material / '
    'portrait / unknown\n'
    '  "subject": "<一句话描述图中主体 + 与用户需求的关联，<=60 字>",\n'
    '  "brand_signals": ["<画面里可识别的品牌字标 / logo / 产品名>", ...],\n'
    '  "usable_for": [<cover / body / background_only / not_usable>],\n'
    '  "quality": "high|medium|low"\n'
    "}}\n\n"
    "严格规则：\n"
    "  - vision_roles 必须从给定字典里挑\n"
    "  - 看不清就用 unknown / not_usable / low\n"
    "  - 不要编造未出现在画面里的品牌名\n\n"
    '输出 JSON（只输出这个对象，不要包裭）。'
)


def _build_tagged_assets(normalized: UserInput, *, use_vision: bool) -> list[UserAsset]:
    """把 UserInput 里的图片 + 文本一起转成 list[UserAsset]。

    图片：use_vision 时“单图 + 用户文本”并发调 LLM 打标；
          失败/关闭时退回空 tag。
    文本：保留全文，role 默认空。
    """
    assets: list[UserAsset] = []

    image_paths = [p for p in normalized.images if p]
    user_text = normalized.text.strip() or "用户未提供文本输入。"
    if use_vision and image_paths:
        tags = _tag_images_llm(image_paths, user_text)
    else:
        tags = [None] * len(image_paths)
    for path, tag in zip(image_paths, tags):
        assets.append(_make_image_asset(path, tag))

    text = normalized.text.strip()
    if text:
        assets.append(UserAsset(kind="text", text=text))

    return assets


def _tag_images_llm(image_paths: list[str], user_text: str) -> list[dict[str, Any] | None]:
    """每张图独立调一次 vision LLM，并发运行。

    某一张失败不会阻塞其他张；失败该位填 None。
    """
    if not image_paths:
        return []

    out: list[dict[str, Any] | None] = [None] * len(image_paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=VISION_PARALLELISM) as pool:
        futures = {
            pool.submit(_tag_one_image_llm, path, user_text): i
            for i, path in enumerate(image_paths)
        }
        for fut in concurrent.futures.as_completed(futures):
            i = futures[fut]
            try:
                out[i] = fut.result()
            except Exception as exc:  # noqa: BLE001 - 单张失败不阻塞整体
                print(
                    f"[warn] vision tag failed for {image_paths[i]}: "
                    f"{type(exc).__name__}: {exc}",
                    file=sys.stderr,
                )
                out[i] = None
    return out


def _tag_one_image_llm(path: str, user_text: str) -> dict[str, Any] | None:
    data_uri = image_to_data_uri(path)
    if not data_uri:
        return None
    data = llms.chat_json(
        [
            {"role": "system", "content": VISION_SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": VISION_USER_TEMPLATE.format(user_text=user_text)},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ]},
        ],
        usage="vision",
        timeout=60,
        _chat=llms.chat,
    )
    return data


def _make_image_asset(path: str, tag: dict[str, Any] | None) -> UserAsset:
    if not isinstance(tag, dict):
        return UserAsset(kind="image", path=path)
    vision_roles = _filter_allowed(tag.get("vision_roles"), ALLOWED_VISION_ROLES)
    usable_for = _filter_allowed(tag.get("usable_for"), ALLOWED_USABLE_FOR)
    brand_signals = [str(b).strip() for b in (tag.get("brand_signals") or []) if str(b).strip()]
    subject = str(tag.get("subject") or "").strip()[:60]
    quality_raw = str(tag.get("quality") or "").strip().lower()
    quality = quality_raw if quality_raw in ALLOWED_QUALITY else ""
    return UserAsset(
        kind="image",
        path=path,
        vision_roles=vision_roles,
        subject=subject,
        brand_signals=brand_signals,
        usable_for=usable_for,
        quality=quality,
    )


def _filter_allowed(value: Any, allowed: set[str]) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(v) for v in value]
    else:
        items = []
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = item.strip().lower()
        if v in allowed and v not in seen:
            out.append(v)
            seen.add(v)
    return out


def _missing_fields(text: str, intention: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not text:
        missing.append("topic")
    if not intention.get("goal"):
        missing.append("goal")
    return missing


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
