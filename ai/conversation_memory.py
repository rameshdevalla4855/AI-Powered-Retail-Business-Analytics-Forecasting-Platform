"""Lightweight session-based conversation memory for the AI assistant."""

from __future__ import annotations

import streamlit as st


class ConversationMemory:
    """Store recent queries inside Streamlit session state."""

    def __init__(self) -> None:
        if "ai_history" not in st.session_state:
            st.session_state["ai_history"] = []

    def add(self, query: str, response: str) -> None:
        """Append a query-response pair to memory."""
        st.session_state["ai_history"].append({"query": query, "response": response})

    def recent(self, limit: int = 5) -> list[dict[str, str]]:
        """Return the most recent entries."""
        return list(st.session_state["ai_history"][-limit:])
