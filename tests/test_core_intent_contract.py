from __future__ import annotations

from nori.core import ClientBrief, ContentTask, IntentContract


def test_intent_contract_freezes_user_goal_and_acceptance_requirements():
    brief = ClientBrief(
        brand_name="Holly Shit开心拉屎",
        goals=["涨粉", "卖文创产品"],
        audience=["高压打工人"],
        positioning_notes=["用屎尿屁幽默表达反焦虑"],
        constraints=["保留不羁、自信、有趣、搞怪"],
        taboos=["不要低俗猎奇"],
    )
    task = ContentTask(
        task_id="task_1",
        platform="xhs",
        topic="厕所快乐哲学",
        objective="让用户理解带薪拉屎和休息权",
        brief={
            "must_include": ["杯子", "贴纸"],
            "tone": ["不羁", "搞怪"],
            "deliverable": "xhs_note",
        },
    )

    contract = IntentContract.from_brief_and_task(brief, task)

    assert contract.contract_id == "intent_task_1"
    assert contract.brand_name == "Holly Shit开心拉屎"
    assert contract.platform == "xhs"
    assert contract.primary_goal == "让用户理解带薪拉屎和休息权"
    assert contract.business_goals == ["涨粉", "卖文创产品"]
    assert contract.must_include == ["Holly Shit开心拉屎", "厕所快乐哲学", "杯子", "贴纸"]
    assert contract.tone == ["不羁", "自信", "有趣", "搞怪"]
    assert contract.deliverables == ["xhs_note"]
    assert contract.taboos == ["不要低俗猎奇"]


def test_intent_contract_reports_missing_required_terms():
    contract = IntentContract(
        contract_id="intent_task_1",
        brand_name="Holly Shit开心拉屎",
        primary_goal="卖产品",
        must_include=["杯子", "贴纸"],
        taboos=["不要低俗"],
    )

    assert contract.missing_terms("这是一篇只讲理念的文案") == ["杯子", "贴纸"]
    assert contract.missing_terms("Holly 的杯子和贴纸都可以贴在工位") == []
