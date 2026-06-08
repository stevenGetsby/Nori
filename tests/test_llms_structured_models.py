from __future__ import annotations

import nori.core as core
import nori.core.llms as llms
from nori.core import contracts


def test_removed_structured_helper_result_models_are_not_public_contracts():
    removed = {
        "IntentLLMResult",
        "StructuredCallResult",
        "TargetSelectionResult",
    }

    assert removed.isdisjoint(contracts.__all__)
    assert removed.isdisjoint(core.__all__)
    for name in removed:
        assert not hasattr(contracts, name)
        assert not hasattr(core, name)
        assert not hasattr(llms, name)
