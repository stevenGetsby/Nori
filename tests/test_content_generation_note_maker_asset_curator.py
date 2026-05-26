from nori.content_generation.models import AssetBundle, UserAsset
from nori.content_generation.note_maker import asset_curator


def test_asset_curator_builds_bundle_from_llm_indices_and_text_buckets():
    assets = [
        UserAsset(kind="image", path="/tmp/a.jpg"),
        UserAsset(kind="text", text="text asset"),
        UserAsset(kind="image", path="/tmp/b.jpg"),
        UserAsset(kind="image", path="/tmp/c.jpg"),
    ]

    bundle = asset_curator.bundle_from_curator_data(
        {
            "main_image_indices": ["2", 1, "bad"],
            "aux_image_indices": [3, 2, 99],
            "text_points": ["  point  ", "", "x", "y", "z", "u", "v"],
            "brand_facts": [" brand "],
            "data_points": [" 42 "],
        },
        assets,
    )

    assert [asset.path for asset in bundle.main_images] == ["/tmp/b.jpg"]
    assert [asset.path for asset in bundle.aux_images] == ["/tmp/c.jpg", "/tmp/a.jpg"]
    assert bundle.text_points == ["point", "x", "y", "z", "u", "v"]
    assert bundle.brand_facts == ["brand"]
    assert bundle.data_points == ["42"]


def test_asset_curator_prompts_json_call_with_asset_payloads():
    assets = [
        UserAsset(kind="image", path="/tmp/main.jpg", vision_roles=["product_shot"], subject="主体"),
        UserAsset(kind="text", text="用户卖点" * 80),
    ]
    calls: list[dict] = []

    def fake_json_call(*, system: str, user: str, timeout: int):
        calls.append({"system": system, "user": user, "timeout": timeout})
        return {
            "main_image_indices": [0],
            "aux_image_indices": [],
            "text_points": ["用户卖点"],
            "brand_facts": [],
            "data_points": [],
        }

    bundle = asset_curator.curate_assets_llm(
        assets,
        {"creative_goal": "种草", "tone": "朋友安利", "note_type": "图文"},
        {"goal": "产品种草"},
        json_call=fake_json_call,
    )

    assert [asset.path for asset in bundle.main_images] == ["/tmp/main.jpg"]
    assert calls[0]["timeout"] == 60
    assert "图片素材" in calls[0]["user"]
    assert "文本素材" in calls[0]["user"]
    assert "product_shot" in calls[0]["user"]
    assert "用户卖点" in calls[0]["user"]


def test_asset_curator_skips_llm_when_no_assets():
    def fail_json_call(*args, **kwargs):
        raise AssertionError("empty assets should not call the LLM")

    bundle = asset_curator.curate_assets_llm([], {}, {}, json_call=fail_json_call)

    assert bundle == AssetBundle()


def test_asset_curator_pick_visual_paths_uses_cover_and_caps_gallery():
    images = [UserAsset(kind="image", path=f"/tmp/{index}.jpg") for index in range(12)]
    bundle = AssetBundle(main_images=images[:3], aux_images=images[3:])

    cover, gallery = asset_curator.pick_visual_paths(bundle)

    assert cover == "/tmp/0.jpg"
    assert gallery == [f"/tmp/{index}.jpg" for index in range(1, 9)]
