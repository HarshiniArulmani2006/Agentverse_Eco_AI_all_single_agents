"""
WildGuard AI – Session Memory Manager
Stores the last MAX_HISTORY exchanges per session.
"""
from typing import List, Dict, Any
import time
import uuid

MAX_HISTORY = 20  # messages per session


class SessionMemory:
    """Thread-safe in-memory session store."""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create(self, session_id: str) -> str:
        """Ensure session exists; return session_id."""
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "history": [],
                "created_at": time.time(),
                "last_active": time.time(),
            }
        else:
            self._sessions[session_id]["last_active"] = time.time()
        return session_id

    def new_session(self) -> str:
        """Create and return a fresh session ID."""
        session_id = str(uuid.uuid4())
        self.get_or_create(session_id)
        return session_id

    def add_exchange(self, session_id: str, role: str, content: str):
        """Append a message to the session history."""
        self.get_or_create(session_id)
        history = self._sessions[session_id]["history"]
        history.append({"role": role, "content": content, "timestamp": time.time()})
        # Keep only the last MAX_HISTORY messages
        if len(history) > MAX_HISTORY:
            self._sessions[session_id]["history"] = history[-MAX_HISTORY:]

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Return conversation history for a session."""
        if session_id not in self._sessions:
            return []
        return self._sessions[session_id]["history"]

    def get_history_for_gemini(self, session_id: str) -> List[Dict[str, str]]:
        """Format history as Gemini-compatible list of {role, parts}."""
        history = self.get_history(session_id)
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})
        return gemini_history

    def clear(self, session_id: str):
        """Clear session history."""
        if session_id in self._sessions:
            self._sessions[session_id]["history"] = []

    def delete(self, session_id: str):
        """Remove session entirely."""
        self._sessions.pop(session_id, None)


# Singleton
memory = SessionMemory()
