"""Parse free-form analytics questions into structured intent and filter hints."""

from __future__ import annotations

import re
from typing import Any


class QueryParser:
    """Extract simple entities like states and categories from a query."""

    def parse(self, query: str) -> dict[str, Any]:
        """Return a lightweight structured representation of the query."""
        normalized = query.lower().strip()
        states = re.findall(r"\b([a-z]+)\b", normalized)
        return {
            "query": query,
            "filters": {"states": states[:3]},
            "keywords": normalized.split(),
        }
