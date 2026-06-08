"""Text intake normalization helpers for IntakeAgent."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.agents.user_profiling.schemas import IntakeResult, UserInput

from . import taxonomy as _taxonomy


GOAL_RULES = _taxonomy.GOAL_RULES
FORMAT_RULES = _taxonomy.FORMAT_RULES
TONE_RULES = _taxonomy.TONE_RULES
ANTI_RULES = _taxonomy.ANTI_RULES
CREATIVE_RULES = _taxonomy.CREATIVE_RULES
COMMERCIAL_RULES = _taxonomy.COMMERCIAL_RULES
GUARDRAIL_RULES = _taxonomy.GUARDRAIL_RULES
DATA_RULES = _taxonomy.DATA_RULES
QUESTION_MAP = _taxonomy.QUESTION_MAP


def normalize_input(user_input: UserInput | str, images: list[str] | None) -> UserInput:
    if isinstance(user_input, UserInput):
        extra_images = list(images or [])
        return UserInput(text=user_input.text, images=[*user_input.images, *extra_images])
    return UserInput(text=str(user_input or ""), images=list(images or []))


def rule_intake(normalized: UserInput) -> IntakeResult:
    """Build deterministic text-intake fallback from raw user input."""
    text = normalized.text.strip()
    intention = {
        "goal": _taxonomy.pick_first(text, GOAL_RULES),
        "format": _taxonomy.pick_first(text, FORMAT_RULES) or "小红书图文",
        "tone": _taxonomy.pick_many(text, TONE_RULES),
        "anti": _taxonomy.pick_many(text, ANTI_RULES),
    }
    context = {
        "creative_assets": _taxonomy.creative_assets(text, normalized.images),
        "commercial_assets": _taxonomy.commercial_assets(text),
        "guardrails": _taxonomy.guardrails(text),
        "data_refs": _taxonomy.data_refs(text),
        "images": [image_context(path) for path in normalized.images],
    }
    missing = missing_fields(text, intention)
    questions = _taxonomy.questions_for_missing(missing)
    return IntakeResult(
        intention=intention,
        context=context,
        missing=missing,
        questions=questions,
    )


def normalize_llm_result(data: dict[str, Any], normalized: UserInput, fallback: IntakeResult) -> IntakeResult:
    """Normalize optional text-intake LLM JSON into an IntakeResult."""
    intention_data = data.get("intention") if isinstance(data.get("intention"), dict) else {}
    context_data = data.get("context") if isinstance(data.get("context"), dict) else {}
    intention = {
        "goal": _taxonomy.allowed_label(intention_data.get("goal"), GOAL_RULES, fallback.intention.get("goal", "")),
        "format": _taxonomy.allowed_label(intention_data.get("format"), FORMAT_RULES, fallback.intention.get("format", "小红书图文")),
        "tone": _taxonomy.allowed_list(intention_data.get("tone"), _taxonomy.allowed_values(TONE_RULES), fallback.intention.get("tone", []), _taxonomy.label_aliases(TONE_RULES)),
        "anti": _taxonomy.allowed_list(intention_data.get("anti"), _taxonomy.allowed_values(ANTI_RULES), fallback.intention.get("anti", []), _taxonomy.label_aliases(ANTI_RULES)),
    }
    context = {
        "creative_assets": _taxonomy.allowed_list(
            context_data.get("creative_assets"),
            _taxonomy.allowed_values(CREATIVE_RULES) | {"图片资产"},
            fallback.context.get("creative_assets", []),
            _taxonomy.label_aliases(CREATIVE_RULES) | {"image_assets": "图片资产"},
        ),
        "commercial_assets": _taxonomy.allowed_list(
            context_data.get("commercial_assets"),
            _taxonomy.allowed_values(COMMERCIAL_RULES),
            fallback.context.get("commercial_assets", []),
            _taxonomy.label_aliases(COMMERCIAL_RULES),
        ),
        "guardrails": _taxonomy.allowed_list(
            context_data.get("guardrails"),
            _taxonomy.allowed_values(GUARDRAIL_RULES) | _taxonomy.allowed_values(ANTI_RULES),
            fallback.context.get("guardrails", []),
            _taxonomy.label_aliases(GUARDRAIL_RULES) | _taxonomy.label_aliases(ANTI_RULES),
        ),
        "data_refs": _taxonomy.allowed_list(
            context_data.get("data_refs"),
            _taxonomy.allowed_values(DATA_RULES),
            fallback.context.get("data_refs", []),
            _taxonomy.label_aliases(DATA_RULES),
        ),
        "images": [image_context(path) for path in normalized.images],
    }
    if normalized.images and "图片资产" not in context["creative_assets"]:
        context["creative_assets"].append("图片资产")
    missing = _taxonomy.normalize_missing(
        data.get("missing"),
        text=normalized.text.strip(),
        intention=intention,
    )
    questions = _taxonomy.normalize_questions(data.get("questions"), missing)
    return IntakeResult(
        intention=intention,
        context=context,
        missing=missing,
        questions=questions,
        metadata=dict(fallback.metadata),
    )


def image_context(path: str) -> dict[str, Any]:
    suffix = Path(path).suffix.lower().lstrip(".")
    return {"path": path, "kind": suffix or "image", "usage": "context"}


def missing_fields(text: str, intention: dict[str, Any]) -> list[str]:
    return _taxonomy.missing_fields(text, intention)


def dedupe(items: list[str]) -> list[str]:
    return _taxonomy.dedupe(items)

