"""Artifact execution stage for content generation specs."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from nori.agents.content_generation.content_producer import ContentProducerAgent
from nori.agents.content_generation.schemas import ContentDesignSpec, ContentPackage
from nori.agents.market_analysis.schemas import NoteSkill
from nori.core import AccountOperationProject, AgentBase, ClientBrief, ContentTask, IntentContract, LLMFactory, UserAsset


class ArtifactGenerationAgent(AgentBase):
    """Instantiate a `ContentDesignSpec` into the current artifact package contract."""

    stage_name = "artifact_generation"

    def __init__(
        self,
        *,
        content_producer: Any | None = None,
        llm_factory: LLMFactory | None = None,
    ) -> None:
        super().__init__(stage_name=self.stage_name, use_llm=True, llm_factory=llm_factory)
        self.content_producer = content_producer or ContentProducerAgent(llm_factory=self.llm_factory)

    def run(
        self,
        *,
        spec: ContentDesignSpec | dict[str, Any],
        task: ContentTask | dict[str, Any],
        skills: list[NoteSkill | dict[str, Any]],
        assets: list[UserAsset | dict[str, Any]] | None = None,
        out_dir: str | Path,
        client_brief: ClientBrief | dict[str, Any] | None = None,
        project: AccountOperationProject | None = None,
        intent: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        intent_contract: IntentContract | dict[str, Any] | None = None,
        use_cover: bool = True,
    ) -> ContentPackage:
        normalized_spec = spec if isinstance(spec, ContentDesignSpec) else ContentDesignSpec.from_dict(spec)
        selected_skills = _selected_skills(skills, normalized_spec)
        spec_dict = normalized_spec.to_dict()
        execution_intent = {**dict(intent or {}), "content_design_spec": spec_dict}
        execution_context = {**dict(context or {}), "content_design_spec": spec_dict}
        return self.content_producer.run(
            task,
            skills=selected_skills,
            assets=assets,
            out_dir=out_dir,
            client_brief=client_brief,
            project=project,
            intent=execution_intent,
            context=execution_context,
            intent_contract=intent_contract,
            use_cover=use_cover,
        )


def _selected_skills(
    skills: list[NoteSkill | dict[str, Any]],
    spec: ContentDesignSpec,
) -> list[NoteSkill | dict[str, Any]]:
    selected_ids = {
        str(ref.get("skill_id") or "")
        for ref in spec.selected_skill_refs
        if isinstance(ref, dict) and ref.get("skill_id")
    }
    if not selected_ids:
        return list(skills)
    selected = [
        skill for skill in skills
        if _skill_id(skill) in selected_ids
    ]
    return selected or list(skills)


def _skill_id(skill: NoteSkill | dict[str, Any]) -> str:
    if isinstance(skill, NoteSkill):
        return skill.skill_id
    if isinstance(skill, dict):
        return str(skill.get("skill_id") or skill.get("id") or "")
    return ""


__all__ = ["ArtifactGenerationAgent"]
