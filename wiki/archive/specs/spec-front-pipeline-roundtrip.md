<!-- Last verified: 2026-05-24 | Current stage: P1 Account-Ops Backend -->

# Spec: Front Pipeline Round Trip

## Background

The intake and account-planning boundary is the first durable product pipeline:

```text
UserInput
-> IntakeResult
-> AccountPlannerInput
-> AccountPlanResult
-> AccountOperationProject
```

These models already emitted `to_dict()` snapshots, but the front-pipeline models did not all provide explicit `from_dict()` restoration. That makes future artifact replay, case logs, and ops handoff code more likely to grow ad hoc parsing.

## Goal

Make the front pipeline restorable through model classes:

- `UserInput.from_dict(...)`;
- `IntakeResult.from_dict(...)`;
- `AccountPlannerInput.from_dict(...)`;
- `AccountPlanResult.from_dict(...)`.

## Non-Goals

- Do not change serialized JSON shapes.
- Do not add persistence or database runtime.
- Do not change agent fallback behavior.

## Acceptance

- `UserInput.from_dict(user_input.to_dict()).to_dict() == user_input.to_dict()`.
- `IntakeResult.from_dict(intake.to_dict()).to_dict() == intake.to_dict()`.
- `AccountPlannerInput.from_dict(planner_input.to_dict()).to_dict() == planner_input.to_dict()`.
- `AccountPlanResult.from_dict(plan.to_dict()).to_dict() == plan.to_dict()`.
- Existing Intake, AccountPlanner, and account-positioning tests still pass.

## Verification

- `python -m pytest tests/test_agent_models.py tests/test_gen_agents_intaker.py tests/test_gen_agents_account_planner.py tests/test_ops_models_account_positioning.py -q`
