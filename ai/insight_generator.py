"""Generate concise business insights from analytics results."""

from __future__ import annotations

import pandas as pd


class InsightGenerator:
    """Create natural-language guidance from analysis results."""

    def generate(self, data: pd.DataFrame, intent: str) -> str:
        """Return a short insight based on the intent and data."""
        if data.empty:
            return "No data is available for this request."
        if intent == "monthly_sales":
            return "Revenue trend is available; focus on the strongest and weakest periods for planning."
        if intent == "top_products":
            return "Promote the leading products and review stock availability around peak demand."
        if intent == "revenue_by_state":
            return "Target high-performing regions with retention and upsell campaigns."
        if intent == "payment_analysis":
            return "Review payment mix to simplify checkout and reduce friction."
        if intent == "top_customers":
            return "Prioritize top customers with loyalty offers and personalized campaigns."
        if intent == "review_analysis":
            return "Use feedback patterns to improve delivery experience and product quality."
        if intent == "forecast":
            return "Plan inventory and staffing around forecasted demand trends."
        return "Review the generated output and turn it into an action plan for the business."
