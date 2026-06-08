"""Class-owned package contract for NoteMakerAgent."""
from __future__ import annotations

from typing import Any, Callable

from nori.agents.content_generation.schemas import AssetBundle, CandidateTitle
from nori.core import UserAsset
from nori.shared.prompting import json_block, json_prompt


JsonCall = Callable[..., dict[str, Any]]


class NoteSkillSelector:
    """Pick the best note skill for the current intent."""

    system_prompt = "你是 Nori 的 Skill 选择器，只输出 JSON。"

    def pick(
        self,
        skills: list[dict[str, Any]],
        intent: dict[str, Any],
        context: dict[str, Any],
        *,
        json_call: JsonCall,
        error_type=RuntimeError,
    ) -> dict[str, Any]:
        summary = [
            {
                "skill_id": skill.get("skill_id"),
                "label": skill.get("label"),
                "goal": skill.get("goal"),
                "tone": skill.get("tone"),
                "note_type": skill.get("note_type"),
                "creative_goal": skill.get("creative_goal"),
                "metrics_summary": skill.get("metrics_summary"),
            }
            for skill in skills
        ]
        data = json_call(
            system=self.system_prompt,
            user=(
                f"用户意图：\n{json_prompt(intent)}\n\n"
                f"上下文：\n{json_prompt(context)}\n\n"
                f"候选 skill：\n{json_block(summary)}\n\n"
                "按这些维度选 1 个最契合用户意图的 skill：\n"
                "  - 热点证据：上下文里是否有可追溯的热点、趋势、样本或用户明确提供的趋势 brief\n"
                "  - 账号可信度：这个账号/品牌能不能自然参与，不要为了追热点选择不可信的 skill\n"
                "  - 受众匹配：目标用户是否真的会关心这个角度\n"
                "  - 内容缺口：是否能提供新的判断、方法或清单，而不是复述热词\n"
                "  - 图文可视化：是否能拆成清晰封面和 5-9 页图文结构\n"
                "  - 风险：是否容易造成夸大、蹭热点、假体验或敏感声明\n"
                '输出 {"skill_id": "..."}。'
            ),
            timeout=30,
        )
        chosen_id = str(data.get("skill_id") or "").strip()
        for skill in skills:
            if skill.get("skill_id") == chosen_id:
                return skill
        raise error_type(f"SkillPicker 返回未知 skill_id: {chosen_id!r}")


class NoteAssetCurator:
    """Group tagged assets into NoteMaker's AssetBundle contract."""

    system_prompt = "你是 Nori 的素材整理工序，只输出 JSON。"

    def curate(
        self,
        assets: list[UserAsset],
        skill: dict[str, Any],
        intent: dict[str, Any],
        *,
        json_call: JsonCall,
    ) -> AssetBundle:
        images = [(i, a) for i, a in enumerate(assets) if a.kind == "image"]
        texts = [(i, a) for i, a in enumerate(assets) if a.kind == "text" and a.text.strip()]

        image_input = [
            {
                "index": i,
                "path": a.path,
                "vision_roles": list(a.vision_roles),
                "subject": a.subject,
                "brand_signals": list(a.brand_signals),
                "usable_for": list(a.usable_for),
                "quality": a.quality,
            }
            for i, a in images
        ]
        text_input = [
            {"index": i, "text": a.text.strip()[:240]}
            for i, a in texts
        ]

        if not image_input and not text_input:
            return AssetBundle()

        data = json_call(
            system=self.system_prompt,
            user=(
                f"创作目标：{skill.get('creative_goal', '')}\n"
                f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
                f"用户意图：{json_prompt(intent)}\n\n"
                f"图片素材（按 index 引用）：\n{json_block(image_input)}\n\n"
                f"文本素材（按 index 引用）：\n{json_block(text_input)}\n\n"
                "请把素材整理成 5 个桶：\n"
                "  - main_image_indices：主视觉图片 index（封面优先）\n"
                "  - aux_image_indices：辅助图 index\n"
                "  - text_points：用户的卖点/描述短句\n"
                "  - brand_facts：品牌名/口号/理念/人设\n"
                "  - data_points：数据/数字/案例\n"
                "保留原文关键词，不要扩写。text_points 每条 <=80 字；brand_facts 每条 <=60 字；每个文本桶最多 6 条。\n"
                '输出 JSON：{"main_image_indices": [], "aux_image_indices": [], '
                '"text_points": [], "brand_facts": [], "data_points": []}'
            ),
            timeout=60,
        )
        return self.bundle_from_data(data, assets)

    def bundle_from_data(self, data: dict[str, Any], assets: list[UserAsset]) -> AssetBundle:
        images = [(i, a) for i, a in enumerate(assets) if a.kind == "image"]
        bundle = AssetBundle()
        main_idx = self.int_list(data.get("main_image_indices"))
        aux_idx = self.int_list(data.get("aux_image_indices"))
        used: set[int] = set()
        for i in main_idx:
            if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
                bundle.main_images.append(assets[i])
                used.add(i)
        for i in aux_idx:
            if 0 <= i < len(assets) and assets[i].kind == "image" and i not in used:
                bundle.aux_images.append(assets[i])
                used.add(i)
        for i, asset in images:
            if i not in used:
                bundle.aux_images.append(asset)
        if not bundle.main_images and bundle.aux_images:
            bundle.main_images.append(bundle.aux_images.pop(0))

        bundle.text_points = self.str_list(data.get("text_points"))[:6]
        bundle.brand_facts = self.str_list(data.get("brand_facts"))[:6]
        bundle.data_points = self.str_list(data.get("data_points"))[:6]
        return bundle

    def pick_visual_paths(self, bundle: AssetBundle) -> tuple[str, list[str]]:
        cover = bundle.main_images[0].path if bundle.main_images else ""
        others = [a.path for a in bundle.main_images[1:] + bundle.aux_images if a.path]
        return cover, others[:8]

    def int_list(self, value: Any) -> list[int]:
        out: list[int] = []
        for item in value or []:
            try:
                out.append(int(item))
            except (TypeError, ValueError):
                continue
        return out

    def str_list(self, value: Any) -> list[str]:
        return [str(item).strip() for item in (value or []) if str(item).strip()]


class NoteComposer:
    """Compose and normalize the final note fields."""

    system_prompt = "你是 Nori 的小红书 note 写手，只输出 JSON。"

    def compose(
        self,
        skill: dict[str, Any],
        bundle: AssetBundle,
        intent: dict[str, Any],
        *,
        json_call: JsonCall,
        error_type=RuntimeError,
    ) -> dict[str, Any]:
        data = json_call(
            system=self.system_prompt,
            user=(
                f"创作目标：{skill.get('creative_goal', '')}\n"
                f"语气：{skill.get('tone', '')}；类型：{skill.get('note_type', '')}\n"
                f"用户意图：{json_prompt(intent)}\n\n"
                f"素材卖点：{json_prompt(bundle.text_points)}\n"
                f"品牌信息：{json_prompt(bundle.brand_facts)}\n"
                f"数据点：{json_prompt(bundle.data_points)}\n\n"
                "热点证据：从用户意图或上下文里读取 hotspot / trend / market evidence；"
                "如果没有真实来源，必须当成假设写，不要伪装成已验证热点。\n"
                "账号可信度：只有当产品、品牌、人设或使用场景能自然接住热点时才借势；"
                "不要为了追热点牺牲可信度。\n"
                "首图一眼看懂：标题和开场要支持封面在 1 秒内讲清利益点。\n\n"
                f"标题规则：\n{json_block(skill.get('title_rules') or [])}\n\n"
                f"开场规则：\n{json_block(skill.get('opening_rules') or [])}\n\n"
                f"正文结构：\n{json_block(skill.get('body_structure') or [])}\n\n"
                f"互动规则：\n{json_block(skill.get('interaction_rules') or [])}\n\n"
                f"禁止项：{json_prompt(skill.get('avoid_rules') or [])}\n\n"
                "按规则写一篇可发布的小红书 note：\n"
                "  - title：推荐标题，<=20 字；热点标题不能只堆热词，要有账号角度\n"
                "  - candidate_titles：3-5 个候选，每个含 text / rule_name（命中的 title_rules.name）/ rationale\n"
                "  - body：开场 → 主体段落 → 互动钩子，<=1000 字；优先写可保存的判断/清单/步骤\n"
                "  - tags：3-5 个，每个 <=8 字\n"
                "  - comment_hook：评论引导一句话\n"
                "  - validation：{status: pass|needs_human_review, issues: [...]}"
                "，命中禁止项、缺热点证据、账号角度牵强或首图不够清楚时 status=needs_human_review\n"
                "真实性边界：不要伪造用户体验、截图、官方背书或前后对比证据；"
                "医疗、金融、法律、投资类表述必须降级为谨慎建议。\n\n"
                '输出 JSON：{"title":"","candidate_titles":[],'
                '"body":"","tags":[],"comment_hook":"","validation":{"status":"","issues":[]}}'
            ),
            timeout=90,
        )
        return self.normalize(data, error_type=error_type)

    def normalize(
        self,
        data: dict[str, Any],
        *,
        error_type=RuntimeError,
    ) -> dict[str, Any]:
        title = str(data.get("title") or "").strip()
        body = str(data.get("body") or "").strip()
        if not title or not body:
            raise error_type("NoteComposer 缺 title 或 body")

        candidates: list[CandidateTitle] = []
        for item in data.get("candidate_titles") or []:
            if isinstance(item, dict) and item.get("text"):
                candidates.append(CandidateTitle(
                    text=str(item["text"]).strip()[:30],
                    rule_name=str(item.get("rule_name") or "").strip(),
                    rationale=str(item.get("rationale") or "").strip(),
                ))
        if not candidates:
            candidates.append(CandidateTitle(text=title, rule_name="", rationale=""))

        tags = [str(tag).strip() for tag in (data.get("tags") or []) if str(tag).strip()][:5]
        hook = str(data.get("comment_hook") or "").strip()

        validation = data.get("validation") if isinstance(data.get("validation"), dict) else {}
        status = str(validation.get("status") or "pass").strip() or "pass"
        issues = [str(item).strip() for item in (validation.get("issues") or []) if str(item).strip()]

        return {
            "title": title,
            "body": body,
            "tags": tags,
            "comment_hook": hook,
            "candidate_titles": candidates,
            "validation": {"status": status, "issues": issues},
        }


__all__ = ["NoteAssetCurator", "NoteComposer", "NoteSkillSelector"]
