"""Session manager for local runtime orchestration."""
from __future__ import annotations

from .models import Session, SessionEvent, TaskGoal, Turn, utc_now_iso


class SessionManager:
    """Create, mutate, and retrieve in-process sessions."""

    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}

    def create_session(self, *, user_id: str = "", profile_id: str = "", metadata: dict | None = None) -> Session:
        session = Session(user_id=user_id, profile_id=profile_id, metadata=dict(metadata or {}))
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self.sessions.get(session_id)

    def append_turn(self, session_id: str, *, role: str, content: str, metadata: dict | None = None) -> Turn:
        session = self._require_session(session_id)
        turn = Turn(role=role, content=content, metadata=dict(metadata or {}))
        session.turns.append(turn)
        session.updated_at = utc_now_iso()
        return turn

    def start_task(
        self,
        session_id: str,
        *,
        goal: str,
        workflow_name: str = "",
        acceptance: list[str] | None = None,
        metadata: dict | None = None,
    ) -> TaskGoal:
        session = self._require_session(session_id)
        task = TaskGoal(
            goal=goal,
            workflow_name=workflow_name,
            acceptance=list(acceptance or []),
            metadata=dict(metadata or {}),
        )
        session.task_goals.append(task)
        session.events.append(SessionEvent(event_type="task_started", payload=task.to_dict()))
        session.updated_at = utc_now_iso()
        return task

    def _require_session(self, session_id: str) -> Session:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(f"session not found: {session_id}")
        return session
