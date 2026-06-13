"""Backend session store adapter."""
from __future__ import annotations

from typing import Any

from nori.sessions import Session, SessionManager, TaskGoal, Turn

from ..contracts import ApiError


class BackendSessionStore:
    """Backend-facing port around the runtime SessionManager."""

    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager

    def list_sessions(self) -> list[Session]:
        return list(self.session_manager.sessions.values())

    def create_session(
        self,
        *,
        user_id: str = "",
        profile_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Session:
        return self.session_manager.create_session(
            user_id=user_id,
            profile_id=profile_id,
            metadata=dict(metadata or {}),
        )

    def get_session(self, session_id: str) -> Session | None:
        return self.session_manager.get_session(session_id)

    def require_session(self, session_id: str) -> Session:
        session = self.get_session(session_id)
        if session is None:
            raise ApiError(f"session not found: {session_id}", status_code=404)
        return session

    def save_session(self, session_id: str) -> None:
        self.session_manager.save_session(session_id)

    def append_turn(
        self,
        session_id: str,
        *,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Turn:
        try:
            return self.session_manager.append_turn(
                session_id,
                role=role,
                content=content,
                metadata=dict(metadata or {}),
            )
        except KeyError as exc:
            raise ApiError(str(exc).strip("'"), status_code=404) from exc

    def start_task(
        self,
        session_id: str,
        *,
        goal: str,
        workflow_name: str = "",
        acceptance: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TaskGoal:
        try:
            return self.session_manager.start_task(
                session_id,
                goal=goal,
                workflow_name=workflow_name,
                acceptance=list(acceptance or []),
                metadata=dict(metadata or {}),
            )
        except KeyError as exc:
            raise ApiError(str(exc).strip("'"), status_code=404) from exc

    def find_task(self, session: Session, task_id: str) -> TaskGoal | None:
        return next((item for item in session.task_goals if item.task_id == task_id), None)
