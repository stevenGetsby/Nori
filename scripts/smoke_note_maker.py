"""Smoke test for IntakeAgent + NoteMakerAgent + CoverDirectorAgent (纯 LLM 路径).

加载 Holly skill_guides JSON + Holly 品牌素材目录：
  1. IntakeAgent       — 用 vision LLM 给每张品牌素材图打语义标签
  2. NoteMakerAgent    — 用 tagged assets 写 note 草稿
  3. CoverDirectorAgent— 让 LLM 从 tagged assets 里自己挑封面参考图并生成封面

用法:
    PYTHONPATH=. python scripts/smoke_note_maker.py
    PYTHONPATH=. python scripts/smoke_note_maker.py --no-cover
    PYTHONPATH=. python scripts/smoke_note_maker.py --no-vision    # 跳过 vision 打标
    PYTHONPATH=. python scripts/smoke_note_maker.py --skills <path> --assets-dir <dir>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nori.agent_models import UserAsset, UserInput
from nori.gen_agents import CoverDirectorAgent, IntakeAgent, NoteMakerAgent


DEFAULT_SKILLS = "nori/skill_base/data/xhs_note_analyzer/holly/20260515_174142_note_skill_guides.json"
DEFAULT_ASSETS_DIR = "SHOWCASE/Holly"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def _load_skills(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("skills") if isinstance(data, dict) else data
    if not skills:
        raise ValueError(f"no skills found in {path}")
    return list(skills)


def _collect_assets(root: Path) -> list[UserAsset]:
    assets: list[UserAsset] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        suffix = p.suffix.lower()
        if suffix in IMAGE_EXTS:
            assets.append(UserAsset(kind="image", path=str(p)))
        elif suffix in {".md", ".txt"}:
            try:
                text = p.read_text(encoding="utf-8").strip()
            except UnicodeDecodeError:
                continue
            if text:
                assets.append(UserAsset(kind="text", text=text))
    return assets


def _merge_vision_tags(
    raw_assets: list[UserAsset],
    intake_assets: list[UserAsset],
) -> list[UserAsset]:
    """把 IntakeAgent 打过 vision tag 的 image asset 合并回原始 asset 列表。

    text asset 保留原文（Intaker 只看 text 摘要，不存全文）。
    """
    tagged_by_path = {a.path: a for a in intake_assets if a.kind == "image" and a.path}
    out: list[UserAsset] = []
    for a in raw_assets:
        if a.kind == "image" and a.path in tagged_by_path:
            tagged = tagged_by_path[a.path]
            out.append(UserAsset(
                kind="image",
                path=a.path,
                vision_roles=list(tagged.vision_roles),
                subject=tagged.subject,
                brand_signals=list(tagged.brand_signals),
                usable_for=list(tagged.usable_for),
                quality=tagged.quality,
            ))
        else:
            out.append(a)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="NoteMakerAgent smoke test.")
    parser.add_argument("--skills", default=DEFAULT_SKILLS)
    parser.add_argument("--assets-dir", default=DEFAULT_ASSETS_DIR)
    parser.add_argument("--goal", default="产品种草")
    parser.add_argument("--tone", default="朋友安利")
    parser.add_argument("--out", default="")
    parser.add_argument("--no-cover", dest="make_cover", action="store_false", default=True)
    parser.add_argument("--no-vision", dest="use_vision", action="store_false", default=True,
                        help="跳过 IntakeAgent 的 vision 打标工序")
    parser.add_argument("--cover-size", default="1072x1440")
    args = parser.parse_args()

    skills_path = Path(args.skills)
    assets_dir = Path(args.assets_dir)
    if not skills_path.exists():
        print(f"[error] skills file missing: {skills_path}", file=sys.stderr)
        return 1
    if not assets_dir.exists():
        print(f"[error] assets dir missing: {assets_dir}", file=sys.stderr)
        return 1

    skills = _load_skills(skills_path)
    raw_assets = _collect_assets(assets_dir)
    if not raw_assets:
        print(f"[error] no assets collected from {assets_dir}", file=sys.stderr)
        return 1

    image_paths = [a.path for a in raw_assets if a.kind == "image"]
    intent_text = (
        f"为该品牌做一篇{args.goal}主题的小红书图文，语气{args.tone}。"
        f"附带的图片为品牌全部可用素材。"
    )
    # user_text 让下游 CoverDirector 的选图工序看得到原始诉求
    intent = {
        "goal": args.goal,
        "tone": [args.tone],
        "format": "小红书图文",
        "user_text": intent_text,
    }

    print(f"[info] skills={len(skills)} assets={len(raw_assets)} images={len(image_paths)}")
    print(f"[info] running IntakeAgent (use_vision={args.use_vision}) ...")
    intake = IntakeAgent().run(
        UserInput(text=intent_text, images=image_paths),
        use_vision=args.use_vision,
    )
    image_assets_tagged = [a for a in intake.assets if a.kind == "image"]
    tagged_image_count = sum(1 for a in image_assets_tagged if a.vision_roles)
    print(f"[ok]  intake intention={intake.intention} tagged_images={tagged_image_count}/{len(image_paths)}")

    # 把每张图打出来：路径 + 角色 + 用途 + 品牌信号 + 主体描述
    print(f"[info] vision tags per image ({len(image_assets_tagged)} images):")
    for i, a in enumerate(image_assets_tagged):
        name = Path(a.path).name if a.path else "?"
        roles = ",".join(a.vision_roles) or "-"
        usable = ",".join(a.usable_for) or "-"
        signals = ",".join(a.brand_signals) or "-"
        q = a.quality or "-"
        subj = a.subject or "-"
        print(f"  [{i:02d}] {name}")
        print(f"       roles={roles}  usable={usable}  quality={q}")
        print(f"       brand_signals={signals}")
        print(f"       subject={subj}")

    assets = _merge_vision_tags(raw_assets, intake.assets)

    print("[info] running NoteMakerAgent ...")
    try:
        draft = NoteMakerAgent().run(skills, assets, intent=intent)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] note_maker failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    payload = draft.to_dict()
    # 默认把 intake 详细 assets 塞进结果 JSON，无论是否生成封面
    payload["intake_summary"] = {
        "intention": dict(intake.intention),
        "tagged_image_count": tagged_image_count,
        "assets": [a.to_dict() for a in intake.assets],
    }
    out_path = Path(args.out) if args.out else assets_dir / "note_draft.json"

    if args.make_cover:
        skill_for_cover = next(
            (s for s in skills if (s.get("skill_id") if isinstance(s, dict) else getattr(s, "skill_id", None)) == draft.skill_id),
            skills[0],
        )
        cover_out = (out_path.parent / "covers").resolve()
        print("[info] running CoverDirectorAgent (LLM picks reference images from tagged assets) ...")
        try:
            cover = CoverDirectorAgent().run(
                draft, skill_for_cover, assets,
                out_dir=cover_out, size=args.cover_size, intent=intent,
                tagged_assets=assets,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] cover_director failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        else:
            draft.cover_path = cover.cover_path
            # 重新拼 payload，保留 intake_summary
            base = draft.to_dict()
            base["intake_summary"] = payload["intake_summary"]
            base["cover_result"] = cover.to_dict()
            payload = base
            print(f"[ok] cover -> {cover.cover_path}")
            print(f"[ok] reference_paths used = {len(cover.reference_paths)}")
            for rp in cover.reference_paths:
                print(f"       ref: {rp}")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
