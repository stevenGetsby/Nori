import importlib
import json
from pathlib import Path

import nori.core.llms as llms

from nori.agents.user_profiling import IntakeAgent, UserInput


intaker_module = importlib.import_module("nori.agents.user_profiling.intaker.intaker")
HOLLY_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "holly_showcase"


def test_intaker_text_goal_format_and_tone():
    result = IntakeAgent(use_llm=False).run("帮我做一篇小红书图文，给新品种草，要高级但不要硬广")

    assert result.ready
    assert result.intention["goal"] == "产品种草"
    assert result.intention["format"] == "小红书图文"
    assert "高级" in result.intention["tone"]
    assert "不要硬广" in result.intention["anti"]


def test_intaker_text_with_images_as_context():
    result = IntakeAgent(use_llm=False).run(
        UserInput(
            text="做一篇品牌品宣小红书，参考 logo 和品牌色，调性亲和",
            images=["assets/logo.png", "assets/product.jpg"],
        )
    )

    assert result.ready
    assert result.intention["goal"] == "品牌认知"
    assert "亲和" in result.intention["tone"]
    assert "品牌标志" in result.context["creative_assets"]
    assert "品牌色" in result.context["creative_assets"]
    assert "图片资产" in result.context["creative_assets"]
    assert len(result.context["images"]) == 2


def test_intaker_holly_showcase_materials():
    text = (HOLLY_FIXTURE_DIR / "brief.md").read_text(encoding="utf-8")
    images = sorted(
        str(path)
        for path in (HOLLY_FIXTURE_DIR / "assets").iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )

    result = IntakeAgent(use_llm=False).run(UserInput(text=text, images=images))

    assert result.ready
    assert result.intention["goal"] == "涨粉"
    assert result.intention["format"] == "小红书图文"
    assert "有趣" in result.intention["tone"]
    assert "不要违规" in result.intention["anti"]
    assert {"设计语言", "人设", "IP角色", "口号", "图片资产"} <= set(result.context["creative_assets"])
    assert len(result.context["images"]) == len(images)
    assert len(images) > 0


def test_intaker_requires_goal_when_missing():
    result = IntakeAgent(use_llm=False).run("帮我写一下这个品牌")

    assert not result.ready
    assert "goal" in result.missing
    assert result.questions


def test_intaker_uses_llm_when_enabled(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        assert usage == "llm"
        assert "用户文字" in messages[1]["content"]
        return json.loads("""
        {
            "intention": {
                "goal": "销售转化",
                "format": "小红书图文",
                "tone": ["亲和"],
                "anti": ["不要硬广"]
            },
            "context": {
                "creative_assets": ["品牌标志"],
                "commercial_assets": ["商品链接"],
                "guardrails": ["不要硬广"],
                "data_refs": []
            },
            "missing": [],
            "questions": []
        }
        """)

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    result = IntakeAgent(use_llm=True).run("帮我做一篇小红书，别硬广，要带商品链接转化")

    assert result.ready
    assert result.intention["goal"] == "销售转化"
    assert result.context["commercial_assets"] == ["商品链接"]


def test_intaker_text_uses_chat_json_helper(monkeypatch):
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        return {
            "intention": {
                "goal": "销售转化",
                "format": "小红书图文",
                "tone": ["亲和"],
                "anti": ["不要硬广"],
            },
            "context": {
                "creative_assets": ["品牌标志"],
                "commercial_assets": ["商品链接"],
                "guardrails": ["不要硬广"],
                "data_refs": [],
            },
            "missing": [],
            "questions": [],
        }

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    result = IntakeAgent(use_llm=True).run(
        "帮我做一篇小红书，别硬广，要带商品链接转化",
        use_vision=False,
    )

    assert result.ready
    assert result.intention["goal"] == "销售转化"
    assert result.context["commercial_assets"] == ["商品链接"]
    assert len(calls) == 1
    assert calls[0]["usage"] == "llm"
    assert calls[0]["kwargs"]["json_mode"] is True
    assert "用户文字" in calls[0]["messages"][1]["content"]


def test_intaker_accepts_legacy_english_llm_labels(monkeypatch):
    def fake_chat_json(messages, *, usage="llm", **kwargs):
        return json.loads("""
        {
            "intention": {
                "goal": "sales_conversion",
                "format": "xhs_note",
                "tone": ["friendly"],
                "anti": ["no_hard_sell"]
            },
            "context": {
                "creative_assets": ["logo"],
                "commercial_assets": ["product_link"],
                "guardrails": ["no_hard_sell"],
                "data_refs": []
            },
            "missing": [],
            "questions": []
        }
        """)

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    result = IntakeAgent(use_llm=True).run("帮我做一篇小红书，别硬广，要带商品链接转化")

    assert result.intention["goal"] == "销售转化"
    assert result.intention["format"] == "小红书图文"
    assert result.intention["tone"] == ["亲和"]
    assert result.intention["anti"] == ["不要硬广"]
    assert result.context["creative_assets"] == ["品牌标志"]
    assert result.context["commercial_assets"] == ["商品链接"]


def test_intaker_falls_back_when_llm_fails(monkeypatch):
    def broken_chat_json(*args, **kwargs):
        raise RuntimeError("llm down")

    monkeypatch.setattr(llms, "chat_json", broken_chat_json)
    result = IntakeAgent(use_llm=True).run("帮我做一篇小红书图文，给新品种草，要高级")

    assert result.ready
    assert result.intention["goal"] == "产品种草"
    assert result.intention["format"] == "小红书图文"
    assert result.metadata["llm_error"]["stage"] == "intake_text"
    assert result.metadata["llm_error"]["reason"] == "api_error"


def test_intaker_falls_back_when_chat_json_fails(monkeypatch):
    def broken_chat_json(*args, **kwargs):
        raise llms.ChatJSONError("bad json", "not json")

    monkeypatch.setattr(llms, "chat_json", broken_chat_json)
    result = IntakeAgent(use_llm=True).run(
        "帮我做一篇小红书图文，给新品种草，要高级",
        use_vision=False,
    )

    assert result.ready
    assert result.metadata["llm_error"]["stage"] == "intake_text"
    assert result.metadata["llm_error"]["reason"] == "parse_error"
    assert result.intention["goal"] == "产品种草"
    assert result.intention["format"] == "小红书图文"


# ============ vision 打标工序（_tag_images_llm / _build_tagged_assets）============

_TINY_PNG_BYTES = __import__("base64").b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)


def _write_tiny_png(path):
    path.write_bytes(_TINY_PNG_BYTES)
    return str(path)


def test_intaker_tags_images_with_vision_llm(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")
    b = _write_tiny_png(tmp_path / "b.png")

    # vision 工序现在每张图单独调一次 LLM，返回该图的 tag dict（无 {"assets": [...]} 外壳）
    payloads_by_path = {
        a: {
            "vision_roles": ["product_shot", "brand_logo"],
            "subject": "便携马桶贴正面特写",
            "brand_signals": ["holly shit"],
            "usable_for": ["cover", "body"],
            "quality": "high",
        },
        b: {
            "vision_roles": ["scene_photo"],
            "subject": "工位实拍",
            "brand_signals": [],
            "usable_for": ["body"],
            "quality": "medium",
        },
    }

    chat_calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        chat_calls.append({"messages": messages, "usage": usage})
        # 通过 data-uri 长度区分两张图不太靠谱;这里改用调用顺序匹配,但因为并发,顺序无关
        # 我们直接用 image_url 内容长度做一个粗略 hash 来挑 payload
        user_parts = messages[1]["content"]
        img_part = next(p for p in user_parts if isinstance(p, dict) and p.get("type") == "image_url")
        uri = img_part["image_url"]["url"]
        # 两张图字节相同(都是 _TINY_PNG_BYTES),所以 uri 相同;按调用顺序返回不同 payload
        idx = (len(chat_calls) - 1) % 2
        target = a if idx == 0 else b
        return payloads_by_path[target]

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    # 关掉并发以便用顺序断言（线程池 max_workers=1 等价串行）
    monkeypatch.setattr(intaker_module, "VISION_PARALLELISM", 1)

    result = IntakeAgent(use_llm=False).run(
        UserInput(text="给品牌种草", images=[a, b]),
        use_vision=True,
    )

    image_assets = [x for x in result.assets if x.kind == "image"]
    assert [x.path for x in image_assets] == [a, b]
    assert image_assets[0].vision_roles == ["product_shot", "brand_logo"]
    assert image_assets[0].usable_for == ["cover", "body"]
    assert image_assets[0].brand_signals == ["holly shit"]
    assert image_assets[0].quality == "high"
    assert image_assets[1].vision_roles == ["scene_photo"]
    assert image_assets[1].quality == "medium"
    # 文本也进 assets
    text_assets = [x for x in result.assets if x.kind == "text"]
    assert text_assets and text_assets[0].text == "给品牌种草"
    # 每张图独立调用一次（共 2 次）
    assert len(chat_calls) == 2
    # 每次 user content 必须是 text + image_url 的多模态数组
    for call in chat_calls:
        assert call["usage"] == "vision"
        user_content = call["messages"][1]["content"]
        assert isinstance(user_content, list)
        types = [part.get("type") for part in user_content]
        assert "text" in types and "image_url" in types
        # 单图：image_url 只出现一次
        assert types.count("image_url") == 1


def test_intaker_vision_passes_user_text_in_prompt(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")
    captured: list[str] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        assert usage == "vision"
        for part in messages[1]["content"]:
            if isinstance(part, dict) and part.get("type") == "text":
                captured.append(part["text"])
        return {}

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    IntakeAgent(use_llm=False).run(
        UserInput(text="给品牌种草，要可爱风格", images=[a]),
        use_vision=True,
    )

    assert captured
    assert "给品牌种草，要可爱风格" in captured[0]


def test_intaker_vision_uses_chat_json_helper_and_isolates_failures(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")
    b = _write_tiny_png(tmp_path / "b.png")
    calls: list[dict] = []

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        calls.append({"messages": messages, "usage": usage, "kwargs": kwargs})
        if len(calls) == 2:
            raise llms.ChatJSONError("bad vision json", "{")
        return {
            "vision_roles": ["product_shot"],
            "subject": "便携产品特写",
            "brand_signals": ["nori"],
            "usable_for": ["cover"],
            "quality": "high",
        }

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    monkeypatch.setattr(intaker_module, "VISION_PARALLELISM", 1)

    result = IntakeAgent(use_llm=False).run(
        UserInput(text="给品牌种草", images=[a, b]),
        use_vision=True,
    )

    image_assets = [x for x in result.assets if x.kind == "image"]
    assert [x.path for x in image_assets] == [a, b]
    assert image_assets[0].vision_roles == ["product_shot"]
    assert image_assets[0].usable_for == ["cover"]
    assert image_assets[0].quality == "high"
    assert image_assets[1].vision_roles == []
    assert image_assets[1].subject == ""
    assert len(calls) == 2
    assert all(call["usage"] == "vision" for call in calls)
    assert all(call["kwargs"]["timeout"] == 60 for call in calls)
    assert all(call["kwargs"]["json_mode"] is True for call in calls)


def test_intaker_vision_runs_one_call_per_image(tmp_path, monkeypatch):
    """每张图独立调一次 vision LLM（不再 batch）。"""
    paths = [_write_tiny_png(tmp_path / f"p{i}.png") for i in range(10)]
    call_count = {"n": 0}

    def fake_chat_json(messages, *, usage="llm", **kwargs):
        assert usage == "vision"
        call_count["n"] += 1
        # 每次只见 1 张图
        user_parts = messages[1]["content"]
        img_count = sum(1 for p in user_parts if isinstance(p, dict) and p.get("type") == "image_url")
        assert img_count == 1, f"expected single image per call, got {img_count}"
        return {
            "vision_roles": ["unknown"],
            "subject": "",
            "brand_signals": [],
            "usable_for": ["body"],
            "quality": "low",
        }

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)

    result = IntakeAgent(use_llm=False).run(
        UserInput(text="t", images=paths),
        use_vision=True,
    )

    assert call_count["n"] == 10
    image_assets = [a for a in result.assets if a.kind == "image"]
    assert len(image_assets) == 10
    assert all(a.vision_roles == ["unknown"] for a in image_assets)


def test_intaker_vision_falls_back_to_empty_tag_when_llm_fails(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")

    def broken_chat_json(*args, **kwargs):
        raise RuntimeError("vision down")

    monkeypatch.setattr(llms, "chat_json", broken_chat_json)
    result = IntakeAgent(use_llm=False).run(
        UserInput(text="t", images=[a]),
        use_vision=True,
    )

    image_assets = [x for x in result.assets if x.kind == "image"]
    assert len(image_assets) == 1
    assert image_assets[0].path == a
    assert image_assets[0].vision_roles == []
    assert image_assets[0].subject == ""


def test_intaker_skips_vision_when_use_llm_false(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")
    called = {"n": 0}

    def fake_chat_json(*args, **kwargs):
        called["n"] += 1
        return {}

    monkeypatch.setattr(llms, "chat_json", fake_chat_json)
    # 不显式传 use_vision，依赖 use_llm=False 时自动关掉 vision
    result = IntakeAgent(use_llm=False).run(UserInput(text="t", images=[a]))

    assert called["n"] == 0
    image_assets = [x for x in result.assets if x.kind == "image"]
    assert image_assets[0].vision_roles == []


def test_intaker_filters_unknown_role_and_normalizes_case(tmp_path, monkeypatch):
    a = _write_tiny_png(tmp_path / "a.png")

    # 单图调用：直接返回 tag dict（无 {"assets": [...]} 外壳）
    payload = {
        "vision_roles": ["Brand_Logo", "NOT_A_REAL_ROLE", "ip_character"],
        "subject": "X" * 200,
        "brand_signals": ["  ", "holly  "],
        "usable_for": ["Cover", "weird"],
        "quality": "HIGH",
    }

    monkeypatch.setattr(llms, "chat_json", lambda *a, **k: payload)

    result = IntakeAgent(use_llm=False).run(
        UserInput(text="t", images=[a]),
        use_vision=True,
    )
    img = [x for x in result.assets if x.kind == "image"][0]
    assert img.vision_roles == ["brand_logo", "ip_character"]
    assert img.usable_for == ["cover"]
    assert img.quality == "high"
    assert img.brand_signals == ["holly"]
    assert len(img.subject) == 60
