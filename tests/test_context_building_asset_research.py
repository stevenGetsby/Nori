from nori.core import AssetLibrary, AssetRecord
from nori.core import AccountOperationProject
from nori.core import ClientBrief
from nori.market_analysis.models import CompetitorResearch, CompetitorSample


def test_asset_library_round_trips_and_filters_usable_assets():
    library = AssetLibrary(
        library_id="assets_spring",
        assets=[
            AssetRecord(
                asset_id="logo",
                kind="image",
                path="/assets/logo.png",
                usage=["cover", "brand"],
                tags=["brand"],
                source="client",
            ),
            AssetRecord(
                asset_id="old_photo",
                kind="image",
                path="/assets/old.png",
                usage=["cover"],
                status="archived",
            ),
            AssetRecord(
                asset_id="copy_point",
                kind="text",
                text="本地配送快",
                usage=["body"],
            ),
        ],
        notes=["客户素材库"],
    )

    restored = AssetLibrary.from_dict(library.to_dict())

    assert restored.to_dict() == library.to_dict()
    assert restored.get("logo").path == "/assets/logo.png"
    assert restored.get("missing") is None
    assert [asset.asset_id for asset in restored.usable_assets("cover")] == ["logo"]
    assert [asset.asset_id for asset in restored.usable_assets()] == ["logo", "copy_point"]


def test_competitor_research_round_trips_top_samples_and_task_references():
    research = CompetitorResearch(
        research_id="research_flowers",
        platform="xhs",
        keywords=["花艺", "社区花店"],
        samples=[
            CompetitorSample(
                sample_id="sample_low",
                note_id="xhs_low",
                title="普通花束",
                keyword="花艺",
                metrics={"liked": 20, "collected": 5},
            ),
            CompetitorSample(
                sample_id="sample_high",
                author_name="花艺研究所",
                note_id="xhs_high",
                title="母亲节花别乱买",
                url="https://xhs.example/high",
                keyword="母亲节花束",
                metrics={"likes": 200, "collected": 80},
                content_angles=["避坑清单"],
                source_refs=[{"source": "manual"}],
            ),
        ],
        insights=["避坑标题表现更好"],
    )

    restored = CompetitorResearch.from_dict(research.to_dict())
    refs = restored.to_task_references(limit=1)

    assert restored.to_dict() == research.to_dict()
    assert restored.top_samples(metric="liked", limit=1)[0].sample_id == "sample_high"
    assert restored.top_samples(metric="collected", limit=1)[0].sample_id == "sample_high"
    assert refs == [
        {
            "source": "competitor_research",
            "sample_id": "sample_high",
            "platform": "xhs",
            "note_id": "xhs_high",
            "title": "母亲节花别乱买",
            "keyword": "母亲节花束",
            "url": "https://xhs.example/high",
        }
    ]


def test_account_operation_project_round_trips_asset_and_competitor_models():
    project = AccountOperationProject(
        project_id="ops_001",
        client_brief=ClientBrief(brand_name="春日花房"),
        asset_library=AssetLibrary(
            library_id="assets_001",
            assets=[AssetRecord(asset_id="product_001", kind="image", usage=["cover"])],
        ),
        competitor_research=CompetitorResearch(
            research_id="research_001",
            samples=[CompetitorSample(sample_id="sample_001", title="对标笔记")],
        ),
    )

    restored = AccountOperationProject.from_dict(project.to_dict())

    assert restored.to_dict() == project.to_dict()
    assert restored.asset_library.assets[0].asset_id == "product_001"
    assert restored.competitor_research.samples[0].title == "对标笔记"


def test_legacy_project_without_new_models_gets_empty_defaults():
    restored = AccountOperationProject.from_dict({"project_id": "legacy"})

    assert restored.project_id == "legacy"
    assert restored.asset_library.to_dict() == AssetLibrary().to_dict()
    assert restored.competitor_research.to_dict() == CompetitorResearch().to_dict()
