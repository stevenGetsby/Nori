import json

from nori.agent_utils import write_agent_log
from nori.agent_utils.case_log import write_agent_log as direct_write_agent_log


def test_agent_utils_reexports_case_log_helper():
    assert write_agent_log is direct_write_agent_log
    assert write_agent_log.__module__ == "nori.agent_utils.case_log"


def test_write_agent_log_keeps_input_output_and_config(tmp_path):
    path = write_agent_log(
        agent="account_planner",
        case="unit case",
        input_data={"text": "hello"},
        output_data={"tags": {"platform": "小红书"}},
        config={"mode": "test"},
        log_dir=tmp_path,
    )

    assert path.exists()
    assert path.name.startswith("account_planner_unit_case_")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["agent"] == "account_planner"
    assert data["case"] == "unit case"
    assert data["config"] == {"mode": "test"}
    assert data["input"] == {"text": "hello"}
    assert data["output"]["tags"]["platform"] == "小红书"
