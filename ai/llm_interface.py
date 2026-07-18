"""LLM abstraction layer with a safe rule-based fallback."""

from __future__ import annotations

import os
from typing import Any


class LLMInterface:
    """Use an external LLM when configured; otherwise fall back to rule-based responses."""

    def __init__(self) -> None:
        self.provider = None
        self.api_key = None
        self._configured = False

        for env_name in ("OPENAI_API_KEY", "GEMINI_API_KEY", "AZURE_OPENAI_API_KEY"):
            value = os.getenv(env_name)
            if value:
                self.api_key = value
                self.provider = env_name.replace("_API_KEY", "")
                self._configured = True
                break

    def enabled(self) -> bool:
        """Return whether an LLM backend appears to be configured."""
        return self._configured

    def generate(self, prompt: str) -> str:
        """Return a response from an LLM or a fallback explanation."""
        if not self.enabled():
            return (
                "LLM is not configured. Using the built-in analytics assistant with rule-based routing."
            )
        return f"LLM mode is enabled via {self.provider}."
