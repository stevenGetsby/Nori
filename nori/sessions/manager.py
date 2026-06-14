"""Session manager for local runtime orchestration."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .schemas import Session, SessionEvent, TaskGoal, Turn, utc_now_iso


class SessionManager:
    """Create, mutate, retrieve, and optionally persist runtime sessions."""

    def __init__(self, *, storage_root: str | Path | None = None) -> None:
        self.sessions: dict[str, Session] = {}
        self.storage_root = Path(storage_root) if storage_root is not None else None
        self._load_sessions()

    def create_session(self, *, user_id: str = "", profile_id: str = "", metadata: dict | None = None) -> Session:
        session = Session(user_id=user_id, profile_id=profile_id, metadata=dict(metadata or {}))
        self.sessions[session.session_id] = session
        self.save_session(session.session_id)
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self.sessions.get(session_id)

    def save_session(self, session_id: str) -> None:
        if self.storage_root is None:
            return
        session = self._require_session(session_id)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        path = self._session_path(session.session_id)
        tmp_path = path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(session.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(path)

    def append_turn(self, session_id: str, *, role: str, content: str, metadata: dict | None = None) -> Turn:
        session = self._require_session(session_id)
        turn = Turn(role=role, content=content, metadata=dict(metadata or {}))
        session.turns.append(turn)
        session.updated_at = utc_now_iso()
        self.save_session(session_id)
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
        self.save_session(session_id)
        return task

    def _require_session(self, session_id: str) -> Session:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(f"session not found: {session_id}")
        return session

    def _load_sessions(self) -> None:
        if self.storage_root is None or not self.storage_root.is_dir():
            return
        for path in sorted(self.storage_root.glob("session_*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(data, dict):
                continue
            session = Session.from_dict(data)
            if session.session_id:
                self.sessions[session.session_id] = session

    def _session_path(self, session_id: str) -> Path:
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", str(session_id or "").strip())
        return self.storage_root / f"{safe or 'session'}.json"
