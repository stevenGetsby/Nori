import json
import time
from pathlib import Path

from data_collect.adapter import DataCollector, DownloadRule, SearchRule, TopNotesRule


def _note(keyword: str, note_id: str, liked: int, time_ms: int) -> dict:
    return {
        "source_keyword": keyword,
        "note_id": note_id,
        "title": f"title {note_id}",
        "desc": f"desc {note_id}",
        "user_id": "author-id",
        "nickname": "author",
        "liked_count": str(liked),
        "collected_count": "1",
        "comment_count": "1",
        "share_count": "1",
        "tag_list": json.dumps([{"name": "tag"}], ensure_ascii=False),
        "image_list": json.dumps(["image"], ensure_ascii=False),
        "type": "normal",
        "note_url": f"https://www.xiaohongshu.com/explore/{note_id}",
        "time": str(time_ms),
    }


class FakeCollector(DataCollector):
    def __init__(self, project_root: Path):
        super().__init__(project_root=project_root, account_pool_save_type="none")
        self.search_calls: list[SearchRule] = []
        self.download_calls: list[DownloadRule] = []

    def search(self, rule: SearchRule) -> dict:
        self.search_calls.append(rule)
        keyword = str(rule.keywords[0])
        data_dir = Path(rule.data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        output_path = data_dir / "search_contents_test.json"
        existing = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else []

        now_ms = int(time.time() * 1000)
        recent_ms = now_ms - 24 * 60 * 60 * 1000
        old_ms = now_ms - 90 * 24 * 60 * 60 * 1000
        if keyword == "热门足够":
            rows = [
                _note(keyword, "recent_1000", 1000, recent_ms),
                _note(keyword, "recent_900", 900, recent_ms),
                _note(keyword, "recent_800", 800, recent_ms),
                _note(keyword, "recent_700", 700, recent_ms),
                _note(keyword, "recent_600", 600, recent_ms),
                _note(keyword, "recent_500", 500, recent_ms),
            ]
        elif rule.sort == "popular":
            rows = [
                _note(keyword, "old_hot", 9999, old_ms),
                _note(keyword, "recent_900", 900, recent_ms),
                _note(keyword, "recent_400", 400, recent_ms),
                _note(keyword, "recent_300", 300, recent_ms),
                _note(keyword, "recent_200", 200, recent_ms),
                _note(keyword, "recent_100", 100, recent_ms),
            ]
        else:
            rows = []
        output_path.write_text(json.dumps(existing + rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "completed", "data_dir": str(data_dir)}

    def download(self, rule: DownloadRule) -> list[str]:
        self.download_calls.append(rule)
        save_dir = Path(rule.save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        paths = [
            save_dir / "xhs_recent_low_cover.jpg",
            save_dir / "xhs_recent_low_image_0.jpg",
            save_dir / "xhs_recent_low_video.mp4",
        ]
        for path in paths:
            path.write_bytes(b"asset")
        return [str(path) for path in paths]


def test_collect_top_notes_stops_when_popular_has_five_qualified_notes(tmp_path):
    collector = FakeCollector(tmp_path)

    result = collector.collect_top_notes(TopNotesRule(
        platform="xhs",
        keywords=["热门足够"],
        top_k_per_keyword=5,
        data_dir=str(tmp_path / "skill_data"),
    ))

    # 单次 search 调用，max_notes=40 表示一次抓两页 popular
    assert [call.sort for call in collector.search_calls] == ["popular"]
    assert [call.max_notes for call in collector.search_calls] == [40]
    assert [note.liked for note in result.hot_notes] == [1000, 900, 800, 700, 600]
    assert "recent_500" not in {note.note_id for note in result.hot_notes}
    assert result.insufficient == []


def test_collect_top_notes_picks_top_k_by_likes_across_popular_two_pages(tmp_path):
    collector = FakeCollector(tmp_path)

    result = collector.collect_top_notes(TopNotesRule(
        platform="xhs",
        keywords=["反焦虑设计"],
        top_k_per_keyword=5,
        data_dir=str(tmp_path / "skill_data"),
    ))

    # 只搜一次 popular（max_notes=40 → crawler 内部翻 2 页）
    assert [call.sort for call in collector.search_calls] == ["popular"]
    assert [call.max_notes for call in collector.search_calls] == [40]
    # 不筛时间窗、不筛 min_liked；按 likes 降序取 top_k：old_hot=9999 也入选
    assert [note.liked for note in result.hot_notes] == [9999, 900, 400, 300, 200]
    assert len({note.note_id for note in result.hot_notes}) == 5
    assert result.insufficient == []

    keyword_dir = Path(result.source_keyword_dirs["反焦虑设计"])
    selected = json.loads((keyword_dir / "selected_notes.json").read_text(encoding="utf-8"))
    assert len(selected) == 5
    assert (keyword_dir / "old_hot" / "note.json").exists()


def test_collect_top_notes_reports_insufficient_when_pool_below_top_k(tmp_path):
    collector = FakeCollector(tmp_path)
    # FakeCollector "反焦虑设计" 分支只返回 6 条，需要 10 条 → insufficient
    result = collector.collect_top_notes(TopNotesRule(
        platform="xhs",
        keywords=["反焦虑设计"],
        top_k_per_keyword=10,
        data_dir=str(tmp_path / "skill_data"),
    ))

    assert len(result.hot_notes) == 6
    assert result.insufficient == [{
        "keyword": "反焦虑设计",
        "got": 6,
        "need": 10,
    }]


def test_collect_top_notes_stores_poster_assets_under_keyword_dir(tmp_path):
    collector = FakeCollector(tmp_path)

    result = collector.collect_top_notes(TopNotesRule(
        platform="xhs",
        keywords=["反焦虑设计"],
        days=15,
        top_k_per_keyword=1,
        pool_size=3,
        download_media=True,
        data_dir=str(tmp_path / "skill_data"),
    ))

    keyword_dir = Path(result.source_keyword_dirs["反焦虑设计"])
    poster_dir = keyword_dir / result.hot_notes[0].note_id
    assert poster_dir.exists()
    assert (poster_dir / "note.json").exists()
    assert (poster_dir / "images" / "cover.jpg").exists()
    assert (poster_dir / "images" / "image_0.jpg").exists()
    assert (poster_dir / "video.mp4").exists()
    assert not (keyword_dir / "posters").exists()
