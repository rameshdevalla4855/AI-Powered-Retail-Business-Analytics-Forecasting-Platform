"""Simple reporting helpers for AI analysis outputs."""

from __future__ import annotations

import pandas as pd


class ReportGenerator:
    """Create downloadable report content for the assistant."""

    def to_csv(self, data: pd.DataFrame) -> str:
        """Return CSV content for the current result."""
        return data.to_csv(index=False)

    def to_excel(self, data: pd.DataFrame) -> bytes:
        """Return Excel bytes for the current result."""
        import io

        output = io.BytesIO()
        data.to_excel(output, index=False)
        return output.getvalue()
