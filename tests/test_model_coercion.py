from nori.core import ContentTask
from nori.core.contracts import (
    bool_value,
    dict_list,
    float_value,
    int_list,
    int_value,
    mapping,
    mapping_list,
    optional_str,
    string_list,
)
from nori.core import contracts
from nori.market_analysis.models import NoteEvidence


def test_model_coercion_helpers_keep_shared_defaults():
    assert mapping({"a": 1}) == {"a": 1}
    assert mapping([("a", 1)]) == {}
    assert mapping_list([{"a": 1}, "skip", {"b": 2}]) == [{"a": 1}, {"b": 2}]
    assert dict_list("skip") == []
    assert string_list("topic") == ["topic"]
    assert string_list(["topic", "", 3]) == ["topic", "", "3"]
    assert string_list(["topic", "", "  "], drop_blank=True) == ["topic"]
    assert optional_str(None) is None
    assert optional_str("") is None
    assert optional_str(42) == "42"
    assert bool_value(True) is True
    assert bool_value("true") is True
    assert bool_value("false") is False
    assert bool_value("0") is False
    assert bool_value("unknown", default=True) is True
    assert int_value("12") == 12
    assert int_value(True, default=7) == 7
    assert int_value("bad", default=3) == 3
    assert int_list("10", drop_non_positive=True) == [10]
    assert int_list(["5", True, "bad", 0, 3], drop_non_positive=True) == [5, 3]
    assert float_value("1.25") == 1.25
    assert float_value(True, default=None) is None
    assert float_value("bad", default=0.5) == 0.5


def test_domain_and_workflow_models_share_coercion_contracts():
    evidence = NoteEvidence.from_dict(
        {
            "liked": "120",
            "collected": True,
            "image_paths": ["cover.png", "", 7],
            "cover_path": "",
        }
    )
    task = ContentTask.from_dict({"priority": "2", "required_assets": "hero_image"})

    assert evidence.liked == 120
    assert evidence.collected == 0
    assert evidence.image_paths == ["cover.png", "7"]
    assert evidence.cover_path is None
    assert task.priority == 2
    assert task.required_assets == ["hero_image"]
